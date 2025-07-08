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

## Modern CLI Tools

The configuration assumes these modern CLI tools are installed:

- **[ripgrep (rg)](https://github.com/BurntSushi/ripgrep)**: Fast text search
- **[fd](https://github.com/sharkdp/fd)**: Fast file finder
- **[bat](https://github.com/sharkdp/bat)**: Better cat with syntax highlighting
- **[eza](https://github.com/eza-community/eza)**: Modern ls replacement
- **[jq](https://github.com/jqlang/jq)/[yq](https://github.com/mikefarah/yq)**: JSON/YAML processing
- **[fzf](https://github.com/junegunn/fzf)**: Fuzzy finder
- **[delta](https://github.com/dandavison/delta)**: Better git diff

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
