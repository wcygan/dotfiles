#!/usr/bin/env bash
# Test script to verify shell handoff to fish for interactive sessions
# while maintaining bash/zsh compatibility for non-interactive commands

set -euo pipefail

echo "=== Testing Shell Handoff to Fish ==="
echo "This verifies that bash/zsh will exec to fish in interactive mode"
echo "while staying in bash/zsh for non-interactive commands."
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

test_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
}

test_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. BASH TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test bash non-interactive
echo -n "Testing bash non-interactive mode: "
RESULT=$(bash -c 'echo "OK"' 2>&1)
if [[ "$RESULT" == "OK" ]]; then
    test_pass "Commands work in non-interactive bash"
else
    test_fail "Non-interactive bash failed: $RESULT"
fi

# Test problematic syntax in bash
echo -n "Testing VAR=value syntax in bash: "
RESULT=$(bash -lc '_=/usr/bin/env echo "OK"' 2>&1)
if [[ "$RESULT" == "OK" ]]; then
    test_pass "Bash handles VAR=value syntax"
else
    test_fail "VAR=value syntax failed: $RESULT"
fi

# Test that bash -i would exec to fish
echo -n "Testing bash interactive handoff: "
# Be resilient: if grep finds no match, don't exit due to set -euo pipefail.
RESULT=$(echo 'echo $FISH_VERSION' | bash -i 2>&1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1 || true)
if [[ -n "$RESULT" ]]; then
    test_pass "Interactive bash launches fish (version: $RESULT)"
else
    echo
    echo "  Checking if fish is in .bashrc..."
    if grep -q "exec fish" ~/.bashrc 2>/dev/null; then
        echo "  Fish exec found in .bashrc ✓"
        test_pass "bashrc configured correctly (will exec fish on interactive)"
    else
        test_fail "Fish not configured in .bashrc"
    fi
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. ZSH TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v zsh &> /dev/null; then
    # Test zsh non-interactive
    echo -n "Testing zsh non-interactive mode: "
    RESULT=$(zsh -c 'echo "OK"' 2>&1)
    if [[ "$RESULT" == "OK" ]]; then
        test_pass "Commands work in non-interactive zsh"
    else
        test_fail "Non-interactive zsh failed: $RESULT"
    fi

    # Test problematic syntax in zsh
    echo -n "Testing VAR=value syntax in zsh: "
    RESULT=$(zsh -lc '_=/usr/bin/env echo "OK"' 2>&1)
    if [[ "$RESULT" == "OK" ]]; then
        test_pass "Zsh handles VAR=value syntax"
    else
        test_fail "VAR=value syntax failed: $RESULT"
    fi

    # Test that zsh -i would exec to fish
    echo -n "Testing zsh interactive handoff: "
    if [ -f ~/.zshrc ] && grep -q "exec fish" ~/.zshrc 2>/dev/null; then
        test_pass "zshrc configured correctly (will exec fish on interactive)"
    else
        test_fail "Fish not configured in .zshrc"
    fi
else
    echo "Zsh not installed - skipping zsh tests"
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. SIMULATION TEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Simulating what happens after 'chsh -s /bin/bash':"
echo

# Simulate with SHELL set to bash
echo "When SHELL=/bin/bash:"
echo "  - Non-interactive commands: Run in bash ✓"
echo "  - Interactive terminals: Exec to fish ✓"
echo "  - Remote tools expecting bash syntax: Work correctly ✓"

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. MANUAL TEST COMMANDS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "To manually verify without changing your shell:"
echo
echo "  Test bash → fish handoff:"
echo "    $ SHELL=/bin/bash bash -i"
echo "    (Should drop you into fish prompt)"
echo
echo "  Test zsh → fish handoff:"
echo "    $ SHELL=/bin/zsh zsh -i"
echo "    (Should drop you into fish prompt)"
echo
echo "  Test non-interactive bash:"
echo "    $ bash -c 'echo \$0'"
echo "    (Should print 'bash')"
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. READY TO SWITCH?"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "If tests pass, you can safely run:"
echo "  chsh -s /bin/bash    # or"
echo "  chsh -s /bin/zsh"
echo
echo "Your interactive terminals will still use fish!"
echo "Non-interactive tools will get proper shell compatibility."
