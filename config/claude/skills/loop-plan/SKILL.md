---
name: loop-plan
description: One-shot planner that decomposes a goal into a checklist and initializes JSON state for /loop-work to execute under /loop. Use when starting a stateful recurring task, audit, or incremental exploration. Keywords: loop plan, checklist, stateful loop, incremental audit, loop worker
disable-model-invocation: true
argument-hint: [goal description]
allowed-tools: Read, Grep, Glob, Bash
---

# Loop Plan

Decompose a goal into a deterministic checklist that `/loop-work` will execute one item per loop tick. State lives in `/tmp/.loop-state-<hash>.json` where `hash = sha256(repo_root + goal)[:12]`.

State tool (always the same absolute path — works regardless of invocation context):

```
$HOME/.claude/skills/loop-work/scripts/state.py
```

## Inputs

- **Goal**: `$ARGUMENTS` (the user's objective for the loop)

If `$ARGUMENTS` is empty, ask the user for the goal and stop.

## Workflow

### 1. Understand the goal

- Read just enough of the repo to decompose the goal concretely (Glob/Grep/Read). Do **not** start executing work here.
- If the goal is ambiguous, ask one clarifying question before proceeding.

### 2. Check for existing state

```bash
"$HOME/.claude/skills/loop-work/scripts/state.py" list
```

If a state already exists for this repo with a similar goal, surface it and ask: **reuse**, **reset** (`state.py reset`), or **create alongside** (different goal string → different hash).

### 3. Decompose into checklist items

Produce **5–20 items**. Each item must be:

- **Concrete and atomic** — completable in one loop tick (a few minutes of Claude work).
- **Self-contained** — readable without the goal statement; include file paths or scopes where applicable.
- **Ordered** — earlier items unblock later ones where dependencies exist.
- **Verifiable** — the worker should know when it's done.

Bad: `"improve error handling"`. Good: `"audit src/auth/*.ts for unchecked Result returns; list findings"`.

### 4. Initialize state

```bash
"$HOME/.claude/skills/loop-work/scripts/state.py" init "<goal>" "<item 1>" "<item 2>" ...
```

Prints the absolute state file path. Capture it.

### 5. Report and hand off

Output exactly:

1. The goal
2. The state file path
3. The full checklist (from `state.py read`)
4. Ready-to-paste command:

   ```
   /loop 10m /loop-work
   ```

   (adjust interval as needed: `5m`, `15m`, `1h`)

5. Reminder: the worker may append discovered items mid-loop but will not modify the goal.

## Notes

- The hash is deterministic — re-running `/loop-plan` with the same goal in the same repo fails loudly (by design). Use `state.py reset` first, or change the goal string.
- Housekeeping: `state.py cleanup --days 7` removes stale states repo-wide.
- Keep this skill planning-only. Do not execute any checklist items here.
