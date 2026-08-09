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

# All non-Docker tests
make test

# Python driver across Ubuntu and Fedora
make test-docker
```

## Test Descriptions

### `make test-pre`
- Runs Ruff and the complete locked pytest suite
- Exercises the Python CLI and its modules without changing a real home
- Is the first required check for code and documentation changes

### `make test-local`
- Runs the pytest checks that focus on an ephemeral `HOME`
- Covers managed-link behavior without changing your real configuration

### `make test-shell`
- Runs the Python shell-handoff test suite
- Covers interactive Bash/zsh -> Fish behavior without modifying startup files

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
