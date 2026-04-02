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
# Multi-line block to exec fish only in interactive bash
BASH_EXEC_FISH='
if case $- in *i*) true;; *) false;; esac; then
  if command -v fish >/dev/null 2>&1; then
    exec fish -l
  fi
fi
'
ensure_line "$BASHRC" "DOTFILES:EXEC_FISH" "$BASH_EXEC_FISH"

# 3) Ensure ~/.bash_profile sources .bashrc and .profile for login shells
#    SSH sessions start login shells which read .bash_profile, not .bashrc.
#    Only create/modify if the user's login shell is bash.
if [[ "$(basename "${SHELL:-}")" == "bash" ]]; then
  BASH_PROFILE="$HOME/.bash_profile"
  touch "$BASH_PROFILE"

  BASH_PROFILE_SOURCE_BASHRC='
# Source .bashrc for login shells
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi'
  ensure_line "$BASH_PROFILE" "DOTFILES:BASH_PROFILE_SOURCE_BASHRC" "$BASH_PROFILE_SOURCE_BASHRC"

  BASH_PROFILE_SOURCE_PROFILE='
# Source .profile for other env setup (deno, cargo, etc.)
if [ -f ~/.profile ]; then
    . ~/.profile
fi'
  ensure_line "$BASH_PROFILE" "DOTFILES:BASH_PROFILE_SOURCE_PROFILE" "$BASH_PROFILE_SOURCE_PROFILE"
fi

# Zsh
ZSHRC="$HOME/.zshrc"
touch "$ZSHRC"

# 1) Source Nix shell helpers
ensure_line "$ZSHRC" "DOTFILES:NIX_SHELL_HELPERS" "source \"$HOME/.config/shell-nix.sh\" 2>/dev/null || true"

# 2) Interactive exec to fish
# Multi-line block to exec fish only in interactive zsh
ZSH_EXEC_FISH='
if [[ -o interactive ]] && command -v fish >/dev/null 2>&1; then
  exec fish -l
fi
'
ensure_line "$ZSHRC" "DOTFILES:EXEC_FISH" "$ZSH_EXEC_FISH"

# Zshenv — ensure non-interactive zsh (e.g. Zed env capture) gets Nix PATH
ZSHENV="$HOME/.zshenv"
touch "$ZSHENV"
ZSHENV_PATH='
export PATH="$HOME/.nix-profile/bin:/nix/var/nix/profiles/default/bin:/opt/homebrew/bin:$HOME/.cargo/bin:$HOME/go/bin:$HOME/.local/bin:$PATH"'
ensure_line "$ZSHENV" "DOTFILES:NIX_PATH" "$ZSHENV_PATH"

echo "✅ Shell handoff configured. Open a new terminal to verify, or run:"
echo "  make test-shell"
