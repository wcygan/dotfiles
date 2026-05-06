#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$(mktemp -d /tmp/link-config-test.XXXXXX)"
export HOME="$TEST_DIR/home"

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

pass() {
    echo "✓ $1"
}

fail() {
    echo "✗ $1"
    exit 1
}

assert_symlink() {
    local path="$1"
    local expected="$2"

    if [[ ! -L "$path" ]]; then
        fail "$path is not a symlink"
    fi

    local actual
    actual="$(readlink "$path")"
    if [[ "$actual" != "$expected" ]]; then
        fail "$path points to $actual, expected $expected"
    fi

    pass "$path links to $expected"
}

echo "Link config integration test"
echo "============================"
echo ""

mkdir -p "$HOME"

DOTFILES_SKIP_FISH_GREETING=1 "$ROOT/scripts/link-config.sh" >/dev/null

assert_symlink "$HOME/.config/git" "$ROOT/config/git"
assert_symlink "$HOME/.config/fish" "$ROOT/config/fish"
assert_symlink "$HOME/.claude" "$ROOT/config/claude"
assert_symlink "$HOME/.codex/skills" "$ROOT/config/codex/skills"

if [[ -d "$ROOT/config/codex/skills" ]]; then
    pass "config/codex/skills exists as the Codex skills source"
else
    fail "config/codex/skills is missing"
fi

echo ""
echo "All link-config checks passed."
