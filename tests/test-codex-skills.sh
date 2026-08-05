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

assert_not_contains() {
    local file="$1"
    local unexpected="$2"
    local label="$3"

    if grep -Fq -- "$unexpected" "$file"; then
        fail "$file contains unexpected text: $unexpected"
    else
        pass "$label"
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
        "ephemeral-chooser/SKILL.md" \
        "find-animation-opportunities/SKILL.md" \
        "goal-supervisor/SKILL.md" \
        "hill-climbing-loop/SKILL.md" \
        "improve-animations/SKILL.md" \
        "loop-protocol/SKILL.md" \
        "monitor-until/SKILL.md" \
        "parallel-orchestrator/SKILL.md" \
        "pi-agent-controller/SKILL.md" \
        "pi-coding-agent/SKILL.md" \
        "pi-sdk/SKILL.md" \
        "pi-skill-teacher/SKILL.md" \
        "review-animations/SKILL.md" \
        "typst-author/SKILL.md"
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

codex_config="$ROOT/config/codex/config.toml"
global_agents="$ROOT/config/codex/AGENTS.md"
assert_contains \
    "$codex_config" \
    'multi_agent_v2 = true' \
    "Codex config enables multi-agent V2"
assert_contains \
    "$codex_config" \
    'max_concurrent_threads_per_session = 12' \
    "Codex config raises the spawned-agent concurrency limit"
assert_contains \
    "$codex_config" \
    'Spawned-agent cap; the primary task is additional.' \
    "Codex config documents that the root is outside the spawned-agent cap"
assert_contains \
    "$global_agents" \
    '## Multi-Agent Coordination' \
    "global Codex guidance defines multi-agent coordination"
assert_contains \
    "$global_agents" \
    'maintain a concise concurrency ledger' \
    "multi-agent coordination requires a concurrency ledger"
assert_contains \
    "$global_agents" \
    'normally 2–4 ready lanes' \
    "multi-agent coordination starts with bounded fan-out"
assert_contains \
    "$global_agents" \
    'Route models by lane:' \
    "multi-agent coordination routes work by model economics"
assert_contains \
    "$global_agents" \
    'A value of 12 permits twelve spawned agents plus the root.' \
    "multi-agent coordination explains concurrency-count semantics"
assert_contains \
    "$global_agents" \
    'Keep synthesis and final acceptance with the root agent.' \
    "multi-agent coordination retains root acceptance"

parallel_orchestrator="$SKILLS_ROOT/parallel-orchestrator/SKILL.md"
assert_contains \
    "$parallel_orchestrator" \
    'normally 2–4 ready lanes' \
    "parallel-orchestrator starts with a bounded first wave"
assert_contains \
    "$parallel_orchestrator" \
    'Expand toward 8 and then 12 spawned lanes only' \
    "parallel-orchestrator scales through evidence-gated waves"
assert_contains \
    "$parallel_orchestrator" \
    'Expected value / usage' \
    "parallel-orchestrator ledger tracks usage value"
assert_contains \
    "$parallel_orchestrator" \
    'agent_type: "luna_lane"' \
    "parallel-orchestrator routes economical lanes to Luna"
assert_contains \
    "$parallel_orchestrator" \
    'Keep the root on Sol' \
    "parallel-orchestrator retains root synthesis"
assert_contains \
    "$SKILLS_ROOT/parallel-orchestrator/agents/openai.yaml" \
    'allow_implicit_invocation: true' \
    "parallel-orchestrator may activate for natural multi-agent requests"

goal_supervisor="$SKILLS_ROOT/goal-supervisor/SKILL.md"
assert_contains \
    "$goal_supervisor" \
    '**Supervisor:** `gpt-5.6-sol`' \
    "goal-supervisor pins the Sol supervisor profile"
assert_contains \
    "$goal_supervisor" \
    '**Standard implementation worker:** native `agent_type: "worker"`' \
    "goal-supervisor prefers the Terra high worker profile"
assert_contains \
    "$goal_supervisor" \
    '**multi-worker mode**' \
    "goal-supervisor supports a bounded multi-worker topology"
assert_contains \
    "$goal_supervisor" \
    '../parallel-orchestrator/SKILL.md' \
    "goal-supervisor composes parallel-orchestrator for independent lanes"
assert_contains \
    "$goal_supervisor" \
    'model: "gpt-5.6-terra"' \
    "goal-supervisor pins the Terra worker model"
assert_contains \
    "$goal_supervisor" \
    'reasoning_effort: "high"' \
    "goal-supervisor pins high worker reasoning"
assert_contains \
    "$goal_supervisor" \
    'Do not wait on workers one by one' \
    "goal-supervisor monitors workers as a set"
assert_contains \
    "$goal_supervisor" \
    'use `xhigh`' \
    "goal-supervisor permits xhigh for especially difficult oversight"
assert_contains \
    "$goal_supervisor" \
    '**Exceptional worker:** `gpt-5.6-sol` with `high`' \
    "goal-supervisor limits Sol workers to an exceptional fallback"
assert_contains \
    "$goal_supervisor" \
    'Name an exceptional Sol worker `[smart-worker] <base title>`.' \
    "goal-supervisor applies the exact visible Smart Worker title prefix"
assert_contains \
    "$goal_supervisor" \
    'Remove all consecutive leading `[Supervisor] `, `[Worker N] `, or' \
    "goal-supervisor normalizes every recognized role prefix"
assert_contains \
    "$goal_supervisor" \
    "Preserve a worker's creation-time profile on" \
    "goal-supervisor preserves the selected worker profile for follow-ups"
assert_contains \
    "$goal_supervisor" \
    'Use a separate visible task only when the user explicitly asks for a' \
    "goal-supervisor limits separate task creation to the explicit fallback"
assert_contains \
    "$goal_supervisor" \
    'fork_turns: "none"' \
    "goal-supervisor uses the current bounded-history spawn schema"
assert_not_contains \
    "$goal_supervisor" \
    'fork_context' \
    "goal-supervisor contains no stale fork_context examples"

animation_finder="$SKILLS_ROOT/find-animation-opportunities/SKILL.md"
animation_reviewer="$SKILLS_ROOT/review-animations/SKILL.md"
assert_contains \
    "$animation_finder" \
    '## Motion Workflow Loop' \
    "animation finder defines the motion workflow loop"
assert_contains \
    "$animation_finder" \
    'hand its exact recipe to `animate`' \
    "animation finder hands accepted recipes to animate"
assert_contains \
    "$animation_finder" \
    'use `review-animations` on the resulting diff' \
    "animation finder closes the loop with review"
assert_contains \
    "$animation_reviewer" \
    '## Motion Workflow Loop' \
    "animation reviewer defines the motion workflow loop"
assert_contains \
    "$animation_reviewer" \
    '`find-animation-opportunities`' \
    "animation reviewer routes unknown candidates to discovery"
assert_contains \
    "$animation_reviewer" \
    'send the concrete finding back to `animate`' \
    "animation reviewer routes blocked changes back to implementation"
assert_contains \
    "$goal_supervisor" \
    'fresh task or Codex restart' \
    "goal-supervisor reports stale worker-role discovery before fallback"
assert_contains \
    "$goal_supervisor" \
    'One blocked lane must not stall unrelated lanes.' \
    "goal-supervisor isolates lane blockers"
assert_contains \
    "$goal_supervisor" \
    'required or optional status' \
    "goal-supervisor records lane criticality"
assert_contains \
    "$goal_supervisor" \
    'Keep one mutating owner per checkout, branch, or external' \
    "goal-supervisor preserves one writer per authority boundary"
assert_contains \
    "$goal_supervisor" \
    'Accept lanes and integrate independently' \
    "goal-supervisor requires lane and integrated acceptance"
assert_contains \
    "$ROOT/config/codex/agents/luna-worker.toml" \
    'name = "luna_worker"' \
    "tracked Luna worker exposes the expected custom-agent name"
assert_contains \
    "$ROOT/config/codex/agents/luna-worker.toml" \
    'model_reasoning_effort = "max"' \
    "tracked Luna worker uses maximum reasoning"
assert_contains \
    "$ROOT/config/codex/agents/luna-lane.toml" \
    'name = "luna_lane"' \
    "tracked Luna lane exposes the expected custom-agent name"
assert_contains \
    "$ROOT/config/codex/agents/luna-lane.toml" \
    'model_reasoning_effort = "medium"' \
    "tracked Luna lane uses economical medium reasoning"
assert_not_contains \
    "$goal_supervisor" \
    "gpt-5.6-luna" \
    "goal-supervisor contains no legacy Luna worker model reference"
assert_contains \
    "$goal_supervisor" \
    "../loop-protocol/SKILL.md" \
    "goal-supervisor composes loop-protocol"
assert_contains \
    "$global_agents" \
    'use one or more native Codex subagents according to the work topology' \
    "global piloting guidance permits multi-worker supervision"
assert_contains \
    "$global_agents" \
    'Monitor workers as a set.' \
    "global piloting guidance avoids serial worker monitoring"

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

pi_agent_controller="$SKILLS_ROOT/pi-agent-controller"
assert_contains \
    "$pi_agent_controller/SKILL.md" \
    'pi --offline --no-session' \
    "pi-agent-controller uses ephemeral one-shot Pi calls"
assert_contains \
    "$pi_agent_controller/SKILL.md" \
    '/skill:<name>' \
    "pi-agent-controller invokes discovered Pi skills without paths"
assert_contains \
    "$pi_agent_controller/SKILL.md" \
    'http://127.0.0.1:8080/v1/models' \
    "pi-agent-controller verifies the deployed local model"
assert_contains \
    "$pi_agent_controller/SKILL.md" \
    'llama-server \' \
    "pi-agent-controller provides the GLM llama.cpp launch command"
assert_contains \
    "$pi_agent_controller/SKILL.md" \
    'explicitly asks to start the model' \
    "pi-agent-controller does not start a large model implicitly"
assert_contains \
    "$pi_agent_controller/SKILL.md" \
    'references/standalone-prompt.md' \
    "pi-agent-controller routes to its standalone prompt contract"

pi_skill_teacher="$SKILLS_ROOT/pi-skill-teacher"
for required_file in \
    "$pi_skill_teacher/SKILL.md" \
    "$pi_skill_teacher/agents/openai.yaml" \
    "$pi_skill_teacher/assets/eval-manifest.example.json" \
    "$pi_skill_teacher/references/evaluation-design.md" \
    "$pi_skill_teacher/references/failure-taxonomy.md" \
    "$pi_skill_teacher/references/pi-skill-design.md" \
    "$pi_skill_teacher/scripts/certification-lock.mjs" \
    "$pi_skill_teacher/scripts/render-mcq.mjs" \
    "$pi_skill_teacher/scripts/run-eval-suite.sh" \
    "$pi_skill_teacher/scripts/run-pi-skill-eval.sh" \
    "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
    "$pi_skill_teacher/scripts/summarize-eval.mjs" \
    "$pi_skill_teacher/scripts/validate-eval-manifest.mjs"; do
    if [[ ! -f "$required_file" ]]; then
        fail "$required_file is missing"
    fi
done
pass "pi-skill-teacher ships its controller, references, assets, and helpers"

assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    '../pi-agent-controller/SKILL.md' \
    "pi-skill-teacher composes the bounded Pi controller"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    '../loop-protocol/SKILL.md' \
    "pi-skill-teacher composes the shared loop contract"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    '--skill <skill-path>' \
    "pi-skill-teacher supplies the exact Pi skill path"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    '/skill:<skill-name>' \
    "pi-skill-teacher forces full Pi skill expansion"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    'Use the <skill-name> skill to help solve this:' \
    "pi-skill-teacher explicitly assigns the skill in the prompt"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    'Never infer activation from score' \
    "pi-skill-teacher verifies activation independently"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    'Relabel every observed certification case as development' \
    "pi-skill-teacher preserves holdout integrity"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    'Certify as one locked transaction' \
    "pi-skill-teacher locks certification across thinking levels"
assert_contains \
    "$pi_skill_teacher/SKILL.md" \
    'root supervisor -> worker/controller (sole skill writer) -> Pi (read-only)' \
    "pi-skill-teacher preserves nested supervision ownership"
assert_contains \
    "$pi_skill_teacher/references/pi-skill-design.md" \
    'Pure-router profile' \
    "pi-skill-teacher supports reference-grounded pure routers"

for shell_script in \
    "$pi_skill_teacher/scripts/run-eval-suite.sh" \
    "$pi_skill_teacher/scripts/run-pi-skill-eval.sh"; do
    if ! bash -n "$shell_script"; then
        fail "$shell_script has invalid Bash syntax"
    fi
done
pass "pi-skill-teacher shell helpers parse"

for node_script in \
    "$pi_skill_teacher/scripts/certification-lock.mjs" \
    "$pi_skill_teacher/scripts/render-mcq.mjs" \
    "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
    "$pi_skill_teacher/scripts/summarize-eval.mjs" \
    "$pi_skill_teacher/scripts/validate-eval-manifest.mjs"; do
    if ! node --check "$node_script"; then
        fail "$node_script has invalid JavaScript syntax"
    fi
done
pass "pi-skill-teacher Node helpers parse"

rendered_teacher_case="$(
    node \
        "$pi_skill_teacher/scripts/render-mcq.mjs" \
        "$pi_skill_teacher/assets/eval-manifest.example.json" \
        D01
)"
if grep -Fq '"answer"' <<<"$rendered_teacher_case" ||
    grep -Fq 'Project configuration takes precedence' <<<"$rendered_teacher_case"; then
    fail "pi-skill-teacher renderer leaked controller-only answer data"
