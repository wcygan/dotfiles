#!/usr/bin/env bash
# Test Starship configuration in isolation

set -euo pipefail

CONFIG_FILE="${1:-config/starship.toml}"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

echo "🧪 Testing Starship configuration: $CONFIG_FILE"
echo ""

# Validate TOML syntax
echo "1. Validating TOML syntax..."
if python3 -c 'import sys, tomllib; tomllib.load(open(sys.argv[1], "rb"))' "$CONFIG_FILE"; then
    echo "   ✅ TOML syntax valid"
else
    echo "   ❌ TOML syntax invalid"
    exit 1
fi

# Print configuration
echo ""
echo "2. Configuration summary:"
STARSHIP_CONFIG="$CONFIG_FILE" starship print-config | sed -n '1,20p'
echo "   ... (truncated)"

# Render the configured prompt in the current directory
echo ""
echo "3. Rendered prompt:"
STARSHIP_CONFIG="$CONFIG_FILE" starship prompt
echo ""

# Explain prompt
echo ""
echo "4. Prompt explanation:"
STARSHIP_CONFIG="$CONFIG_FILE" starship explain

# Performance check
echo ""
echo "5. Performance timings:"
STARSHIP_CONFIG="$CONFIG_FILE" starship timings | sed -n '1,15p'
echo "   ... (truncated)"

echo ""
echo "✅ Configuration test complete!"
echo ""
echo "To use this config temporarily:"
echo "  export STARSHIP_CONFIG=$CONFIG_FILE"
echo "  exec fish -l"
