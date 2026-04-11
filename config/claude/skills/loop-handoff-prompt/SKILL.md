---
name: loop-handoff-prompt
description: Drives a /loop through a handoff-style task queue, executing one task per tick and judging idempotently whether each is already done before acting. State lives in the conversation itself (no sidecar file). Use when running recurring task execution, processing a handoff checklist, or resuming work from a previous session. Keywords loop handoff task queue idempotent resume next steps
disable-model-invocation: true
---

# Loop Handoff Prompt

Drives a loop that iterates through a handoff-style task list, one task per tick, skipping completed work via LLM judgment rather than marker files or a sidecar accumulator.

**Typical invocation:**

```
/loop /loop-handoff-prompt              # dynamic pacing
/loop 10m /loop-handoff-prompt          # fixed interval
```

State lives in the conversation itself. Each tick appends its result so the next tick sees what's already done. No files on disk.

## Per-tick workflow

Copy this checklist at the top of each response and tick items as you complete them:

```
- [ ] 1. Locate or generate the handoff prompt
- [ ] 2. Select the next pending task
- [ ] 3. Verify idempotently (is it already done?)
- [ ] 4. Skip or execute
- [ ] 5. Report the delta
- [ ] 6. Decide continuation
```

### 1. Locate or generate the handoff prompt

Scan the current conversation for a prior block fenced with `=== HANDOFF ===` / `=== END HANDOFF ===`.

- **Found** → reuse it. Do not regenerate, do not rewrite prior decisions.
- **Not found** (first tick) → synthesize a handoff from current session state using the structure below. Emit it inline as a chat message. The `Next Steps` section MUST be a numbered list of concrete, verifiable tasks — this is the queue.

### 2. Select the next pending task

Each Next Steps item is either:

- `- [ ] <task>` — pending
- `- [x] <task>` — done (executed or skipped in a prior tick)

Pick the first `- [ ]` item. If every item is `- [x]`, jump to step 6.

### 3. Verify idempotently (LLM judgment)

Before executing, check whether the task's stated outcome is **already present**. Use whichever signals fit the task:

- Grep for mentioned symbols, files, flags, or test names
- Read the file the task would touch and check for the change
- `jj log` / `git log` for a commit that already landed it
- Run the test the task would add — if it exists and passes, done
- Check CLI output, lint status, or build artifacts where relevant

**Default to skepticism.** Only mark done when the evidence is concrete. "Probably done" is pending. "File exists but contents differ from the task description" is pending.

### 4. Skip or execute

- **Already done** → mark `- [x] <task> — already present (<one-line evidence>)` in the handoff block. Do not re-do the work.
- **Not done** → execute the task. Keep scope narrow: one task per tick. If the task is too large for a tick, do the smallest useful slice and append a follow-up item at the end of Next Steps (never reorder existing items).

### 5. Report the delta

One or two sentences. What was executed, what was skipped, what changed. Do not re-print the full handoff — only the tick's delta.

### 6. Decide continuation

- **Tasks remain** → the loop will fire again on its own cadence. Do nothing special.
- **All tasks done** → print a final summary, state that the queue is drained, and stop. In dynamic `/loop` mode, simply return without scheduling another wake-up. In fixed-interval mode, tell the user to cancel the loop.

## Handoff prompt template

When generating the handoff on the first tick, use this structure. Keep it short — long handoffs eat the context budget the actual work needs.

````
=== HANDOFF ===
## Context Summary
- Goal: <original request>
- Phase: <planning|implementation|testing|review>

## Next Steps
1. - [ ] <concrete task with verifiable outcome>
2. - [ ] <concrete task with verifiable outcome>
3. - [ ] <concrete task with verifiable outcome>

## Important context
- <key decision, constraint, or pattern>
- <key decision, constraint, or pattern>
=== END HANDOFF ===
````

**Writing good Next Steps:** each task should name the file, symbol, or observable outcome so the idempotency check has something to grep for. Vague tasks ("clean up auth") break the whole pattern — rewrite them into concrete slices ("remove unused `legacyAuthMiddleware` from `src/auth/index.ts`") before committing to the queue.

## Guardrails

- **One task per tick.** The loop is the chaining mechanism — resist doing two.
- **Never delete or reorder tasks** you didn't add. Only mark them `[x]` or append new ones.
- **Destructive actions pause the loop.** If a task involves deleting files, force-pushing, dropping data, or touching shared systems, surface it to the user and wait — do not execute silently.
- **Stale handoff → stop.** If the user pivoted or the code shifted enough that queued tasks no longer make sense, stop and ask rather than grinding through obsolete work.
- **Compaction caveat.** Because state lives in the conversation, a context compaction can lose the handoff block. If step 1 finds no block but the conversation clearly has prior work, reconstruct the Next Steps from what remains rather than starting from scratch.

## Related

- `~/.claude/commands/handoff.md` — the non-loop handoff command this skill is modeled on
- `loop-work` skill — sidecar-file alternative: JSON state via `state.py`, initialized by `/loop-plan`, strict scope caps, no LLM-judgment idempotency. Use it when you need cross-session durability or survivable state across compaction; use `loop-handoff-prompt` when you want zero setup and judgment-based skipping
- `claude-code-best-practices/references/loop-patterns.md` — accumulator pattern deep-dive
