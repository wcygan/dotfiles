---
disable-model-invocation: true
---

# Beads Assign

Pick up the next available bead (or a batch of related beads), claim it, implement the work, and close it. Operates as a focused work session against a beads task database.

## Workflow

### 1. Survey Available Work

```bash
bd ready --json
```

If no ready tasks, check for blocked work and report what's blocking progress:

```bash
bd list --status blocked --json
bd list --status open --json
```

### 2. Select Work

Choose what to work on using the selection strategy:

1. **Highest priority first** — P0 before P1 before P2
2. **Unblock others** — prefer tasks that `block` many downstream tasks
3. **Batch related work** — if multiple ready tasks share a label or parent epic, consider claiming them together
4. **Respect the graph** — never skip a blocking dependency

Present the selection to the user before claiming:

```
Ready to claim:
  [id] P[n] — Title
  Reason: [why this task was selected]
  Blocks: [what this unblocks when done]
```

If multiple related tasks are ready in parallel, propose a batch:

```
Batch (same epic / related):
  [id1] P[n] — Title A
  [id2] P[n] — Title B
  Reason: [why these go together]
```

Wait for user confirmation before claiming.

### 3. Claim the Work

```bash
bd update <id> --claim --json
```

For batches, claim all selected tasks:

```bash
bd update <id1> <id2> --claim --json
```

### 4. Understand the Task

Before writing any code, gather context:

- Read the bead's description, acceptance criteria, and design notes: `bd show <id> --json`
- If it has a `--spec-id`, read that spec file
- Check the parent epic for broader context: `bd dep tree <epic-id>`
- Read any related code files mentioned in the description
- Check for related beads with `bd list --label <shared-label> --json`

### 5. Execute the Work

Implement the task following the project's conventions:

1. **Write tests first** if the task involves code changes
2. **Implement the minimal solution** that satisfies acceptance criteria
3. **Run tests** — must pass before proceeding
4. **Format and lint** the code
5. **Commit atomically** with the bead ID in the commit message:
   ```
   git commit -m "Implement feature X (bd-abc)"
   ```

If the task is too large or reveals unexpected complexity:

- Create subtasks: `bd create "Discovered subtask" -p <priority> --deps discovered-from:<current-id> --json`
- Update the current bead's notes: `bd update <id> --design "Found additional complexity: ..." --json`
- Inform the user and propose a revised plan

### 6. Close the Bead

After the work passes all checks:

```bash
bd close <id> --reason "Implemented and tested — <brief summary>" --json
```

For batches, close each completed task individually with its own reason.

### 7. Report and Continue

After closing, present a summary:

```
Completed:
  [id] — Title
  Changes: [files modified, tests added]
  Commit: [hash]

Newly unblocked:
  [id] P[n] — Title (was blocked by completed task)
```

Then check for the next available work:

```bash
bd ready --json
```

Ask the user if they want to continue with the next task or stop.

### 8. Sync at Session End

If using Dolt backend:

```bash
bd sync
```

## Rules

- **Always confirm selection with the user** before claiming tasks.
- **Never use `bd edit`** — it opens an interactive editor. Use `bd update` with flags.
- **Always use `--json` flag** on bd commands.
- **Include bead ID in commit messages** — enables `bd doctor` cross-referencing.
- **Don't claim more than you can finish** — if a batch looks too large, split it.
- **Create discovery beads** for bugs or tasks found during work rather than scope-creeping the current task.
- **Run `bd sync`** at session end if using Dolt backend.

References: [work-selection](references/work-selection.md), [session-patterns](references/session-patterns.md)
