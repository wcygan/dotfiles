---
title: Loop Patterns & Stateful Automation
canonical_url: https://code.claude.com/docs/en/scheduled-tasks
fetch_before_acting: true
---

# Loop Patterns & Stateful Automation

> Before designing loop workflows, WebFetch https://code.claude.com/docs/en/scheduled-tasks for the latest.

## The Core Insight

A loop isn't "run the same thing again." A loop that **accumulates state** across iterations is fundamentally more powerful — each iteration builds on what previous iterations discovered. The key technique is combining loops with **dynamic context injection** (`!` backtick) and **accumulator files** so each iteration knows what came before.

## Loop Archetypes

### 1. Silent Accumulator

Writes findings to a file without interrupting the user. You read the output when ready.

```
/loop 10m /refactor-scanner
```

The skill writes to an accumulator file each iteration. The user reads it on their own schedule. Zero interruption cost, maximum value accumulation.

**Best for**: codebase audits, tech debt scanning, pattern analysis, standup draft building, weekly review compilation.

### 2. Polling Watcher

Checks for a state change and acts when detected.

```
/loop 5m /build-nurse
```

Each iteration checks a condition (CI status, new PR comments, merge conflicts). Takes action only when the state changes. Most iterations are cheap no-ops.

**Best for**: CI monitoring, PR babysitting, deploy watching, dependency alert triage.

### 3. Incremental Explorer

Explores a large space across multiple iterations, tracking coverage to avoid re-exploring.

```
/loop 10m /code-quality-loop
```

Each iteration picks an unexplored area, analyzes it, records findings AND coverage. The exploration set shrinks over time until done.

**Best for**: codebase-wide audits, refactoring discovery, test coverage gap analysis, documentation drift detection.

### 4. Session-Boundary (Non-Loop)

Fires once at session start or end via hooks, not `/loop`. Included here because it fills the same "periodic context" role.

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "cat /tmp/.my-accumulator-$(basename $(pwd)).md 2>/dev/null"
      }]
    }]
  }
}
```

**Best for**: context resumption ("here's where you left off"), re-injecting state from a previous session's accumulator.

## The Accumulator Pattern (Deep Dive)

The most powerful loop technique. Three components work together:

### Component 1: Accumulator File

A structured file that persists across iterations. The loop reads it at the start and appends to it at the end.

```
/tmp/.loop-state-{skill}-{repo}.md
```

Use `/tmp/` for session-scoped state or a project-local path for cross-session persistence.

**Example accumulator structure:**

```markdown
# Refactor Scanner Findings
## Metadata
- Last run: 2026-03-30T14:30:00
- Files scanned: 47/120
- Iteration: 5

## Findings
- [ ] src/auth/login.ts:42 — inconsistent error handling (uses throw where siblings use Result)
- [ ] src/api/users.ts:15 — N+1 query pattern in getUsersWithRoles()
- [x] src/utils/parse.ts:88 — already addressed in commit abc123

## Explored (do not re-scan)
- src/auth/
- src/api/users.ts
- src/api/posts.ts
- src/utils/parse.ts
```

### Component 2: Dynamic Context Injection

Use `!` backtick in the SKILL.md to read the accumulator BEFORE Claude sees the prompt:

```yaml
---
name: refactor-scanner
description: Incrementally scans codebase for refactoring opportunities
disable-model-invocation: true
---

# Refactor Scanner

## Previous findings (do not re-discover these)
!`cat /tmp/.loop-state-refactor-scanner-$(basename $(pwd)).md 2>/dev/null || echo "No previous state — first iteration."`

## Your task
1. Read the "Explored" list above — skip those files/directories
2. Pick the next unexplored directory or file group
3. Analyze for: naming inconsistencies, missing error handling, pattern violations, N+1 queries, dead code
4. Append NEW findings to /tmp/.loop-state-refactor-scanner-$(basename $(pwd)).md
5. Update the "Explored" list and metadata
6. Report only what's new this iteration (keep output brief)
```

This creates a feedback loop: each iteration sees all prior findings and knows what's already covered.

### Component 3: Helper Scripts for Structured I/O

For complex state management, use a script instead of inline shell commands. Bundle it with the skill or use UV/Python for richer logic.

**Bash helper** (`scripts/accumulator.sh`):

```bash
#!/bin/bash
# Usage: accumulator.sh <skill-name> <action> [args...]
# Actions: read, append, mark-explored, summary, reset