fi
pass "pi-skill-teacher renderer hides answer and rule fields"

if ! node \
    "$pi_skill_teacher/scripts/validate-eval-manifest.mjs" \
    "$pi_skill_teacher/assets/eval-manifest.example.json" \
    >/dev/null; then
    fail "pi-skill-teacher example manifest failed validation"
fi
pass "pi-skill-teacher example manifest validates"

teacher_test_tmp="$(mktemp -d)"
trap 'rm -rf "$teacher_test_tmp"' EXIT
teacher_test_project="$teacher_test_tmp/project"
teacher_test_skill="$teacher_test_project/.agents/skills/example-skill"
mkdir -p "$teacher_test_skill/references" "$teacher_test_tmp/bin"
git init -q "$teacher_test_project"

write_teacher_test_skill() {
    cat >"$teacher_test_skill/SKILL.md" <<'EOF'
---
name: example-skill
description: Example test skill.
---

# Example

Read `references/precedence.md`.
EOF
    printf '%s\n' 'Project configuration takes precedence.' \
        >"$teacher_test_skill/references/precedence.md"
}

write_teacher_test_skill
teacher_lock="$teacher_test_tmp/certification-lock.json"
teacher_lock_args=(
    --manifest "$pi_skill_teacher/assets/eval-manifest.example.json"
    --skill "$teacher_test_skill"
    --project "$teacher_test_project"
    --provider test-provider
    --model test-model
    --pi-version "pi-test 1.0"
    --thinking medium,high
)

