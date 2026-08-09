# Compatibility Checklist

| Surface | macOS | Linux/WSL | Evidence |
| --- | --- | --- | --- |
| Missing Nix | Determinate package handoff, then rerun bootstrap | explicit `--install-nix --yes` | `bootstrap.sh` tests |
| Setup runtime | `nix develop` plus locked `uv run` | same | CLI tests |
| Configuration paths | home and XDG-aware | home and XDG-aware | link tests |
| Shell handoff | opt-in only | opt-in only | `make test-shell` |
| Cross-platform acceptance | local macOS check when affected | Ubuntu/Fedora driver | `make test-docker` |

Inspect the earliest platform-specific failure before changing a later symptom.
Use `make test-pre` first, then the narrowest applicable suite. A container
cannot establish macOS package or interactive-shell acceptance.
