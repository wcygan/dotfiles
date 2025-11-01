#!/usr/bin/env bash
# Test Starship configuration in isolation

set -euo pipefail

CONFIG_FILE="${1:-config/starship/starship.toml}"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

echo "🧪 Testing Starship configuration: $CONFIG_FILE"
echo ""

# Validate TOML syntax
echo "1. Validating TOML syntax..."
if STARSHIP_CONFIG="$CONFIG_FILE" starship config &>/dev/null; then
    echo "   ✅ TOML syntax valid"
else
    echo "   ❌ TOML syntax invalid"
    STARSHIP_CONFIG="$CONFIG_FILE" starship config
    exit 1
fi

# Print configuration
echo ""
echo "2. Configuration summary:"
STARSHIP_CONFIG="$CONFIG_FILE" starship print-config | head -n 20
echo "   ... (truncated)"

# Test module detection
echo ""
echo "3. Testing module detection..."

# Test git module (if in git repo)
if git rev-parse --git-dir &>/dev/null; then
    echo "   Testing git_branch:"
    STARSHIP_CONFIG="$CONFIG_FILE" starship module git_branch
    echo "   Testing git_status:"
    STARSHIP_CONFIG="$CONFIG_FILE" starship module git_status
fi

# Test directory module
echo "   Testing directory:"
STARSHIP_CONFIG="$CONFIG_FILE" starship module directory

# Test character module
echo "   Testing character:"
STARSHIP_CONFIG="$CONFIG_FILE" starship module character

# Explain prompt
echo ""
echo "4. Prompt explanation:"
STARSHIP_CONFIG="$CONFIG_FILE" starship explain

# Performance check
echo ""
echo "5. Performance timings:"
STARSHIP_CONFIG="$CONFIG_FILE" starship timings | head -n 15
echo "   ... (truncated)"

echo ""
echo "✅ Configuration test complete!"
echo ""
echo "To use this config temporarily:"
echo "  export STARSHIP_CONFIG=$CONFIG_FILE"
echo "  exec fish -l"