if ! node "$pi_skill_teacher/scripts/certification-lock.mjs" create \
    "${teacher_lock_args[@]}" \
    --output "$teacher_lock" \
    >/dev/null; then
    fail "pi-skill-teacher could not create a certification lock"
fi
if ! node "$pi_skill_teacher/scripts/certification-lock.mjs" verify \
    "${teacher_lock_args[@]}" \
    --lock "$teacher_lock" \
    >/dev/null; then
    fail "pi-skill-teacher could not verify an unchanged certification lock"
fi
pass "pi-skill-teacher certification lock verifies frozen state"

printf '%s\n' '# drift' >>"$teacher_test_skill/SKILL.md"
if node "$pi_skill_teacher/scripts/certification-lock.mjs" verify \
    "${teacher_lock_args[@]}" \
    --lock "$teacher_lock" \
    >/dev/null 2>&1; then
    fail "pi-skill-teacher certification lock accepted skill drift"
fi
pass "pi-skill-teacher certification lock rejects skill drift"
write_teacher_test_skill
printf '%s\n' 'unrelated project drift' >"$teacher_test_project/unrelated.txt"
if node "$pi_skill_teacher/scripts/certification-lock.mjs" verify \
    "${teacher_lock_args[@]}" \
    --lock "$teacher_lock" \
    >/dev/null 2>&1; then
    fail "pi-skill-teacher certification lock accepted project drift"
