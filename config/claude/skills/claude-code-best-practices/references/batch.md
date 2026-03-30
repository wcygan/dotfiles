---
title: Batch Fan-Out
canonical_url: https://code.claude.com/docs/en/common-workflows
fetch_before_acting: true
---

# Batch Fan-Out (/batch)

> Before using /batch, WebFetch https://code.claude.com/docs/en/common-workflows for the latest.

## Summary

`/batch` fans out a large changeset to many worktree agents running in parallel. It interviews you to understand the scope, then spawns as many agents as needed — dozens, hundreds, or even thousands — each working in its own git worktree.

### When to Use

- **Large code migrations** (e.g., update API across 200 files)
- **Bulk refactors** (e.g., rename pattern across entire codebase)
- **Mass dependency updates** (e.g., upgrade library usage everywhere)
- **Any parallelizable work** where each unit is independent

### How It Works

1. **Interview phase**: `/batch` asks you what needs to change, how to verify, and what scope to cover
2. **Planning phase**: Claude analyzes the codebase and breaks work into independent units
3. **Fan-out phase**: Each unit gets its own worktree agent working in parallel
4. **Convergence**: Results are collected and merged

### Usage

```
/batch
```

Claude interviews you interactively, then handles the rest. Each agent:
- Gets its own isolated git worktree
- Works on a specific subset of the changeset
- Can run tests and verify its own changes
- Reports back results

### Key Characteristics

- **Worktree isolation**: every agent works in its own copy of the repo
- **True parallelism**: agents run concurrently, not sequentially
- **Scale**: handles from a few files to thousands
- **Verification**: each agent can run tests on its subset

### vs. Manual Approaches

| Approach | Scale | Isolation | Automation |
|----------|-------|-----------|------------|
| Single session | 1-10 files | None | Manual |
| Multiple `claude -w` | 2-10 tasks | Per worktree | Semi-manual |
| `/batch` | Unlimited | Per worktree | Fully automated |

### Tips

- Be specific about the change pattern during the interview
- Provide clear verification criteria (e.g., "tests must pass", "no type errors")
- Works best when each change unit is independent (no cross-file dependencies between units)
- Review the plan before confirming fan-out
