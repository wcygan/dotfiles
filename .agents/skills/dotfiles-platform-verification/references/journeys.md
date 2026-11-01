# Journeys

Run from the repository root. Capture stdout and stderr to a log; the scripts
print the commands they run and the guest/container results.

## Preflight

```sh
git status --short
git diff --exit-code -- flake.lock uv.lock agent-skills.lock.toml
make --dry-run help >/dev/null
```

A dirty tree is acceptable only for unrelated user work. The verification runs
must not modify tracked files.

## 1. macOS isolated host

Runs `make test-syntax`, `make test-pre`, install twice, doctor, and strict verify
inside a temporary HOME/XDG/CODEX/RUSTUP/CARGO tree.

```sh
python3 tests/macos_e2e.py | tee /tmp/dotfiles-macos-host.log
```

Useful flags:

```sh
python3 tests/macos_e2e.py --reuse-rustup   # reuse host rustup/cargo caches
python3 tests/macos_e2e.py --skip-tests     # install/doctor/verify only
python3 tests/macos_e2e.py --keep           # retain the temp tree for debugging
```

Success:

- exit 0
- `macOS isolated acceptance passed`
- 501 tests pass before the install
- strict verify prints 21 `[PASS]` lines and no `[FAIL]`

Cleanup check:

```sh
ls -d /tmp/dotfiles-macos-e2e-* 2>/dev/null || echo "no host temp trees"
```

`--keep` prints the retained path; remove it manually when done.

Measured here: 54.6s fully isolated, 37.4s with `--reuse-rustup`.

## 2. macOS Tart VM

Clones a base image, boots it headless with the checkout shared in, copies the
checkout, installs Nix if absent, runs install twice, doctor, verify, then
deletes the VM and verifies deletion.

```sh
python3 tests/macos_vm_e2e.py | tee /tmp/dotfiles-macos-vm.log
```

Useful flags:

```sh
python3 tests/macos_vm_e2e.py --base tahoe-base
python3 tests/macos_vm_e2e.py --base ghcr.io/cirruslabs/macos-tahoe-base:latest
python3 tests/macos_vm_e2e.py --keep          # leave the VM running
python3 tests/macos_vm_e2e.py --with-tests    # also run test-syntax/test-pre in the VM
```

Success:

- exit 0
- `macOS Tart acceptance passed`
- strict verify prints 21 `[PASS]` lines and no `[FAIL]`
- the script reports `cleanup failed` if the VM still exists

Cleanup checks:

```sh
tart list | grep dotfiles-e2e || echo "no Tart e2e VMs"
ls /tmp/dotfiles-e2e-*.log 2>/dev/null || echo "no Tart e2e logs"
```

The base image (`tahoe-base`) is retained. The in-guest Nix store and toolchain
are deleted with the VM. If `--keep` was used, the script prints the stop and
delete commands.

Measured here: 288.3s with a fresh `tahoe-base` that has no Nix. A pre-warmed
base would be faster.

## 3. Ubuntu container

Builds the image, runs the Dockerfile's cold and warm installs plus doctor and
verify, then runs the smoke command.

```sh
python3 tests/docker_matrix.py --case ubuntu | tee /tmp/dotfiles-ubuntu.log
```

## 4. Fedora container

Same flow with `Dockerfile.fedora`.

```sh
python3 tests/docker_matrix.py --case fedora | tee /tmp/dotfiles-fedora.log
```

Both cases at once:

```sh
python3 tests/docker_matrix.py | tee /tmp/dotfiles-linux.log
```

Useful flags:

```sh
python3 tests/docker_matrix.py --keep         # retain the built images
python3 tests/docker_matrix.py --prune-cache  # global Docker build-cache prune
python3 tests/docker_matrix.py --dry-run      # print commands only
```

Success:

- exit 0
- the smoke command finds `fish`, `rg`, and `nvim`
- fish loads `nix-try`, `__direnv_export_eval`, and `NIX_CONFIG`
- strict verify passes inside the container

Cleanup checks:

```sh
docker ps -a --format '{{.Image}}' | grep nixdotfiles || echo "no containers"
docker images --format '{{.Repository}}:{{.Tag}}' | grep nixdotfiles || echo "no test images"
```

The default removes each built image after its smoke test. `--keep` retains the
images (about 22.5 GB for both) so reruns are a cache hit. Containers are always
removed by `docker run --rm`.

Measured here: 6.9s for both cases with warm Docker layers and `--keep`. A cold
build cache or a changed Dockerfile input is much slower.

## Evidence Checklist

| Check | Expected |
|---|---|
| host exit code | 0 |
| host temp tree | absent |
| Tart exit code | 0 |
| `dotfiles-e2e-*` VMs | absent |
| Docker exit code | 0 |
| `nixdotfiles` containers | absent |
| Docker images | absent by default; present only with `--keep` |
| `git status --short` | only unrelated user work |
| lockfiles | unchanged |

## Failure Handling

- Host run: the temp tree is removed in `finally`. If `rmtree` fails, the run
  fails; remove the printed path before rerunning.
- Tart run: the VM is stopped and deleted in `finally`; the script verifies
  `tart list`. If `cleanup failed` appears, run `tart delete <vm>` and rerun.
- Docker run: the image is removed in `finally`, including after a failed build
  or smoke test. If removal fails, run `docker image rm -f <tag>`.
- Keep the log after a failure. It is the evidence for the next investigation.
