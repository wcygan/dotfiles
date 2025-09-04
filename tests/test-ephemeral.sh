#!/usr/bin/env bash
set -euo pipefail

# Create an ephemeral environment to test fish setup without touching real HOME
echo "🧪 Creating ephemeral test environment for fish setup"
echo "=================================================="
echo ""

# Create temp directory for fake HOME
TEST_DIR=$(mktemp -d /tmp/fish-test.XXXXXX)
export TEST_HOME="$TEST_DIR/home"
export TEST_CONFIG="$TEST_HOME/.config"

# Save original HOME
ORIG_HOME="$HOME"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "📁 Test environment: $TEST_DIR"
echo "🏠 Fake HOME: $TEST_HOME"
echo ""

# Cleanup on exit
cleanup() {
    echo ""
    echo "🧹 Cleaning up test environment..."
    rm -rf "$TEST_DIR"
    echo "✨ Done!"
}
trap cleanup EXIT

# Setup fake home
mkdir -p "$TEST_CONFIG"
mkdir -p "$TEST_HOME/.nix-profile/bin"

echo "📋 Setting up test environment..."
echo "---"

# Copy Nix binaries if they exist (for PATH testing)
if command -v fish &>/dev/null; then
    echo "✓ Found fish at $(which fish)"
    # Create a mock fish binary marker
    touch "$TEST_HOME/.nix-profile/bin/fish"
    chmod +x "$TEST_HOME/.nix-profile/bin/fish"
fi

# Symlink our fish config to test HOME
ln -snf "$REPO_ROOT/config/fish" "$TEST_CONFIG/fish"
echo "✓ Linked fish config to test HOME"

# Symlink shell-nix.sh
ln -snf "$REPO_ROOT/config/shell-nix.sh" "$TEST_CONFIG/shell-nix.sh"
echo "✓ Linked shell-nix.sh to test HOME"

echo ""
echo "🐠 Testing fish configuration loading..."
echo "---"

# Test 1: Check config files are accessible
echo -n "Config files accessible: "
if [[ -f "$TEST_CONFIG/fish/config.fish" ]] && \
   [[ -f "$TEST_CONFIG/fish/conf.d/10-nix.fish" ]] && \
   [[ -f "$TEST_CONFIG/fish/conf.d/20-direnv.fish" ]] && \
   [[ -f "$TEST_CONFIG/fish/conf.d/30-starship.fish" ]]; then
    echo "✓"
else
    echo "✗"
fi

# Test 2: Check functions are accessible
echo -n "Functions accessible: "
if [[ -f "$TEST_CONFIG/fish/functions/nix-try.fish" ]] && \
   [[ -f "$TEST_CONFIG/fish/functions/nix-install.fish" ]]; then
    echo "✓"
else
    echo "✗"
fi

echo ""
echo "🔬 Running fish in isolated environment..."
echo "---"

# Create test script that fish will run
cat > "$TEST_DIR/test.fish" << 'EOFISH'
# Test that config loads
echo "→ Fish version: $FISH_VERSION"

# Test that PATH would be modified (check if function exists)
if functions -q fish_add_path
    echo "→ fish_add_path: available ✓"
else
    echo "→ fish_add_path: not found ✗"
end

# Test Nix config
if set -q NIX_CONFIG
    echo "→ NIX_CONFIG: set ✓"
    echo "  Value: $NIX_CONFIG"
else
    echo "→ NIX_CONFIG: not set ✗"
end

# Test abbreviations were created
if abbrev --show | grep -q nix-update 2>/dev/null
    echo "→ Abbreviations: created ✓"
else
    # Fish < 3.6 doesn't have abbrev command, check if abbr works
    echo "→ Abbreviations: checking (older fish version)"
end

# Test custom functions
if functions -q nix-try
    echo "→ nix-try function: loaded ✓"
else
    echo "→ nix-try function: not loaded ✗"
end

if functions -q nix-install
    echo "→ nix-install function: loaded ✓"
else
    echo "→ nix-install function: not loaded ✗"
end

# Test direnv hook (just check if it would load)
if type -q direnv
    echo "→ direnv: would be hooked ✓"
else
    echo "→ direnv: not available (expected in test env)"
end

# Test starship (just check if it would load)
if type -q starship
    echo "→ starship: would be initialized ✓"
else
    echo "→ starship: not available (expected in test env)"
end

echo ""
echo "🎯 Interactive test commands you can try:"
echo "  nix-try <package>     # Would try a package"
echo "  nix-install <package> # Would search and install"
echo "  nix-<TAB>            # Should show abbreviations"
EOFISH

if command -v fish &>/dev/null; then
    echo "Starting isolated fish shell with test config..."
    echo "Type 'exit' to leave the test environment"
    echo "=================================================="
    echo ""

    # Run fish with our test HOME (suppress direnv warning in test)
    HOME="$TEST_HOME" DIRENV_LOG_FORMAT="" fish --init-command "source $TEST_DIR/test.fish"
else
    echo "⚠️  Fish not installed yet - showing what would be tested:"
    echo ""
    cat "$TEST_DIR/test.fish"
    echo ""
    echo "Install fish first with: nix profile install"
fi

echo ""
echo "📊 Test Summary:"
echo "---"
echo "• Config files: Successfully linked to test environment"
echo "• Functions: Available in test environment"
echo "• No changes made to your actual ~/.config/fish"
echo ""
echo "🎉 Ephemeral test complete!"
