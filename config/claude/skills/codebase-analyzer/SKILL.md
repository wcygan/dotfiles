---
name: codebase-analyzer
description: >
  Iteratively analyze a codebase for improvement opportunities using the accumulator
  pattern. Each invocation explores unexplored directories, records findings, and
  tracks progress. Designed for /loop with parallel sub-agent exploration.
  Use when auditing code quality, finding tech debt, or reviewing an unfamiliar codebase.
  Keywords: analyze, improve, refactor, code quality, tech debt, audit, review codebase,
  code review, patterns, dead code, security, performance
disable-model-invocation: true
argument-hint: [target-directory]
---

# Codebase Improvement Analyzer

Incrementally explores a codebase across loop iterations, accumulating findings
in `/tmp/{repo-name}/improvement-analysis.json`. Each iteration picks unexplored
areas, analyzes them, and records what it finds — so the next iteration knows
what's been covered and what's been found.

## Script Path
!`echo "${CLAUDE_SKILL_DIR}/scripts/analyzer.py"`

## Accumulator State
!`uv run --quiet --script "${CLAUDE_SKILL_DIR}/scripts/analyzer.py" read 2>/dev/null || echo "Status: uninitialized"`

## Next Targets
!`uv run --quiet --script "${CLAUDE_SKILL_DIR}/scripts/analyzer.py" next-targets 2>/dev/null || echo "Run init first"`

## Progress
!`uv run --quiet --script "${CLAUDE_SKILL_DIR}/scripts/analyzer.py" stats 2>/dev/null || echo "Not started"`

---

## Instructions

Use the **Script Path** above for all analyzer commands. Refer to it as `ANALYZER` below.

### If status is "uninitialized" or "corrupted"

Initialize: run `uv run --quiet --script ANALYZER init`
(If `$ARGUMENTS` specifies a target directory, note it for focused exploration.)
Then proceed to the Explore phase.

### If status is "in_progress" — Explore Phase

1. **Read the state above.** Skip explored directories. Do not re-discover listed findings.

2. **Read the Next Targets.** These are 2-3 unexplored directories sorted by priority.

3. **Spawn 2-3 parallel sub-agents** (one per target) using the Agent tool with
   `subagent_type: Explore`. Each agent gets ONE directory and this prompt:

   > Analyze "{directory}" for code improvement opportunities.
   > Use Glob, Read, Grep. Compare against patterns in sibling files.
   > Categories: error-handling-gap, pattern-violation, naming-inconsistency,
   > missing-test, security-concern, performance-issue, dead-code, tech-debt.
   > Flag deviations from established patterns, not generic advice.
   > Return: file path, line number, category, severity, description (2-3 sentences).
   > Limit to 5-8 most impactful findings. Skip trivial style nits.

4. **Record findings:** for each, run:
   `uv run --quiet --script ANALYZER record-finding --file "path" --line N --category "cat" --severity "sev" --desc "description"`

5. **Mark explored:** `uv run --quiet --script ANALYZER mark-explored "dir"`

6. **Brief status** — only report new findings and progress this iteration.

### If next-targets returns "DONE" or findings exceed 50

Run `uv run --quiet --script ANALYZER report` and present results by severity.

## Stopping Conditions

- All directories explored (next-targets returns "DONE")
- 50+ findings accumulated
- User interrupts

Always generate the report before stopping.

## Reset

Run `uv run --quiet --script ANALYZER init --force` to start fresh.
