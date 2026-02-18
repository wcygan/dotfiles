---
name: fast-commit
description: Stage all changes with git add -A and commit immediately with a concise message derived from recent work. Use when you want to quickly commit everything without interactive review or confirmation. Keywords: fast commit, quick commit, commit everything, stage all, commit all, ship it
disable-model-invocation: true
argument-hint: [optional message override]
allowed-tools: Bash(git *)
---

# Fast Commit

Stage all tracked and untracked changes, then commit immediately with a short message
based on what was just accomplished in the conversation.

## Workflow

### 1. Stage Everything

```bash
git add -A
```

### 2. Check What's Staged

```bash
git diff --staged --stat
```

If the working tree is already clean (nothing staged), report that and stop.

### 3. Generate Commit Message

If `$ARGUMENTS` is provided, use it directly as the commit message — skip message generation.

Otherwise, look at the conversation context (what was just implemented, fixed, or changed)
and write a short imperative message under 72 chars. Keep it simple — one line, no body.

### 4. Commit Immediately

```bash
git commit -m "<message>"
```

No confirmation. No split suggestions. Just commit.

### 5. Confirm

```bash
git log --oneline -1
```

Show the committed SHA and message so the user knows it landed.

## Rules

- **Speed over ceremony** — the message should take 5 seconds to write
- **Stage everything** — `git add -A`, not selective staging
- **No confirmation prompt** — this is fast mode by design
- **No linting, no tests** — user's responsibility in fast mode
- If `.env` or obvious credential files appear in `--stat`, warn before committing them
