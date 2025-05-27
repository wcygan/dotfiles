# Will's Dotfiles

Modern shell configuration for Bash and Zsh with enhanced features and cross-platform support.

## Installation

### Prerequisites

Install Deno:

```bash
# macOS/Linux
curl -fsSL https://deno.land/install.sh | sh

# Windows (PowerShell)
irm https://deno.land/install.ps1 | iex

# Or via package managers
brew install deno          # Homebrew
cargo install deno --locked # Cargo
npm install -g @deno/cli   # npm
```

### Install Dotfiles

```bash
git clone https://github.com/wcygan/dotfiles.git && cd dotfiles
deno run --allow-all install-safely.ts
```

This will:
- Backup your existing dotfiles
- Install new configuration
- Reload your shell

## Usage

### Essential Commands

```bash
# Edit/reload shell config
vv    # Edit current shell config
ss    # Reload current shell config

# Modern CLI tools (if installed)
ll    # Better ls with exa
cat   # Syntax highlighting with bat

# Development shortcuts
d     # Open development workspace
mm    # Git main branch helper
```

### What's Included

- Enhanced shell prompts with git status
- Modern CLI tool aliases
- Development tool integrations
- Cross-platform compatibility
- Editor configurations (Cursor, Zed, VS Code, Vim)

## Rollback

If you need to restore your original configuration:

```bash
deno run --allow-all rollback.ts ~/.dotfiles-backup-TIMESTAMP
```

The installation script will show you the exact backup directory path.

## Customization

Add personal settings to `~/.extra`:

```bash
# Git credentials
GIT_AUTHOR_NAME="Your Name"
GIT_AUTHOR_EMAIL="your.email@example.com"

# Custom aliases
alias myproject="cd ~/path/to/project"

# Environment variables
export API_KEY="your-secret-key"
```
