---
name: loop-work
description: Stateful loop worker. Reads JSON checklist state initialized by /loop-plan and executes the next pending item per tick. Designed to be invoked via /loop (e.g. `/loop 10m /loop-work`) or fired inline by the model for an immediate tick on an existing plan. Keywords: loop worker, stateful loop, checklist executor, incremental worker
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Loop Work

One tick of a stateful loop. State lives in `/tmp/.loop-state-<hash>.json` and is managed **only** through `state.py` — never edit the file directly.

State tool:

```
$HOME/.claude/skills/loop-work/scripts/state.py
```

## Current state
!`"$HOME/.claude/skills/loop-work/scripts/state.py" read 2>&1 || echo "NO_STATE"`

## Claimed item for this tick
!`"$HOME/.claude/skills/loop-work/scripts/state.py" next-item 2>&1 || echo "NO_STATE"`

## Instructions

Calling `next-item` above already **started the tick** and **claimed** the item (auto-atomic: bumps tick counter, reclaims any stale `in_progress` from crashed ticks, marks the returned item `in_progress`). You do **not** need to call `mark-progress`.

### Tool reference

```bash
state=$HOME/.claude/skills/loop-work/scripts/state.py
"$state" read                    # current state summary
"$state" mark-done <id>          # complete the claimed item
"$state" append-item "<text>"    # add a discovered follow-up (schema-safe, dedup)
"$state" stats                   # one-line summary
"$state" reset                   # delete state for current repo (manual cleanup)
```

### Tick workflow

1. **Short-circuit checks** (in order, before any work):
   - If "Claimed item" above starts with `DONE` → print `LOOP DONE: <goal>`, run `stats`, stop. Do nothing else.
   - If "Current state" contains `NO_STATE` → print an error telling the user to run `/loop-plan <goal>` first, stop.

2. **Execute exactly the claimed item.** Stay strictly in scope:
   - Do not work ahead on other items.
   - Hard cap: ~5 file edits and 0 commits per tick unless the item explicitly authorizes more.
   - No destructive operations without an explicit item authorizing them.

3. **Record discoveries** (optional): if the work reveals concrete follow-up tasks within the goal, append each with `state.py append-item "<text>"`. Items must be atomic and concrete — no speculation, no meta-items.

4. **Complete** the item: `state.py mark-done <id>`.

5. **Report** — terse, 3–6 lines:
   - Item id + text
   - What was actually done (files touched, findings)
   - Any items appended this tick
   - `state.py stats` output

### Rules

- **Never modify the goal.** Fixed at plan time.
- **Never edit the JSON state file directly.** Always go through `state.py`.
- **Never call `next-item` again in the same tick.** It would claim a second item and double-count the tick.
- **Stay idempotent.** If the tick crashes mid-work, the item stays `in_progress`; it will be auto-reclaimed on the next tick after 30 minutes.
- **Be quiet on no-ops.** If there's nothing to do, one line is enough.
