---
name: context-repo-execute
description: >
  Work a context-repo plan step by step. Reads
  context/specs/<slug>/plan.md, executes tasks in order on a feature
  branch with checkpoints, runs tests between steps, appends progress to
  memory/notes.md, and deletes the plan from plans/active when complete.
  Use when a plan exists and you want to start (or resume) execution.
  Keywords: execute plan, work the plan, context repo execute, resume plan
disable-model-invocation: true
argument-hint: <feature-slug>
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# /context-repo-execute

Work a `context/specs/<slug>/plan.md` step by step.

**Slug**: `$ARGUMENTS`. If missing, list plans in `context/plans/active/`
and ask which one.

Read `../context-repo/references/structure.md` for file conventions.

## Preconditions (verify before starting)

1. Cwd is inside a git repo. `context/` resolves as
   `$(git rev-parse --show-toplevel)/context`.
2. `context/specs/<slug>/plan.md` exists.
3. The plan has **zero open questions** in its "Open questions (must
   resolve before execution)" section. If any remain, stop and tell the
   user to resolve them first.
4. The working tree is **clean** (no uncommitted changes). If dirty, stop
   and tell the user. Do not auto-stash.
5. If `repos.toml` exists, every area named in the plan maps to a listed
   project (or to a directory inside one).

## Workflow

### 1. Load the plan

Parse the task list from `plan.md`. Each task has: area, files, change,
verify command, owner, depends-on, rollback. All paths are relative to
the repo root.

### 2. Create (or resume on) the feature branch

- Branch name: `<slug>` (e.g., `feat/<slug>` if that's the repo convention
  — confirm with the user on first run).
- If the branch doesn't exist, create it from the current branch.
- If it exists and HEAD is ahead of its base, this is a resume. Read
  `memory/notes.md` to find the last completed task and continue from the
  next one after confirming with the user.

### 3. Append starting entry to memory

Append a dated entry to `context/memory/notes.md`:

```markdown
## YYYY-MM-DD HH:MM — Executing <slug>
Starting plan with N tasks on branch <branch>.
```

Never edit prior entries.

### 4. Execute tasks in dependency order

For each task, in order:

1. **Announce**: print the task number, area, title.
2. **Delegate the work.** If `/incremental-execution` is available, use it
   for the actual code change. Otherwise:
   - Read the files named in the task
   - Make the minimal change to satisfy the task
   - Keep the diff small and focused
3. **Verify**: run the task's `verify` command. If it fails:
   - Stop the entire execution
   - Do NOT revert; leave the state for the user to inspect
   - Print the failure and the task number
   - Append failure note to `memory/notes.md`
4. **Commit** with a message referencing the slug:
   `<slug>: <task title>`. Do not push.
5. **Confirm with user** before proceeding to the next task: "Task N
   complete and verified. Continue to task N+1?" (Allow batching only if
   the user explicitly says "run all remaining".)
6. **Append progress** to `memory/notes.md` after each successful task.

### 5. On failure

- Leave all commits and the working tree in place.
- Write a detailed failure note to `memory/notes.md` including: task number,
  command that failed, last 20 lines of output, suggested next action.
- Tell the user how to resume: "Fix the issue, then run
  `/context-repo-execute <slug>` again — I'll pick up from task N."
- Do not auto-retry.

### 6. On completion

When every task verified green:
- Append completion note to `memory/notes.md`
- Delete `context/plans/active/<slug>.md` (the canonical plan remains in
  `context/specs/<slug>/plan.md`)
- Tell the user: the feature branch is ready to push and PR. Do NOT auto-push.
- Suggest next step: "Review the branch diff, push, and open a PR. Consider
  `/context-repo-adr new` if this work introduced a decision worth recording."

### 7. Resume behavior

If the skill is re-invoked for a slug mid-execution:
- Re-read the plan and `memory/notes.md`
- Find the highest completed task number from memory
- Verify HEAD is at the expected commit (message references that task)
- Resume from the next task after confirming with the user

## Hard rules

- **Never push** automatically. The user owns the push/PR step.
- **Never modify files outside the areas listed in the plan.** If
  `repos.toml` exists, the areas must be listed projects or subdirectories
  of them.
- **Never skip the verify command.** If it's missing from a task, stop
  and ask the user to add one.
- **Never auto-revert on failure.** Failed state is diagnostic gold.
- **Never edit prior entries in `memory/notes.md`.** Append-only.
- **Never run `git push --force`.** Ever.
- **Never switch away from the feature branch** mid-execution.
- All paths are relative to the repo root. No `../`, no absolutes.
- Stop at the first failure. Humans decide whether to continue.

## References

- [`../context-repo/references/structure.md`](../context-repo/references/structure.md) — `plan.md` format (task schema, verify commands), the append-only rules for `memory/notes.md`, the delete-on-merge rule for `plans/active/`.
- [`../context-repo/references/workflow.md`](../context-repo/references/workflow.md) — `execute` sits at the end of the feature-ship chain; see "Resume interrupted execution" for re-invocation behavior.

## Related skills

| Direction | Skill | Why |
|-----------|-------|-----|
| **Prerequisite** | `/context-repo-plan <slug>` | Refuses to run without a plan. All "must-resolve" open questions must be closed first. |
| **Delegates to** | `/incremental-execution` | Per-task execution (TDD loop, small commits) when available |
| **Follow-up** | `/context-repo-adr new` | Record decisions that emerged during execution (often — "we tried X and it didn't work, so...") |
| Follow-up | `/create-pr` | The feature branch needs a PR after execution. Never auto-opened. |
| On failure | `/debug` | General-purpose debugger for the failing verify command |
| After completion | `/context-repo-refresh` | Execution often invalidates arch maps — run next time you map |

On successful completion, tell the user: (1) the branch is ready to push,
(2) consider `/context-repo-adr new` if decisions emerged, (3) the plan
has been removed from `plans/active/`.
