#!/usr/bin/env bash
set -euo pipefail

DEFAULT_ALLOWED_TOOLS="Read,Grep,Glob,WebFetch,WebSearch,Bash(cat *),Bash(ls *),Bash(git status*),Bash(git diff*),Bash(git show*),Bash(git log*)"
DEFAULT_DISALLOWED_TOOLS="Edit,Write,MultiEdit,NotebookEdit"

usage() {
    cat <<'USAGE'
Usage:
  consult_claude.sh [options] "<request>"
  consult_claude.sh [options] < prompt.txt

Options:
  --model <name>             Claude model to use. Defaults to $CLAUDE_MODEL or opus.
  --allowed-tools <tools>    Read-only allowlist. Defaults to $CONSULT_CLAUDE_ALLOWED_TOOLS or a safe local set.
  --disallowed-tools <tools> Write-capable denylist. Defaults to $CONSULT_CLAUDE_DISALLOWED_TOOLS or Edit/Write tools.
  --unsafe                   Use --dangerously-skip-permissions. Also enabled by CONSULT_CLAUDE_UNSAFE=1.
  --safe                     Force safe mode even when CONSULT_CLAUDE_UNSAFE is set.
  --bare                     Use Claude bare mode for deterministic API-key-backed runs.
  --output-format <format>   text, json, or stream-json.
  --max-budget-usd <amount>  Pass a spend cap to Claude Code.
  --append-system-prompt <p> Append extra instructions after the built-in grounding prompt.
  --claude-arg <arg>         Pass one additional raw argument to claude. Repeat as needed.
  --best-practices <path>    Path to claude-code-best-practices. Defaults are auto-detected.
  --print-prompt             Print the assembled prompts without running claude.
  --print-command            Print the claude command without running it.
  -h, --help                 Show this help.
USAGE
}

model="${CLAUDE_MODEL:-opus}"
allowed_tools="${CONSULT_CLAUDE_ALLOWED_TOOLS:-$DEFAULT_ALLOWED_TOOLS}"
disallowed_tools="${CONSULT_CLAUDE_DISALLOWED_TOOLS:-$DEFAULT_DISALLOWED_TOOLS}"
best_practices_dir="${CLAUDE_BEST_PRACTICES_DIR:-}"
output_format="${CONSULT_CLAUDE_OUTPUT_FORMAT:-}"
max_budget_usd="${CONSULT_CLAUDE_MAX_BUDGET_USD:-}"
extra_system_prompt=""
print_prompt=false
print_command=false
bare=false
unsafe=false
extra_claude_args=()

