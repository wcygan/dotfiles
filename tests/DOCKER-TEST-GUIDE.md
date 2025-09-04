# Docker Test Guide

## Quick Start

```bash
# Build and run the test container
./test-docker.sh

# Once inside the container, run:
./run-tests.fish
```

## What Gets Tested Automatically

The `run-tests.fish` script checks:
- ✅ Fish configuration loads properly
- ✅ Nix environment variables are set
- ✅ Custom functions (nix-try, nix-install) are available
- ✅ Abbreviations are created
- ✅ Direnv hook is configured (if available)
- ✅ Starship prompt is initialized (if available)

## Manual Testing Checklist

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
# nix-update → nix flake update && nix profile upgrade
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

When you run `./run-tests.fish`, you should see:
- Multiple "✅" marks for passed tests
- Details about loaded configurations
- A summary showing most/all tests passed

Some tests might show "ℹ️" (info) instead of pass/fail - this is normal in the Docker environment where certain tools might not be installed.

## Exit the Container

```fish
exit
# or press Ctrl+D
```

The container is automatically removed after exit (--rm flag), leaving no traces on your system.