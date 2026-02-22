---
title: Merge Strategy
description: 3-tier worktree merge protocol using bd merge-slot for serialized conflict-free merges
tags: [merge, worktree, merge-slot, conflict-resolution, git]
---

# Merge Strategy

## Overview

When multiple builder agents work in parallel worktrees, their changes must be merged
back to the main branch serially. The `bd merge-slot` primitive enforces one-at-a-time
merging. This document defines the 3-tier merge protocol.

## Why Serialized Merging

Parallel merges cause quadratic conflict rates. With N agents merging simultaneously:
- Agent A's merge invalidates Agent B's diff
- Both see the same base commit, both try to advance HEAD
- Result: race conditions, lost work, or manual resolution

Serialized merging (one agent at a time) reduces this to linear: each agent rebases
onto the latest HEAD before merging.

## Merge Order

When multiple agents complete in the same sprint, merge in this order:

1. **Data/Schema tasks** — migrations, seed data, type definitions
2. **API tasks** — routes, middleware, validation
3. **Fullstack tasks** — combined (data portion lands first naturally)
4. **UI tasks** — components, pages, styles
5. **Infra tasks** — config, CI, build scripts

This ordering minimizes conflicts because each layer depends on the one above it.
Schema changes land first so API code sees correct types, and UI code sees correct
API shapes.

## The 3-Tier Protocol

### Tier 1: Fast-Forward Merge (Happy Path)

The agent's worktree branch is directly ahead of main. No conflicts possible.

```bash
# Orchestrator acquires merge slot on behalf of agent
bd merge-slot acquire --json

# In the agent's worktree:
git checkout main
git merge --ff-only worktree-builder-auth

# If fast-forward succeeds:
git push origin main
bd merge-slot release
bd close $TASK_ID --reason "Merged via fast-forward"
```

**When this works:** The agent was the first to merge, or main hasn't changed since
the agent branched.

### Tier 2: Rebase + Retry (Another Agent Merged First)

Fast-forward fails because main has advanced. Rebase the agent's branch onto the
new main and retry.

```bash
# Fast-forward failed — main has new commits
bd merge-slot acquire --json  # Already held, skip if so

# Rebase agent's branch onto updated main
git fetch origin main
git checkout worktree-builder-auth
git rebase origin/main

# If rebase succeeds (no conflicts):
git checkout main
git merge --ff-only worktree-builder-auth
git push origin main
bd merge-slot release
bd close $TASK_ID --reason "Merged via rebase"
```

**When this works:** Changes don't overlap with what other agents modified.
This is the common case when tasks are in different bounded contexts.

### Tier 3: Escalate to Human (Genuine Conflict)

Rebase produces merge conflicts that require human judgment.

```bash
# Rebase hit conflicts
git rebase --abort   # Clean up

# Release the merge slot so other agents aren't blocked
bd merge-slot release

# Report to orchestrator
echo "MERGE_CONFLICT: Task $TASK_ID has conflicts with main"
echo "Files: $(git diff --name-only origin/main..worktree-builder-auth)"
```

The orchestrator:
1. Reports the conflict to the user with file list and both sides
2. Leaves the task `in_progress` (not closed)
3. Continues merging other agents' work
4. User resolves manually or on next `/clone-sprint` invocation

**When this happens:** Two agents modified the same files (should be rare with
vertical-slice decomposition and bounded-context isolation).

## Orchestrator Merge Flow

The orchestrator manages the merge slot and coordinates agent results:

```
for each completed agent (in merge-order):
    1. acquire merge-slot (wait if held)
    2. attempt fast-forward (Tier 1)
    3. if fails → rebase + retry (Tier 2)
    4. if fails → abort rebase, release slot, record conflict (Tier 3)
    5. release merge-slot
    6. close task (if merged successfully)
```

### Pseudocode

```
completed_agents = sort_by_merge_order(agents)
merge_results = []

for agent in completed_agents:
    # Step 1: Acquire
    slot = bd merge-slot acquire --wait --json

    # Step 2: Fetch latest main
    git fetch origin main

    # Step 3: Try fast-forward
    if git merge --ff-only agent.branch:
        git push origin main
        bd merge-slot release
        bd close agent.task_id
        merge_results.append({agent, status: "merged", tier: 1})
        continue

    # Step 4: Try rebase
    git checkout agent.branch
    if git rebase origin/main:
        git checkout main
        git merge --ff-only agent.branch
        git push origin main
        bd merge-slot release
        bd close agent.task_id
        merge_results.append({agent, status: "merged", tier: 2})
        continue

    # Step 5: Escalate
    git rebase --abort
    bd merge-slot release
    conflict_files = git diff --name-only origin/main..agent.branch
    merge_results.append({agent, status: "conflict", files: conflict_files})

return merge_results
```

## Worktree Lifecycle

### Creation (by orchestrator via Task tool)

```python
Task(
    name="builder-auth",
    subagent_type="general-purpose",
    isolation="worktree",
    prompt="... task description ..."
)
```

Claude Code creates the worktree automatically at `.claude/worktrees/builder-auth/`.

### Agent Work (inside worktree)

The agent works normally — edit, test, commit. All commits land on the worktree branch.

```bash
# Agent's branch is automatically created by Claude Code
# Agent commits normally:
git add -A
git commit -m "feat(auth): implement login form"
```

### Cleanup (after merge)

Successful merge:
```bash
git worktree remove .claude/worktrees/builder-auth
git branch -d worktree-builder-auth
```

Failed merge (Tier 3):
```bash
# Keep worktree for manual resolution
# User can: cd .claude/worktrees/builder-auth && git rebase main
```

## Conflict Prevention

The best merge strategy is avoiding conflicts entirely:

1. **Vertical slices by bounded context** — each agent owns different directories
2. **Scaffold first** — shared config/schema lands before feature work
3. **File target declarations** — each task lists its expected files, orchestrator
   checks for overlap before assigning to same sprint
4. **Different bounded contexts per sprint** — select tasks from distinct contexts

### File Overlap Check

Before spawning agents, the orchestrator should verify no two tasks in the same
sprint target the same files:

```
for each pair (task_a, task_b) in sprint_batch:
    files_a = extract_file_targets(task_a.description)
    files_b = extract_file_targets(task_b.description)
    if intersection(files_a, files_b) is not empty:
        warn("Potential conflict: {task_a.id} and {task_b.id} both touch {overlap}")
        # Move one task to next sprint
```

## Recovery from Mid-Sprint Failure

If the orchestrator crashes mid-merge:

1. **Check merge-slot state**: `bd merge-slot check --json`
   - If held by a dead process → `bd merge-slot release`
2. **Check task states**: `bd list --status in_progress --json`
   - Orphaned in_progress tasks → reset to open or close if work is on branch
3. **Check worktrees**: `git worktree list`
   - Orphaned worktrees with commits → attempt merge on next invocation
   - Empty worktrees → remove

The next `/clone-sprint` invocation picks up from current state automatically.
