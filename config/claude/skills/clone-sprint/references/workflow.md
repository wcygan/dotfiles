---
title: Workflow
description: State detection, sprint phases, and orchestration flow for clone-sprint
tags: [workflow, state-machine, phases, sprint, orchestration]
---

# Workflow

## Overview

Clone-sprint is an idempotent state machine. Each invocation of `/clone-sprint <slug>`
detects the current state and executes the appropriate phase. Users invoke the skill
repeatedly — each invocation runs one sprint (2-3 tasks).

## State Detection

On every invocation, the orchestrator checks three conditions to determine the phase:

| Condition | Phase | Action |
|-----------|-------|--------|
| No `clone-research/{slug}/` directory | **Error** | Abort — research must exist |
| Research exists, no `.beads/` directory | **Phase 1** | Initialize DAG + run first sprint |
| `.beads/` exists, `bd ready` returns tasks | **Phase 2** | Run next sprint |
| `.beads/` exists, `bd ready` returns empty, in_progress tasks exist | **Phase 2b** | Resume — check for orphaned tasks |
| `.beads/` exists, all tasks closed | **Phase 3** | Final report |

### Detection Logic

```bash
RESEARCH_DIR="clone-research/$SLUG"
BEADS_DIR=".beads"

# Check research exists
if [ ! -d "$RESEARCH_DIR" ]; then
    echo "ERROR: Run /clone-research $SLUG first"
    exit 1
fi

# Check beads initialized
if [ ! -d "$BEADS_DIR" ]; then
    # Phase 1: Initialize
    execute_phase_1
    exit 0
fi

# Check ready tasks
READY=$(bd ready --json)
READY_COUNT=$(echo "$READY" | jq 'length')

if [ "$READY_COUNT" -gt 0 ]; then
    # Phase 2: Sprint
    execute_phase_2 "$READY"
    exit 0
fi

# Check in-progress tasks (possibly orphaned)
IN_PROGRESS=$(bd list --status in_progress --json)
IP_COUNT=$(echo "$IN_PROGRESS" | jq 'length')

if [ "$IP_COUNT" -gt 0 ]; then
    # Phase 2b: Resume / recovery
    execute_phase_2b "$IN_PROGRESS"
    exit 0
fi

# All done
execute_phase_3
```

## Phase 1: Initialize & Decompose

**Trigger:** Research directory exists, no `.beads/` directory.

**Steps:**

### 1.0 Verify Research Completeness

Before reading research docs, verify the output is usable:

1. **Read `00-INDEX.md` first** — it lists known gaps from the research phase
2. **Check each doc file exists:**
   ```bash
   for doc in 01-product-thesis 02-feature-priority-matrix 03-mvp-scope-contract \
     04-core-user-journeys 05-domain-model 06-system-architecture \
     07-revenue-pricing-model 08-api-surface-spec 09-design-system-brief; do
       [ -f "clone-research/$SLUG/$doc.md" ] || echo "MISSING: $doc.md"
   done
   ```
3. **If `05-domain-model.md` is missing → ABORT.** Bounded contexts are required for
   epic creation. Tell the user to re-run `/clone-research` or create doc 05 manually.
4. **For other missing docs, degrade gracefully:**
   - Missing doc 08 → skip API endpoint embedding in task descriptions
   - Missing doc 09 → skip design token embedding
   - Missing doc 07 → skip billing context entirely
   - Note all gaps in the DAG report to the user

5. **Inform the user** if this is the first decomposition:
   ```
   Initializing task DAG from research output. If you haven't reviewed the
   research docs yet, you can Ctrl-C now, review 00-INDEX.md and skim docs
   02, 05, 06, then re-run. The DAG will be built from these documents as-is.
   ```

### 1.1 Read Research Documents

Read all available documents from `clone-research/{slug}/`:

```
00-INDEX.md              (executive summary, cross-reference map, known gaps)
01-product-thesis.md
02-feature-priority-matrix.md
03-mvp-scope-contract.md
04-core-user-journeys.md
05-domain-model.md
06-system-architecture.md
07-revenue-pricing-model.md
08-api-surface-spec.md
09-design-system-brief.md
```

