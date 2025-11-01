#!/usr/bin/env bash
# Validate Zed configuration files for JSON syntax
# Supports extended JSON with // comments

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

SETTINGS_FILE="$DOTFILES_ROOT/config/zed/settings.json"
KEYMAP_FILE="$DOTFILES_ROOT/config/zed/keymap.json"

validate_json_with_comments() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo "❌ File not found: $file"
        return 1
    fi

    # Strip // comments and validate JSON structure
    # This is a simple approach; jq doesn't support // comments natively
    if command -v jq >/dev/null 2>&1; then
        # Remove // comments (simple regex, doesn't handle strings with //)
        sed 's|//.*||g' "$file" | jq . >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "✅ Valid: $(basename "$file")"
            return 0
        else
            echo "❌ Invalid JSON: $(basename "$file")"
            return 1
        fi
    else
        echo "⚠️  jq not found, skipping validation for $(basename "$file")"
        return 0
    fi
}

main() {
    echo "🔍 Validating Zed configuration files..."
    echo ""

    local errors=0

    validate_json_with_comments "$SETTINGS_FILE" || ((errors++))
    validate_json_with_comments "$KEYMAP_FILE" || ((errors++))

    echo ""
    if [[ $errors -eq 0 ]]; then
        echo "✨ All configuration files are valid!"
        return 0
    else
        echo "❌ Found $errors invalid configuration file(s)"
        return 1
    fi
}

main "$@"
