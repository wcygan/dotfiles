#!/usr/bin/env bash

set -euo pipefail

# Detect OS
OS=$(uname -s)
ARCH=$(uname -m)

echo "Detected OS: $OS ($ARCH)"

# Check if Nix is already installed
if command -v nix &> /dev/null; then
    echo "Nix is already installed at $(which nix)"
    echo "Nix version: $(nix --version)"
    exit 0
fi

echo "Installing Nix..."

# Use Determinate Systems installer for better experience
# Works on macOS, Linux (including Fedora and Ubuntu)
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install

# Source Nix environment
if [ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]; then
    . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
fi

echo "Nix installation completed!"
echo "Please restart your shell or run: source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"
