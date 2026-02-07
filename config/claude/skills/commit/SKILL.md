---
name: commit
description: Analyze staged changes and create a well-crafted conventional commit. Handles unstaged files, pre-commit hook failures, and multi-file changes. Use when ready to commit, or when you want help writing a good commit message. Keywords: commit, git commit, stage, conventional commit, commit message
disable-model-invocation: true
argument-hint: [optional message override]
---

# Smart Commit

Analyze staged (and optionally unstaged) changes, generate a conventional commit message, and commit atomically.

## Workflow

### 1. Assess Working State

```bash
git status
git diff --staged --stat
git diff --stat
```

Determine:
- **Staged changes**: ready to commit
- **Unstaged changes**: ask user if they should be included
- **Untracked files**: flag any that look like they should be tracked

If nothing is staged and there are unstaged changes, ask the user which files to stage before proceeding.

### 2. Analyze the Diff

```bash
git diff --staged
```

Read the full staged diff. Understand:
- What files changed and why
- Whether this is a single logical change (good) or multiple concerns (suggest splitting)
- Whether any files look like they shouldn't be committed (`.env`, credentials, large binaries, lock files that weren't intentionally updated)

### 3. Generate Commit Message

Use conventional commit format:

```
<type>(<scope>): <subject>

<body>
```

**Type selection:**
| Type | When |
|------|------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `chore` | Build process, tooling, dependencies |
| `perf` | Performance improvement |
| `style` | Formatting, missing semicolons, etc. |
| `ci` | CI/CD configuration |

**Rules:**
- Subject line: imperative mood, no period, under 72 chars
- Scope: the module/component affected (optional but preferred)
- Body: explain **why**, not **what** (the diff shows what)
- If `$ARGUMENTS` is provided, use it as the subject line instead of generating one

### 4. Confirm and Commit

Present the proposed commit message to the user. If they approve:

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject line here

Body explaining why this change was made.
EOF
)"
```

### 5. Handle Pre-Commit Hook Failures

If the commit fails due to a pre-commit hook:

1. Read the hook output to understand what failed
2. Fix the issue (formatting, linting, etc.)
3. Re-stage the fixed files: `git add <fixed-files>`
4. Create a **NEW** commit (never `--amend` — the previous commit didn't happen)
5. Repeat until the commit succeeds

### 6. Post-Commit Verification

```bash
git status
git log --oneline -1
```

Confirm the commit was created and working tree is in expected state.

## Split Detection

If the staged changes contain multiple unrelated concerns, suggest splitting:

```
I notice the staged changes include both a bug fix in auth.ts and a
refactor in utils.ts. Consider committing these separately:
  1. git reset HEAD utils.ts → commit the fix first
  2. git add utils.ts → commit the refactor second
```

## Quick Mode

If `$ARGUMENTS` is provided, use it as the commit message subject and skip the interactive confirmation:

```
/commit fix login redirect on expired sessions
```

Becomes: `fix: fix login redirect on expired sessions`
