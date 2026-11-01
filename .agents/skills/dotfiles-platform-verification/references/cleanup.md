# Cleanup Contract

Every run owns its temp tree or VM and must remove it. Shared caches and base
images are retained deliberately; they are not run-owned.

## Ownership

| Artifact | Owner | Removed by a passing run | Retained |
|---|---|---|---|
| `/tmp/dotfiles-macos-e2e-*` temp tree | macOS host journey | yes, in `finally` | only with `--keep` |
| Tart VM `dotfiles-e2e-*` | Tart journey | yes, `tart stop` + `tart delete`, then verified with `tart list` | only with `--keep` |
| Tart VM log `/tmp/dotfiles-e2e-*.log` | Tart journey | yes, on success | kept on failure or `--keep` |
| Docker container | Docker matrix | yes, `docker run --rm` | never |
| Docker image `nixdotfiles:test-<distro>` | Docker matrix | yes, `docker image rm -f`, including after failure | only with `--keep` |
| Docker build cache | shared | no | yes; `--prune-cache` is opt-in and global |
| Docker base layers | shared | no | yes |
| Tart base `tahoe-base` | shared | no | yes |
| Tart OCI cache | shared | no | yes; `tart prune --entries caches` is a separate manual action |
| Nix store | shared | no | yes |
| Logs in `/tmp` | caller | no | yes, small evidence |

## Verify Cleanup

Run these after every journey:

```sh
ls -d /tmp/dotfiles-macos-e2e-* 2>/dev/null || echo "no host temp trees"
tart list | grep dotfiles-e2e || echo "no Tart e2e VMs"
ls /tmp/dotfiles-e2e-*.log 2>/dev/null || echo "no Tart e2e logs"
docker ps -a --format '{{.Image}}' | grep nixdotfiles || echo "no containers"
docker images --format '{{.Repository}}:{{.Tag}}' | grep nixdotfiles || echo "no test images"
```

Interpretation:

- Host tree absent: pass.
- Tart e2e VM absent: pass. The persistent `tahoe-base` and any pre-existing
  `tahoe-base-e2e-test` are not this run's artifacts.
- Docker containers absent: pass.
- Docker images absent: pass for the default cleanup. Present only with
  `--keep`; say so in the handoff.
- `git status --short`: only unrelated user work.

## What Never to Delete

Never delete these as part of a run:

- `tahoe-base` or another Tart base image;
- pre-existing Tart VMs that the run did not clone;
- Docker base layers or build cache by default;
- the Nix store or profile generations;
- the user's real HOME, XDG, CODEX, RUSTUP, or CARGO state.

`tart prune --entries caches` and `docker builder prune` are manual space
reclaims, not verification cleanup.

## Failure Cleanup

The scripts clean in `finally`, including after a failed install or smoke test.
Still verify:

- If a Tart VM remains, run `tart delete <vm>` and rerun the journey.
- If a Docker image remains, run `docker image rm -f <tag>`.
- If a host temp tree remains, remove the printed path.
- Keep the failed run's log. The cleanup proof and the failure evidence are
  separate; do not delete the log to make the cleanup check pass.

## Concurrency and Isolation

Run one platform journey at a time on one host:

- Docker uses fixed image tags `nixdotfiles:test-ubuntu` and
  `nixdotfiles:test-fedora`;
- Docker build cache and the Nix store are shared;
- Tart VM names use a one-second timestamp;
- the macOS host journey uses a unique `mktemp` tree but shares the Nix store.

If two runs must overlap, give them separate image tags, VM names, and temp
roots; this skill does not provide that isolation.

## Disk Notes

- `tahoe-base` is tens of GB, and a macOS VM needs roughly 50 GB of free disk.
- Docker test images are about 11 GB each; both are about 22.5 GB.
- Keeping images (`--keep`) makes reruns fast; the default Docker cleanup frees
  them.
- The Tart OCI cache and Docker build cache are the large shared caches. Reclaim
  them manually only when their reuse cost is not worth the space.
