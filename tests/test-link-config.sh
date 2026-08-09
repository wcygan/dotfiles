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

assert_file_copy() {
    local path="$1"
    local expected="$2"

    if [[ ! -f "$path" ]]; then
        fail "$path is not a regular file"
    fi

    if [[ -L "$path" ]]; then
        fail "$path should be a local file, not a symlink"
    fi

    if ! cmp -s "$path" "$expected"; then
        fail "$path does not match $expected"
    fi

    pass "$path is a local copy of $expected"
}

echo "Link config integration test"
echo "============================"
echo ""

mkdir -p "$HOME" "$CODEX_HOME/agents" "$CODEX_HOME/skills"
printf '%s\n' 'machine-local agent placeholder' >"$CODEX_HOME/agents/local-agent.toml"
printf '%s\n' 'external skill catalog placeholder' >"$CODEX_HOME/skills/README.md"

DOTFILES_SKIP_FISH_GREETING=1 "$ROOT/scripts/link-config.sh" >/dev/null

assert_symlink "$HOME/.config/git" "$ROOT/config/git"
assert_symlink "$HOME/.config/fish" "$ROOT/config/fish"
assert_symlink "$HOME/.bunfig.toml" "$ROOT/config/bunfig.toml"
assert_symlink "$HOME/.config/.bunfig.toml" "$ROOT/config/bunfig.toml"
assert_symlink "$HOME/.config/deno" "$ROOT/config/deno"
assert_file_copy "$CODEX_HOME/config.toml" "$ROOT/config/codex/config.toml"
assert_symlink "$CODEX_HOME/AGENTS.md" "$ROOT/config/codex/AGENTS.md"

if [[ -f "$CODEX_HOME/agents/local-agent.toml" && ! -L "$CODEX_HOME/agents/local-agent.toml" ]]; then
    pass "unrelated machine-local Codex agents are preserved"
else
    fail "unrelated machine-local Codex agent was changed"
fi

if [[ -f "$CODEX_HOME/skills/README.md" && ! -L "$CODEX_HOME/skills" ]]; then
    pass "external Codex skills catalog is preserved"
else
    fail "external Codex skills catalog was changed"
fi

if [[ -e "$HOME/.claude" || -L "$HOME/.claude" ]]; then
    fail "$HOME/.claude should not be created"
else
    pass "Claude configuration remains machine-local"
fi

if [[ -e "$HOME/.pi/agent/skills" || -L "$HOME/.pi/agent/skills" ]]; then
    fail "$HOME/.pi/agent/skills should not be created"
else
    pass "Pi configuration remains machine-local without a duplicate link"
fi

if [[ -d "$HOME/.local/bin" ]]; then
    pass "npm global bin directory exists"
else
    fail "$HOME/.local/bin was not created"
fi

if [[ -d "$HOME/.local/lib" ]]; then
    pass "npm global lib directory exists"
else
    fail "$HOME/.local/lib was not created"
fi

if grep -Fxq 'prefix=${HOME}/.local' "$HOME/.npmrc"; then
    pass "npm global prefix is configured for ~/.local"
else
    fail "$HOME/.npmrc does not configure npm global prefix"
fi

if grep -Fxq 'min-release-age=1' "$HOME/.npmrc"; then
    pass "npm minimum release age is one day"
else
    fail "$HOME/.npmrc does not configure npm one-day minimum release age"
fi

cat >>"$CODEX_HOME/config.toml" <<'LOCAL_CODEX_STATE'

[projects."/tmp/private-project"]
trust_level = "trusted"
LOCAL_CODEX_STATE

cat >"$HOME/.npmrc" <<'LOCAL_NPM_CONFIG'
registry=https://registry.npmjs.org/
prefix=/tmp/wrong-prefix
save-exact=true
min-release-age=1
prefix=/tmp/duplicate-prefix
min-release-age=7
LOCAL_NPM_CONFIG

DOTFILES_SKIP_FISH_GREETING=1 "$ROOT/scripts/link-config.sh" >/dev/null

if [[ -L "$CODEX_HOME/config.toml" ]]; then
    fail "$CODEX_HOME/config.toml should remain a local file after re-link"
fi

if grep -Fq '[projects."/tmp/private-project"]' "$CODEX_HOME/config.toml"; then
    pass "existing local Codex trust state is preserved"
else
    fail "existing local Codex trust state was overwritten"
fi

if grep -Fxq 'registry=https://registry.npmjs.org/' "$HOME/.npmrc" && \
   grep -Fxq 'save-exact=true' "$HOME/.npmrc"; then
    pass "existing local npm config is preserved"
else
    fail "existing local npm config was overwritten"
fi

if [[ "$(grep -Ec '^[[:space:]]*prefix[[:space:]]*=' "$HOME/.npmrc")" == "1" ]] && \
   grep -Fxq 'prefix=${HOME}/.local' "$HOME/.npmrc"; then
    pass "npm global prefix is updated idempotently"
else
    fail "npm global prefix was not updated idempotently"
fi

if [[ "$(grep -Ec '^[[:space:]]*min-release-age[[:space:]]*=' "$HOME/.npmrc")" == "1" ]] && \
   grep -Fxq 'min-release-age=1' "$HOME/.npmrc"; then
    pass "npm minimum release age is one day idempotently"
else
    fail "npm minimum release age was not set to one day idempotently"
fi

if [[ -f "$ROOT/config/bunfig.toml" ]]; then
    pass "config/bunfig.toml exists as the Bun config source"
else
    fail "config/bunfig.toml is missing"
fi

if [[ -f "$ROOT/config/deno/deno.jsonc" ]]; then
    pass "config/deno/deno.jsonc exists as the Deno cooldown config source"
else
    fail "config/deno/deno.jsonc is missing"
fi

if [[ -f "$ROOT/config/codex/config.toml" ]]; then
    pass "config/codex/config.toml exists as the Codex config template"
else
    fail "config/codex/config.toml is missing"
fi

if [[ -f "$ROOT/config/codex/AGENTS.md" ]]; then
    pass "config/codex/AGENTS.md exists as the Codex global instructions source"
else
    fail "config/codex/AGENTS.md is missing"
fi

if [[ -e "$ROOT/config/pi/skills" || -L "$ROOT/config/pi/skills" ]]; then
    fail "config/pi/skills should not exist"
else
    pass "config/pi/skills is absent"
fi

if grep -q "link_pi_skills" "$ROOT/scripts/link-config.sh"; then
    fail "link-config.sh should not create ~/.pi/agent/skills"
else
    pass "link-config.sh leaves Pi's duplicate skills path alone"
fi

if [[ -e "$ROOT/scripts/install-skills.sh" ]]; then
    fail "dotfiles should not include a global agent-skill installer"
else
    pass "dotfiles does not install global agent skills"
fi

if [[ -f "$ROOT/.agents/skills/config-change/SKILL.md" ]]; then
    pass "project-local operating skills are retained"
else
    fail "project-local operating skills are missing"
fi

echo ""
echo "All link-config checks passed."
