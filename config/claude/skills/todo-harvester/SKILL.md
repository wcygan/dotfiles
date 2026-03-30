---
name: todo-harvester
description: Find new TODO, FIXME, HACK, and XXX comments introduced on the current branch and create GitHub issues to track them. Designed for /loop usage. Keywords: todo, fixme, hack, issue, harvest, sweep, loop
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# TODO Harvester

Scan the current branch for new TODO/FIXME/HACK/XXX comments and create GitHub issues.

## Setup

```bash
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
TRACKER="/tmp/.todo-harvester-${REPO_NAME}"
touch "$TRACKER"
```

## Workflow

### 1. Find the Base

```bash
git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master
```

If both fail, report "No remote base branch found" and stop.

### 2. Extract New TODOs

```bash
git diff $(git merge-base HEAD origin/main)...HEAD | grep -iE '^\+.*(TODO|FIXME|HACK|XXX)' | grep -v '^\+\+\+'
```

Parse each match to extract file path (from diff hunk headers) and comment text.

### 3. Deduplicate

For each TODO, compute key: `{file}:{text_trimmed}`. Skip if already in `$TRACKER`.

### 4. Process Each TODO (max 5 per iteration)

**a. Gather context:**
- Read 5 lines before/after the TODO in the actual file
- Author: `git log --format='%an' -1 -- {file}`
- Commit: `git log --oneline -1 -- {file}`

**b. Skip if:**
- In a test file AND text is generic ("add more tests", "finish this", "implement later")
- Already tracked: `gh issue list -S "{TODO text}" --state open --json title -q '.[].title'` returns a match
- File has uncommitted changes (active WIP)

**c. Create issue:**

```bash
gh issue create \
  --title "{TYPE}: {brief description}" \
  --body "$(cat <<'EOF'
**File:** `{file}:{line}`
**Comment:** `{full TODO text}`
**Commit:** {short sha} — {commit message}

### Context
```
{surrounding code}
```
EOF
)" \
  --label "{label}"
```

**Label mapping:** TODO=`todo`, FIXME=`bug`, HACK/XXX=`tech-debt`

Create missing labels first: `gh label create {label} --force`

### 5. Update Tracker

```bash
echo "{file}:{text_trimmed}" >> "$TRACKER"
```

### 6. Report

- "Found {N} new TODOs, created {M} issues: {list of issue URLs}"
- Or: "No new TODOs on this branch"

## Guardrails

- **Max 5 issues per iteration** — stop after 5 even if more TODOs found
- **Branch-only** — only TODOs in the diff from base, never pre-existing
- **No duplicates** — tracker file + GitHub issue search
- **Present results** — always show created issue URLs to the user
- **Skip WIP** — ignore TODOs in files with uncommitted changes
