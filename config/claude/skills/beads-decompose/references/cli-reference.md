---
title: Beads CLI Reference
description: Complete bd command reference for task creation, dependencies, and management
tags: [beads, cli, bd, commands]
---

# Beads CLI Reference

## Initialization

```bash
bd init                    # Standard setup (prompts for role)
bd init --stealth          # Local-only, no repo commits
bd init --contributor      # Fork workflow, separate planning repo
bd init --team             # Branch collaboration
bd init --backend dolt     # Version-controlled SQL backend
```

## Creating Issues

```bash
# Basic creation
bd create "Title" -t task -p 1 --json

# Types: bug, feature, task, epic, chore
# Priorities: 0 (critical) to 4 (backlog)

# With description
bd create "Title" -t feature -p 1 -d "Description text" --json

# With parent (creates hierarchical subtask)
bd create "Subtask" -p 1 --parent <epic-id> --json

# With labels
bd create "Title" -l "backend,api" --json

# With dependency link
bd create "Title" -t bug -p 1 --deps discovered-from:<parent-id> --json

# From a file
bd create -f feature-plan.md --json
bd create "Title" --body-file=description.md --json

# With external reference (GitHub issue, Jira, etc.)
bd create "Title" --external-ref "gh-123" --json

# With spec reference
bd create "Title" --spec-id "docs/specs/auth.md" --json
```

## Updating Issues

```bash
bd update <id> --status in_progress --json
bd update <id> --priority 1 --json
bd update <id> --claim --json           # Atomically claim + set in_progress
bd update <id> --description "text" --json
bd update <id> --title "new title" --json
bd update <id> --design "notes" --json
bd update <id> --acceptance "criteria" --json

# Batch updates
bd update <id1> <id2> <id3> --priority 0 --json
```

## Dependencies

```bash
# Add dependency (child depends on parent)
bd dep add <child-id> <parent-id>

# With type
bd dep add <child-id> <parent-id> --type discovered-from

# View dependency tree
bd dep tree <id>

# Detect cycles
bd dep cycles
```

### Dependency Types

| Type | Meaning | Affects ready queue? |
|------|---------|---------------------|
| `blocks` | Hard dependency — child can't start until parent done | Yes |
| `related` | Soft association — informational only | No |
| `parent-child` | Epic/subtask hierarchy | No |
| `discovered-from` | Found during work on another task | No |

## Finding Work

```bash
bd ready --json                    # Tasks with no open blockers
bd ready --priority 1 --json       # Filter by priority
bd stale --days 30 --json          # Stale tasks
bd blocked                         # View blocked items
bd stats                           # Progress overview
```

## Closing & Reopening

```bash
bd close <id> --reason "Done" --json
bd close <id1> <id2> --reason "Batch complete" --json
bd reopen <id> --reason "Reopening" --json
```

## Listing & Filtering

```bash
bd list --status open --json
bd list --status open --priority 1 --json
bd list --assignee alice --json
bd list --type bug --json
bd list --label bug,critical --json
bd list --title-contains "auth" --json
bd list --no-assignee --json
bd list --priority-min 0 --priority-max 1 --json
```

## Labels

```bash
bd label add <id> <label> --json
bd label remove <id> <label> --json
bd label list <id> --json
bd label list-all --json
```

## Viewing Issues

```bash
bd show <id> --json
bd info --json                     # Database/config info
```

## Issue Statuses

- `open` — Ready to work on
- `in_progress` — Currently being worked on
- `blocked` — Cannot proceed
- `deferred` — Deliberately postponed
- `closed` — Work completed
- `pinned` — Stays open indefinitely

## Issue Types

- `epic` — Large feature with subtasks (supports dotted IDs up to 3 levels)
- `feature` — New functionality
- `task` — General work item
- `bug` — Something broken
- `chore` — Maintenance

## Hierarchical IDs

Epics automatically generate dotted child IDs:

```
bd-a3f8e9        (Epic)
bd-a3f8e9.1      (Task)
bd-a3f8e9.1.1    (Subtask)
```

Up to 3 nesting levels supported.

## Sync & Maintenance

```bash
bd sync                            # Push/pull with remote (Dolt)
bd admin compact --stats --json    # View compaction stats
bd admin cleanup --dry-run --json  # Preview cleanup
bd doctor                          # Health check
bd orphans --json                  # Find orphaned tasks
bd duplicates --dry-run            # Find duplicate tasks
```
