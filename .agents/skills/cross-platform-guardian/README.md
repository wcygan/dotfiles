# Cross-Platform Guardian Reference

Use this skill for changes that could diverge across macOS, Ubuntu, Fedora, or
Linux/WSL.

The platform boundary is `bootstrap.sh` -> Nix -> `nix develop` -> `uv run
--locked python -m dotfiles_setup`. macOS uses a Determinate installer package
handoff when Nix is missing. Linux/WSL only runs the official installer after
`./bootstrap.sh --install-nix --yes`.

Validation layers:

- `make test-pre`: locked Ruff and pytest.
- `make test-local`: ephemeral-HOME-focused pytest.
- `make test-shell`: shell-handoff pytest.
- `make test-docker`: Python Ubuntu/Fedora driver.
- `make test`: all non-Docker tests.

Treat the Docker result as Linux acceptance only. Run relevant checks on macOS
for changes to shell initialization, path handling, or the package handoff.

Rollback package changes with `nix profile rollback`. Managed links protect
existing local paths with timestamped backups; keep a known-good Git tag before
a broad configuration migration.
