---
disable-model-invocation: true
---

# Beads Decompose

Decompose a product design into executable beads tasks with dependencies, priorities, and hierarchy. Reads design docs, specs, or descriptions and creates a structured task graph using the `bd` CLI.

## Workflow

### 1. Understand the Design

Read the input — a design doc, spec file, feature description, or user explanation. Identify:

- **Goals**: What the product/feature achieves
- **Components**: Distinct systems, services, or modules involved
- **User flows**: End-to-end paths through the feature
- **External dependencies**: APIs, databases, third-party services
- **Risks & unknowns**: Areas needing spikes or investigation

### 2. Verify Beads is Initialized

```bash
bd info --json
```

If not initialized, ask the user which mode to use:
- `bd init` — standard
- `bd init --stealth` — local-only, no repo commits
- `bd init --contributor` — separate planning repo

### 3. Decompose into Hierarchy

Break the design into a **3-level hierarchy**:

**Epics** (top-level deliverables):
- Each epic = one shippable slice of the product
- Should be independently valuable when complete
- Name with the outcome, not the activity (e.g., "User Authentication" not "Build auth")

**Tasks** (concrete work items under each epic):
- Each task = 1-4 hours of focused work for a single agent
- Must have clear acceptance criteria
- Should be testable/verifiable in isolation

**Subtasks** (optional, for complex tasks):
- Only create when a task has distinct sequential phases
- Each subtask = a single atomic operation

### 4. Map Dependencies

Identify blocking relationships between tasks:

- **Hard blocks** (`blocks`): Task B literally cannot start until Task A is done (e.g., DB schema before API endpoints)
- **Soft relationships** (`related`): Useful context but not blocking
- **Discovery links** (`discovered-from`): Bug or task found while working on another

Only use `blocks` for true sequential dependencies. Over-constraining the graph reduces parallelism.

### 5. Assign Priorities

Use the beads priority scale:

| Priority | Meaning | Use for |
|----------|---------|---------|
| P0 | Critical | Blockers, security, data loss risks |
| P1 | High | Core functionality, MVP path |
| P2 | Medium | Important but not blocking launch |
| P3 | Low | Nice-to-have, polish |
| P4 | Backlog | Future consideration |

### 6. Execute — Create Tasks in Beads

Create the full hierarchy using `bd` commands. Always use `--json` flag.

**Step-by-step execution order:**

1. Create epics first
2. Create tasks under each epic (using `--parent`)
3. Add dependencies between tasks (`bd dep add`)
4. Add labels for cross-cutting concerns (`bd label add`)
5. Verify the graph: `bd dep tree <epic-id>` for each epic
6. Show ready work: `bd ready --json`

### 7. Present the Plan

After creating all tasks, present a summary:

- Total epics, tasks, subtasks created
- Dependency graph visualization (`bd dep tree`)
- Suggested execution order (what's ready now)
- Identified risks or areas needing spike tasks
- Estimated parallel lanes (how many agents could work simultaneously)

## Output Format

For each created task, report:

```
[id] [type] P[n] — Title
  └─ depends on: [parent-ids]
  └─ blocks: [child-ids]
```

End with the full dependency tree and `bd ready` output.

## Rules

- **Never use `bd edit`** — it opens an interactive editor. Use `bd update` with flags instead.
- **Always use `--json` flag** on bd commands for parseable output.
- **Run `bd sync`** at the end if using Dolt backend.
- **Don't over-decompose** — if a task takes <30 min, it probably doesn't need subtasks.
- **Don't over-constrain** — only add `blocks` dependencies for true sequential requirements.
- **Label cross-cutting concerns** — use labels like `frontend`, `backend`, `database`, `api`, `testing` to enable filtering.

References: [cli-reference](references/cli-reference.md), [decomposition-patterns](references/decomposition-patterns.md)