case "${CONSULT_CLAUDE_UNSAFE:-}" in
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
        --allowed-tools|--allowedTools)
            [[ $# -ge 2 ]] || { echo "error: --allowed-tools requires a value" >&2; exit 2; }
            allowed_tools="$2"
            shift 2
            ;;
        --disallowed-tools|--disallowedTools)
            [[ $# -ge 2 ]] || { echo "error: --disallowed-tools requires a value" >&2; exit 2; }
            disallowed_tools="$2"
            shift 2
            ;;
        --unsafe)
            unsafe=true
            shift
            ;;
        --safe)
            unsafe=false
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
        --max-budget-usd)
            [[ $# -ge 2 ]] || { echo "error: --max-budget-usd requires a value" >&2; exit 2; }
            max_budget_usd="$2"
            shift 2
            ;;
        --append-system-prompt)
            [[ $# -ge 2 ]] || { echo "error: --append-system-prompt requires a value" >&2; exit 2; }
            if [[ -n "$extra_system_prompt" ]]; then
                extra_system_prompt+=$'\n\n'
            fi
            extra_system_prompt+="$2"
            shift 2
            ;;
        --claude-arg)
            [[ $# -ge 2 ]] || { echo "error: --claude-arg requires a value" >&2; exit 2; }
            extra_claude_args+=("$2")
            shift 2
            ;;
        --best-practices)
            [[ $# -ge 2 ]] || { echo "error: --best-practices requires a path" >&2; exit 2; }
            best_practices_dir="$2"
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

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

normalize_dir() {
    local dir="$1"
    [[ -d "$dir" ]] || return 1
    (cd "$dir" && pwd -P)
}

resolve_best_practices_dir() {
    local candidate repo_root

    if [[ -n "$best_practices_dir" ]]; then
        if [[ -f "$best_practices_dir/SKILL.md" ]]; then
            normalize_dir "$best_practices_dir"
            return 0
        fi
        echo "error: --best-practices does not contain SKILL.md: $best_practices_dir" >&2
        return 1
    fi

    if [[ -n "${DOTFILES_DIR:-}" ]]; then
        candidate="$DOTFILES_DIR/config/claude/skills/claude-code-best-practices"
        if [[ -f "$candidate/SKILL.md" ]]; then
            normalize_dir "$candidate"
            return 0
        fi
    fi

    if repo_root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null)"; then
        candidate="$repo_root/config/claude/skills/claude-code-best-practices"
        if [[ -f "$candidate/SKILL.md" ]]; then
            normalize_dir "$candidate"
            return 0
        fi
    fi

    for candidate in \
        "$script_dir/../../../../claude/skills/claude-code-best-practices" \
        "$HOME/.claude/skills/claude-code-best-practices" \
        "$PWD/config/claude/skills/claude-code-best-practices"
    do
        if [[ -f "$candidate/SKILL.md" ]]; then
            normalize_dir "$candidate"
            return 0
        fi
    done

    echo "error: could not find claude-code-best-practices skill" >&2
    echo "Set CLAUDE_BEST_PRACTICES_DIR or pass --best-practices /path/to/skill." >&2
    return 1
}

best_practices_dir="$(resolve_best_practices_dir)"
cwd="$(pwd -P)"

grounding_prompt="$(cat <<PROMPT
You are Claude Code being consulted by Codex as an external, mostly read-only subagent.

First inspect the local Claude Code best-practices skill:
$best_practices_dir

Read its SKILL.md before answering. Then read the specific references that match the request:
- references/headless.md for Claude CLI, headless mode, output formats, permissions, and scripts.
- references/sub-agents.md for external-agent framing and delegation patterns.
- references/skill-best-practices.md and references/skills.md for skill authoring or review.
- references/tools-reference.md for tool permission syntax and tool behavior.
- references/writing-claude-md.md for CLAUDE.md work.

Default mode: read-only consultation. Do not edit files, create files, run destructive commands, or perform irreversible actions unless the request explicitly asks for changes.
PROMPT
)"

if [[ -n "$extra_system_prompt" ]]; then
    grounding_prompt+=$'\n\n'
    grounding_prompt+="$extra_system_prompt"
fi

consult_prompt="$(cat <<PROMPT
Current working directory:
$cwd

User request:
$request

Return a concise, actionable answer. Include file paths and line numbers for codebase claims when possible. If you cannot verify something, say so.
PROMPT
)"

claude_args=()

if [[ "$bare" == true ]]; then
    claude_args+=(--bare)
fi

claude_args+=(--model "$model")
claude_args+=(--append-system-prompt "$grounding_prompt")

if [[ -n "$output_format" ]]; then
    claude_args+=(--output-format "$output_format")
fi

if [[ -n "$max_budget_usd" ]]; then
    claude_args+=(--max-budget-usd "$max_budget_usd")
fi

if [[ "$unsafe" == true ]]; then
    claude_args+=(--dangerously-skip-permissions)
else
    claude_args+=(--allowed-tools "$allowed_tools")
    claude_args+=(--disallowed-tools "$disallowed_tools")
fi

if [[ ${#extra_claude_args[@]} -gt 0 ]]; then
    claude_args+=("${extra_claude_args[@]}")
fi

claude_args+=(-p "$consult_prompt")

if [[ "$print_prompt" == true ]]; then
    printf '%s\n' '--- append-system-prompt ---'
    printf '%s\n' "$grounding_prompt"
    printf '%s\n' '--- prompt ---'
    printf '%s\n' "$consult_prompt"
    exit 0
fi

if [[ "$print_command" == true ]]; then
    printf 'claude'
    printf ' %q' "${claude_args[@]}"
    printf '\n'
    exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
    echo "error: claude CLI not found on PATH" >&2
    exit 127
fi

exec claude "${claude_args[@]}"
