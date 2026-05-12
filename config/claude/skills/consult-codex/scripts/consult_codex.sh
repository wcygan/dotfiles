#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'USAGE'
Usage:
  consult_codex.sh [options] "<request>"
  consult_codex.sh [options] < prompt.txt

Options:
  --model <name>            Codex model to use. Defaults to $CODEX_MODEL or config.toml default.
  --sandbox <mode>          read-only | workspace-write | danger-full-access. Default read-only.
  --unsafe                  Use --dangerously-bypass-approvals-and-sandbox. Also enabled by
                            CONSULT_CODEX_UNSAFE=1. Mutually exclusive with --sandbox.
  --safe                    Force safe mode even when CONSULT_CODEX_UNSAFE is set.
  --bare                    Pass --ignore-user-config --ignore-rules for deterministic runs.
  --output-format <fmt>     text (default, prints last message) or json (passes --json).
  --raw-output              Print Codex's full stdout event stream instead of just the last message.
  --append-prompt <text>    Append extra context to the assembled prompt.
  --codex-arg <arg>         Pass one additional raw argument to codex. Repeat as needed.
  --codex-docs <path>       Path to codex-docs skill. Defaults are auto-detected.
  --print-prompt            Print the assembled prompts without running codex.
  --print-command           Print the codex command without running it.
  -h, --help                Show this help.
USAGE
}

model="${CODEX_MODEL:-}"
sandbox="read-only"
codex_docs_dir="${CODEX_DOCS_DIR:-}"
output_format="${CONSULT_CODEX_OUTPUT_FORMAT:-text}"
append_prompt=""
print_prompt=false
print_command=false
raw_output=false
bare=false
unsafe=false
safe_override=false
extra_codex_args=()

case "${CONSULT_CODEX_UNSAFE:-}" in
    1|true|TRUE|yes|YES)
        unsafe=true
        ;;
esac

while [[ $# -gt 0 ]]; do
    case "$1" in
        --model)
            [[ $# -ge 2 ]] || { echo "error: --model requires a value" >&2; exit 2; }
            model="$2"
            shift 2
            ;;
        --sandbox)
            [[ $# -ge 2 ]] || { echo "error: --sandbox requires a value" >&2; exit 2; }
            sandbox="$2"
            shift 2
            ;;
        --unsafe)
            unsafe=true
            shift
            ;;
        --safe)
            unsafe=false
            safe_override=true
            shift
            ;;
        --bare)
            bare=true
            shift
            ;;
        --output-format)
            [[ $# -ge 2 ]] || { echo "error: --output-format requires a value" >&2; exit 2; }
            output_format="$2"
            shift 2
            ;;
        --raw-output)
            raw_output=true
            shift
            ;;
        --append-prompt)
            [[ $# -ge 2 ]] || { echo "error: --append-prompt requires a value" >&2; exit 2; }
            if [[ -n "$append_prompt" ]]; then
                append_prompt+=$'\n\n'
            fi
            append_prompt+="$2"
            shift 2
            ;;
        --codex-arg)
            [[ $# -ge 2 ]] || { echo "error: --codex-arg requires a value" >&2; exit 2; }
            extra_codex_args+=("$2")
            shift 2
            ;;
        --codex-docs)
            [[ $# -ge 2 ]] || { echo "error: --codex-docs requires a path" >&2; exit 2; }
            codex_docs_dir="$2"
            shift 2
            ;;
        --print-prompt)
            print_prompt=true
            shift
            ;;
        --print-command)
            print_command=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "error: unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
        *)
            break
            ;;
    esac
done

if [[ $# -gt 0 ]]; then
    request="$*"
elif [[ ! -t 0 ]]; then
    request="$(cat)"
else
    echo "error: provide a request as arguments or stdin" >&2
    usage >&2
    exit 2
fi

if [[ -z "${request//[[:space:]]/}" ]]; then
    echo "error: request is empty" >&2
    exit 2
fi

case "$output_format" in
    text|json) ;;
    *)
        echo "error: --output-format must be text or json (got: $output_format)" >&2
        exit 2
        ;;
esac

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

normalize_dir() {
    local dir="$1"
    [[ -d "$dir" ]] || return 1
    (cd "$dir" && pwd -P)
}

resolve_codex_docs_dir() {
    local candidate repo_root

    if [[ -n "$codex_docs_dir" ]]; then
        if [[ -f "$codex_docs_dir/SKILL.md" ]]; then
            normalize_dir "$codex_docs_dir"
            return 0
        fi
        echo "error: --codex-docs does not contain SKILL.md: $codex_docs_dir" >&2
        return 1
    fi

    if [[ -n "${DOTFILES_DIR:-}" ]]; then
        candidate="$DOTFILES_DIR/config/codex/skills/codex-docs"
        if [[ -f "$candidate/SKILL.md" ]]; then
            normalize_dir "$candidate"
            return 0
        fi
    fi

    if repo_root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null)"; then
        candidate="$repo_root/config/codex/skills/codex-docs"
        if [[ -f "$candidate/SKILL.md" ]]; then
            normalize_dir "$candidate"
            return 0
        fi
    fi

    for candidate in \
        "$script_dir/../../../../codex/skills/codex-docs" \
        "$HOME/.codex/skills/codex-docs" \
        "$PWD/config/codex/skills/codex-docs"
    do
        if [[ -f "$candidate/SKILL.md" ]]; then
            normalize_dir "$candidate"
            return 0
        fi
    done

    echo "error: could not find codex-docs skill" >&2
    echo "Set CODEX_DOCS_DIR or pass --codex-docs /path/to/skill." >&2
    return 1
}