fi
pass "pi-skill-teacher certification lock rejects project drift"
rm "$teacher_test_project/unrelated.txt"

teacher_valid_log="$teacher_test_tmp/valid.jsonl"
cat >"$teacher_valid_log" <<EOF
{"type":"message_end","message":{"role":"user","content":[{"type":"text","text":"<skill name=\"example-skill\" location=\"$teacher_test_skill/SKILL.md\">test</skill>"}]}}
{"type":"tool_execution_start","toolName":"read","args":{"path":"$teacher_test_skill/references/precedence.md"}}
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"{\"D01\":\"B\"}"}]}}
EOF

teacher_score_args=(
    --manifest "$pi_skill_teacher/assets/eval-manifest.example.json"
    --case D01
    --log "$teacher_valid_log"
    --skill-name example-skill
    --skill-path "$teacher_test_skill/SKILL.md"
    --activation forced
    --thinking medium
    --allowed-tools read
    --run-exit-code 0
)
teacher_valid_score="$(
    node "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
        "${teacher_score_args[@]}"
)"
if ! grep -Fq '"passed": true' <<<"$teacher_valid_score" ||
    ! grep -Fq '"skill_location_matched": true' <<<"$teacher_valid_score"; then
    fail "pi-skill-teacher scorer rejected valid forced evidence"
