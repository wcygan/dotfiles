#!/usr/bin/env bash

set -euo pipefail

# Detect OS
OS=$(uname -s)
ARCH=$(uname -m)

echo "Detected OS: $OS ($ARCH)"

# First, try to source Nix daemon if it exists but nix isn't in PATH
if [ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]; then
    echo "Found Nix daemon profile, sourcing it..."
    . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
fi

# Check if Nix is already installed
if command -v nix &> /dev/null; then
    echo "Nix is already installed at $(which nix)"
    echo "Nix version: $(nix --version)"
    exit 0
fi

# Check if Nix receipt exists (indicating partial/broken installation)
if [ -f /nix/receipt.json ]; then
    echo "Found existing Nix receipt at /nix/receipt.json"
    echo "This indicates a previous Nix installation that may be incomplete."
    echo ""
    echo "Options:"
    echo "1. Try to repair the installation by re-sourcing the profile"
    echo "2. Uninstall and reinstall Nix cleanly"
    echo ""
    echo "Attempting to repair first..."

    # Try various profile locations
    PROFILES=(
        "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"
        "/etc/profile.d/nix.sh"
        "$HOME/.nix-profile/etc/profile.d/nix.sh"
    )

    for profile in "${PROFILES[@]}"; do
        if [ -f "$profile" ]; then
            echo "Sourcing $profile..."
            . "$profile"
            if command -v nix &> /dev/null; then
                echo "Successfully recovered Nix installation!"
                echo "Nix version: $(nix --version)"
                exit 0
            fi
        fi
    done

    echo "Could not recover existing Nix installation."
    echo "The installer will attempt to continue with the existing installation."
fi

echo "Installing Nix..."

# Detect if we're in a container (Docker, Podman, etc.)
INSTALL_FLAGS=""
if [ -f /.dockerenv ] || [ -n "${container:-}" ] || ! command -v systemctl &>/dev/null; then
    echo "Container environment detected (no systemd). Using --init none flag..."
    INSTALL_FLAGS="--init none"
fi

# Use Determinate Systems installer for better experience
# Works on macOS, Linux (including Fedora and Ubuntu)
# Add --no-confirm for non-interactive installation
# Add --force flag if receipt exists to handle existing installations
if [ -f /nix/receipt.json ]; then
    echo "Using existing Nix installation..."
    if [ -n "$INSTALL_FLAGS" ]; then
        curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install linux $INSTALL_FLAGS --no-confirm --force 2>/dev/null || {
            echo "Note: Installer detected existing installation. Attempting to use it."
        }
    else
        curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install --no-confirm --force 2>/dev/null || {
            echo "Note: Installer detected existing installation. Attempting to use it."
        }
    fi
else
    if [ -n "$INSTALL_FLAGS" ]; then
        curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install linux $INSTALL_FLAGS --no-confirm
    else
        curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install --no-confirm
    fi
fi

# Source Nix environment
if [ -f /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]; then
    . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
fi

echo "Nix installation completed!"
echo "Please restart your shell or run: source /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"
