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

After installation, you'll have access to convenient shell aliases and functions:

```bash
# Enhanced navigation
alias l='exa -l'        # Detailed file listing
alias c='clear'         # Clear current terminal screen
alias ..='cd ..'        # Go up one directory
alias ...='cd ../.. '   # Go up two directories

# Git shortcuts
alias gs='git status'    # git status
alias gc='git commit'    # git commit
alias gp='git push'      # git push

# Utility functions
alias g='gemini'         # Start Gemini CLI
alias x='claude'         # Start Claude Code
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

- Learn about [shell configuration](/docs/configuration/shell)
