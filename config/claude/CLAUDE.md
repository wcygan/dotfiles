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

## Version Control: jj over git

**Default to `jj` (Jujutsu) in any repo that has a `.jj` directory.** jj is git-compatible — teammates using plain git are unaffected — but local history rewriting, rebasing, and conflict handling are dramatically better. A `PreToolUse` hook (`hooks/enforce-jj.sh`) blocks mutating `git` commands inside jj-managed repos and suggests the jj equivalent.

- **Use jj for**: `commit`, `describe`, `rebase`, `squash`, `split`, `restore`, `abandon`, `new`, `edit`, `bookmark` moves, `git fetch`/`git push` via `jj git ...`, undo via `jj undo` / `jj op restore`.
- **Fall back to git for**: LFS, submodules, `.gitattributes`, git hooks, signed push to protected branches — the hook lets these through. Prefix with `JJ_OVERRIDE=1` to bypass the hook if it blocks something legitimately git-only.
- **If stuck on a jj command or concept**, load the `jj` skill (`/jj` or just ask about jj workflows). It covers the full git→jj translation, colocated-repo gotchas, and day-to-day recipes (split, squash, stacked rebase, conflict resolution).
- **Pure-git repos (no `.jj` dir)** are unaffected — the hook is a no-op there, and git is the right tool.

## Sub-Agents

Use 2-3 parallel agents for: codebase exploration, research, code quality audits, bug investigation.

**Never** for: single file reads, sequential tasks, trivial operations.

## Agent Teams

Use teams for inter-agent debate and coordination (2-3 agents typical, 4-5 for complex audits). Never have two agents edit the same file. Always include a devils-advocate for major decisions.

## Communication

- Default concise; defer to session or project overrides
- No preamble/postamble
- Direct answers