codex_docs_dir="$(resolve_codex_docs_dir)"
cwd="$(pwd -P)"

# Codex has no system-prompt flag, so the grounding instructions are folded
# into the single prompt that gets passed to `codex exec`.
grounding_prompt="$(cat <<PROMPT
You are Codex being consulted by Claude Code as an external, mostly read-only subagent.

First inspect the local Codex docs skill:
$codex_docs_dir

Read its SKILL.md before answering. Then read the specific references that match the request:
- references/agents-md.md for AGENTS.md discovery and instruction layering.
- references/skills.md for skill format, discovery, and progressive disclosure.
- references/subagents.md for delegation patterns and sandbox inheritance.
- references/hooks.md for lifecycle hooks and matchers.
- references/rules.md for command execution rules and execpolicy.
- references/config-basic.md and references/config-advanced.md for config.toml layering, profiles, sandbox, MCP, and providers.

Default mode: read-only consultation. Do not edit files, create files, run destructive commands, or perform irreversible actions unless the request explicitly asks for changes.
PROMPT
)"

if [[ -n "$append_prompt" ]]; then
    grounding_prompt+=$'\n\n'
    grounding_prompt+="$append_prompt"
fi

consult_prompt="$(cat <<PROMPT
$grounding_prompt

Current working directory:
$cwd

User request:
$request

Return a concise, actionable answer. Include file paths and line numbers for codebase claims when possible. If you cannot verify something, say so.
PROMPT
)"

if [[ "$safe_override" == true ]]; then
    unsafe=false
fi

codex_args=(exec --skip-git-repo-check --color never)

if [[ "$bare" == true ]]; then
    codex_args+=(--ignore-user-config --ignore-rules)
fi

if [[ -n "$model" ]]; then
    codex_args+=(--model "$model")
fi

if [[ "$unsafe" == true ]]; then
    codex_args+=(--dangerously-bypass-approvals-and-sandbox)
else
    codex_args+=(--sandbox "$sandbox")
fi

if [[ "$output_format" == "json" ]]; then
    codex_args+=(--json)
fi

# Capture only the final assistant message via --output-last-message so the
# default text mode produces clean prose, not the full event-stream. Skipped
# when --raw-output is set or when --output-format=json (which streams JSONL
# the caller wants to see directly).
last_msg_file=""
use_last_message=false
if [[ "$raw_output" != true && "$output_format" == "text" ]]; then
    use_last_message=true
    last_msg_file="$(mktemp -t consult-codex-last-message.XXXXXX)"
    trap 'rm -f "$last_msg_file"' EXIT
    codex_args+=(--output-last-message "$last_msg_file")
fi

if [[ ${#extra_codex_args[@]} -gt 0 ]]; then
    codex_args+=("${extra_codex_args[@]}")
fi

codex_args+=("$consult_prompt")

if [[ "$print_prompt" == true ]]; then
    printf '%s\n' '--- grounding prompt ---'
    printf '%s\n' "$grounding_prompt"
    printf '%s\n' '--- consult prompt ---'
    printf '%s\n' "$consult_prompt"
    exit 0
fi

if [[ "$print_command" == true ]]; then
    printf 'codex'
    printf ' %q' "${codex_args[@]}"
    printf '\n'
    exit 0
fi

if ! command -v codex >/dev/null 2>&1; then
    echo "error: codex CLI not found on PATH" >&2
    exit 127
fi

if [[ "$use_last_message" == true ]]; then
    # Discard the event-stream stdout; print only the final message. Stderr
    # passes through so genuine errors stay visible. set -e propagates a
    # non-zero exit code before we try to read the (possibly empty) tmpfile.
    codex "${codex_args[@]}" >/dev/null
    cat "$last_msg_file"
else
    exec codex "${codex_args[@]}"
fi
