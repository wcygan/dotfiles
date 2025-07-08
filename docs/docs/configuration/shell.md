---
sidebar_position: 1
---

# Shell Configuration

The dotfiles provide comprehensive shell configuration for both Bash and Zsh.

## Configuration Files

### Core Files

- **`.bashrc`** / **`.zshrc`**: Main shell configuration
- **`.bash_profile`**: Bash login shell configuration
- **`.path.sh`**: PATH environment variable management
- **`.exports.sh`**: Environment variables
- **`.aliases.sh`**: Command aliases
- **`.functions.sh`**: Shell functions
- **`.extra.sh`**: Personal configuration (not tracked)

### File Loading Order

#### Bash

1. `.bash_profile` (login shells)
2. `.bashrc` (non-login shells)
3. Common files (path, exports, aliases, functions, extra)

#### Zsh

1. `.zshrc`
2. Common files (path, exports, aliases, functions, extra)

## Common Aliases

### Navigation

```bash
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias ~="cd ~"
alias -- -="cd -"
```

### Enhanced Commands

```bash
alias ll="eza -la --git"
alias la="eza -la"
alias l="eza -l"
alias tree="eza --tree"
```

### Git Shortcuts

```bash
alias g="git"
alias gs="git status"
alias ga="git add"
alias gc="git commit"
alias gp="git push"
alias gl="git log --oneline"
```

## Environment Variables

### Development Tools

```bash
export EDITOR="vim"
export VISUAL="$EDITOR"
export PAGER="less"
```

### Language Settings

```bash
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
```

### History Configuration

```bash
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoreboth:erasedups
```

## Shell Functions

### Project Navigation

```bash
# Quick project access
function proj() {
  cd ~/Development/$1
}

# Create directory and cd into it
function mkd() {
  mkdir -p "$@" && cd "$_"
}
```

### Development Helpers

```bash
# Find process by name
function findproc() {
  ps aux | grep -v grep | grep "$1"
}

# Extract various archive formats
function extract() {
  # Handles .tar.gz, .zip, .7z, etc.
}
```

## Customization

### Adding Personal Configuration

Create `~/.extra.sh` for personal settings:

```bash
# Personal aliases
alias myproject="cd ~/projects/myproject"

# Private environment variables
export MY_API_KEY="..."

# Custom functions
function my_function() {
  echo "My custom function"
}
```

### Platform-Specific Configuration

The shell configuration automatically detects and loads platform-specific
settings:

```bash
# macOS specific
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS configurations
fi

# Linux specific
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # Linux configurations
fi
```

## Modern CLI Tools

The configuration assumes these modern CLI tools are installed:

- **ripgrep (rg)**: Fast text search
- **fd**: Fast file finder
- **bat**: Better cat with syntax highlighting
- **eza**: Modern ls replacement
- **jq/yq**: JSON/YAML processing
- **fzf**: Fuzzy finder
- **delta**: Better git diff

## Tips

### Reload Configuration

```bash
# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc
```

### Check Active Aliases

```bash
# List all aliases
alias

# Check specific alias
alias ll
```

### Debug Shell Startup

```bash
# Start shell with debug output
bash -x
zsh -x
```
