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

Builds the Dockerfile's `acceptance` stage with `--output type=cacheonly`. The
install, reinstall, `doctor`, `verify`, and smoke check are `RUN` steps, so a
passing build is the check. Nothing is exported or run afterwards. `make
test-linux` is the same build plus the test suite (`--target tests`).

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
python3 tests/docker_matrix.py --keep         # also load nixdotfiles:test-<distro>
python3 tests/docker_matrix.py --target tests # also run the test suite
python3 tests/docker_matrix.py --prune-cache  # global Docker build-cache prune
python3 tests/docker_matrix.py --dry-run      # print commands only
```

Success:

- exit 0 (the build passed)
- the smoke `RUN` step finds `fish`, `rg`, and `nvim`
- fish loads `nix-try`, `__direnv_export_eval`, and `NIX_CONFIG`
- strict verify passes in its `RUN` step

Cleanup checks:

```sh
docker images --format '{{.Repository}}:{{.Tag}}' | grep nixdotfiles || echo "no test images"
```

The default loads no image and runs no container. `--keep` loads the tagged
image so you can debug inside it. Docker reuses unchanged stages; a cold build
cache or a changed `flake.nix`, `flake.lock`, or `rust-toolchain.toml` is much
slower (see `tests/DOCKER-TEST-GUIDE.md`).

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
- Docker run: a failed `RUN` step fails the build and prints its log. Fix that
  step and rerun; a loaded `--keep` image is removed with `docker image rm -f <tag>`.
- Keep the log after a failure. It is the evidence for the next investigation.