Extract:
- Executive summary (doc 00) → agent preamble "What We're Building" context
- Product thesis (doc 01) → agent preamble detail
- P0 features with effort estimates (doc 02) → task list
- MVP scope and acceptance criteria (doc 03) → task acceptance fields
- User journeys (doc 04) → task ordering
- Bounded contexts and entities (doc 05) → epics and domain context
- Stack and file structure (doc 06) → agent instructions
- Pricing features (doc 07) → billing tasks if P0
- API endpoints (doc 08) → API task descriptions
- Design tokens (doc 09) → UI task descriptions

### 1.2 Initialize Beads

```bash
bd init --quiet
```

### 1.3 Create Task DAG

Follow the decomposition process in [task-decomposition.md](task-decomposition.md):

1. Create scaffold epic (priority 1, labeled `scaffold`)
2. Create scaffold subtasks
3. Create feature epics (one per bounded context with P0 features)
4. Create feature subtasks with rich descriptions
5. Wire dependencies (scaffold → epics → subtasks)
6. Validate DAG (`bd swarm validate`)

### 1.4 Report DAG to User

Present the task DAG summary:

```
## Task DAG Created

**Project:** {slug}
**Epics:** {count}
**Tasks:** {total_count}
**Estimated Sprints:** {ceil(total_count / 2.5)}

### Epics:
1. Project Scaffold (4 tasks) — P0, blocks all
2. Auth System (3 tasks) — P0, blocked by Scaffold
3. Workspace System (3 tasks) — P1, blocked by Auth
4. Project System (3 tasks) — P1, blocked by Workspace

### Ready Now:
- Scaffold: Project Init — infra
- Scaffold: Database Setup — data
- Scaffold: Design System Foundation — ui
```

### 1.5 Run First Sprint

Immediately proceed to Phase 2 with the ready tasks from the scaffold epic.
This avoids requiring the user to invoke `/clone-sprint` a second time just to
start work.

## Phase 2: Sprint Execution

**Trigger:** `.beads/` exists and `bd ready` returns tasks.

**Steps:**

### 2.1 Select Sprint Batch

Query ready tasks and select 2-3 for this sprint:

```bash
READY=$(bd ready --json)
```

**Selection criteria** (in priority order):
1. Higher priority tasks first (lower number = higher priority)
2. Tasks from different bounded contexts (minimize file overlap)
3. Tasks with no file target overlap (check descriptions)
4. Prefer tasks that unblock the most downstream work

**Hard limit:** Never select more than 3 tasks per sprint.

### 2.2 Claim Tasks

```bash
for task_id in $SELECTED_TASKS; do
    bd update $task_id --claim
done
```

### 2.3 Compose Agent Prompts

For each selected task:

1. Determine agent type from task labels (see [agent-roles.md](agent-roles.md))
2. Build common preamble from project context
3. Append type-specific instructions
4. Append task description, acceptance criteria, and design notes
5. Include task ID for commit message prefixing

### 2.4 Spawn Builder Agents

Spawn all agents in a single response (parallel execution):

```python
# All agents spawned together — Claude Code runs them in parallel
Task(
    name="builder-auth-login",
    subagent_type="general-purpose",
    isolation="worktree",
    prompt=agent_prompt_1
)

Task(
    name="builder-workspace-create",
    subagent_type="general-purpose",
    isolation="worktree",
    prompt=agent_prompt_2
)
```

### 2.5 Wait for Completion

All agents run in foreground (not background) so the orchestrator waits for
all to complete before proceeding to merge.

### 2.6 Merge Results

Follow the merge protocol in [merge-strategy.md](merge-strategy.md):

1. Sort completed agents by merge order (data → API → fullstack → UI → infra)
2. For each agent:
   a. Acquire merge slot
   b. Attempt Tier 1 (fast-forward)
   c. If fail → Tier 2 (rebase + retry)
   d. If fail → Tier 3 (escalate, skip)
   e. Release merge slot
   f. Close task if merged

