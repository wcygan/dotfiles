#!/usr/bin/env bash
# Apply Starship preset to config file

set -euo pipefail

PRESET="${1:-}"
OUTPUT="${2:-config/starship/starship.toml}"

if [[ -z "$PRESET" ]]; then
    echo "Usage: $0 <preset-name> [output-file]"
    echo ""
    echo "Available presets:"
    echo "  - nerd-font-symbols"
    echo "  - pure-preset"
    echo "  - pastel-powerline"
    echo "  - tokyo-night"
    echo "  - gruvbox-rainbow"
    echo ""
    echo "Preview a preset:"
    echo "  starship preset <preset-name>"
    exit 1
fi

echo "📦 Applying Starship preset: $PRESET"
echo ""

# Create backup if file exists
if [[ -f "$OUTPUT" ]]; then
    BACKUP="${OUTPUT}.backup.$(date +%s)"
    echo "📋 Backing up existing config to: $BACKUP"
    cp "$OUTPUT" "$BACKUP"
fi

# Preview first
echo "Preview of preset:"
echo "---"
starship preset "$PRESET" -o - | head -n 30
echo "..."
echo "---"
echo ""

# Confirm
read -p "Apply this preset to $OUTPUT? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
fi

# Apply preset
echo "✏️  Writing preset to $OUTPUT..."
mkdir -p "$(dirname "$OUTPUT")"
starship preset "$PRESET" -o "$OUTPUT"

echo ""
echo "✅ Preset applied successfully!"
echo ""
echo "Test the new configuration:"
echo "  exec fish -l"
echo ""
echo "Or run validation:"
echo "  ./scripts/test-config.sh $OUTPUT"
