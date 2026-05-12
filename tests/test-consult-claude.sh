#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
SCRIPT="$ROOT/config/codex/skills/consult-claude/scripts/consult_claude.sh"

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

[[ -x "$SCRIPT" ]] || fail "consult_claude.sh is not executable"

prompt_output="$("$SCRIPT" --print-prompt "Do a read-only smoke check.")"
grep -F -- "$ROOT/config/claude/skills/claude-code-best-practices" <<<"$prompt_output" >/dev/null \
    || fail "prompt did not resolve claude-code-best-practices path"
grep -F -- "references/headless.md" <<<"$prompt_output" >/dev/null \
    || fail "prompt did not cite headless reference"
grep -F -- "Do not edit files" <<<"$prompt_output" >/dev/null \
    || fail "prompt did not include read-only instruction"

command_output="$("$SCRIPT" --print-command "Do a read-only smoke check.")"
grep -F -- "--allowed-tools" <<<"$command_output" >/dev/null \
    || fail "safe command did not include allowed tools"
grep -F -- "--disallowed-tools" <<<"$command_output" >/dev/null \
    || fail "safe command did not include disallowed tools"
if grep -F -- "--dangerously-skip-permissions" <<<"$command_output" >/dev/null; then
    fail "safe command included dangerous permissions"
fi

unsafe_command_output="$("$SCRIPT" --print-command --unsafe "Do an unsafe smoke check.")"
grep -F -- "--dangerously-skip-permissions" <<<"$unsafe_command_output" >/dev/null \
    || fail "unsafe command did not include dangerous permissions"
if grep -F -- "--allowed-tools" <<<"$unsafe_command_output" >/dev/null; then
    fail "unsafe command should not include safe allowed-tools policy"
fi

echo "consult-claude smoke test passed"