SKILL="$1"
ACTION="$2"
REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
STATE_FILE="/tmp/.loop-state-${SKILL}-${REPO}.md"

case "$ACTION" in
  read)
    cat "$STATE_FILE" 2>/dev/null || echo "# ${SKILL} — First Run"
    ;;
  append)
    shift 2
    echo "- [ ] $*" >> "$STATE_FILE"
    ;;
  mark-explored)
    shift 2
    echo "$*" >> "$STATE_FILE.explored"
    ;;
  get-unexplored)
    # List directories not yet explored
    EXPLORED="$STATE_FILE.explored"
    if [ -f "$EXPLORED" ]; then
      find src/ -type d -maxdepth 2 | grep -v -F -f "$EXPLORED"
    else
      find src/ -type d -maxdepth 2
    fi | head -3
    ;;
  summary)
    TOTAL=$(grep -c '^\- \[' "$STATE_FILE" 2>/dev/null || echo 0)
    OPEN=$(grep -c '^\- \[ \]' "$STATE_FILE" 2>/dev/null || echo 0)
    EXPLORED=$(wc -l < "$STATE_FILE.explored" 2>/dev/null || echo 0)
    echo "Findings: $TOTAL ($OPEN open) | Explored: $EXPLORED paths"
    ;;
  reset)
    rm -f "$STATE_FILE" "$STATE_FILE.explored"
    echo "State cleared."
    ;;
esac
```

**UV/Python helper** for richer logic (`scripts/accumulator.py`):

```python
#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///

"""Structured accumulator for loop skills.

Usage:
  accumulator.py read <skill>
  accumulator.py append <skill> <finding>
  accumulator.py next-target <skill>
  accumulator.py stats <skill>
"""

import json, sys, os, hashlib
from pathlib import Path
from datetime import datetime

def state_path(skill: str) -> Path:
    repo = Path(os.popen("git rev-parse --show-toplevel 2>/dev/null").read().strip() or ".").name
    return Path(f"/tmp/.loop-state-{skill}-{repo}.json")

def load(skill: str) -> dict:
    p = state_path(skill)
    if p.exists():
        return json.loads(p.read_text())
    return {"findings": [], "explored": [], "iteration": 0, "created": datetime.now().isoformat()}

def save(skill: str, state: dict):
    state["updated"] = datetime.now().isoformat()
    state_path(skill).write_text(json.dumps(state, indent=2))

def main():
    action, skill = sys.argv[1], sys.argv[2]
    state = load(skill)

    if action == "read":
        # Format state for injection into skill context
        if not state["findings"]:
            print("No previous state — first iteration.")
        else:
            print(f"## Iteration {state['iteration']} | {len(state['findings'])} findings")
            print(f"\n### Already explored (skip these):")
            for p in state["explored"]:
                print(f"- {p}")
            print(f"\n### Findings so far:")
            for f in state["findings"]:
                status = "x" if f.get("resolved") else " "
                print(f"- [{status}] {f['location']}: {f['description']}")

    elif action == "append":
        finding = {"location": sys.argv[3], "description": " ".join(sys.argv[4:]),
                   "iteration": state["iteration"], "resolved": False}
        # Deduplicate by location
        if not any(f["location"] == finding["location"] for f in state["findings"]):
            state["findings"].append(finding)
        save(skill, state)

    elif action == "next-target":
        # Find directories not yet explored
        import subprocess
        all_dirs = subprocess.run(["find", "src/", "-type", "d", "-maxdepth", "2"],
                                 capture_output=True, text=True).stdout.strip().split("\n")
        unexplored = [d for d in all_dirs if d and d not in state["explored"]]
        if unexplored:
            print(unexplored[0])
        else:
            print("DONE — all directories explored")

    elif action == "mark-explored":
        path = sys.argv[3]
        if path not in state["explored"]:
            state["explored"].append(path)
        state["iteration"] += 1
        save(skill, state)

    elif action == "stats":
        total = len(state["findings"])
        open_count = sum(1 for f in state["findings"] if not f.get("resolved"))
        print(f"Iteration: {state['iteration']} | Findings: {total} ({open_count} open) | Explored: {len(state['explored'])} paths")

