---
name: autoresearch
description: >
  Iterates autonomously on a code quality metric — one change, verify, keep or revert, repeat.
  Use when optimizing test coverage, reducing lint errors, or improving benchmarks.
  Keywords: autoresearch, optimize, iterate, coverage, lint, benchmark, autonomous
disable-model-invocation: true
context: fork
effort: high
argument-hint: [goal] [max=N]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Autoresearch

Autonomous code quality improvement loop. ONE change per iteration, mechanical verification, keep or revert.

## Current project state

```
Git log: !`git log --oneline -5 2>/dev/null || echo '(no git history)'`
Project files: !`ls -1 package.json Cargo.toml go.mod pyproject.toml Makefile justfile 2>/dev/null || echo '(no recognized project files)'`
```

## Arguments

Parse `$ARGUMENTS`:
- **goal**: What to optimize (required)
- **max=N**: Iteration cap (default: 10)

If no goal provided, stop with an error.

## Protocol

Copy this checklist and update as you progress:

```
Autoresearch Progress:
- [ ] Phase 1: Discover (detect toolchain, metric command, verify command, baseline)
- [ ] Phase 2: Plan (rank improvement opportunities)
- [ ] Phase 3: Loop (iterate until done)
- [ ] Phase 4: Report (summary with kept/reverted changes)
```

### Phase 1: Discover

1. Detect build/test/lint toolchain from project files
2. Determine **metric command** (outputs a number) and **verify command** (exits 0 on pass)
3. Run both to establish baseline
4. If no mechanical metric is discoverable, explain why and stop

### Phase 2: Plan

1. Scan codebase for improvement opportunities relevant to the goal
2. Rank by expected impact (highest first)
3. Check git history to avoid repeating past attempts

### Phase 3: Loop

Each iteration:

1. Read git log and `.autoresearch-results.tsv` (learn from past iterations)
2. Read target code
3. Make ONE focused change
4. `git add -A && git commit -m "experiment: <description>"`
5. Run verify command
6. Run metric command
7. Compare to best value — improved? Keep. Worse or same? `git revert HEAD --no-edit`
8. Append result to `.autoresearch-results.tsv`

References: [loop-protocol](references/loop-protocol.md), [error-recovery](references/error-recovery.md), [change-priorities](references/change-priorities.md)

**On verify failure:** attempt ONE quick fix. If it works, amend and continue. If not, revert.

**On 3 consecutive reverts:** stop (you're stuck).

### Phase 4: Report

```
## Autoresearch Results

**Goal**: <goal>
**Iterations**: <completed> / <max>
**Baseline**: <starting metric> → **Final**: <ending metric> (<delta>%)

### Changes Kept
- <hash>: <description> (+<delta>)

### Changes Reverted
- <description>: <reason>

### Next Run Suggestions
- <what to try next>
```

## Results log format

Tab-separated, one row per iteration in `.autoresearch-results.tsv`:

```
iteration	commit	metric_value	delta	status	description
```

Status values: `kept`, `reverted`, `crashed`, `stuck`

## Safety

- NEVER `git push`, modify CI/CD, or disable tests/lint to game a metric
- NEVER commit secrets or sensitive data
- If unsure whether a change is safe, skip it
