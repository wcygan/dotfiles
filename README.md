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

## Updating Existing Installation

If you already have the dotfiles installed and want to apply new changes:

### Quick Update

```bash
cd ~/dotfiles
git pull origin main
deno run --allow-all install-safely.ts --force
```

### Manual Update Steps

1. **Navigate to dotfiles directory:**
   ```bash
   cd ~/dotfiles
   ```

2. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

3. **Apply changes (with backup):**
   ```bash
   deno run --allow-all install-safely.ts
   ```
   
   Or force update without prompts:
   ```bash
   deno run --allow-all install-safely.ts --force
   ```

4. **Reload your shell:**
   ```bash
   ss  # Or restart your terminal
   ```

### What Gets Updated

- Shell configuration files (`.bashrc`, `.zshrc`, etc.)
- Aliases and functions
- Editor configurations
- Platform-specific settings
- New features and improvements

**Note:** Your existing backup will be preserved, and a new backup will be created if needed.

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

Add personal settings to `~/.extra.sh`:

```bash
# Git credentials
GIT_AUTHOR_NAME="Your Name"
GIT_AUTHOR_EMAIL="your.email@example.com"

# Custom aliases
alias myproject="cd ~/path/to/project"

# Environment variables
export API_KEY="your-secret-key"
```