fi
pass "pi-skill-teacher scorer verifies exact forced skill location"

if node "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
    --manifest "$pi_skill_teacher/assets/eval-manifest.example.json" \
    --case D01 \
    --log "$teacher_valid_log" \
    --skill-name example-skill \
    --skill-path "$teacher_test_tmp/wrong/SKILL.md" \
    --activation forced \
    --allowed-tools read \
    --run-exit-code 0 \
    >/dev/null 2>&1; then
    fail "pi-skill-teacher scorer accepted a same-name skill from the wrong path"
fi
pass "pi-skill-teacher scorer rejects wrong-path skill expansion"

teacher_unauthorized_log="$teacher_test_tmp/unauthorized.jsonl"
cat >"$teacher_unauthorized_log" <<EOF
{"type":"message_end","message":{"role":"user","content":[{"type":"text","text":"<skill name=\"example-skill\" location=\"$teacher_test_skill/SKILL.md\">test</skill>"}]}}
{"type":"tool_execution_start","toolName":"read","args":{"path":"$teacher_test_skill/references/precedence.md"}}
{"type":"tool_execution_start","toolName":"bash","args":{"command":"true"}}
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"{\"D01\":\"B\"}"}]}}
EOF
if node "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
    --manifest "$pi_skill_teacher/assets/eval-manifest.example.json" \
    --case D01 \
    --log "$teacher_unauthorized_log" \
    --skill-name example-skill \
    --skill-path "$teacher_test_skill/SKILL.md" \
    --activation forced \
    --allowed-tools read \
    --run-exit-code 0 \
    >/dev/null 2>&1; then
    fail "pi-skill-teacher scorer accepted an unauthorized tool"
fi
pass "pi-skill-teacher scorer rejects unauthorized tools"

teacher_invalid_schema_log="$teacher_test_tmp/invalid-schema.jsonl"
cat >"$teacher_invalid_schema_log" <<EOF
{"type":"message_end","message":{"role":"user","content":[{"type":"text","text":"<skill name=\"example-skill\" location=\"$teacher_test_skill/SKILL.md\">test</skill>"}]}}
{"type":"tool_execution_start","toolName":"read","args":{"path":"$teacher_test_skill/references/precedence.md"}}
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"{\"D01\":\"Z\"}"}]}}
EOF
if teacher_invalid_schema_score="$(
    node "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
        --manifest "$pi_skill_teacher/assets/eval-manifest.example.json" \
        --case D01 \
        --log "$teacher_invalid_schema_log" \
        --skill-name example-skill \
        --skill-path "$teacher_test_skill/SKILL.md" \
        --activation forced \
        --allowed-tools read \
        --run-exit-code 0
)"; then
    fail "pi-skill-teacher scorer accepted an invalid choice label"
fi
if ! grep -Fq '"schema_exact": false' <<<"$teacher_invalid_schema_score"; then
    fail "pi-skill-teacher scorer did not classify the invalid choice as schema failure"
fi
pass "pi-skill-teacher scorer enforces available choice labels"

teacher_missing_final_log="$teacher_test_tmp/missing-final.jsonl"
cat >"$teacher_missing_final_log" <<EOF
{"type":"message_end","message":{"role":"user","content":[{"type":"text","text":"<skill name=\"example-skill\" location=\"$teacher_test_skill/SKILL.md\">test</skill>"}]}}
EOF
if teacher_missing_final_score="$(
    node "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
        --manifest "$pi_skill_teacher/assets/eval-manifest.example.json" \
        --case D01 \
        --log "$teacher_missing_final_log" \
        --skill-name example-skill \
        --skill-path "$teacher_test_skill/SKILL.md" \
        --activation forced \
        --allowed-tools read \
        --run-exit-code 0
)"; then
    fail "pi-skill-teacher scorer accepted a missing final assistant response"
