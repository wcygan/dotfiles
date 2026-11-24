# Docker Test Guide

## Quick Start

```bash
# Does this work on Linux? Run from the repository root on any host with Docker.
make test-linux

# The acceptance check on both distros, with local layer reuse
make test-docker

# Fetch dependencies during the first install, as CI does without an archive
DOCKER_SKIP_PREWARM=1 make test-docker
```

| Command | Distro | What it proves |
|---------|--------|----------------|
| `make test-linux` | Ubuntu; `DOCKER_CASE=fedora` for Fedora | First install, second install, `doctor`, `verify`, the login-shell smoke check, then `make test-syntax test-pre` |
| `make test-docker` | Ubuntu and Fedora; `DOCKER_CASE` selects one | Everything above except the test suite |

Neither command opens an interactive container or leaves an image behind.

## How It Works

Each check is a `RUN` step in `Dockerfile.ubuntu` or `Dockerfile.fedora`, so a
check passes when the build passes. The stages build on each other:

| Stage | Contents | Rebuilt when |
|-------|----------|--------------|
| `base` | Distro packages, the `tester` user, the pinned Nix fixture | The Dockerfile changes |
| `prewarm` | Nix closure of the profile and dev shell, pinned Rust toolchain | `flake.nix`, `flake.lock`, or `rust-toolchain.toml` changes |
| `acceptance` | Install, reinstall, `doctor`, `verify`, smoke check | `bootstrap.sh`, `src/`, `config/`, `pyproject.toml`, or `uv.lock` changes |
| `tests` | `make test-syntax test-pre` | Any file in the build context changes |

Docker reuses every stage whose inputs are unchanged. A run that changes
nothing finishes in about a second and proves nothing new; a change under
`src/` reruns the install checks and the tests but not the downloads.

Measured on an Apple silicon Mac (`linux/arm64`, Ubuntu unless noted):

| Run | Time |
|-----|------|
| `DOCKER_CASE=ubuntu make test-docker`, nothing cached | 211 s, of which `prewarm` is 189 s |
| `DOCKER_CASE=fedora make test-docker`, nothing cached | 162 s, of which `prewarm` is 126 s |
| `make test-linux` after a change under `src/` | 36 s: 7 s install checks, 29 s tests |
| `make test-linux` with nothing changed | 1 s |

`docker builder prune` discards the `prewarm` stage, and the next run downloads
it again.

The `prewarm` stage lets local installs reuse the Nix store paths and Rust
toolchain. CI uses a shared archive for Ubuntu when available. Fedora and
Ubuntu cache misses outside the default branch set `DOCKER_SKIP_PREWARM=1` to
fetch pinned dependencies during the first install. The scheduled freshness
workflow also skips prewarm and tests with the current container tags.

## Driver Options

```bash
python3 tests/docker_matrix.py --case fedora     # one distro
python3 tests/docker_matrix.py --target tests    # also run the test suite
python3 tests/docker_matrix.py --keep            # also load nixdotfiles:test-<distro>
python3 tests/docker_matrix.py --dry-run         # print commands only
```

`--layer-cache DIR` (or `DOCKER_LAYER_CACHE`) reads the `base` and `prewarm`
stages from a directory and fills it when it is empty. CI uses it with
`actions/cache`; it needs a `docker-container` Buildx builder, so leave it
unset locally.

## Manual Container Debugging

When the driver fails, the build output ends with the failing step. To explore
the installed result, `make docker-ubuntu` or `make docker-fedora` builds the
`acceptance` stage and opens a shell in it. Reproduce the failing command with
`./bootstrap.sh`. On Linux, a missing
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
# /home/tester/.config/fish/conf.d/10-nix.fish
# /home/tester/.config/fish/conf.d/20-direnv.fish
# /home/tester/.config/fish/conf.d/30-starship.fish
# /home/tester/.config/fish/config.fish
# /home/tester/.config/fish/functions/nix-install.fish
# /home/tester/.config/fish/functions/nix-try.fish
```

## Expected Output Summary

Each command prints one line per distro, such as `ubuntu tests: passed in 36s`,
and exits non-zero at the first failing step. The first run downloads the
container images, the Nix closure, and the Rust toolchain.
