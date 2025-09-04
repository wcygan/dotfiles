#!/usr/bin/env bash
set -euo pipefail

# enable flakes (user-level)
mkdir -p "$HOME/.config/nix"
if ! grep -q 'experimental-features' "$HOME/.config/nix/nix.conf" 2>/dev/null; then
  echo "experimental-features = nix-command flakes" >> "$HOME/.config/nix/nix.conf"
fi

# install all packages from the root flake
nix profile install . --impure