fi
if ! grep -Fq '"runtime_status": "missing_final_assistant"' \
    <<<"$teacher_missing_final_score"; then
    fail "pi-skill-teacher scorer did not classify the missing final response"
fi
pass "pi-skill-teacher scorer separates runtime completion failures"

teacher_batch_log="$teacher_test_tmp/batch.jsonl"
cat >"$teacher_batch_log" <<EOF
{"type":"message_end","message":{"role":"user","content":[{"type":"text","text":"<skill name=\"example-skill\" location=\"$teacher_test_skill/SKILL.md\">test</skill>"}]}}
{"type":"tool_execution_start","toolName":"read","args":{"path":"$teacher_test_skill/references/precedence.md"}}
{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"{\"D01\":\"B\",\"C01\":\"A\"}"}]}}
EOF
if ! node "$pi_skill_teacher/scripts/score-pi-jsonl.mjs" \
    --manifest "$pi_skill_teacher/assets/eval-manifest.example.json" \
    --case D01,C01 \
    --log "$teacher_batch_log" \
    --skill-name example-skill \
    --skill-path "$teacher_test_skill/SKILL.md" \
    --activation forced \
    --allowed-tools read \
    --run-exit-code 0 \
    >/dev/null; then
    fail "pi-skill-teacher scorer rejected a valid batch"
fi
pass "pi-skill-teacher scorer supports exact multi-case batches"

cat >"$teacher_test_tmp/bin/pi" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--version" ]]; then
    echo "pi-test 1.0"
    exit 0
fi

