---
name: nix-manager
description: "Manage Nix package, profile, flake, and diagnostic work in this dotfiles repository. Use when changing flake.nix, troubleshooting Nix, applying profile changes, or explaining the locked Nix setup."
---

# Nix Manager

## Outcome

Keep this repository's Nix package profile reproducible across macOS, Ubuntu,
Fedora, and Linux/WSL. The repository defines the package closure; Nix profile
state is a user-owned result of the supported setup flow.

## Route First

Use `$dotfiles-operations` for every repository Nix task. Add the matching
specialist when the task crosses one of these boundaries:

- `$nix-update` for any `flake.lock` update or package-version comparison.
- `$cross-platform-guardian` for bootstrap, package, platform, or profile
  behavior that can differ across supported systems.
- `$config-change` for a configuration change that also needs a package.

Do not treat this skill's examples as a substitute for the current
`flake.nix`, `Makefile`, or operations validation matrix.

## Inspect

Before changing Nix-owned files, read the current `flake.nix`, `Makefile`, and
the relevant module under `src/dotfiles_setup/`. Inspect the worktree first:

```bash
git status --short
git diff -- flake.nix flake.lock
```

For a live profile, installation, or verification request, also inspect the
supported state rather than ambient `PATH`:

```bash
./bootstrap.sh doctor
./bootstrap.sh verify
nix profile list --json
```

## Boundaries

- `flake.nix` is the source of package selection and declared systems;
  `flake.lock` pins its inputs.
- `bootstrap.sh` is the only root setup entry point. Profile installation and
  upgrade use `./bootstrap.sh profile`; normal consumers keep committed locks
  unchanged.
- `make update` is the explicit all-input update path. It is the only normal
  workflow here that changes `flake.lock`; use `$nix-update` before running it.
- `nix profile rollback` is the recovery path for an already-applied profile
  generation. It is a user-state mutation and requires explicit authority.
- Read the actual flake input when its branch, package version, or supported
  output matters. Do not encode a copied branch name or package inventory in
  agent guidance.

## Workflows

### Package change

1. Edit only `flake.nix`, retaining its existing package grouping and supported
   systems. Do not update `flake.lock` for a package-list change.
2. Run `make test-pre`, then `make test-eval` for the four-system contract.
3. After authority to mutate the user profile, run:

   ```bash
   ./bootstrap.sh profile
   ./bootstrap.sh verify
   ```

4. Report evaluation evidence separately from installed-profile and platform
   evidence.

### Input update

Use `$nix-update`. It owns the lock diff, package-version comparison, and
validation sequence. Run `make update` only for an explicit update request;
then verify the profile and confirm no unrelated lockfile changed.

### Diagnosis

Start at the first failed boundary: pending recovery or mutation lock, Nix
availability, exact profile origin, profile store outputs, then managed links.
Use `./bootstrap.sh recover` only to inspect; applying recovery needs explicit
authority. Do not repair an exact-profile failure by changing the global Nix
configuration or trusting a binary found on ambient `PATH`.

## Validation and Handoff

Use the validation matrix in `$dotfiles-operations`; Nix package or system
changes require `make test-pre` and `make test-eval`. Cross-platform bootstrap
work also requires Docker and affected-platform evidence. Before finishing:

```bash
git diff --check
git diff --exit-code -- flake.lock uv.lock
git status --short
```

Report the files changed, lockfile intent, commands and results, platform
evidence, profile/recovery state, rollback path, and commit/push status.

## References

- Repository architecture and the validation matrix:
  `$dotfiles-operations`.
- Advanced Nix language patterns and standalone-project examples:
  [REFERENCE.md](REFERENCE.md). They are not the dotfiles repository contract;
  load them only when the current flake and operations guidance do not answer
  the Nix-language question.
