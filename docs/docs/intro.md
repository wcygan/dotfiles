---
sidebar_position: 1
slug: /
---

# Dotfiles

Welcome to my dotfiles repository

## Features

- **🚀 Modern CLI Tools**: Configurations for ripgrep, fd, bat, eza, fzf, and more
- **🐟 Fish Shell**: Full fish configuration with functions, abbreviations, and aliases  
- **📦 Nix Package Management**: Reproducible tool installation via flake.nix
- **🔗 Safe Symlink Management**: Automated config linking with backup/restore

## Quick Start

```bash
# Clone the repository
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles

# Install Nix package manager (if not already installed)
curl -L https://nixos.org/nix/install | sh

# Run tests
make test-pre

# Link configurations
make link-config
```

## Repository Structure

```
dotfiles/
├── config/           # Configuration files (fish, starship, etc.)
├── scripts/          # Installation and utility scripts
├── flake.nix         # Nix package definitions
├── tests/            # Test suites
└── docs/             # This documentation site
```

## Principles

- **Idempotent**: Every script is safe to run twice
- **Cross-platform**: Works on macOS, Ubuntu, and Fedora
- **Minimal surface area**: Simple configs under `config/`, packages in `flake.nix`
- **Test-first operations**: Pre-flight checks before any changes
- **Rollbackable**: All changes can be reverted
