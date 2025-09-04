#!/usr/bin/env bash
set -euo pipefail

# Setup user-specific git configuration
# This keeps personal info out of the shared dotfiles

CONFIG_FILE="$HOME/.config/git/config.local"

# Check if config.local already exists
if [ -f "$CONFIG_FILE" ]; then
    echo "✓ Git user config already exists at $CONFIG_FILE"
    echo ""
    echo "Current configuration:"
    git config --file "$CONFIG_FILE" --get user.name 2>/dev/null || echo "  user.name: (not set)"
    git config --file "$CONFIG_FILE" --get user.email 2>/dev/null || echo "  user.email: (not set)"
    echo ""
    read -p "Do you want to update it? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "→ Keeping existing configuration"
        exit 0
    fi
fi

# Ensure directory exists
mkdir -p "$(dirname "$CONFIG_FILE")"

# Prompt for user information
echo "Setting up Git user configuration..."
echo ""

# Get current global values as defaults
current_name=$(git config --global user.name 2>/dev/null || echo "")
current_email=$(git config --global user.email 2>/dev/null || echo "")

# Prompt for name
if [ -n "$current_name" ]; then
    read -p "Enter your name [$current_name]: " name
    name="${name:-$current_name}"
else
    read -p "Enter your name: " name
fi

# Prompt for email
if [ -n "$current_email" ]; then
    read -p "Enter your email [$current_email]: " email
    email="${email:-$current_email}"
else
    read -p "Enter your email: " email
fi

# Write to config.local
git config --file "$CONFIG_FILE" user.name "$name"
git config --file "$CONFIG_FILE" user.email "$email"

echo ""
echo "✓ Git user configuration saved to $CONFIG_FILE"
echo "  user.name: $name"
echo "  user.email: $email"

# Optional: Remove global config if it exists (to avoid confusion)
if [ -n "$current_name" ] || [ -n "$current_email" ]; then
    echo ""
    read -p "Remove global git user config (now redundant)? [Y/n] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        git config --global --unset user.name 2>/dev/null || true
        git config --global --unset user.email 2>/dev/null || true
        echo "→ Removed global git user configuration"
    fi
fi
