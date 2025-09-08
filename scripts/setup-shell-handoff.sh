#!/usr/bin/env bash
set -euo pipefail

# Idempotently configure bash/zsh to:
# 1) source ~/.config/shell-nix.sh for Nix env
# 2) exec to fish in interactive sessions (leaving non-interactive untouched)

backup_once() {
  local file="$1"
  if [[ -f "$file" && ! -L "$file" ]]; then
    local bkp="${file}.backup.$(date +%s)"
    cp "$file" "$bkp"
    echo "→ Backed up $file → $bkp"
  fi
}

ensure_line() {
  local file="$1"; shift
  local marker="$1"; shift
  local content="$*"
  grep -Fq "$marker" "$file" 2>/dev/null || {
    backup_once "$file"
    {
      echo ""
      echo "# Added by dotfiles setup-shell-handoff.sh ($marker)"
      echo "$content"
    } >> "$file"
    echo "→ Updated $file ($marker)"
  }
}

# Ensure ~/.config exists (link-config.sh usually handles this)
mkdir -p "$HOME/.config"

# Bash
BASHRC="$HOME/.bashrc"
touch "$BASHRC"

# 1) Source Nix shell helpers
ensure_line "$BASHRC" "DOTFILES:NIX_SHELL_HELPERS" "source \"$HOME/.config/shell-nix.sh\" 2>/dev/null || true"

# 2) Interactive exec to fish
read -r -d '' BASH_EXEC_FISH <<'EOF'
if case $- in *i*) true;; *) false;; esac; then
  if command -v fish >/dev/null 2>&1; then
    exec fish -l
  fi
fi
EOF
ensure_line "$BASHRC" "DOTFILES:EXEC_FISH" "$BASH_EXEC_FISH"

# Zsh
ZSHRC="$HOME/.zshrc"
touch "$ZSHRC"

# 1) Source Nix shell helpers
ensure_line "$ZSHRC" "DOTFILES:NIX_SHELL_HELPERS" "source \"$HOME/.config/shell-nix.sh\" 2>/dev/null || true"

# 2) Interactive exec to fish
read -r -d '' ZSH_EXEC_FISH <<'EOF'
if [[ -o interactive ]] && command -v fish >/dev/null 2>&1; then
  exec fish -l
fi
EOF
ensure_line "$ZSHRC" "DOTFILES:EXEC_FISH" "$ZSH_EXEC_FISH"

echo "✅ Shell handoff configured. Open a new terminal to verify, or run:"
echo "  make test-shell"

