#!/usr/bin/env bash
# Test lazygit configuration
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

pass() {
    echo -e "${GREEN}✓${NC} $*"
}

fail() {
    echo -e "${RED}✗${NC} $*"
}

info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $*"
}

# Track test results
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name="$1"
    local test_command="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    if eval "$test_command" >/dev/null 2>&1; then
        pass "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        fail "$test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Detect OS
case "$(uname -s)" in
    Darwin)
        OS="macos"
        CONFIG_DIR="$HOME/Library/Application Support/lazygit"
        ;;
    Linux)
        OS="linux"
        CONFIG_DIR="$HOME/.config/lazygit"
        ;;
    *)
        OS="unknown"
        fail "Unsupported OS: $(uname -s)"
        exit 1
        ;;
esac

echo "================================"
echo "Lazygit Configuration Test"
echo "================================"
echo
info "OS: $OS"
info "Config directory: $CONFIG_DIR"
echo

# Test installations
echo "=== Installation Tests ==="
run_test "lazygit is installed" "command -v lazygit"
run_test "delta is installed" "command -v delta"
run_test "git is installed" "command -v git"
echo

# Test config directory
echo "=== Configuration Tests ==="
run_test "Config directory exists" "test -d '$CONFIG_DIR'"

if [ -d "$CONFIG_DIR" ]; then
    run_test "config.yml exists" "test -f '$CONFIG_DIR/config.yml'"

    if [ -f "$CONFIG_DIR/config.yml" ]; then
        # Validate YAML syntax
        if command -v yq >/dev/null 2>&1; then
            run_test "config.yml is valid YAML" "yq eval . '$CONFIG_DIR/config.yml'"
        elif command -v python3 >/dev/null 2>&1; then
            run_test "config.yml is valid YAML" "python3 -c 'import yaml; yaml.safe_load(open(\"$CONFIG_DIR/config.yml\"))'"
        else
            warn "Cannot validate YAML (yq or python3 not found)"
        fi

        # Check for delta pager configuration
        if grep -q "delta" "$CONFIG_DIR/config.yml" 2>/dev/null; then
            pass "Delta pager configured in config.yml"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            warn "Delta pager not found in config.yml"
        fi
        TESTS_RUN=$((TESTS_RUN + 1))
    fi
fi
echo

# Test git/delta configuration
echo "=== Git/Delta Configuration ==="
if command -v git >/dev/null 2>&1; then
    PAGER=$(git config --global core.pager || echo "")
    if [ "$PAGER" = "delta" ]; then
        pass "git core.pager is set to delta"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        warn "git core.pager is not set to delta (current: ${PAGER:-not set})"
    fi
    TESTS_RUN=$((TESTS_RUN + 1))

    DIFF_FILTER=$(git config --global interactive.diffFilter || echo "")
    if echo "$DIFF_FILTER" | grep -q "delta"; then
        pass "git interactive.diffFilter configured for delta"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        warn "git interactive.diffFilter not configured for delta"
    fi
    TESTS_RUN=$((TESTS_RUN + 1))
fi
echo

# Test delta functionality
echo "=== Delta Functionality ==="
if command -v delta >/dev/null 2>&1; then
    # Create temporary git repo for testing
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    git init >/dev/null 2>&1
    git config user.name "Test User" >/dev/null 2>&1
    git config user.email "test@example.com" >/dev/null 2>&1

    echo "line 1" > test.txt
    git add test.txt
    git commit -m "Initial commit" >/dev/null 2>&1
    echo "line 2" >> test.txt

    if git diff | delta --dark --paging=never >/dev/null 2>&1; then
        pass "Delta can process git diff output"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        fail "Delta cannot process git diff output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    TESTS_RUN=$((TESTS_RUN + 1))

    cd - >/dev/null
    rm -rf "$TEMP_DIR"
fi
echo

# Test lazygit execution
echo "=== Lazygit Execution ==="
if command -v lazygit >/dev/null 2>&1; then
    # Test that lazygit can print config dir
    if lazygit --print-config-dir >/dev/null 2>&1; then
        pass "lazygit --print-config-dir works"
        TESTS_PASSED=$((TESTS_PASSED + 1))

        REPORTED_DIR=$(lazygit --print-config-dir)
        if [ "$REPORTED_DIR" = "$CONFIG_DIR" ]; then
            pass "Config directory matches expected location"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            warn "Config directory mismatch: expected $CONFIG_DIR, got $REPORTED_DIR"
        fi
        TESTS_RUN=$((TESTS_RUN + 2))
    else
        fail "lazygit --print-config-dir failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TESTS_RUN=$((TESTS_RUN + 1))
    fi

    # Test lazygit version
    if lazygit --version >/dev/null 2>&1; then
        VERSION=$(lazygit --version | head -n1)
        pass "lazygit version: $VERSION"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        fail "lazygit --version failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    TESTS_RUN=$((TESTS_RUN + 1))
fi
echo

# Print summary
echo "================================"
echo "Test Summary"
echo "================================"
echo "Tests run: $TESTS_RUN"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
fi
echo

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
