---
name: dotfiles-platform-verification
description: "Run and verify this dotfiles repository's real install path on macOS and Linux, including isolated-host macOS acceptance, an ephemeral Tart macOS VM, and Ubuntu/Fedora Docker containers. Use when asked to test platforms end to end, reproduce a platform failure, check install idempotency, or confirm that verification runs clean up their temp trees, VMs, containers, and images."
---

# Dotfiles Platform Verification

## Outcome

Run the real install path on every locally available platform, capture the
evidence, and remove every artifact the run owns. A pass means the checkout
installed twice, doctor and strict verify succeeded, and cleanup is confirmed.
A missing prerequisite is a coverage gap, never a pass.

## Start Here

1. Read `$dotfiles-operations`; this skill adds the platform matrix, not a
   second install contract.
2. Inspect `git status --short` and confirm the lockfiles are unchanged.
3. `make help` to confirm the targets and scripts still exist.
4. Read [references/journeys.md](references/journeys.md) for exact commands and
   [references/cleanup.md](references/cleanup.md) for what each run owns.
5. Run one platform at a time. Docker tags and Nix profile names are shared, so
   concurrent runs on one host can collide.

## Prerequisites

| Platform | Needs |
|---|---|
| macOS isolated host | macOS, Nix, roughly 2 GB free |
| macOS Tart VM | Apple Silicon, Tart 2.x, a local base such as `tahoe-base` (or `--base ghcr.io/cirruslabs/macos-tahoe-base:latest`), roughly 50 GB free for the base |
| Ubuntu container | Docker or OrbStack, a host architecture with a matching image, network access for Nix |
| Fedora container | Same as Ubuntu |

If Docker, Tart, the base image, or Nix is missing, report the gap. Do not
substitute a weaker check and call it a pass.

## Journeys

| Journey | Entry point | Observable success | Owned cleanup |
|---|---|---|---|
| macOS isolated host | `make test-macos` | exit 0, `macOS isolated acceptance passed`, 501 tests | temp tree removed |
| macOS Tart VM | `make test-macos-vm` | exit 0, `macOS Tart acceptance passed`, 21 verify PASS | VM deleted and verified gone |
| Ubuntu container | `python3 tests/docker_matrix.py --case ubuntu` | exit 0, smoke `verify` plus fish/rg/nvim | container removed by `--rm`; image removed unless `--keep` |
| Fedora container | `python3 tests/docker_matrix.py --case fedora` | same as Ubuntu | same as Ubuntu |

The scripts are the authoritative helpers. Do not reimplement their steps by
hand. Details and evidence commands are in
[references/journeys.md](references/journeys.md).

## Rules

- Never run a host-mutating `./bootstrap.sh install` as a platform test. That is
  a deployment, not this skill's isolated verification.
- `--keep` is the only reason to leave a temp tree, VM, or image. Use it for
  debugging, not for a passing run.
- Shared caches and bases are retained: the Nix store, Docker base layers and
  build cache, and Tart base images. `--prune-cache` is opt-in and global.
- Capture exit codes, PASS/FAIL counts, and the cleanup checks. Keep logs under
  `/tmp`; they are small and are the evidence.
- A failed run still cleans its owned instance. If cleanup fails, report the
  exact leftover and do not claim a pass.

## Coverage Gaps

State these explicitly in a handoff:

- Intel macOS is not covered by Tart; the Intel job is manual in GitHub Actions.
- Docker covers Ubuntu and Fedora userland, not real Linux hardware or the host
  kernel.
- WSL is not covered by the local matrix.
- Local Docker runs the host architecture; the CI amd64 result is separate
  evidence.
- `make test-macos` isolates HOME/XDG/CODEX/RUSTUP/CARGO but not launchd. It does
  not configure the nightly scheduler.
- The Tart VM is ephemeral macOS; it does not prove host integration such as
  launchd or App Store state.

## Validate

1. Run one journey end to end and keep the exit code and PASS count.
2. Run the cleanup checks in [references/cleanup.md](references/cleanup.md).
3. Confirm `git status --short` shows only unrelated user work and the lockfiles
   are unchanged.
4. `make test-pre` for the repository gates.
