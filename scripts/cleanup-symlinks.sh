#!/usr/bin/env bash
set -euo pipefail

echo "🧹 Nix Dotfiles Cleanup Script"
echo "=============================="
echo ""
echo "This will remove all symlinks created by the installer."
echo "Original files backed up with .backup.* will be preserved."
echo ""

# Check for dry-run mode
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" || "${1:-}" == "-n" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No changes will be made"
    echo ""
fi

# Function to safely remove a symlink
remove_symlink() {
    local target="$1"
    local expanded_target="${target/#\~/$HOME}"

    if [ -L "$expanded_target" ]; then
        if $DRY_RUN; then
            echo "[DRY] Would remove symlink: $target"
            echo "      Points to: $(readlink "$expanded_target")"
        else
            rm "$expanded_target"
            echo "✅ Removed symlink: $target"
        fi
    elif [ -e "$expanded_target" ]; then
        echo "⚠️  Not a symlink (skipping): $target"
    else
        echo "⏭️  Not found (skipping): $target"
    fi
}

echo "Removing configuration symlinks..."
echo ""

# Remove all symlinks created by link-config.sh
remove_symlink "~/.tmux.conf"
remove_symlink "~/.config/shell-nix.sh"
remove_symlink "~/.config/fish"
remove_symlink "~/.config/starship.toml"
remove_symlink "~/.config/zed"
remove_symlink "~/.config/ghostty"

# VSCode config location varies by platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    VSCODE_CONFIG_DIR="$HOME/Library/Application Support/Code/User"
else
    VSCODE_CONFIG_DIR="$HOME/.config/Code/User"
fi

if [ -d "$VSCODE_CONFIG_DIR" ]; then
    remove_symlink "$VSCODE_CONFIG_DIR/settings.json"
    remove_symlink "$VSCODE_CONFIG_DIR/keybindings.json"
fi

echo ""

# Look for backup files
echo "Checking for backup files..."
BACKUPS_FOUND=false

# Check each location separately
if ls ~/.tmux.conf.backup.* >/dev/null 2>&1; then
    BACKUPS_FOUND=true
fi

if ls ~/.config/*.backup.* >/dev/null 2>&1; then
    BACKUPS_FOUND=true
fi

if [ -d "$VSCODE_CONFIG_DIR" ] && ls "$VSCODE_CONFIG_DIR"/*.backup.* >/dev/null 2>&1; then
    BACKUPS_FOUND=true
fi

if $BACKUPS_FOUND; then
    echo ""
    echo "📦 Found backup files from previous installations:"
    ls -la ~/.tmux.conf.backup.* 2>/dev/null || true
    ls -la ~/.config/*.backup.* 2>/dev/null || true
    if [ -d "$VSCODE_CONFIG_DIR" ]; then
        ls -la "$VSCODE_CONFIG_DIR"/*.backup.* 2>/dev/null || true
    fi
    echo ""
    echo "These backup files were created when the installer replaced existing configs."
    echo "You may want to restore or remove them manually."
else
    echo "No backup files found."
fi

echo ""

if $DRY_RUN; then
    echo "🔍 Dry run complete. Run without --dry-run to actually remove symlinks."
else
    echo "✅ Cleanup complete!"
    echo ""
    echo "Next steps for migration:"
    echo "1. Clone/move your new dotfiles to: /Users/wcygan/Development/dotfiles"
    echo "2. Set up new symlinks from the new location"
    echo "3. Consider restoring any .backup.* files if needed"
fi

echo ""
echo "Note: Nix packages remain installed. Use 'nix profile list' to see them."
echo "To completely remove Nix, use the official Nix uninstaller."
