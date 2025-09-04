---
sidebar_position: 1
slug: /
---

# Dotfiles

Modern developer configuration with safe installation and Nix package management.

## Installation

Just three commands:

```bash
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles
./install.sh
```

## What Happens During Installation

The `install.sh` script performs:

### Pre-flight Checks
- Detects your OS (macOS, Ubuntu, or Fedora)
- Verifies required tools (curl, git)
- Confirms sudo access if needed

### Installation Steps
1. **Nix Setup**: Installs Nix package manager via Determinate Systems
2. **Package Installation**: Installs all tools from `flake.nix`
3. **Configuration Linking**: Symlinks configs to appropriate locations

### Post-flight Verification
- Confirms all tools are installed
- Validates configuration files
- Provides shell-specific next steps

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
├── scripts/            # Installation scripts
├── flake.nix           # Nix package definitions
├── install.sh          # One-command installer
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
nix flake update
nix profile upgrade '.*'
```

### Add New Tools
Edit `flake.nix`, then:
```bash
nix profile install .
```

### Uninstall Configs
```bash
make uninstall
```

### Run Tests
```bash
make test-pre    # Pre-flight checks
make test-local  # Full test suite
```

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
