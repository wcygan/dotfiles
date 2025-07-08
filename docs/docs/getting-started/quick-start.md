---
sidebar_position: 2
---

# Quick Start Guide

Get up and running with the dotfiles configuration in minutes.

## Essential Commands

### Installation & Management

```bash
# Install dotfiles
deno task install

# Check installation status
deno task test

# Rollback if needed
deno task rollback
```

### Development Tasks

```bash
# Run pre-commit checks
deno task pre-commit

# Run CI checks locally
deno task ci:check

# Clean old backups
deno task clean-backups
```

## Key Features

### 1. Safe Installation

The installation process:

- Creates automatic backups before any changes
- Validates all operations before execution
- Provides rollback capabilities
- Supports dry-run mode for testing

### 2. Shell Aliases and Functions

After installation, you'll have access to powerful shell aliases and functions:

```bash
# Enhanced navigation
ll    # Detailed file listing with git status
..    # Go up one directory
...   # Go up two directories

# Git shortcuts
gs    # git status
gc    # git commit
gp    # git push

# Utility functions
mkd   # Create directory and cd into it
proj  # Quick project navigation
```

### 3. Modern Shell Configuration

Your shell will be configured with:

- **Aliases**: Shortcuts for common commands
- **Functions**: Powerful shell functions
- **Path Management**: Organized PATH configuration
- **Environment Variables**: Development-friendly defaults

### 4. Editor Configuration

Includes configurations for:

- VS Code
- Zed
- Cursor
- Vim

## Customization

### Personal Configuration

Create `~/.extra.sh` for personal settings that won't be overwritten:

```bash
# ~/.extra.sh
export MY_API_KEY="..."
alias myproject="cd ~/projects/myproject"
```

### Claude Commands

Add custom commands in `~/.claude/commands/`:

```bash
mkdir -p ~/.claude/commands/custom
echo "My custom command" > ~/.claude/commands/custom/my-command.md
```

## Troubleshooting

### Common Issues

**Deno not found**

```bash
# Install Deno
curl -fsSL https://deno.land/install.sh | sh
```

**Permission denied**

```bash
# Ensure scripts are executable
chmod +x scripts/*.ts
```

**Backup directory full**

```bash
# Clean old backups
deno task clean-backups
```

## Next Steps

- Explore the [configuration options](/docs/configuration/shell)
- Learn about [shell configuration](/docs/configuration/shell)
- Set up [editor integrations](/docs/configuration/editors)
