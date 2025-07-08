---
sidebar_position: 1
---

# Installation

Welcome to the dotfiles installation guide. This repository provides a modern,
safe installation process for developer configuration files.

## Prerequisites

- **Deno**: Required for running installation scripts
- **Git**: For cloning the repository
- **Shell**: Bash or Zsh

## Quick Start

```bash
# Clone the repository
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles

# Install dotfiles with automatic backup
deno task install
```

## Installation Options

### Standard Installation

The standard installation creates backups of existing files before installing:

```bash
deno task install
```

### Force Installation

Skip confirmation prompts (backups are still created):

```bash
deno task install:force
```

### Custom Installation

Run the installation script directly with options:

```bash
deno run --allow-all scripts/install-safely.ts --help
```

## What Gets Installed

The installation process manages these dotfiles:

- **Shell Configuration**: `.zshrc`, `.bashrc`, `.bash_profile`
- **Shell Scripts**: `.path.sh`, `.exports.sh`, `.aliases.sh`, `.functions.sh`,
  `.extra.sh`
- **Editor Configuration**: `.vimrc`
- **Claude Configuration**: `CLAUDE.md` and custom commands
- **User Scripts**: Tools copied to `~/.tools/`

## Backup and Rollback

### Automatic Backups

Every installation creates timestamped backups in `~/.dotfiles-backup/`:

```bash
~/.dotfiles-backup/
└── 2024-01-15T10-30-45.123Z/
    ├── .bashrc
    ├── .zshrc
    └── ...
```

### Rollback to Previous State

If you need to restore previous configurations:

```bash
# List available backups
ls ~/.dotfiles-backup/

# Rollback to most recent backup
deno task rollback

# Rollback to specific backup
deno run --allow-all scripts/rollback.ts --backup=2024-01-15T10-30-45.123Z
```

## Platform Support

The installation scripts are cross-platform and support:

- macOS
- Linux
- Windows (with PowerShell profile support)

## Next Steps

After installation:

1. Review the [Quick Start Guide](./quick-start)
2. Configure [Shell Settings](/docs/configuration/shell)
3. Customize your [Shell Configuration](/docs/configuration/shell)
