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
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"

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
    mkdir -p "$(dirname "$dst")"
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
      mv "$dst" "$dst.backup.$(date +%s)"
    fi
    ln -snf "$src" "$dst"
    echo "→ $dst ↦ $src"
  fi
}

link_codex_skills() {
  local src="$CFG_SRC/codex/skills"
  local dst="$CODEX_HOME_DIR/skills"

  if $DRY_RUN; then
    echo "[DRY] Would link: $dst → $src"
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
      echo "      (would migrate existing $dst contents into $src first)"
    elif [ -L "$dst" ]; then
      echo "      (would replace existing symlink)"
    fi
    return 0
  fi

  mkdir -p "$src" "$(dirname "$dst")"

  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    local backup="$dst.backup.$(date +%s)"
    local backup_created=false

    if [ -d "$dst" ]; then
      shopt -s dotglob nullglob
      local entries=("$dst"/*)
      shopt -u dotglob nullglob

      for entry in "${entries[@]}"; do
        local name
        name="$(basename "$entry")"

        if [ -e "$src/$name" ] || [ -L "$src/$name" ]; then
          if ! $backup_created; then
            mkdir -p "$backup"
            backup_created=true
          fi
          mv "$entry" "$backup/$name"
        else
          mv "$entry" "$src/"
        fi
      done

      if rmdir "$dst" 2>/dev/null; then
        if $backup_created; then
          echo "→ Backed up Codex skills conflicts to $backup"
        fi
      else
        if ! $backup_created; then
          mkdir -p "$backup"
          backup_created=true
        fi
        mv "$dst" "$backup/skills"
        echo "→ Backed up existing Codex skills directory to $backup"
      fi
    else
      mv "$dst" "$backup"
      echo "→ Backed up existing Codex skills path to $backup"
    fi
  fi

  ln -snf "$src" "$dst"
  echo "→ $dst ↦ $src"
}

link_codex_agents_md() {
  link "$CFG_SRC/codex/AGENTS.md" "$CODEX_HOME_DIR/AGENTS.md"
}

install_codex_config_toml() {
  local src="$CFG_SRC/codex/config.toml"
  local dst="$CODEX_HOME_DIR/config.toml"

  if $DRY_RUN; then
    if [ -L "$dst" ]; then
      echo "[DRY] Would migrate Codex config symlink to local file: $dst"
    elif [ -e "$dst" ]; then
      echo "[DRY] Would preserve existing local Codex config: $dst"
    else
      echo "[DRY] Would copy Codex config template: $src → $dst"
    fi
    return 0
  fi

  mkdir -p "$(dirname "$dst")"

  if [ -L "$dst" ]; then
    local tmp
    tmp="$(mktemp "$(dirname "$dst")/.config.toml.XXXXXX")"
    if [ -e "$dst" ]; then
      cp -p "$dst" "$tmp"
    else
      cp -p "$src" "$tmp"
    fi
    rm "$dst"
    mv "$tmp" "$dst"
    echo "→ Migrated Codex config symlink to local file: $dst"
  elif [ -e "$dst" ]; then
    echo "→ Preserved existing local Codex config: $dst"
  else
    cp -p "$src" "$dst"
    echo "→ Copied Codex config template to local file: $dst"
  fi
}

configure_npm_settings() {
  local npmrc="$HOME/.npmrc"
  local prefix='${HOME}/.local'
  local min_release_age_days="1"

  if $DRY_RUN; then
    echo "[DRY] Would ensure npm global prefix in $npmrc: $prefix"
    echo "[DRY] Would ensure npm minimum release age in $npmrc: $min_release_age_days days"
    echo "[DRY] Would ensure npm global directories exist under: $HOME/.local"
    return 0
  fi

  mkdir -p "$HOME/.local/bin" "$HOME/.local/lib"

  if [ ! -e "$npmrc" ]; then
    {
      printf 'prefix=%s\n' "$prefix"
      printf 'min-release-age=%s\n' "$min_release_age_days"
    } > "$npmrc"
    echo "→ Configured npm settings in $npmrc"
    return 0
  fi

  local tmp
  tmp="$(mktemp)"
  awk -v prefix="$prefix" -v min_release_age_days="$min_release_age_days" '
    BEGIN {
      wrote_prefix = 0
      wrote_min_release_age = 0
    }
    /^[[:space:]]*prefix[[:space:]]*=/ {
      if (!wrote_prefix) {
        print "prefix=" prefix
        wrote_prefix = 1
      }
      next
    }
    /^[[:space:]]*min-release-age[[:space:]]*=/ {
      if (!wrote_min_release_age) {
        print "min-release-age=" min_release_age_days
        wrote_min_release_age = 1
      }
      next
    }
    { print }
    END {
      if (!wrote_prefix) {
        print "prefix=" prefix
      }
      if (!wrote_min_release_age) {
        print "min-release-age=" min_release_age_days
      }
    }
  ' "$npmrc" > "$tmp"

  if cmp -s "$tmp" "$npmrc"; then
    rm -f "$tmp"
    echo "→ npm settings already configured in $npmrc"
    return 0
  fi

  cp -p "$npmrc" "$npmrc.backup.$(date +%s)"
  cat "$tmp" > "$npmrc"
  rm -f "$tmp"
  echo "→ Updated npm settings in $npmrc"
}

# Git config (XDG-compliant location)
link "$CFG_SRC/git" "$CFG_DST/git"

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

# npm globals should be user-writable even when npm itself is provided by Nix.
# npm v11 supports a release-age cooldown in days.
configure_npm_settings

# Bun reads a global bunfig from $HOME/.bunfig.toml, or from
# $XDG_CONFIG_HOME/.bunfig.toml when that environment variable is set.
link "$CFG_SRC/bunfig.toml" "$HOME/.bunfig.toml"
link "$CFG_SRC/bunfig.toml" "$CFG_DST/.bunfig.toml"

# Deno has project config discovery rather than a built-in global config path.
# Shell wrappers source this file for dependency-management commands when no
# project deno.json/deno.jsonc is already in scope.
link "$CFG_SRC/deno" "$CFG_DST/deno"

# ghostty config
link "$CFG_SRC/ghostty" "$HOME/.config/ghostty"

# Claude configuration (for Claude Code CLI)
link "$CFG_SRC/claude" "$HOME/.claude"

# Codex config.toml is mutable user state; copy the template once, then preserve it.
install_codex_config_toml
link_codex_agents_md
link_codex_skills

# Zellij config
link "$CFG_SRC/zellij" "$HOME/.config/zellij"

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
if [[ "${DOTFILES_SKIP_FISH_GREETING:-}" == "1" ]]; then
  :
elif command -v fish >/dev/null 2>&1; then
  if $DRY_RUN; then
    echo "[DRY] Would disable fish greeting"
  else
    fish -c "set -U fish_greeting" 2>/dev/null || true
    echo "→ Disabled fish greeting"
  fi
fi
