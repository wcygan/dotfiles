---
title: Work Selection Strategy
description: How to choose the best next task from the beads ready queue
tags: [beads, selection, priority, scheduling]
---

# Work Selection Strategy

## Priority Matrix

When multiple tasks are ready, score them using this matrix:

| Factor | Weight | How to evaluate |
|--------|--------|-----------------|
| Priority level | High | P0 > P1 > P2 > P3 > P4 |
| Unblock factor | High | Count downstream tasks blocked by this one |
| Batch potential | Medium | Can this be done alongside related ready tasks? |
| Complexity fit | Medium | Does this match the current session's remaining capacity? |
| Staleness | Low | Older tasks slightly preferred over newer ones |

## Selection Algorithm

1. **Filter**: `bd ready --json` — only tasks with no open blockers
2. **Sort by priority**: P0 first, then P1, etc.
3. **Break ties with unblock factor**: Check `bd dep tree` for each candidate — prefer tasks that unblock the most downstream work
4. **Check for batches**: Among top candidates, group by parent epic or shared labels. If 2-3 related tasks are all ready, propose as a batch.
5. **Assess fit**: If the top candidate looks like a multi-day effort, flag it to the user — it may need decomposition first (use beads-decompose)

## Batch Selection Rules

Batch related tasks when:

- They share the **same parent epic** and none depends on the other
- They touch the **same module/area** (e.g., both are API endpoint tasks)
- They have **shared labels** (e.g., both labeled `frontend`)
- Combined effort is **under 4 hours**

Do NOT batch when:

- Tasks are in **different epics** with no relationship
- Combined effort exceeds a reasonable session
- One task's output might change the approach for the other

## Handling Edge Cases

### No ready tasks

```bash
bd list --status blocked --json    # What's blocked?
bd list --status open --json       # Anything open but unclaimed?
bd stats                           # Overall progress
```

Report to user:
- How many tasks are blocked and by what
- Whether the blocking tasks are in progress (someone else is working on them)
- If nothing is in progress, suggest claiming a blocker

### Everything is P3/P4

If only low-priority work remains, ask the user:
- Should we tackle the backlog?
- Are there new priorities not yet in beads?
- Is the project nearing completion?

### Task too large

If a ready task looks like it needs decomposition:
1. Don't claim it yet
2. Suggest using `beads-decompose` to break it down
3. After decomposition, the subtasks will appear in `bd ready`

### Stale in-progress tasks

```bash
bd stale --days 7 --status in_progress --json
```

If tasks have been in_progress for a long time, flag them:
- They may be abandoned and need reclaiming
- They may be blocked on something not tracked in beads
- Ask the user before touching someone else's claimed work

## Multi-Agent Awareness

When working in a multi-agent setup:

- Check assignee before claiming: `bd show <id> --json` — if already assigned, skip
- Prefer tasks no one has touched
- After claiming, start work promptly — don't hoard tasks
- If you discover you can't finish, unclaim: `bd update <id> --status open --json`