skill_path=""
arguments=("$@")
for ((index = 0; index < ${#arguments[@]}; index++)); do
    if [[ "${arguments[$index]}" == "--skill" ]]; then
        skill_path="${arguments[$((index + 1))]}"
    fi
done

prompt="${arguments[$((${#arguments[@]} - 1))]}"
case_id="D01"
answer="B"
if [[ "$prompt" == *"C01."* ]]; then
    case_id="C01"
    answer="A"
fi

printf '%s\n' \
    "{\"type\":\"message_end\",\"message\":{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"<skill name=\\\"example-skill\\\" location=\\\"$skill_path/SKILL.md\\\">test</skill>\"}]}}" \
    "{\"type\":\"tool_execution_start\",\"toolName\":\"read\",\"args\":{\"path\":\"$skill_path/references/precedence.md\"}}" \
    "{\"type\":\"message_end\",\"message\":{\"role\":\"assistant\",\"content\":[{\"type\":\"text\",\"text\":\"{\\\"$case_id\\\":\\\"$answer\\\"}\"}]}}"
EOF
chmod +x "$teacher_test_tmp/bin/pi"

teacher_suite_output="$teacher_test_tmp/suite"
teacher_suite_summary="$(
    PATH="$teacher_test_tmp/bin:$PATH" \
        "$pi_skill_teacher/scripts/run-eval-suite.sh" \
        --activation forced \
        --split dev \
        --manifest "$pi_skill_teacher/assets/eval-manifest.example.json" \
        --output-dir "$teacher_suite_output" \
        --cwd "$teacher_test_project" \
        --provider test-provider \
        --model test-model \
        --thinking medium,high \
        --tools read \
        --skill "$teacher_test_skill" \
        --skill-name example-skill
)"
if ! grep -Fq '"overall_passed": true' <<<"$teacher_suite_summary" ||
    ! grep -Fq '"score_files": 2' <<<"$teacher_suite_summary"; then
    fail "pi-skill-teacher suite runner did not complete both thinking levels"
fi
pass "pi-skill-teacher suite runner completes and summarizes locked-shape runs"

teacher_cert_suite_output="$teacher_test_tmp/certification-suite"
teacher_cert_suite_summary="$(
    PATH="$teacher_test_tmp/bin:$PATH" \
        "$pi_skill_teacher/scripts/run-eval-suite.sh" \
        --activation forced \
        --split certification \
        --manifest "$pi_skill_teacher/assets/eval-manifest.example.json" \
        --output-dir "$teacher_cert_suite_output" \
        --cwd "$teacher_test_project" \
        --provider test-provider \
        --model test-model \
        --thinking medium,high \
        --tools read \
        --skill "$teacher_test_skill" \
        --skill-name example-skill \
        --lock "$teacher_lock"
)"
if ! grep -Fq '"overall_passed": true' <<<"$teacher_cert_suite_summary" ||
    ! grep -Fq '"score_files": 2' <<<"$teacher_cert_suite_summary"; then
    fail "pi-skill-teacher locked certification suite did not finish atomically"
fi
pass "pi-skill-teacher locked certification runs all levels before summary"

if grep -R -Eq '/Users/|/home/' "$pi_skill_teacher"; then
    fail "pi-skill-teacher contains a machine-specific home path"
fi
pass "pi-skill-teacher contains no machine-specific home paths"

for explicit_skill in autoresearch hill-climbing-loop monitor-until pi-skill-teacher review-animations; do
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

ephemeral_chooser="$SKILLS_ROOT/ephemeral-chooser"
ephemeral_reference="$ephemeral_chooser/references/ephemeral-chooser.html"
ephemeral_contract="$ephemeral_chooser/references/chooser-contract.md"

for required_file in \
    "$ephemeral_chooser/SKILL.md" \
    "$ephemeral_chooser/agents/openai.yaml" \
    "$ephemeral_reference" \
    "$ephemeral_contract"; do
    if [[ ! -f "$required_file" ]]; then
        fail "$required_file is missing"
    fi
done
pass "ephemeral-chooser ships its entrypoint, metadata, and local references"

assert_contains \
    "$ephemeral_chooser/SKILL.md" \
    "references/ephemeral-chooser.html" \
    "ephemeral-chooser routes to the local HTML reference"
assert_contains \
    "$ephemeral_chooser/SKILL.md" \
    "references/chooser-contract.md" \
    "ephemeral-chooser routes to the promotion contract"
assert_contains \
    "$ephemeral_chooser/agents/openai.yaml" \
    "allow_implicit_invocation: false" \
    "ephemeral-chooser requires explicit invocation"
assert_contains \
    "$ephemeral_reference" \
    'data-chooser="project-card"' \
    "ephemeral-chooser includes the project-card example"
assert_contains \
    "$ephemeral_reference" \
    'data-chooser="save-feedback"' \
    "ephemeral-chooser includes the save-feedback example"
assert_contains \
    "$ephemeral_reference" \
    'data-chooser="filter-summary"' \
    "ephemeral-chooser includes the filter-summary example"
assert_contains \
    "$ephemeral_reference" \
    'queryKey: "ec.project-card"' \
    "ephemeral-chooser namespaces selection state"
assert_contains \
    "$ephemeral_reference" \
    "window.history.replaceState" \
    "ephemeral-chooser persists review state without polluting history"
assert_contains \
    "$ephemeral_reference" \
    'addEventListener("keydown"' \
    "ephemeral-chooser supports keyboard variant selection"
assert_contains \
    "$ephemeral_reference" \
    "authorizationMatches" \
    "ephemeral-chooser separates URL state from promotion authorization"
assert_contains \
    "$ephemeral_reference" \
    'id="confirmation-input"' \
    "ephemeral-chooser requires exact stable-ID confirmation"
assert_contains \
    "$ephemeral_reference" \
    "sessionStorage" \
    "ephemeral-chooser retains local authorization across final-state reloads"
assert_contains \
    "$ephemeral_reference" \
    "finalizeChooser" \
    "ephemeral-chooser includes winner finalization"
assert_contains \
    "$ephemeral_contract" \
    '"beforeState": "absent"' \
    "ephemeral-chooser records generated-file baseline absence"
assert_contains \
    "$ephemeral_contract" \
    '"generatedSha256": "<sha256>"' \
    "ephemeral-chooser hashes cleanup-owned files"

template_count="$(grep -Fc '<template data-template=' "$ephemeral_reference")"
if [[ "$template_count" -ne 9 ]]; then
    fail "ephemeral-chooser expected 9 inert variant templates, found $template_count"
fi
pass "ephemeral-chooser ships three variants for each example"

if grep -Eq 'https?://|/Users/|/home/' "$ephemeral_reference"; then
    fail "ephemeral-chooser HTML reference contains an external or machine-specific path"
fi
pass "ephemeral-chooser HTML reference is local and machine-independent"

if node - "$ephemeral_reference" <<'NODE'
const fs = require("node:fs");

const file = process.argv[2];
const html = fs.readFileSync(file, "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/);

if (!script) {
    throw new Error("inline script is missing");
}

new Function(script[1]);
NODE
then
    pass "ephemeral-chooser inline JavaScript parses"
else
    fail "ephemeral-chooser inline JavaScript is invalid"
fi

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
