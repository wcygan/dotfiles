#!/usr/bin/env bash
set -euo pipefail

# Check for dry-run mode
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" || "${1:-}" == "-n" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No changes will be made"
    echo ""
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG_SRC="$REPO_ROOT/config"
CFG_DST="$HOME/.config"

mkdir -p "$CFG_DST"

link() {
  local src="$1" dst="$2"

  if $DRY_RUN; then
    echo "[DRY] Would link: $dst → $src"
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
      echo "      (would backup existing $dst)"
    elif [ -L "$dst" ]; then
      echo "      (would replace existing symlink)"
    fi
  else
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
      mv "$dst" "$dst.backup.$(date +%s)"
    fi
    ln -snf "$src" "$dst"
    echo "→ $dst ↦ $src"
  fi
}

# examples you can grow over time:
# link "$CFG_SRC/nvim" "$CFG_DST/nvim"
# link "$CFG_SRC/gitconfig" "$HOME/.gitconfig"

# tmux config
link "$CFG_SRC/tmux/tmux.conf" "$HOME/.tmux.conf"

# keep your Nix shell helpers:
link "$CFG_SRC/shell-nix.sh" "$CFG_DST/shell-nix.sh"

# fish config (directory link keeps the whole tree under version control)
link "$CFG_SRC/fish" "$HOME/.config/fish"

# starship config
link "$CFG_SRC/starship.toml" "$HOME/.config/starship.toml"

# zed config
link "$CFG_SRC/zed" "$HOME/.config/zed"

# ghostty config
link "$CFG_SRC/ghostty" "$HOME/.config/ghostty"

# Claude configuration (for Claude Code CLI)
link "$CFG_SRC/claude" "$HOME/.claude"

# VSCode config
# Determine VSCode config location based on platform
if [[ "$OSTYPE" == "darwin"* ]]; then
  VSCODE_CONFIG_DIR="$HOME/Library/Application Support/Code/User"
else
  VSCODE_CONFIG_DIR="$HOME/.config/Code/User"
fi

# Create VSCode config directory if it doesn't exist
if ! $DRY_RUN; then
  mkdir -p "$VSCODE_CONFIG_DIR"
fi

# Link VSCode settings and keybindings
if [ -d "$VSCODE_CONFIG_DIR" ] || $DRY_RUN; then
  link "$CFG_SRC/vscode/settings.json" "$VSCODE_CONFIG_DIR/settings.json"
  link "$CFG_SRC/vscode/keybindings.json" "$VSCODE_CONFIG_DIR/keybindings.json"
else
  echo "⚠️  VSCode config directory not found, skipping VSCode config"
fi

# Disable fish greeting if fish is installed
if command -v fish >/dev/null 2>&1; then
  if $DRY_RUN; then
    echo "[DRY] Would disable fish greeting"
  else
    fish -c "set -U fish_greeting" 2>/dev/null || true
    echo "→ Disabled fish greeting"
  fi
fi
