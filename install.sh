#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "1) Installing Nix (if needed)…"
if ! command -v nix >/dev/null 2>&1; then
  "$ROOT/scripts/install-nix.sh"
  # source daemon (multi-user) if present
  if [ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]; then
    . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
  fi
else
  echo "Nix already installed."
fi

echo "2) Installing packages from flake…"
"$ROOT/scripts/install-packages.sh"

echo "3) Linking configs…"
"$ROOT/scripts/link-config.sh"

echo "Done."
echo "Next: add 'source ~/.config/shell-nix.sh' to your shell rc (zshrc/bashrc) once."