### 2.7 Sprint Report

Present results to user:

```
## Sprint Complete

**Completed:** 2/3 tasks merged
**Failed:** 1 task (merge conflict — Auth: Login Form)

### Merged:
- [x] Scaffold: Database Setup — data (fast-forward)
- [x] Scaffold: Design System Foundation — ui (rebase)

### Needs Attention:
- [ ] Auth: Login Form — fullstack (conflict in src/lib/auth.ts)

### Progress:
- Total tasks: 16
- Completed: 6 (37.5%)
- Ready for next sprint: 3
- Blocked: 7
- Estimated remaining sprints: 4

Run `/clone-sprint {slug}` to execute the next sprint.
```

## Phase 2b: Resume / Recovery

**Trigger:** No ready tasks, but in_progress tasks exist.

This means a previous sprint was interrupted. Recovery steps:

1. **Check for worktrees** with completed work:
   ```bash
   git worktree list
   ```

2. **For each in_progress task:**
   - If worktree exists with commits → attempt merge
   - If worktree exists but empty → remove worktree, reset task to open
   - If no worktree → reset task to open

3. **After recovery**, check `bd ready` again and proceed to Phase 2 if tasks available.

```bash
IN_PROGRESS=$(bd list --status in_progress --json)

for task in $(echo "$IN_PROGRESS" | jq -r '.[].id'); do
    WORKTREE_PATH=".claude/worktrees/builder-*"

    if [ -d "$WORKTREE_PATH" ] && git -C "$WORKTREE_PATH" log --oneline -1 2>/dev/null; then
        # Has commits — try to merge
        attempt_merge "$task" "$WORKTREE_PATH"
    else
        # No work done — reset
        bd update "$task" --status open --assignee ""
    fi
done
```

## Phase 3: Completion

**Trigger:** All tasks are closed.

**Steps:**

### 3.1 Final Statistics

```bash
bd stats --json
```

### 3.2 Completion Report

```
## Project Build Complete

**Project:** {slug}
**Total Tasks:** {total}
**Sprints Used:** {sprint_count}
**Merge Conflicts Resolved:** {conflict_count}

### Epic Summary:
- [x] Project Scaffold (4/4 tasks)
- [x] Auth System (3/3 tasks)
- [x] Workspace System (3/3 tasks)
- [x] Project System (3/3 tasks)

### Next Steps:
1. Review the generated code
2. Run the full test suite: `npm test`
3. Start the dev server: `npm run dev`
4. Consider P1/P2 features for the next phase
```

### 3.3 Suggest Next Actions

- Manual code review
- End-to-end testing
- Deployment setup
- P1 feature planning (re-run decomposition for P1 features)

## Timing Expectations

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1 (Init) | 3-5 min | Read 9 docs + create DAG + first sprint |
| Phase 2 (Sprint) | 5-15 min | Depends on task complexity |
| Phase 2b (Recovery) | 1-3 min | Check worktrees + reset |
| Phase 3 (Complete) | < 1 min | Stats and report |

A typical MVP with 15-20 tasks takes 6-8 sprint invocations.

## Error Handling

| Error | Response |
|-------|----------|
| Research dir missing | Clear message: "Run `/clone-research {slug}` first" |
| `bd` not installed | Instruct user to install beads: `npm install -g @beads/bd` |
| Agent crashes | Leave task in_progress; Phase 2b recovery on next invocation |
| All agents fail | Report failures; user can retry or investigate |
| Merge slot stuck | `bd merge-slot release` + retry |
| Dependency cycle | `bd swarm validate` catches this at DAG creation time |

## Orchestrator State

The orchestrator is **stateless** — all state lives in beads (`.beads/` directory)
and git (worktrees, branches). This means:

- Any Claude Code session can run `/clone-sprint`
- No orchestrator-specific state files needed
- Crash recovery is automatic via beads task states
- Multiple users can run sprints (beads handles concurrency)
