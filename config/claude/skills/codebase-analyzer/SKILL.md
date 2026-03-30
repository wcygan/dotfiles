---
name: codebase-analyzer
description: >
  Iteratively analyze a codebase for improvement opportunities using the accumulator
  pattern. Each invocation explores unexplored directories, records findings, and
  tracks progress. Designed for /loop. Uses agent sub-agents for parallel exploration.
  Keywords: analyze, improve, refactor, code quality, tech debt, audit, review codebase
disable-model-invocation: true
---

# Codebase Improvement Analyzer

Incrementally explores a codebase across loop iterations, accumulating findings
in `/tmp/{repo-name}/improvement-analysis.json`. Each iteration picks unexplored
areas, analyzes them, and records what it finds — so the next iteration knows
what's been covered and what's been found.

## Accumulator State
!`uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py read 2>/dev/null || echo "Status: uninitialized"`

## Next Targets
!`uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py next-targets 2>/dev/null || echo "Run init first"`

## Progress
!`uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py stats 2>/dev/null || echo "Not started"`

---

## Instructions

### If status is "uninitialized" or "corrupted"

Initialize the accumulator:
```bash
uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py init
```
Then proceed to the Explore phase below.

### If status is "in_progress" — Explore Phase

1. **Read the state above.** Note which directories are explored (skip them) and
   which findings already exist (do not re-discover them).

2. **Read the Next Targets.** These are 2-3 unexplored directories sorted by priority.

3. **Spawn 2-3 parallel sub-agents** (one per target directory) using the Agent tool:

   For each target directory, spawn an Explore agent with this prompt:
   ```
   Analyze the directory "{directory}" in this repository for code improvement opportunities.

   Use Glob to list files, Read to examine code, Grep to search for patterns.

   Look for these categories (focus on the most impactful):
   - error-handling-gap: Missing error checks, bare catch blocks, ignored returns
   - pattern-violation: Code that does things differently from sibling files
   - naming-inconsistency: Mixed conventions within the same module
   - missing-test: Public functions/methods with no test coverage
   - security-concern: Hardcoded secrets, SQL concatenation, missing validation
   - performance-issue: N+1 queries, unbounded loops with I/O, missing pagination
   - dead-code: Unused exports, commented-out blocks, unreachable branches
   - tech-debt: TODO/FIXME comments, deprecated API usage, duplicated logic

   IMPORTANT: Compare new code against patterns in SIBLING files in the same
   directory. Flag deviations from established patterns, not generic best practices.

   Return findings as a structured list. For each finding include:
   - file path (relative to repo root)
   - line number (if applicable)
   - category (from list above)
   - severity (critical/high/medium/low)
   - description (2-3 sentences, specific and actionable)

   Limit to the 5-8 most impactful findings. Skip trivial style nits.
   ```

4. **Record each finding** from the agent results:
   ```bash
   uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py record-finding \
     --file "path/to/file.ts" --line 42 \
     --category "error-handling-gap" --severity "medium" \
     --desc "HTTP response status not checked before JSON parsing"
   ```

5. **Mark each directory explored:**
   ```bash
   uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py mark-explored "src/utils"
   ```

6. **Print brief status** of what was found this iteration. Keep output concise —
   just new findings and progress.

### If next-targets returns "DONE" or findings exceed 50

Transition to Report phase:
```bash
uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py report
```
Present the report organized by severity. Suggest which findings to address first.

## Stopping Conditions

Stop the loop when ANY of these are true:
- All directories explored (next-targets returns "DONE")
- 50+ findings accumulated (enough to act on)
- User interrupts

Always run the report command before stopping.

## Reset

To start fresh on the same repo:
```bash
uv run --quiet --script ${CLAUDE_SKILL_DIR}/scripts/analyzer.py init --force
```

## Design Notes

- State lives outside the repo (`/tmp/`) — never pollutes git
- Atomic writes prevent corruption on interrupt
- Deduplication by content hash prevents repeat findings across iterations
- Priority scoring explores source-heavy directories first
- Sub-agents (not agent teams) for parallelism — lighter, well-supported
- Each iteration should take 2-5 minutes; a typical repo finishes in 3-8 iterations
