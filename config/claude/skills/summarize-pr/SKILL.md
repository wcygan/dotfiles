---
name: summarize-pr
description: Read a pull request and produce a concise summary of what changed, why, key decisions, and risks. Use when reviewing others' PRs, catching up on merged work, or triaging a PR queue. Keywords: summarize PR, PR summary, review PR, understand PR, what does this PR do, PR overview, triage PR
disable-model-invocation: true
argument-hint: [PR-number-or-URL]
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(gh *)
---

# Summarize PR

Read a pull request and produce a structured, actionable summary. Designed for quickly understanding what a PR does without reading every line of the diff.

## Gather PR Data

```bash
# PR metadata
gh pr view $ARGUMENTS[0] --json title,body,author,labels,milestone,createdAt,additions,deletions,changedFiles,baseRefName,headRefName,reviewDecision,reviews,comments

# File-level changes
gh pr diff $ARGUMENTS[0] --name-only

# Full diff
gh pr diff $ARGUMENTS[0]

# CI status
gh pr checks $ARGUMENTS[0] --json name,state,conclusion 2>/dev/null
```

## Produce the Summary

### TL;DR
One sentence: what does this PR do and why?

### Motivation
Why was this change made? Pull from:
- PR description/body
- Linked issues (look for "Closes #N", "Fixes #N" in the body)
- If an issue is linked, fetch it: `gh issue view <N> --json title,body`

### What Changed
Group changes by logical concern, not by file. For each group:
- What was added, modified, or removed
- The implementation approach in 1-2 sentences

Prioritize: lead with the most important changes, not the largest files.

### Architecture & Design Decisions
Note any significant choices:
- New patterns introduced
- Dependencies added or removed
- Schema or API changes
- Configuration changes

### Risks & Review Focus Areas
Flag things a reviewer should look closely at:
- **Breaking changes**: API modifications, schema migrations, removed features
- **Security**: auth changes, input handling, new endpoints
- **Performance**: new queries, loops over collections, missing pagination
- **Missing coverage**: new code paths without tests
- **Rollback complexity**: would this be hard to revert?

### CI Status
If checks are available, summarize: passing, failing, or pending.

### Stats
```
Author: @name
Files changed: N (+additions, -deletions)
Labels: [list]
Reviews: N approved / N changes requested / N pending
```

## Guidelines

- **Be opinionated**: don't just describe, evaluate. "This PR adds caching but doesn't handle cache invalidation" is more useful than "This PR adds caching"
- **Estimate review effort**: "Quick review (~10 min, small surface area)" or "Deep review needed (~30 min, touches auth and payments)"
- **Compare to the PR description**: if the PR claims to do X but the diff shows Y, flag the discrepancy
- **Note what's NOT in the PR**: if the PR description mentions follow-up work, call it out so reviewers know the scope is intentionally limited
