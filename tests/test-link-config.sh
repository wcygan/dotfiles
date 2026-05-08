#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$(mktemp -d /tmp/link-config-test.XXXXXX)"
export HOME="$TEST_DIR/home"
export CODEX_HOME="$TEST_DIR/codex-home"

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
assert_symlink "$CODEX_HOME/config.toml" "$ROOT/config/codex/config.toml"
assert_symlink "$CODEX_HOME/AGENTS.md" "$ROOT/config/codex/AGENTS.md"
assert_symlink "$CODEX_HOME/skills" "$ROOT/config/codex/skills"

if [[ -f "$ROOT/config/codex/config.toml" ]]; then
    pass "config/codex/config.toml exists as the Codex user config source"
else
    fail "config/codex/config.toml is missing"
fi

if [[ -f "$ROOT/config/codex/AGENTS.md" ]]; then
    pass "config/codex/AGENTS.md exists as the Codex global instructions source"
else
    fail "config/codex/AGENTS.md is missing"
fi

if [[ -d "$ROOT/config/codex/skills" ]]; then
    pass "config/codex/skills exists as the Codex skills source"
else
    fail "config/codex/skills is missing"
fi

echo ""
echo "All link-config checks passed."
