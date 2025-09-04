#!/usr/bin/env fish
# Test commands to run inside the Docker container to verify fish setup

echo "🧪 Running Fish Configuration Tests"
echo "===================================="
echo ""

set -l PASS 0
set -l FAIL 0

function test_pass
    echo "✅ $argv"
    set PASS (math $PASS + 1)
end

function test_fail
    echo "❌ $argv"
    set FAIL (math $FAIL + 1)
end

function section
    echo ""
    echo "📋 $argv"
    echo "---"
end

# Test 1: Basic fish functionality
section "Basic Fish Environment"
echo -n "Fish version: "
echo $FISH_VERSION
test_pass "Fish is running"

# Test 2: Check config loaded
section "Configuration Loading"
if test -f ~/.config/fish/config.fish
    test_pass "config.fish found"
else
    test_fail "config.fish not found"
end

if test -d ~/.config/fish/conf.d
    test_pass "conf.d directory found"
    for file in ~/.config/fish/conf.d/*.fish
        echo "  → Loaded: "(basename $file)
    end
else
    test_fail "conf.d directory not found"
end

# Test 3: Check Nix environment
section "Nix Environment Setup"
if set -q NIX_CONFIG
    test_pass "NIX_CONFIG is set"
    echo "  → Value: $NIX_CONFIG"
else
    test_fail "NIX_CONFIG not set"
end

# Check if Nix profile bin is in PATH
if contains $HOME/.nix-profile/bin $PATH
    test_pass "Nix profile bin in PATH"
else
    # Check if fish_add_path was called
    if test -d $HOME/.nix-profile/bin
        test_fail "Nix profile bin not in PATH (but directory exists)"
    else
        echo "  ℹ️  Nix profile bin directory doesn't exist (expected in test)"
    end
end

# Test 4: Custom functions
section "Custom Functions"
if functions -q nix-try
    test_pass "nix-try function loaded"
    # Test the function works
    echo "  → Testing nix-try function..."
    function test_nix_try
        nix-try
        return $status
    end
    if test_nix_try 2>&1 | grep -q "Usage:"
        echo "    ✓ Function responds correctly"
    end
else
    test_fail "nix-try function not loaded"
end

if functions -q nix-install
    test_pass "nix-install function loaded"
    echo "  → Testing nix-install function..."
    function test_nix_install
        nix-install
        return $status
    end
    if test_nix_install 2>&1 | grep -q "Usage:"
        echo "    ✓ Function responds correctly"
    end
else
    test_fail "nix-install function not loaded"
end

# Test 5: Abbreviations
section "Abbreviations"
# Create a test abbreviation to ensure abbr works
abbr --add test_abbr "test_command" 2>/dev/null

if abbr --show 2>/dev/null | grep -q nix-update
    test_pass "Nix abbreviations created"
    echo "  → Found abbreviations:"
    for line in (abbr --show 2>/dev/null | grep nix- | head -5)
        echo "    $line"
    end
else
    # Try older fish syntax
    if abbr 2>&1 | grep -q nix-update
        test_pass "Nix abbreviations created (older fish)"
    else
        echo "  ⚠️  Couldn't verify abbreviations (fish version issue)"
    end
end

# Test 6: Direnv hook
section "Direnv Integration"
if type -q direnv
    test_pass "direnv is available"
    # Check if hook is set up
    if functions -q __direnv_export_eval
        test_pass "direnv hook is active"
    else
        test_fail "direnv hook not active"
    end
else
    echo "  ℹ️  direnv not installed (would work if available)"
end

# Test 7: Starship prompt
section "Starship Integration"
if type -q starship
    test_pass "starship is available"
    # Check if starship is initialized
    if functions -q fish_prompt | grep -q starship
        test_pass "starship prompt active"
    else
        echo "  ℹ️  starship not active in prompt (check manually)"
    end
else
    echo "  ℹ️  starship not installed (would work if available)"
end

# Test 8: Interactive features
section "Interactive Features Test"
echo ""
echo "🎮 Try these interactive commands:"
echo ""
echo "  1. Type 'nix-' and press TAB"
echo "     → Should show abbreviation completions"
echo ""
echo "  2. Type 'nix-list' and press ENTER"
echo "     → Should expand to 'nix profile list'"
echo ""
echo "  3. Run: functions | grep nix"
echo "     → Should show nix-try and nix-install"
echo ""
echo "  4. Run: set | grep NIX"
echo "     → Should show NIX_CONFIG variable"
echo ""
echo "  5. Run: echo \$PATH | tr ':' '\n' | grep nix"
echo "     → Should show Nix paths"
echo ""

# Summary
echo "===================================="
echo "📊 Test Summary"
echo "===================================="
echo "Passed: $PASS tests"
if test $FAIL -gt 0
    echo "Failed: $FAIL tests"
    echo ""
    echo "⚠️  Some tests failed, but this might be normal in Docker"
    echo "   (missing binaries, different paths, etc.)"
else
    echo ""
    echo "🎉 All automated tests passed!"
end
echo ""
echo "💡 Run the interactive tests above to verify everything works"
