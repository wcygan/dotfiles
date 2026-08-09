---
name: cross-platform-guardian
description: "Protect macOS, Ubuntu, Fedora, and Linux/WSL compatibility in this dotfiles repository. Use for portability reviews, Nix changes, bootstrap changes, and platform test failures."
---

# Cross-Platform Guardian

## Outcome

Keep the setup path reproducible across macOS, Ubuntu, Fedora, and Linux/WSL
without hard-coded machine paths or untested platform assumptions.

## Current Setup Boundary

- `bootstrap.sh` is the supported entry point. It loads Nix, enters `nix
  develop .#default`, and runs `uv run --locked python -m dotfiles_setup`.
- macOS delegates missing-Nix installation to the Determinate package handoff.
- Linux and WSL require `./bootstrap.sh --install-nix --yes` before the
  bootstrapper runs the official Determinate installer.
- Python modules under `src/dotfiles_setup/` own profile, link, cleanup,
  diagnostics, Rust, Git identity, and opt-in shell handoff behavior.
- The default install must not edit Bash or zsh startup files; `shell-handoff`
  is explicit.

## Review Workflow

1. Inspect `bootstrap.sh`, the affected Python module, `flake.nix`, and the
   matching pytest coverage before proposing a change.
2. Check macOS and Linux/WSL behavior separately. Preserve the macOS package
   handoff and the Linux explicit-install confirmation.
3. Keep platform paths behind the functions in `links.py`; use `HOME`,
   `XDG_CONFIG_HOME`, and `CODEX_HOME` rather than user-specific paths.
4. Run `make test-pre`, then the focused suite: `make test-local` for links,
   `make test-shell` for handoff, and `make test-docker` for Ubuntu/Fedora
   acceptance when the blast radius is cross-platform.
5. Report platform evidence, skipped checks, and the rollback path. Nix package
   regressions roll back with `nix profile rollback`; managed links preserve
   timestamped backups.

## Stop Conditions

Do not claim macOS packaged behavior from a Linux container. Do not add a
second installer, restore retired shell setup scripts, or mutate user startup
files without the explicit shell-handoff request.
