---
name: diff-explain
description: Explain a diff in plain English. Works with staged changes, unstaged changes, commits, branches, or PR numbers. Use when you want to understand what changed and why. Keywords: diff, explain diff, what changed, understand changes, diff summary, review changes, read diff
disable-model-invocation: true
argument-hint: [ref|PR-number|--staged|--unstaged]
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(gh *)
---

# Diff Explain

Explain a diff in plain, conversational English. Focus on **what changed** and **why it likely changed**, not just listing modified files.

## Determine the Diff Source

Parse `$ARGUMENTS` to determine what diff to explain:

| Argument | Command |
|----------|---------|
| (none) | `git diff` (unstaged changes) |
| `--staged` | `git diff --staged` |
| `--unstaged` | `git diff` |
| A number (e.g., `123`) | `gh pr diff 123` |
| A commit hash | `git show <hash>` |
| A branch name | `git diff main...<branch>` |
| Two refs (e.g., `v1.0..v1.1`) | `git diff <ref1>...<ref2>` |

## Gather Context

1. Get the diff using the appropriate command above
2. Get the file list: `git diff --stat` (or equivalent for the source)
3. If it's a PR, also fetch: `gh pr view <number> --json title,body,labels`

## Explain the Changes

Structure the explanation as:

### Overview
One paragraph: what is this change about at a high level? What problem does it solve or what feature does it add?

### Key Changes
For each logically grouped change:
- **What**: which files changed and what was modified
- **Why**: infer the motivation from the code context
- **How**: brief description of the implementation approach

Group related file changes together (e.g., "Updated the User model and its tests" rather than listing each file separately).

### Notable Details
Flag anything interesting:
- Breaking changes or API modifications
- New dependencies added
- Configuration changes
- Files deleted or renamed
- Potential risks or things a reviewer should look closely at

### Summary Stats
```
Files changed: N
Insertions: +N
Deletions: -N
```

## Guidelines

- **Be conversational**, not mechanical. "Added a retry mechanism to the HTTP client" is better than "Modified http_client.ts lines 45-60"
- **Infer intent** from the code. If a function was renamed from `getData` to `fetchUserProfile`, note that the rename improves clarity, don't just say "renamed function"
- **Highlight the important parts**. A 500-line diff might have one key architectural decision — find it and lead with it
- **Note what's missing** if relevant: "This adds the API endpoint but doesn't include tests yet"
- **Skip boilerplate**: don't explain auto-generated changes, lock file updates, or formatting-only diffs unless they're the entire change
