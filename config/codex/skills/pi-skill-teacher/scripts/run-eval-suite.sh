#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    cat <<'EOF'
Usage:
  run-eval-suite.sh \
    --activation <baseline|forced|natural> \
    --split <manifest-split> \
    --manifest <manifest.json> \
    --output-dir <new-absolute-directory> \
    --cwd <project-directory> \
    --provider <provider> \
    --model <model-id> \
    --thinking <comma-separated-levels> \
    [--tools <list|none>] \
    [--skill <skill-directory> --skill-name <name>] \
    [--lock <certification-lock.json>] \
    [--require-strict] \
    [--offline]

Certification requires forced activation, a lock, and the complete thinking
level list from that lock. Intermediate scores stay in the output directory and
are summarized only after every requested case and level has run.
EOF
}

fail() {
    echo "run-eval-suite.sh: $*" >&2
    exit 2
}

activation=""
split=""
manifest=""
output_dir=""
project_cwd=""
provider=""
model=""
thinking_csv=""
tools="read"
skill_path=""
skill_name=""
lock_file=""
offline=false
require_strict=false

while (($# > 0)); do
    case "$1" in
        --activation|--split|--manifest|--output-dir|--cwd|--provider|--model|--thinking|--tools|--skill|--skill-name|--lock)
            (($# >= 2)) || fail "$1 requires a value"
            case "$1" in
                --activation) activation="$2" ;;
                --split) split="$2" ;;
                --manifest) manifest="$2" ;;
                --output-dir) output_dir="$2" ;;
                --cwd) project_cwd="$2" ;;
                --provider) provider="$2" ;;
                --model) model="$2" ;;
                --thinking) thinking_csv="$2" ;;
                --tools) tools="$2" ;;
                --skill) skill_path="$2" ;;
                --skill-name) skill_name="$2" ;;
                --lock) lock_file="$2" ;;
            esac
            shift 2
            ;;
        --offline)
            offline=true
            shift
            ;;
        --require-strict)
            require_strict=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            fail "unknown argument: $1"
            ;;
    esac
done

case "$activation" in
    baseline|forced|natural) ;;
    *) fail "--activation must be baseline, forced, or natural" ;;
esac

[[ -n "$split" ]] || fail "--split is required"
[[ -f "$manifest" ]] || fail "manifest does not exist: $manifest"
manifest="$(cd "$(dirname "$manifest")" && pwd)/$(basename "$manifest")"

[[ -n "$project_cwd" ]] || fail "--cwd is required"
[[ -d "$project_cwd" ]] || fail "project directory does not exist: $project_cwd"
project_cwd="$(cd "$project_cwd" && pwd)"

[[ -n "$provider" ]] || fail "--provider is required"
[[ -n "$model" ]] || fail "--model is required"
[[ -n "$thinking_csv" ]] || fail "--thinking is required"
if ! thinking_csv="$(
    node -e '
const levels = process.argv[1].split(",").map((value) => value.trim()).filter(Boolean);
if (
  levels.length === 0 ||
  new Set(levels).size !== levels.length ||
  levels.some((level) => !/^[a-z]+$/.test(level))
) {
  process.exit(2);
}
process.stdout.write(levels.join(","));
' "$thinking_csv"
)"; then
    fail "--thinking must contain unique comma-separated lowercase levels"
fi

