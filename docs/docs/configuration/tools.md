---
sidebar_position: 2
---

# Tools Configuration

This dotfiles setup is optimized for modern command-line tools that enhance developer productivity.

## Required Tools

### Core Development Tools

These tools are essential for the full dotfiles experience:

- **[Deno](https://deno.land/)**: JavaScript/TypeScript runtime for scripts
- **[Git](https://git-scm.com/)**: Version control system
- **[GitHub CLI](https://cli.github.com/)**: GitHub operations from the terminal

### Modern CLI Replacements

Replace legacy Unix tools with these modern alternatives:

#### ripgrep (rg) - Replace grep
```bash
# Install
brew install ripgrep  # macOS
sudo apt install ripgrep  # Ubuntu

# Usage
rg "pattern" --type rust
rg "TODO" -g "*.ts"
```

#### fd - Replace find
```bash
# Install
brew install fd  # macOS
sudo apt install fd-find  # Ubuntu

# Usage
fd ".rs$" src/
fd --type f --extension md
```

#### bat - Replace cat
```bash
# Install
brew install bat  # macOS
sudo apt install bat  # Ubuntu

# Usage
bat README.md
bat src/main.rs --language rust
```

#### eza - Replace ls
```bash
# Install
brew install eza  # macOS
cargo install eza  # Any platform with Rust

# Usage
eza -la --git
eza --tree --level=2
```

## JSON/YAML Processing

### jq - JSON processor
```bash
# Install
brew install jq  # macOS
sudo apt install jq  # Ubuntu

# Usage
cat package.json | jq '.dependencies'
kubectl get pods -o json | jq '.items[].metadata.name'
```

### yq - YAML processor
```bash
# Install
brew install yq  # macOS
sudo snap install yq  # Ubuntu

# Usage
yq '.version' docker-compose.yml
yq -i '.services.web.image = "myapp:latest"' docker-compose.yml
```

## Additional Productivity Tools

### fzf - Fuzzy finder
```bash
# Install
brew install fzf  # macOS
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# Usage with other tools
# Interactive file selection
vim $(fzf)

# Git branch switching
git checkout $(git branch | fzf)
```

### delta - Better git diff
```bash
# Install
brew install git-delta  # macOS
cargo install git-delta  # Any platform with Rust

# Configure git to use delta
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
```

## Tool Configuration

### Shell Integration

The dotfiles automatically configure aliases and functions for these tools:

```bash
# Aliases configured automatically
alias grep="rg"
alias find="fd"
alias cat="bat"
alias ls="eza"

# Functions for common patterns
function search() {
  rg "$1" --type-add 'code:*.{js,ts,rs,go,java}' -tcode
}
```

### Environment Variables

Tools are configured via environment variables in `.exports.sh`:

```bash
export BAT_THEME="Dracula"
export FZF_DEFAULT_COMMAND="fd --type f"
export FZF_DEFAULT_OPTS="--height 40% --reverse"
```

## Installation Script

A convenient installation script for all tools:

```bash
#!/bin/bash
# Install modern CLI tools

# macOS (using Homebrew)
if [[ "$OSTYPE" == "darwin"* ]]; then
  brew install ripgrep fd bat eza jq yq fzf git-delta gh deno
fi

# Ubuntu/Debian
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo apt update
  sudo apt install -y ripgrep fd-find bat jq gh
  
  # Install tools not in apt
  cargo install eza git-delta
  
  # Install yq
  sudo snap install yq
  
  # Install Deno
  curl -fsSL https://deno.land/install.sh | sh
fi
```

## Verification

After installation, verify all tools:

```bash
# Check installations
command -v rg && echo "✓ ripgrep installed"
command -v fd && echo "✓ fd installed"
command -v bat && echo "✓ bat installed"
command -v eza && echo "✓ eza installed"
command -v jq && echo "✓ jq installed"
command -v yq && echo "✓ yq installed"
command -v fzf && echo "✓ fzf installed"
command -v delta && echo "✓ delta installed"
command -v gh && echo "✓ GitHub CLI installed"
command -v deno && echo "✓ Deno installed"
```