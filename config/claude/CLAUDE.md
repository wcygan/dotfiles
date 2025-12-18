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

## Commit Rules

- All tests pass
- Code formatted and linted
- Single logical change with tests

## CLI Tools

**Prefer**: `rg`, `fd`, `bat`, `eza`, `jq`, `yq`, `fzf`, `delta`, `gh`

## Sub-Agents

Use 2-3 parallel agents for: codebase exploration, research, code quality audits, bug investigation.

**Never** for: single file reads, sequential tasks, trivial operations.

## Communication

- Concise (max 4 lines unless asked)
- No preamble/postamble
- Direct answers
