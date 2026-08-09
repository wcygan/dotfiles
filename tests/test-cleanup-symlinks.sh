#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/cleanup-symlinks-test.XXXXXX")"
HOME="$TEST_DIR/home"
CODEX_HOME="$HOME/.codex"

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

mkdir -p "$HOME/.config" "$CODEX_HOME" "$TEST_DIR/source/git" \
    "$TEST_DIR/source/codex" "$TEST_DIR/source/claude" "$TEST_DIR/source/skills"

ln -s "$TEST_DIR/source/git" "$HOME/.config/git"
ln -s "$TEST_DIR/source/codex" "$CODEX_HOME/AGENTS.md"
ln -s "$TEST_DIR/source/claude" "$HOME/.claude"
ln -s "$TEST_DIR/source/skills" "$CODEX_HOME/skills"
printf '%s\n' 'machine-local Codex state' >"$CODEX_HOME/config.toml"

HOME="$HOME" CODEX_HOME="$CODEX_HOME" "$ROOT/scripts/cleanup-symlinks.sh" >/dev/null

[[ ! -e "$HOME/.config/git" && ! -L "$HOME/.config/git" ]] || fail "active git symlink was not removed"
[[ ! -e "$CODEX_HOME/AGENTS.md" && ! -L "$CODEX_HOME/AGENTS.md" ]] || fail "active Codex instructions symlink was not removed"
[[ -L "$HOME/.claude" ]] || fail "legacy Claude symlink should be left untouched"
[[ -L "$CODEX_HOME/skills" ]] || fail "machine-local Codex skills symlink should be left untouched"
[[ -f "$CODEX_HOME/config.toml" && ! -L "$CODEX_HOME/config.toml" ]] || fail "machine-local Codex config should be left untouched"

echo "Cleanup symlink checks passed."
