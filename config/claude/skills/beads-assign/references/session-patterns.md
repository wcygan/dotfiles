---
title: Session Patterns
description: Common work session patterns for executing beads tasks
tags: [beads, session, workflow, patterns]
---

# Session Patterns

## Pattern 1: Single Focus

Best for: complex P0/P1 tasks that need full attention.

```
1. bd ready --json
2. Select highest-priority task
3. bd update <id> --claim --json
4. Deep dive — read spec, understand context
5. Write tests → implement → verify
6. git commit -m "... (bd-xxx)"
7. bd close <id> --reason "..." --json
8. bd ready --json → report what's newly unblocked
9. bd sync (if Dolt)
```

## Pattern 2: Batch Sprint

Best for: multiple small related tasks (P2/P3, same epic).

```
1. bd ready --json
2. Identify 2-4 related ready tasks
3. bd update <id1> <id2> <id3> --claim --json
4. For each task:
   a. Read context
   b. Implement + test
   c. Commit with bead ID
   d. bd close <id> --reason "..." --json
5. bd ready --json → report progress
6. bd sync (if Dolt)
```

## Pattern 3: Unblock Chain

Best for: when high-priority downstream work is blocked.

```
1. bd list --status blocked --json → identify what's stuck
2. Trace backwards to find the root blocker
3. bd update <blocker-id> --claim --json
4. Implement the blocker
5. bd close <blocker-id> --reason "..." --json
6. Verify downstream tasks are now ready: bd ready --json
7. Optionally continue with the newly unblocked tasks
8. bd sync (if Dolt)
```

## Pattern 4: Discovery Session

Best for: exploratory work that generates new tasks.

```
1. bd update <spike-id> --claim --json
2. Investigate the spike/research task
3. Document findings in bead notes:
   bd update <id> --design "Findings: ..." --json
4. Create discovered tasks:
   bd create "Found: ..." --deps discovered-from:<spike-id> --json
5. bd close <spike-id> --reason "Investigation complete" --json
6. bd ready --json → show newly created tasks
7. bd sync (if Dolt)
```

## Commit Message Convention

Always include the bead ID in commit messages:

```bash
# Single task
git commit -m "Add user signup validation (bd-a1b2)"

# Multi-task batch
git commit -m "Implement catalog search and filter endpoints (bd-c3d4, bd-e5f6)"
```

This enables `bd doctor` to cross-reference open issues against git history and detect orphans.

## Discovery During Execution

When you find unexpected work while implementing a task:

**Do:**
- Create a new bead: `bd create "Found: ..." -t bug -p <priority> --deps discovered-from:<current-id> --json`
- Add a note to the current bead: `bd update <id> --design "Note: also found X, tracked as bd-xyz" --json`
- Stay focused on the current task

**Don't:**
- Scope-creep the current task to include the discovery
- Silently fix it without tracking
- Ignore it

## Session Boundaries

**Start of session:**
```bash
bd info --json          # Verify beads is initialized
bd ready --json         # See what's available
bd stats                # Overall progress snapshot
```

**End of session:**
```bash
bd sync                 # Push changes (Dolt)
bd ready --json         # Show remaining work
bd stats                # Progress summary
```

If leaving work incomplete:
```bash
# Don't leave tasks claimed but idle — either finish or release
bd update <id> --status open --json
bd update <id> --design "Partial progress: completed X, remaining Y" --json
```

## Error Recovery

**Claimed but can't finish:**
```bash
bd update <id> --status open --json
bd update <id> --design "Releasing: <reason>. Progress so far: <notes>" --json
```

**Found a blocker mid-task:**
```bash
bd update <id> --status blocked --json
bd create "Blocker: <description>" -t bug -p 0 --json
bd dep add <current-id> <blocker-id>
```

**Tests failing after implementation:**
- Don't close the bead
- Fix the tests or implementation
- Only close when green
