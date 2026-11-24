---
name: nix-update
description: Compare locked Nix package versions, update flake inputs for review, or update and apply the dotfiles profile.
---

# Update Nix inputs

Start with `git status --short`, `git diff -- flake.lock`, and the input
revisions in the working copy of `flake.lock`. Preserve pre-existing edits.
Use [nix-manager](../nix-manager/SKILL.md) for package selection and profile
mechanics.

## Choose how far to take the update

- **Compare versions.** Use the requested revisions and system. A comparison
  can be completed without writing the lock or installing a profile.
- **Update the lockfile for review.** From the repository root, run the
  lock-update step of the [Makefile](../../../Makefile):
  `nix --extra-experimental-features "nix-command flakes" flake update --refresh`.
  Append the requested input name for a single-input update. Inspect the lock
  diff and verify the result. The installed profile stays at its previous
  generation.
- **Update all inputs and apply them to this machine.** With both effects
  authorized, run `make update`. It updates the lock, then runs
  `./bootstrap.sh profile`. For a single input, run the scoped lock update
  above and the authorized profile step. To apply an already-reviewed lock,
  run only `./bootstrap.sh profile`.

## Verify and report

Inspect the changed input revisions. Compare the requested or important
packages actually selected in `flake.nix` before and after the update. Follow
the input, target system, and local overrides used by each package. Report any
version you could not determine.

For a lock change, run `make test-eval` to evaluate all four declared systems,
`nix build .#default --dry-run --no-write-lock-file` for the host build plan,
and `make test-pre`. After a profile application, run `./bootstrap.sh verify`.
If a combined update fails, inspect the lock diff and profile state to find
which step completed before retrying. Preserve the user's existing changes.

Report changed input revisions, material package changes, verification
results, and whether the host profile was applied. If the inputs were already
current, say so.
