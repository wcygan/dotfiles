#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  run-pi-skill-eval.sh \
    --activation <baseline|forced|natural> \
    --cwd <project-directory> \
    --provider <provider> \
    --model <model-id> \
    --thinking <level> \
    --prompt-file <question.txt> \
    --output <absolute-path.jsonl> \
    [--tools <list|none>] \
    [--skill <skill-directory> --skill-name <name>] \
    [--offline]

The output path must be outside the target project and must not already exist.
Forced activation requires --skill and --skill-name.
EOF
}

fail() {
    echo "run-pi-skill-eval.sh: $*" >&2
    exit 2
}

activation=""
project_cwd=""
provider=""
model=""
thinking=""
prompt_file=""
output_file=""
tools="read"
skill_path=""
skill_name=""
offline=false

while (($# > 0)); do
    case "$1" in
        --activation)
            (($# >= 2)) || fail "--activation requires a value"
            activation="$2"
            shift 2
            ;;
        --cwd)
            (($# >= 2)) || fail "--cwd requires a value"
            project_cwd="$2"
            shift 2
            ;;
        --provider)
            (($# >= 2)) || fail "--provider requires a value"
            provider="$2"
            shift 2
            ;;
        --model)
            (($# >= 2)) || fail "--model requires a value"
            model="$2"
            shift 2
            ;;
        --thinking)
            (($# >= 2)) || fail "--thinking requires a value"
            thinking="$2"
            shift 2
            ;;
        --prompt-file)
            (($# >= 2)) || fail "--prompt-file requires a value"
            prompt_file="$2"
            shift 2
            ;;
        --output)
            (($# >= 2)) || fail "--output requires a value"
            output_file="$2"
            shift 2
            ;;
        --tools)
            (($# >= 2)) || fail "--tools requires a value"
            tools="$2"
            shift 2
            ;;
        --skill)
            (($# >= 2)) || fail "--skill requires a value"
            skill_path="$2"
            shift 2
            ;;
        --skill-name)
            (($# >= 2)) || fail "--skill-name requires a value"
            skill_name="$2"
            shift 2
            ;;
        --offline)
            offline=true
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

[[ -n "$project_cwd" ]] || fail "--cwd is required"
[[ -d "$project_cwd" ]] || fail "project directory does not exist: $project_cwd"
project_cwd="$(cd "$project_cwd" && pwd)"

[[ -n "$provider" ]] || fail "--provider is required"
[[ -n "$model" ]] || fail "--model is required"
[[ -n "$thinking" ]] || fail "--thinking is required"
[[ -f "$prompt_file" ]] || fail "prompt file does not exist: $prompt_file"
[[ -s "$prompt_file" ]] || fail "prompt file is empty: $prompt_file"

[[ "$output_file" == /* ]] || fail "--output must be an absolute path"
case "$output_file" in
    "$project_cwd"|"$project_cwd"/*)
        fail "--output must be outside the target project"
        ;;
esac
[[ ! -e "$output_file" ]] || fail "refusing to overwrite existing log: $output_file"
[[ ! -e "${output_file}.stderr" ]] || fail "refusing to overwrite existing log: ${output_file}.stderr"
[[ -d "$(dirname "$output_file")" ]] || fail "output parent directory does not exist"

if [[ "$activation" == "forced" ]]; then
    [[ -n "$skill_path" ]] || fail "forced activation requires --skill"
    [[ -n "$skill_name" ]] || fail "forced activation requires --skill-name"
    [[ "$skill_name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] ||
        fail "--skill-name must be lowercase kebab-case"

    if [[ "$skill_path" != /* ]]; then
        skill_path="$project_cwd/$skill_path"
    fi
    [[ -f "$skill_path/SKILL.md" ]] ||
        fail "skill directory does not contain SKILL.md: $skill_path"
fi

pi_bin="$(command -v pi || true)"
[[ -n "$pi_bin" ]] || fail "pi is not available on PATH"

pi_args=(
    --provider "$provider"
    --model "$model"
    --thinking "$thinking"
    --no-session
    --no-context-files
    --approve
    --mode json
)

if [[ "$tools" == "none" ]]; then
    pi_args+=(--no-tools)
else
    pi_args+=(--tools "$tools")
fi

if [[ "$offline" == true ]]; then
    pi_args+=(--offline)
fi

question="$(<"$prompt_file")"

case "$activation" in
    baseline)
        pi_args+=(--no-skills)
        prompt="$question"
        ;;
    forced)
        pi_args+=(--no-skills --skill "$skill_path")
        prompt="/skill:$skill_name Use the $skill_name skill to help solve this: $question"
        ;;
    natural)
        prompt="$question"
        ;;
esac

(
    cd "$project_cwd"
    "$pi_bin" "${pi_args[@]}" "$prompt"
) >"$output_file" 2>"${output_file}.stderr"
