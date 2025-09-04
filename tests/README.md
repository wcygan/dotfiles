# Test Suite

Three levels of testing to verify fish configuration before installation.

## Quick Start

```bash
cd tests/

# Pre-flight check (no changes)
./test-fish-setup.sh

# Local isolated test (temp HOME)
./test-ephemeral.sh

# Docker test (full isolation)
./test-docker.sh
```

## Test Descriptions

### `test-fish-setup.sh`
- Validates configuration without making changes
- Checks flake.nix, config files, and dependencies
- Shows what will be installed

### `test-ephemeral.sh` 
- Creates temporary HOME directory
- Tests fish config loading in isolation
- No system changes, automatic cleanup

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