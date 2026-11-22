# Test Suite

Locked Python and platform tests for the tracked dotfiles configuration.

## Quick Start

```bash
# Locked Ruff and complete pytest suite
make test-pre

# Ephemeral-HOME-focused pytest suite
make test-local

# Shell handoff pytest suite (Bash/zsh -> Fish)
make test-shell

# Alias for make test-pre
make test

# Quick Linux evidence from macOS: tests plus install, doctor, verify (Ubuntu)
make test-linux

# Python driver across Ubuntu and Fedora
make test-docker
```

## Test Descriptions

### `make test-pre`
- Runs Ruff and the complete locked pytest suite
- Exercises the Python CLI and its modules without changing a real home
- Is the first required check for code and documentation changes

Within `make test-pre`, `tests/test_crash_sweep.py` crashes four commands
(link, uninstall, shell handoff, and nightly schedule files) before each
journal write, rename, symlink, mkdir, and file creation. It checks recovery at
every crash point and reruns the command once per distinct recovered state,
not after every point. `tests/test_bootstrap.py` covers `--run` and the saved dev
environment with a stand-in `nix`.

### `make test-local`
- Runs the pytest checks that focus on an ephemeral `HOME`
- Covers managed-link behavior without changing your real configuration

### `make test-shell`
- Runs the Python shell-handoff test suite
- Covers interactive Bash/zsh -> Fish behavior without modifying startup files

### `make test-linux`
- Quick way to get Linux evidence from macOS
- Builds the Docker `tests` target: install, reinstall, `doctor`, `verify`, smoke, then the test suite, in an Ubuntu container
- `DOCKER_CASE=fedora` selects Fedora

### `make test-docker`
- Runs the Python driver against Ubuntu and Fedora containers
- Provides the cross-platform acceptance check; it is separate from `make test`

## After Testing

Once tests pass, install:
```bash
./bootstrap.sh            # Full default setup
# or, for links only:
./bootstrap.sh link
exec fish -l              # Start fish
```
