# CLAUDE.md

## Core Philosophy

**Small steps, tests first, green builds, atomic commits.**

## Development Loop

1. Write test first
2. Implement minimal solution
3. Run tests (must pass)
4. Format & lint
5. Commit atomically
6. Repeat

If tests fail, fix before moving on — never skip, disable, or comment out.

## Commit Rules

- All tests pass
- Code formatted and linted
- Single logical change with tests

## CLI Tools

**Prefer**: `rg`, `fd`, `jq`, `yq`, `gh` (over grep, find, cat, etc.)

**Available**: `bat`, `eza`, `fzf`, `delta` (interactive tools on PATH)

## Sub-Agents

Use 2-3 parallel agents for: codebase exploration, research, code quality audits, bug investigation.

**Never** for: single file reads, sequential tasks, trivial operations.

## Agent Teams

Use teams for inter-agent debate and coordination (2-3 agents typical, 4-5 for complex audits). Never have two agents edit the same file. Always include a devils-advocate for major decisions.

## Communication

- Default concise; defer to session or project overrides
- No preamble/postamble
- Direct answers
