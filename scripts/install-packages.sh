#!/usr/bin/env bash
set -euo pipefail

# enable flakes (user-level)
mkdir -p "$HOME/.config/nix"
if ! grep -q 'experimental-features' "$HOME/.config/nix/nix.conf" 2>/dev/null; then
  echo "experimental-features = nix-command flakes" >> "$HOME/.config/nix/nix.conf"
fi

# In containers without systemd, we need to handle single-user mode
if [ -f /.dockerenv ] || [ -n "${container:-}" ] || ! command -v systemctl &>/dev/null; then
  echo "Container environment detected. Checking Nix store permissions..."

  # Get current user (handle case where USER is not set)
  CURRENT_USER="${USER:-$(whoami)}"

  # Check if we can write to /nix/var/nix/db
  if [ ! -w /nix/var/nix/db ]; then
    echo "Fixing Nix store permissions for single-user mode..."
    sudo chown -R "$CURRENT_USER" /nix/var /nix/store 2>/dev/null || {
      echo "Note: Could not change ownership. Trying with sudo for package install..."
      # Try with sudo if we can't change ownership
      sudo nix profile install . --impure
      exit $?
    }
  fi
fi

# install all packages from the root flake
nix profile install . --impure
