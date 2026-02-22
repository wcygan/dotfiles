---
title: Beads Integration
description: bd CLI command patterns and conventions for clone-sprint orchestration
tags: [beads, bd, cli, task-management, conventions]
---

# Beads Integration

## Overview

Beads (`bd`) is the task management substrate for clone-sprint. All task state lives in
`.beads/` as content-addressed files that merge without conflicts. This document covers
the CLI patterns used by the orchestrator and builder agents.

## Environment Setup

### Actor Identity

Every `bd` command uses `$BD_ACTOR` to identify the caller. Set per-agent:

```bash
export BD_ACTOR="clone-sprint-orchestrator"   # orchestrator
export BD_ACTOR="builder-auth"                # builder agent (use bounded context)
```

### Initialization

```bash
bd init --quiet    # Non-interactive; creates .beads/ directory
```

Only run once per project. Subsequent invocations are no-ops.

## Core Command Reference

### Creating Epics (Bounded Contexts)

```bash
bd create "Auth System" -t epic -p 1 --label "auth,scaffold" --description "$(cat <<'DESC'
## Bounded Context: Authentication

Entities: User, Session, Credential
Aggregates: UserAggregate

See: 05-domain-model.md — Auth context
DESC
)"
```

Returns the epic ID (e.g., `bd-a3f8e9`). Store this for child creation.

### Creating Subtasks (Feature Slices)

Subtasks are created as children of their epic. Beads auto-numbers them:

```bash
bd create "Auth: Login Form — fullstack" \
  -p 1 \
  --label "auth,fullstack,md" \
  --acceptance "$(cat <<'ACC'
- [ ] Email/password form with validation
- [ ] POST /api/auth/login endpoint
- [ ] Session cookie set on success
- [ ] Error states: invalid credentials, rate limit
- [ ] Redirect to dashboard on success
ACC
)" \
  --description "$(cat <<'DESC'
## Feature: Login Form

### Entities
- User { id, email, passwordHash, createdAt }
- Session { id, userId, token, expiresAt }

### API Endpoints
- POST /api/auth/login — { email, password } → { user, token }

### File Targets
- src/app/login/page.tsx
- src/api/auth/login/route.ts
- src/lib/auth.ts

### Design Tokens
- Input: h-10 rounded-md border-input
- Button: bg-primary text-primary-foreground
- Error: text-destructive text-sm

### Xref
- 02-feature-priority-matrix.md: F1 (P0, effort: MD)
- 03-mvp-scope-contract.md: Login acceptance criteria
- 08-api-surface-spec.md: POST /api/auth/login
DESC
)"
```

### Adding Dependencies

```bash
# Hard dependency: login-ui blocked by scaffold
bd dep add bd-a3f8e9.1 bd-c2d4e6    # child blocked-by scaffold epic

# Between epics: API epic depends on Auth epic
bd dep add bd-b5c7d9 bd-a3f8e9      # API blocked-by Auth
```

Only `blocks` dependencies affect the `bd ready` queue.

### Querying Ready Tasks

```bash
bd ready --json
```

Returns tasks with no unresolved `blocks` dependencies and status `open`:

```json
[
  {
    "id": "bd-a3f8e9.2",
    "title": "Auth: Signup Form — fullstack",
    "priority": 1,
    "labels": ["auth", "fullstack", "md"],
    "status": "open"
  }
]
```

### Claiming Tasks (Atomic)

```bash
bd update bd-a3f8e9.2 --claim
```

Atomically sets `status=in_progress` and `assignee=$BD_ACTOR`. Prevents race conditions
when multiple agents query `bd ready` simultaneously.

### Closing Tasks

```bash
bd close bd-a3f8e9.2 --reason "Login form implemented with tests"
```

### Viewing Task Details

```bash
bd show bd-a3f8e9.2 --json
```

### Listing with Filters

```bash
bd list --status open --json           # All open tasks
bd list --status in_progress --json    # Currently claimed
bd list --label auth --json            # By bounded context
bd blocked --json                      # Tasks with unresolved deps
```

### Project Statistics

```bash
bd stats --json
```

```json
{
  "total": 24,
  "open": 12,
  "in_progress": 3,
  "closed": 9,
  "progress_percent": 37.5
}
```

## Swarm Commands

### Validate Epic Structure

```bash
bd swarm validate bd-a3f8e9 --verbose
```

Returns parallelism analysis — how many tasks can run concurrently per wave:

```json
{
  "epic_id": "bd-a3f8e9",
  "total_issues": 8,
  "ready_fronts": [
    {"wave": 0, "issues": ["bd-a3f8e9.1", "bd-a3f8e9.2"]},
    {"wave": 1, "issues": ["bd-a3f8e9.3"]}
  ],
  "max_parallelism": 2,
  "swarmable": true
}
```

### Swarm Status

```bash
bd swarm status bd-a3f8e9 --json
```

```json
{
  "epic_id": "bd-a3f8e9",
  "total_issues": 8,
  "completed": [{"id": "bd-a3f8e9.1", "title": "..."}],
  "active": [{"id": "bd-a3f8e9.3", "assignee": "builder-auth"}],
  "ready": [{"id": "bd-a3f8e9.4"}],
  "blocked": [{"id": "bd-a3f8e9.5", "blocked_by": ["bd-a3f8e9.3"]}],
  "progress_percent": 25.0
}
```

## Merge Slot Commands

See [merge-strategy.md](merge-strategy.md) for the full protocol. Quick reference:

```bash
bd merge-slot acquire             # Try to acquire (fails if held)
bd merge-slot acquire --wait      # Queue if held, block until available
bd merge-slot check               # Check availability without acquiring
bd merge-slot release             # Release after merge complete
```

All commands support `--json` for machine consumption.

## Conventions

### Task Title Format

```
"{BoundedContext}: {Feature} — {layer}"
```

Examples:
- `"Auth: Login Form — fullstack"`
- `"Billing: Stripe Webhook — api"`
- `"Dashboard: Activity Feed — ui"`

### Label Taxonomy

| Label | Meaning |
|-------|---------|
| `{context}` | Bounded context name (lowercase): `auth`, `billing`, `dashboard` |
| `{layer}` | Implementation layer: `fullstack`, `data`, `api`, `ui`, `infra` |
| `{effort}` | Effort estimate (mapped from research): `sm`, `md`, `lg`, `xl` |
| `scaffold` | Project scaffolding task (blocks all feature epics) |

**Effort mapping from research:** Research docs use `S/M/L/XL`; beads labels use
`sm/md/lg/xl`. See [task-decomposition.md](task-decomposition.md) for the full mapping.

### Priority Mapping

| Priority | Source | Meaning |
|----------|--------|---------|
| 1 | P0 | Must-have MVP feature |
| 2 | P1 | Should-have feature |
| 3 | P2 | Nice-to-have feature |
| 4 | P3 | Backlog / future |

Scaffold tasks also use priority 1 (P0) since they are must-have. Distinguish scaffold
from feature tasks via the `scaffold` label, not via priority.

### JSON Mode

Every `bd` command supports `--json`. Always use it in automation:

```bash
READY=$(bd ready --json)
TASK_ID=$(echo "$READY" | jq -r '.[0].id')
```

### Error Handling

`bd` exits non-zero on failure. Check exit codes:

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error (invalid args, missing .beads/) |
| 2 | Task not found |
| 3 | Dependency cycle detected |
| 4 | Merge slot contention (acquire failed) |
