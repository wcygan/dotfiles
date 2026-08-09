---
sidebar_position: 1
slug: /
---

# Dotfiles

Modern developer configuration with safe installation and Nix package management.

## Installation

Clone the repository and run the supported bootstrap entry point:

```bash
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles
./bootstrap.sh
```

The bootstrapper loads Nix, enters the default development shell, and invokes
the locked Python CLI:

```bash
nix develop .#default --command uv run --locked python -m dotfiles_setup install
```

By default, installation upgrades or adds the repository Nix profile, links
managed configuration, prepares Rust tooling, and runs verification. Existing
configuration files are backed up before they are replaced by managed links.
Interactive Bash and zsh handoff to Fish is deliberately opt-in:

```bash
./bootstrap.sh install --shell-handoff
```

### Installing Nix

On macOS, if Nix is unavailable, `./bootstrap.sh` opens the Determinate macOS
installer package. Complete the package installation, start a fresh shell, and
rerun `./bootstrap.sh`.

On Linux and WSL, installation is explicit:

```bash
./bootstrap.sh --install-nix --yes
```

That confirmation is required before the bootstrapper invokes the official
Determinate installer.

## What You Get

- **🚀 Modern CLI Tools**: ripgrep, fd, bat, eza, fzf, delta, and more
- **🐟 Fish Shell**: Full configuration with functions and abbreviations  
- **⭐ Starship Prompt**: Beautiful, fast, and context-aware
- **📦 Nix Packages**: Reproducible installations across all platforms
- **🔗 Safe Symlinks**: Automatic backups before any changes

## Supported Platforms

I am personally test the dotfiles on these Operating Systems:

| Platform | Version | Status |
|----------|---------|--------|
| macOS | 12+ (Intel & Apple Silicon) | ✅ Fully supported |
| Ubuntu | 20.04+ | ✅ Fully supported |
| Fedora | 38+ | ✅ Fully supported |

Note: Other Operating Systems may "just work".

## After Installation

Depending on your shell:

### Fish (Recommended)
```bash
exec fish -l
```

### Bash/Zsh
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
source ~/.config/shell-nix.sh
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

## Repository Structure

```
dotfiles/
├── config/             # Configuration files
│   ├── fish/           # Fish shell config
│   ├── starship.toml   # Starship prompt
│   └── shell-nix.sh    # Bash/zsh compatibility
├── src/dotfiles_setup/  # Python setup CLI modules
├── tests/               # Pytest and platform test suites
├── flake.nix           # Nix package definitions
├── bootstrap.sh         # Nix bootstrap and CLI bridge
├── pyproject.toml       # Python project metadata
├── uv.lock              # Locked Python dependencies
└── docs/               # This documentation
```

## Core Principles

- **Idempotent**: Every operation is safe to run multiple times
- **Cross-platform**: Same experience on macOS, Ubuntu, and Fedora
- **Minimal**: Clean configs under `config/`, packages in `flake.nix`
- **Safe**: Pre-flight checks prevent problems, backups enable rollback
- **Reproducible**: Nix ensures identical tool versions everywhere

## Common Tasks

### Update Packages
```bash
make update
```

### Add New Tools
Edit `flake.nix`, then:
```bash
make profile
```

### Setup Commands
```bash
make install                 # Full setup; same as ./bootstrap.sh
make link                    # Link managed config only
make link-dry                # Preview managed link changes
make git-user                # Configure Git identity
make setup-rustup-components # Prepare rust-analyzer
make setup-shell-handoff     # Opt in to Bash/zsh -> Fish handoff
make verify                  # Verify configured environment
make doctor                  # Read-only diagnostics
make uninstall               # Remove managed links after confirmation
make uninstall-dry           # Preview managed-link removal
```

Each setup target has a direct `./bootstrap.sh <command>` equivalent. The
bridge consistently executes `nix develop` and `uv run --locked`; use it rather
than calling project modules from an arbitrary host Python.

### Run Tests

```bash
make test-pre    # Locked Ruff and pytest checks
make test-local  # Ephemeral-HOME-focused pytest
make test-shell  # Shell-handoff pytest
make test-docker # Python Ubuntu/Fedora driver
make test         # All non-Docker tests
```

### Roll Back

`nix profile rollback` restores a previous Nix profile generation. Managed
links save pre-existing paths with timestamped backup names, and rerunning
`make link` or `./bootstrap.sh link` is safe. Tag a known-good repository
revision before a broader migration to retain a straightforward source rollback.

### Python Project Structure

The locked Python project is under `src/dotfiles_setup/`. `cli.py` dispatches
commands to focused modules for Nix profile updates, configuration links and
cleanup, doctor checks, Rust setup, shell handoff, and Git identity. Tests live
under `tests/`; `pyproject.toml` and `uv.lock` define the reproducible Python
environment.


## Troubleshooting

### Command Not Found
After installation, restart your shell or source the appropriate config file.

### Nix Commands Not Working
```bash
# Multi-user installations
source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
```

### Permission Denied
The installer will request sudo when needed. Ensure you're in the sudoers group on Linux.
