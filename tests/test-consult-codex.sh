#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
SCRIPT="$ROOT/config/claude/skills/consult-codex/scripts/consult_codex.sh"

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

[[ -x "$SCRIPT" ]] || fail "consult_codex.sh is not executable"

prompt_output="$("$SCRIPT" --print-prompt "Do a read-only smoke check.")"
grep -F -- "$ROOT/config/codex/skills/codex-docs" <<<"$prompt_output" >/dev/null \
    || fail "prompt did not resolve codex-docs path"
grep -F -- "references/agents-md.md" <<<"$prompt_output" >/dev/null \
    || fail "prompt did not cite agents-md reference"
grep -F -- "Do not edit files" <<<"$prompt_output" >/dev/null \
    || fail "prompt did not include read-only instruction"

command_output="$("$SCRIPT" --print-command "Do a read-only smoke check.")"
grep -F -- "--sandbox read-only" <<<"$command_output" >/dev/null \
    || fail "safe command did not pin --sandbox read-only"
grep -F -- "--output-last-message" <<<"$command_output" >/dev/null \
    || fail "safe command did not capture last message"
if grep -F -- "--dangerously-bypass-approvals-and-sandbox" <<<"$command_output" >/dev/null; then
    fail "safe command included dangerous bypass"
fi

unsafe_command_output="$("$SCRIPT" --print-command --unsafe "Do an unsafe smoke check.")"
grep -F -- "--dangerously-bypass-approvals-and-sandbox" <<<"$unsafe_command_output" >/dev/null \
    || fail "unsafe command did not include dangerous bypass"
if grep -F -- "--sandbox " <<<"$unsafe_command_output" >/dev/null; then
    fail "unsafe command should not also set --sandbox"
fi

bare_command_output="$("$SCRIPT" --print-command --bare "Do a bare smoke check.")"
grep -F -- "--ignore-user-config" <<<"$bare_command_output" >/dev/null \
    || fail "bare command did not ignore user config"
grep -F -- "--ignore-rules" <<<"$bare_command_output" >/dev/null \
    || fail "bare command did not ignore rules"

raw_command_output="$("$SCRIPT" --print-command --raw-output "Do a raw smoke check.")"
if grep -F -- "--output-last-message" <<<"$raw_command_output" >/dev/null; then
    fail "raw-output command should not capture last message"
fi

json_command_output="$("$SCRIPT" --print-command --output-format json "Do a json smoke check.")"
grep -F -- " --json " <<<"$json_command_output " >/dev/null \
    || fail "json output-format did not pass --json"
if grep -F -- "--output-last-message" <<<"$json_command_output" >/dev/null; then
    fail "json output-format should not also capture last message"
fi

echo "consult-codex smoke test passed"
