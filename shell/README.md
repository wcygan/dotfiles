# Shell Configuration Files

This directory contains all shell-related configuration files organized by shell type.

## Directory Structure

```
shell/
├── bash/           # Bash-specific configurations
│   ├── bashrc      # Main bash configuration
│   └── bash_profile # Bash profile for login shells
├── zsh/            # Zsh-specific configurations
│   └── zshrc       # Main zsh configuration
├── powershell/     # PowerShell configurations (Windows)
│   └── profile.ps1 # PowerShell profile
├── common/         # Shared configurations across shells
│   ├── aliases.sh  # Command aliases
│   ├── exports.sh  # Environment variables
│   ├── functions.sh # Shell functions
│   ├── path.sh     # PATH configuration
│   ├── extra.sh    # Extra/private settings
│   └── platform.sh # Platform-specific settings
└── vim/            # Vim editor configuration
    └── vimrc       # Vim settings
```

## Installation

The `install-safely.ts` script automatically copies these files to their appropriate locations:

- **Unix shells (bash/zsh)**: Files are copied to `$HOME` with a dot prefix (e.g., `bashrc` → `.bashrc`)
- **PowerShell**: `profile.ps1` is copied to `~/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1`
- **Common files**: Sourced by both bash and zsh configurations

## Adding New Shells

To add support for a new shell:

1. Create a new directory under `shell/` (e.g., `shell/fish/`)
2. Add the shell configuration files
3. Update `FILE_MAPPINGS` in `scripts/install-safely.ts`
4. Add any special installation logic if needed