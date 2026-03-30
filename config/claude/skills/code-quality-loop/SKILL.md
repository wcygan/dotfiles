---
name: code-quality-loop
description: Continuous code reviewer that compares branch diffs against existing codebase patterns. Catches naming inconsistencies, missing error handling, pattern violations, style drift, missing tests, and obvious bugs by learning what the project already does. Designed for /loop. Keywords: code review, quality, patterns, style, lint, consistency, drift, review loop
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git *)
---

# Code Quality Loop

Iterative reviewer that learns patterns from the existing codebase and flags deviations in your branch changes. Not a style guide — it reads sibling files to understand what THIS project does and compares your new code against that.

## Execution

### 1. Get Branch Diff

```bash
git diff main...HEAD --name-only
git diff main...HEAD
```

If no diff exists or the diff is identical to the last iteration (compare output length and file list), report:

> **No new changes to review.**

Then stop. Do not repeat previous suggestions.

### 2. Identify Changed Files

From `git diff main...HEAD --name-only`, collect the list of changed files. Skip binary files, lock files, and generated files (e.g., `*.lock`, `*.min.js`, `dist/`, `build/`).

### 3. Analyze Each Changed File

For each changed file:

**a. Read the full file** — not just the diff. You need surrounding context to understand local conventions.

**b. Read 2-3 sibling files** in the same directory (same extension, sorted by name). These are the pattern source — the existing code defines the standard.

**c. Read project config** if present (first iteration only): `CLAUDE.md`, `.eslintrc*`, `rustfmt.toml`, `pyproject.toml`, `.editorconfig`, `biome.json`, `deno.json`. Respect what these configure.

**d. Compare the new code against siblings and flag:**

| Category | What to look for |
|----------|-----------------|
| **Naming** | Variables/functions that don't match the file's or siblings' conventions |
| **Error handling** | New code paths missing error handling where siblings have it |
| **Pattern violations** | Doing X differently from how existing code does X (e.g., callbacks vs async/await, different import styles) |
| **Style drift** | Import ordering, string quoting, comment style that differs from siblings |
| **Missing tests** | New exported functions/methods without test coverage (check if test file exists) |
| **Obvious bugs** | Null/undefined risks, off-by-one, resource leaks, unreachable code |

**e. Do NOT flag:**
- Formatting (linter's job)
- Subjective preferences with no codebase precedent
- Pre-existing issues in unchanged code
- Anything already flagged in a previous iteration of this loop

### 4. Present Findings

Output a checklist, max **5 items** per iteration, highest-impact first:

```
## Code Quality Review

- [ ] **`src/auth.ts:42`** — Naming: `getUser()` → use `fetchUser()` to match `fetchRole()` on line 15
- [ ] **`src/db.ts:88`** — Error handling: new query path has no `.catch()`, siblings wrap all queries in try/catch
- [ ] **`lib/utils.rs:31`** — Pattern: uses `unwrap()` but sibling files use `?` operator consistently
- [ ] **`src/api.ts:12`** — Style: imports grouped differently from sibling files (side-effect imports should be last)
- [ ] **`src/auth.ts:55`** — Missing test: exported `validateToken()` has no test — `tests/auth.test.ts` exists but doesn't cover it

*Reviewed N files, compared against M siblings.*
```

If fewer than 5 issues found, report only what exists. If zero issues:

> **All changes consistent with existing patterns.** No issues found.

### 5. Track Suggestions

Maintain a mental log of previously reported issues by file path + line + category. On subsequent iterations:
- Skip any issue already reported (same file, same line range, same category)
- Only report NEW issues from NEW or MODIFIED changes since last iteration
- If a previously reported issue was fixed, do not re-report it

## Guardrails

- **Read-only**: NEVER edit or auto-fix code. Present suggestions only.
- **Branch-scoped**: Only review files changed on the current branch vs main.
- **Pattern-driven**: Compare against what the codebase does, not generic best practices. If the codebase uses `var`, don't suggest `const` — unless siblings use `const`.
- **Specific**: Include file:line, the existing pattern (with location), and the concrete fix. Vague suggestions are useless.
- **Non-repetitive**: Never re-suggest an issue from a prior iteration.
- **Max 5**: Focus on highest-impact issues. More than 5 creates noise.
