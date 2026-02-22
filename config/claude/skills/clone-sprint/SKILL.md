---
name: clone-sprint
description: >
  Sprint-scoped MVP builder that consumes clone-research output. Decomposes research into a
  beads task DAG (epics per bounded context, subtasks per feature slice), spawns worktree-isolated
  builder agents in batches of 2-3, merges via bd merge-slot, and reports progress. Idempotent:
  first invocation creates the DAG; subsequent invocations run the next sprint via bd ready.
  Keywords: clone, build, sprint, MVP, beads, worktree, parallel, task DAG, feature slice
context: fork
disable-model-invocation: true
argument-hint: <slug>
---

# clone-sprint

Sprint-scoped MVP builder. Consumes `clone-research/{slug}/` output, decomposes into a beads
task DAG, and executes one sprint per invocation.

## Prerequisites

1. **Research output must exist:** `clone-research/$ARGUMENTS/` with 9 standardized docs
2. **Beads CLI installed:** `bd` must be on PATH
3. **Git repo initialized:** working directory must be a git repository

If research is missing, tell the user to run `/clone-research $ARGUMENTS` first.
If `bd` is not installed, instruct: `npm install -g @beads/bd`

## Execution Mode

Detect state and execute the appropriate phase:

| State | Phase | Action |
|-------|-------|--------|
| No `clone-research/{slug}/` | **Error** | Abort — research required |
| Research exists, no `.beads/` | **Phase 1** | Initialize DAG + first sprint |
| `.beads/` exists, `bd ready` has tasks | **Phase 2** | Execute next sprint |
| `.beads/` exists, only in_progress tasks | **Phase 2b** | Recovery — reset orphaned tasks |
| `.beads/` exists, all tasks closed | **Phase 3** | Final completion report |

References: [workflow.md](references/workflow.md)

## Research Contract

Clone-sprint expects clone-research output in a specific format. If these change,
both skills must be updated together.

| Doc | Required Sections |
|-----|------------------|
| `00-INDEX.md` | Executive Summary, Cross-Reference Map (optional Known Gaps) |
| `02-feature-priority-matrix.md` | Feature Inventory table with columns: ID, Feature, Priority (`P0`-`P3`), Effort (`S`/`M`/`L`/`XL`) |
| `03-mvp-scope-contract.md` | In Scope table with Acceptance Criteria column |
| `04-core-user-journeys.md` | Journey tables with Step/Action/Screen columns |
| `05-domain-model.md` | **REQUIRED.** Bounded Contexts table with Context/Entities/Responsibility columns |
| `06-system-architecture.md` | Recommended Clone Architecture tables (Frontend, Backend, Infrastructure) |
| `08-api-surface-spec.md` | Resource Endpoints table with Method/Endpoint/Description/Feature columns |
| `09-design-system-brief.md` | Color Palette, Typography, Component Inventory tables |

Docs 01 and 07 provide context but have no strict structural requirements.

## Phase 1: Initialize & Decompose

**When:** First invocation — no `.beads/` directory exists.

1. **Verify research completeness** — read `00-INDEX.md`, check all docs exist, abort if doc 05 missing
2. **Read all available research docs** from `clone-research/$ARGUMENTS/`
3. **Initialize beads:** `bd init --quiet`
3. **Create scaffold epic** (priority 1, labeled `scaffold`) with subtasks for project init, database, design system, CI
5. **Extract bounded contexts** from `05-domain-model.md` → create one epic per context
6. **Extract P0 features** from `02-feature-priority-matrix.md` → create subtasks grouped by context
7. **Build rich task descriptions** embedding entities (doc 05), API endpoints (doc 08),
   acceptance criteria (doc 03), design tokens (doc 09), suggested file targets (doc 06)
8. **Wire dependencies:** scaffold blocks all epics; follow entity relationships and user journeys
9. **Validate DAG:** `bd swarm validate` — check for cycles and compute parallelism
10. **Report DAG summary** to user (epic count, task count, estimated sprints)
11. **Immediately proceed to Phase 2** with ready scaffold tasks

References: [task-decomposition.md](references/task-decomposition.md), [beads-integration.md](references/beads-integration.md)

## Phase 2: Sprint Execution

**When:** `bd ready --json` returns tasks.

1. **Query ready tasks:** `bd ready --json`
2. **Select batch** (2-3 tasks):
   - Higher priority first
   - From different bounded contexts (minimize file overlap)
   - Check file targets for overlap — never assign overlapping tasks to same sprint
   - Hard limit: 3 agents maximum
3. **Claim tasks:** `bd update <id> --claim` for each selected task
4. **Determine agent type** per task from labels (fullstack/data/api/ui/infra)
5. **Compose agent prompts** with common preamble + type-specific instructions + task description
6. **Spawn all agents in ONE message** using Task tool:
   - `subagent_type: "general-purpose"`
   - `isolation: "worktree"`
   - All agents launched in parallel
7. **Wait for all agents to complete**
8. **Merge results serially** using `bd merge-slot`:
   - Order: data → API → fullstack → UI → infra
   - Tier 1: fast-forward (happy path)
   - Tier 2: rebase + retry (another agent merged first)
   - Tier 3: escalate to user (genuine conflict)
9. **Close merged tasks:** `bd close <id> --reason "Merged"`
10. **Report sprint results:**
    - Tasks merged vs failed
    - Overall progress (completed/total, percentage)
    - Ready tasks for next sprint
    - Estimated remaining sprints

References: [agent-roles.md](references/agent-roles.md), [merge-strategy.md](references/merge-strategy.md), [workflow.md](references/workflow.md)

## Phase 3: Completion

**When:** All tasks are closed (`bd ready` empty, no in_progress tasks).

1. **Run `bd stats --json`** for final statistics
2. **Present completion report:**
   - Total tasks and sprints used
   - Epic-by-epic summary (all checkmarks)
   - Merge conflict count
3. **Suggest next steps:**
   - Code review
   - Full test suite run
   - Dev server startup
   - P1/P2 feature planning

References: [workflow.md](references/workflow.md)

## Anti-Patterns

**DO NOT** decompose by horizontal layer (all migrations → all APIs → all UI).
Each task must be a vertical slice within one bounded context.

**DO NOT** create tasks with thin descriptions. Every task must embed entity
definitions, API specs, acceptance criteria, design tokens, and file targets.

**DO NOT** spawn more than 3 agents per sprint. Merge conflicts scale quadratically.

**DO NOT** skip `bd merge-slot`. Direct parallel merges cause race conditions.

**DO NOT** create more than ~30 tasks for an MVP. If you have more, combine
related features into broader slices.

**DO NOT** assign tasks from the same bounded context to the same sprint
unless they have zero file overlap.

## Example Invocations

```bash
# First run: creates DAG from research + runs scaffold sprint
/clone-sprint linear

# Subsequent runs: executes next sprint
/clone-sprint linear

# After all sprints complete: shows final report
/clone-sprint linear
```

Typical MVP: 15-20 tasks across 6-8 sprint invocations.
