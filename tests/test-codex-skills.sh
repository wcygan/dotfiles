#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_ROOT="$ROOT/config/codex/skills"

pass() {
    echo "✓ $1"
}

fail() {
    echo "✗ $1"
    exit 1
}

assert_contains() {
    local file="$1"
    local expected="$2"
    local label="$3"

    if grep -Fq -- "$expected" "$file"; then
        pass "$label"
    else
        fail "$file is missing: $expected"
    fi
}

echo "Codex global skill checks"
echo "========================="
echo ""

if [[ ! -d "$SKILLS_ROOT" ]]; then
    fail "$SKILLS_ROOT is missing"
fi

expected_inventory="$(
    printf '%s\n' \
        "animation-vocabulary/SKILL.md" \
        "autoresearch/SKILL.md" \
        "better-colors/SKILL.md" \
        "better-typography/SKILL.md" \
        "better-ui/SKILL.md" \
        "effect/SKILL.md" \
        "find-animation-opportunities/SKILL.md" \
        "goal-supervisor/SKILL.md" \
        "hill-climbing-loop/SKILL.md" \
        "improve-animations/SKILL.md" \
        "loop-protocol/SKILL.md" \
        "monitor-until/SKILL.md" \
        "review-animations/SKILL.md"
)"
actual_inventory="$(
    find "$SKILLS_ROOT" \
        -path "$SKILLS_ROOT/.system" -prune -o \
        -name SKILL.md -type f -print |
        sed "s|^$SKILLS_ROOT/||" |
        sort
)"

if [[ "$actual_inventory" == "$expected_inventory" ]]; then
    pass "active Codex skill inventory matches the reviewed global catalog"
else
    fail "Codex skill inventory mismatch: ${actual_inventory:-none}"
fi

while IFS= read -r -d '' skill_file; do
    skill_dir="$(basename "$(dirname "$skill_file")")"
    frontmatter="$(awk '
        /^---$/ { count++; next }
        count == 1 { print }
        count == 2 { exit }
    ' "$skill_file")"

    if [[ "$(head -n 1 "$skill_file")" != "---" ]]; then
        fail "$skill_file does not start with YAML frontmatter"
    fi

    delimiter_count="$(grep -c '^---$' "$skill_file" || true)"
    if (( delimiter_count < 2 )); then
        fail "$skill_file does not close its YAML frontmatter"
    fi

    if ! grep -qE '^name:[[:space:]]*"?[a-z0-9-]+"?[[:space:]]*$' <<<"$frontmatter"; then
        fail "$skill_file is missing a valid kebab-case name"
    fi

    if ! grep -qE '^description:[[:space:]]*(".+"|\|)[[:space:]]*$' <<<"$frontmatter"; then
        fail "$skill_file is missing a non-empty description"
    fi

    declared_name="$(
        sed -nE 's/^name:[[:space:]]*"?([a-z0-9-]+)"?[[:space:]]*$/\1/p' \
            <<<"$frontmatter" |
            head -n 1
    )"
    if [[ "$declared_name" != "$skill_dir" ]]; then
        fail "$skill_file declares '$declared_name', expected '$skill_dir'"
    fi

    if grep -qE '^(disable-model-invocation|context|effort|argument-hint|allowed-tools):' \
        <<<"$frontmatter"; then
        fail "$skill_file contains Claude-only frontmatter"
    fi

    pass "$declared_name metadata is Codex-compatible"
done < <(
    find "$SKILLS_ROOT" \
        -path "$SKILLS_ROOT/.system" -prune -o \
        -name SKILL.md -type f -print0
)

goal_supervisor="$SKILLS_ROOT/goal-supervisor/SKILL.md"
assert_contains \
    "$goal_supervisor" \
    "gpt-5.6-sol" \
    "goal-supervisor pins the Sol supervisor"
assert_contains \
    "$goal_supervisor" \
    "gpt-5.6-terra" \
    "goal-supervisor pins the Terra worker"
assert_contains \
    "$goal_supervisor" \
    'thinking: "medium"' \
    "goal-supervisor preserves the worker reasoning field"
assert_contains \
    "$goal_supervisor" \
    "../loop-protocol/SKILL.md" \
    "goal-supervisor composes loop-protocol"

loop_protocol="$SKILLS_ROOT/loop-protocol/SKILL.md"
monitor_until="$SKILLS_ROOT/monitor-until/SKILL.md"
hill_climbing="$SKILLS_ROOT/hill-climbing-loop/SKILL.md"
autoresearch="$SKILLS_ROOT/autoresearch/SKILL.md"

assert_contains \
    "$loop_protocol" \
    "grants no additional authority" \
    "loop-protocol is a reference rather than an authority grant"
assert_contains \
    "$monitor_until" \
    "../loop-protocol/SKILL.md" \
    "monitor-until composes loop-protocol"
assert_contains \
    "$monitor_until" \
    "structurally read-only" \
    "monitor-until keeps a strict read-only boundary"
assert_contains \
    "$hill_climbing" \
    "../loop-protocol/SKILL.md" \
    "hill-climbing-loop composes loop-protocol"
assert_contains \
    "$hill_climbing" \
    "No automatic commits" \
    "hill-climbing-loop rejects automatic experiment commits"
assert_contains \
    "$autoresearch" \
    "Deprecated compatibility entry" \
    "autoresearch is visibly deprecated"
assert_contains \
    "$autoresearch" \
    "../hill-climbing-loop/SKILL.md" \
    "autoresearch routes to hill-climbing-loop"
assert_contains \
    "$autoresearch" \
    "performs no discovery, edits, commands, commits, rollback, or looping by itself" \
    "autoresearch remains a routing shim"

for explicit_skill in autoresearch hill-climbing-loop monitor-until review-animations; do
    metadata_file="$SKILLS_ROOT/$explicit_skill/agents/openai.yaml"
    assert_contains \
        "$metadata_file" \
        "allow_implicit_invocation: false" \
        "$explicit_skill requires explicit invocation"
done

assert_contains \
    "$SKILLS_ROOT/loop-protocol/agents/openai.yaml" \
    "allow_implicit_invocation: true" \
    "loop-protocol may supply baseline safety implicitly"

loop_skill_paths=(
    "$SKILLS_ROOT/autoresearch"
    "$SKILLS_ROOT/hill-climbing-loop"
    "$SKILLS_ROOT/loop-protocol"
    "$SKILLS_ROOT/monitor-until"
)
for forbidden_command in \
    "git reset --hard" \
    "git add -A" \
    "git clean -fd" \
    "git checkout --" \
    "git push --force"; do
    if grep -R -Fq -- "$forbidden_command" "${loop_skill_paths[@]}"; then
        fail "loop skills contain destructive command text: $forbidden_command"
    fi
done
pass "loop skills exclude destructive Git command recipes"

if grep -R -Eq '/Users/|/home/' "${loop_skill_paths[@]}"; then
    fail "loop skills contain a machine-specific home path"
fi
pass "loop skills contain no machine-specific home paths"

echo ""
echo "All Codex global skill checks passed."