if __name__ == "__main__":
    main()
```

**Wire it into a skill via dynamic context injection:**

```yaml
---
name: refactor-scanner
disable-model-invocation: true
---

## Previous State
!`uv run ${CLAUDE_SKILL_DIR}/scripts/accumulator.py read refactor-scanner`

## Next Target
!`uv run ${CLAUDE_SKILL_DIR}/scripts/accumulator.py next-target refactor-scanner`

## Instructions
1. If "DONE" above, report summary and stop
2. Read the files in the target directory
3. Compare against patterns in sibling directories
4. For each finding, run: Bash uv run ${CLAUDE_SKILL_DIR}/scripts/accumulator.py append refactor-scanner "file:line" "description"
5. Mark explored: Bash uv run ${CLAUDE_SKILL_DIR}/scripts/accumulator.py mark-explored refactor-scanner "path"
6. Brief report of this iteration's new findings only
```

## Combining Loops with Hooks

Hooks add deterministic behavior around loop iterations:

### Inject accumulator state after compaction

When context compresses, re-inject the accumulator so Claude doesn't lose track:

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo '## Loop State Reminder:' && cat /tmp/.loop-state-*.md 2>/dev/null"
      }]
    }]
  }
}
```

### Cross-session state persistence

Use a `SessionEnd` hook to copy accumulator state somewhere durable, and a `SessionStart` hook to restore it:

```json
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "cp /tmp/.loop-state-*.md ~/.claude/loop-state/ 2>/dev/null; exit 0"
      }]
    }],
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "cp ~/.claude/loop-state/*.md /tmp/ 2>/dev/null; exit 0"
      }]
    }]
  }
}
```

### Stop hook to keep iterating

Ensure the loop skill doesn't stop prematurely:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Check the accumulator: are there still unexplored targets? If so, respond {\"ok\": false, \"reason\": \"Continue to next target.\"}."
      }]
    }]
  }
}
```

## Design Principles

### Loop efficiency

- **Short-circuit early**: if nothing changed since last iteration, report briefly and stop. Don't re-analyze the same diff.
- **Budget context for the work, not the instructions**: keep SKILL.md under 150 lines. The accumulator provides the context; the skill provides the decision framework.
- **Diff-oriented, not full-scan**: each iteration processes the delta, not the whole codebase.

### Accumulator hygiene

- **Deduplication**: always check before appending (by file:line or content hash)
- **Mark resolved items**: don't delete findings — mark them `[x]` so the loop knows not to re-report them
- **Expiration**: old accumulators from other branches/repos should age out. Use `/tmp/` for auto-cleanup or add timestamps.
- **Structured formats**: JSON (for script consumption) or markdown (for human readability). Pick one per skill.

### Guardrails for looped skills

- **Action limits**: max N writes/pushes/issues per iteration (hard cap in the SKILL.md)
- **Human gate on destructive actions**: loops suggest, humans confirm
- **Dry-run default**: new loops should log what they WOULD do before going live
- **Cost awareness**: a 5m loop runs 96 times in 8 hours. Keep each iteration cheap by short-circuiting when idle.

## Example Patterns

### Codebase refactoring scanner

```
/loop 10m /refactor-scanner
```

Incrementally explores directories, records findings in accumulator, skips already-explored areas. After full coverage, produces a prioritized refactoring plan.

### Standup draft builder

```
/loop 1h /standup-builder
```

Each hour, appends new git commits and PR activity to `~/standup-draft.md`. By morning, the draft is ready to polish.

### PR review quality tracker

```
/loop 30m /review-quality
```

Scans open PRs for review comment quality — are comments actionable? Are questions answered? Accumulates a "review health" score over time.

### Tech debt inventory

```
/loop 15m /debt-inventory
```

Reads code complexity metrics, TODO comments, and suppressed lint rules. Builds a prioritized tech debt inventory in the accumulator. Reads the inventory on each iteration to avoid duplicates.
