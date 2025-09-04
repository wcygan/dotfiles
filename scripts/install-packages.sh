#!/usr/bin/env bash
set -euo pipefail

# enable flakes (user-level)
mkdir -p "$HOME/.config/nix"
if ! grep -q 'experimental-features' "$HOME/.config/nix/nix.conf" 2>/dev/null; then
  echo "experimental-features = nix-command flakes" >> "$HOME/.config/nix/nix.conf"
fi

# install all packages from the root flake
# Check if package is already installed
if nix profile list | grep -q "dotfiles"; then
  echo "Package already installed, upgrading..."
  nix profile upgrade '.*dotfiles.*' --impure
else
  echo "Installing packages from flake..."
  nix profile add . --impure
fi
