# Docker Test Guide

## Quick Start

```bash
# Run the Python Ubuntu/Fedora test driver from the repository root
make test-docker
```

The Docker target is an acceptance check for the locked Python setup CLI. It
does not open an interactive container and it is intentionally separate from
the local `make test` suite.

## What Gets Tested Automatically

The Python driver checks the supported bootstrap and setup behavior on Ubuntu
and Fedora. Use `make test-pre` for locked Ruff and pytest checks, `make
test-local` for ephemeral-HOME-focused pytest, and `make test-shell` for the
shell-handoff pytest suite.

## Manual Container Debugging

When the driver fails, inspect the platform Dockerfile selected by the driver
and reproduce the failing command with `./bootstrap.sh`. On Linux, a missing
Nix installation requires the explicit bootstrap authorization:

```bash
./bootstrap.sh --install-nix --yes
```

Then run the direct CLI-equivalent command, for example `./bootstrap.sh
verify` or `./bootstrap.sh install`.

## Configuration Inspection Checklist

### 1. Basic Functionality
```fish
# Check fish is working
echo $FISH_VERSION

# Check config loaded
ls -la ~/.config/fish/
```

### 2. Nix Environment
```fish
# Verify NIX_CONFIG is set
echo $NIX_CONFIG
# Should output: experimental-features = nix-command flakes

# Check PATH includes Nix
echo $PATH | tr ':' '\n' | grep nix
```

### 3. Custom Functions
```fish
# List our custom functions
functions | grep nix

# Test nix-try function
nix-try
# Should show: Usage: nix-try <package>

# Test nix-install function  
nix-install
# Should show: Usage: nix-install <package>

# Check function locations
type -a nix-try
type -a nix-install
```

### 4. Abbreviations
```fish
# Type this and press TAB:
nix-

# Should show completions like:
# nix-update → nix flake update && nix profile upgrade --no-write-lock-file
# nix-search → nix search nixpkgs
# nix-list → nix profile list
# nix-clean → nix-collect-garbage -d

# Type this and press SPACE:
nix-list
# Should expand to: nix profile list
```

### 5. Interactive Test
```fish
# Try tab completion
nix-<TAB>
# Should show all nix- abbreviations

# Check if functions are in scope
which nix-try
which nix-install
```

### 6. Config Files Check
```fish
# List config structure
find ~/.config/fish -type f -name "*.fish" | sort

# Should show:
# /home/testuser/.config/fish/conf.d/10-nix.fish
# /home/testuser/.config/fish/conf.d/20-direnv.fish
# /home/testuser/.config/fish/conf.d/30-starship.fish
# /home/testuser/.config/fish/config.fish
# /home/testuser/.config/fish/functions/nix-install.fish
# /home/testuser/.config/fish/functions/nix-try.fish
```

## Expected Output Summary

`make test-docker` returns the Python driver's pass/fail result for both
platforms. It may download Nix and container images, so run it after the faster
local suites have passed.