[[ "$output_dir" == /* ]] || fail "--output-dir must be absolute"
case "$output_dir" in
    "$project_cwd"|"$project_cwd"/*)
        fail "--output-dir must be outside the target project"
        ;;
esac
[[ ! -e "$output_dir" ]] || fail "refusing to reuse output directory: $output_dir"

if [[ "$activation" != "baseline" ]]; then
    [[ -n "$skill_path" ]] || fail "$activation activation requires --skill"
    [[ -n "$skill_name" ]] || fail "$activation activation requires --skill-name"
    if [[ "$skill_path" != /* ]]; then
        skill_path="$project_cwd/$skill_path"
    fi
    skill_path="$(cd "$skill_path" && pwd)"
    [[ -f "$skill_path/SKILL.md" ]] ||
        fail "skill directory does not contain SKILL.md: $skill_path"
fi

if [[ "$split" == "certification" ]]; then
    [[ "$activation" == "forced" ]] ||
        fail "certification requires forced activation"
    [[ -f "$lock_file" ]] || fail "certification requires --lock"
    lock_file="$(cd "$(dirname "$lock_file")" && pwd)/$(basename "$lock_file")"
fi

pi_bin="$(command -v pi || true)"
[[ -n "$pi_bin" ]] || fail "pi is not available on PATH"
pi_version="$("$pi_bin" --version)"

validator_args=("$manifest")
if [[ "$activation" != "baseline" ]]; then
    validator_args+=(--skill-dir "$skill_path")
fi
node "$script_dir/validate-eval-manifest.mjs" "${validator_args[@]}" >/dev/null

mkdir -p "$output_dir/prompts" "$output_dir/logs" "$output_dir/scores"
case_list="$(mktemp "$output_dir/.case-ids.XXXXXX")"
trap 'rm -f "$case_list"' EXIT

node -e '
const fs = require("fs");
const [manifestPath, split] = process.argv.slice(1);
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
for (const testCase of manifest.cases ?? []) {
  if (testCase.split === split) process.stdout.write(`${testCase.id}\n`);
}
' "$manifest" "$split" >"$case_list"

[[ -s "$case_list" ]] || fail "manifest has no cases in split: $split"

verify_lock() {
    [[ "$split" == "certification" ]] || return 0
    node "$script_dir/certification-lock.mjs" verify \
        --lock "$lock_file" \
        --manifest "$manifest" \
        --skill "$skill_path" \
        --project "$project_cwd" \
        --provider "$provider" \
        --model "$model" \
        --pi-version "$pi_version" \
        --thinking "$thinking_csv" \
        >/dev/null
}

verify_lock

IFS=',' read -r -a thinking_levels <<<"$thinking_csv"
for thinking in "${thinking_levels[@]}"; do
    thinking="${thinking//[[:space:]]/}"
    [[ -n "$thinking" ]] || fail "--thinking contains an empty level"

    while IFS= read -r case_id; do
        verify_lock

        stem="$activation-$split-$thinking-$case_id"
        prompt_file="$output_dir/prompts/$stem.txt"
        log_file="$output_dir/logs/$stem.jsonl"
        score_file="$output_dir/scores/$stem.score.json"

        node "$script_dir/render-mcq.mjs" "$manifest" "$case_id" >"$prompt_file"

        run_args=(
            --activation "$activation"
            --cwd "$project_cwd"
            --provider "$provider"
            --model "$model"
            --thinking "$thinking"
            --tools "$tools"
            --prompt-file "$prompt_file"
            --output "$log_file"
        )
        if [[ "$activation" == "forced" ]]; then
            run_args+=(--skill "$skill_path" --skill-name "$skill_name")
        fi
        if [[ "$offline" == true ]]; then
            run_args+=(--offline)
        fi

        if "$script_dir/run-pi-skill-eval.sh" "${run_args[@]}"; then
            run_exit_code=0
        else
            run_exit_code=$?
        fi

        score_args=(
            --manifest "$manifest"
            --case "$case_id"
            --log "$log_file"
            --activation "$activation"
            --thinking "$thinking"
            --allowed-tools "$tools"
            --run-exit-code "$run_exit_code"
        )
        if [[ "$activation" != "baseline" ]]; then
            score_args+=(
                --skill-name "$skill_name"
                --skill-path "$skill_path/SKILL.md"
            )
        fi
        if [[ "$require_strict" == true ]]; then
            score_args+=(--require-strict)
        fi

        if node "$script_dir/score-pi-jsonl.mjs" "${score_args[@]}" >"$score_file"; then
            :
        else
            score_exit_code=$?
            if [[ "$score_exit_code" -eq 2 ]]; then
                fail "evaluator failed for $case_id at $thinking"
            fi
        fi

        verify_lock
    done <"$case_list"
done

verify_lock
node "$script_dir/summarize-eval.mjs" "$output_dir/scores"
