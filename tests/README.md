# Test Suite

Preflight and integration tests for the tracked dotfiles configuration.

## Quick Start

```bash
cd tests/

# Pre-flight check (no changes)
./test-fish-setup.sh

# Global Codex skill catalog
./test-codex-skills.sh

# Local isolated test (temp HOME)
./test-ephemeral.sh

# Shell handoff test (bash/zsh → fish)
./test-shell-handoff.sh

# Docker test (full isolation)
./test-docker.sh
```

## Test Descriptions

### `test-fish-setup.sh`
- Validates configuration without making changes
- Checks flake.nix, config files, and dependencies
- Shows what will be installed

### `test-codex-skills.sh`
- Validates the exact active global Codex skill inventory
- Checks Codex-compatible frontmatter and directory names
- Verifies loop composition, explicit invocation policy, and deprecation routing
- Rejects destructive Git recipes and machine-specific home paths

### `test-ephemeral.sh` 
- Creates temporary HOME directory
- Tests fish config loading in isolation
- No system changes, automatic cleanup

### `test-shell-handoff.sh`
- Tests bash/zsh → fish handoff for interactive sessions
- Verifies non-interactive commands stay in bash/zsh
- Validates VAR=value syntax compatibility
- Helps verify setup before running `chsh`

### `test-docker.sh`
- Complete isolation in Docker container
- Full Nix + Fish environment
- Run `./run-tests.fish` inside container for automated tests

## After Testing

Once tests pass, install:
```bash
cd ..
./scripts/link-config.sh  # Create symlinks
exec fish -l              # Start fish
```
