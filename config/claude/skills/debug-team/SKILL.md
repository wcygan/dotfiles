---
name: debug-team
description: Debug complex issues using an agent team with competing hypotheses. Spawns 3-5 investigators that actively challenge each other's theories and converge on the root cause. Use for tough bugs where the root cause is unclear. Keywords: debug team, competing hypotheses, root cause, investigation, multi-agent debug, hard bug, mystery bug
context: fork
disable-model-invocation: true
argument-hint: [symptom-description]
---

# Multi-Hypothesis Debug Team

Debug complex issues by spawning an agent team where investigators hold competing hypotheses, actively challenge each other, and converge on a root cause through structured debate.

## When to Use This vs /debug

- **/debug**: Single-agent or parallel sub-agents that report independently. Good for straightforward bugs.
- **/debug-team**: Full agent team with inter-agent messaging. Investigators actively debate, disprove each other's theories, and converge. Use when the root cause is genuinely unclear and multiple explanations are plausible.

## Prerequisites

Agent teams require this setting in settings.json:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Workflow

### 1. Parse the Symptom

The user provides a symptom description as `$ARGUMENTS`. Before spawning any agents, analyze the symptom yourself:

- Read relevant error messages, stack traces, or logs mentioned in the description
- Identify the affected area of the codebase (use Grep/Glob to locate relevant files)
- Note any environmental factors (timing, platform, configuration)

### 2. Generate Competing Hypotheses

Based on your analysis, formulate 3-5 distinct hypotheses that could explain the symptom. Good hypotheses:

- Are **mutually exclusive** or at least substantially different
- Cover different layers (data, logic, configuration, environment, timing)
- Range from obvious to non-obvious explanations

**Example hypothesis categories:**

| Category | Example |
|----------|---------|
| Data | "Corrupt or unexpected input data" |
| Logic | "Off-by-one or incorrect conditional" |
| State | "Race condition or stale cache" |
| Config | "Environment variable or config mismatch" |
| Dependency | "Breaking change in upstream library" |
| Integration | "API contract violation between services" |

### 3. Spawn the Agent Team

Create a team with one investigator per hypothesis plus a devils-advocate:

```
Create an agent team to debug: [symptom from $ARGUMENTS]

Hypotheses to investigate:
1. [Hypothesis A]: [brief description]
2. [Hypothesis B]: [brief description]
3. [Hypothesis C]: [brief description]

Team composition:
- investigator-1 (implementation-investigator): Investigate hypothesis A.
  Search for evidence in [suggested starting files/dirs].
  Try to PROVE this hypothesis AND actively DISPROVE other hypotheses.
  Share findings with other investigators via messaging.

- investigator-2 (implementation-investigator): Investigate hypothesis B.
  Search for evidence in [suggested starting files/dirs].
  Try to PROVE this hypothesis AND actively DISPROVE other hypotheses.
  Share findings with other investigators via messaging.

- investigator-3 (implementation-investigator): Investigate hypothesis C.
  Search for evidence in [suggested starting files/dirs].
  Try to PROVE this hypothesis AND actively DISPROVE other hypotheses.
  Share findings with other investigators via messaging.

- skeptic (devils-advocate): Challenge ALL theories.
  Monitor investigator findings. Point out confirmation bias.
  Suggest alternative explanations the investigators haven't considered.
  Ask "what evidence would disprove this?" for each theory.

Rules:
- Each investigator must collect BOTH supporting AND contradicting evidence
- Investigators must message each other when they find evidence relevant to another's hypothesis
- The skeptic must challenge any hypothesis that lacks disconfirming evidence
- No hypothesis is accepted until at least one other investigator has tried to disprove it
- Converge when evidence clearly points to one root cause
```

### 4. Guide Investigator Behavior

Each investigator should follow this process:

**Phase 1 - Evidence Gathering (independent)**
1. Read the code in the area relevant to their hypothesis
2. Use Grep to find related patterns, error handling, edge cases
3. Run targeted tests if available (`bash: pytest -k "test_relevant"`)
4. Check git history for recent changes in the area (`git log --oneline -20 -- path/to/file`)
5. Look for the **absence** of expected code (missing validation, error handling, etc.)

**Phase 2 - Cross-examination (collaborative)**
1. Share findings with other investigators via SendMessage
2. Attempt to reproduce the bug under conditions matching their hypothesis
3. Try to DISPROVE at least one other hypothesis with concrete evidence
4. Respond to challenges from the skeptic with additional evidence

**Phase 3 - Convergence**
1. When evidence strongly favors one hypothesis, investigators should acknowledge it
2. The winning investigator documents the full causal chain
3. Other investigators confirm they cannot produce counter-evidence

### 5. Produce the Consensus Report

Once the team converges, synthesize a report with this structure:

```markdown
## Debug Team Report: [Symptom]

### Root Cause
[One-paragraph summary of the confirmed root cause]

### Evidence Chain
1. [Key evidence point 1 with file:line reference]
2. [Key evidence point 2 with file:line reference]
3. [Key evidence point 3 with file:line reference]

### Hypotheses Evaluated

| # | Hypothesis | Verdict | Key Evidence |
|---|-----------|---------|-------------|
| 1 | [Description] | **CONFIRMED** | [Evidence summary] |
| 2 | [Description] | Disproved | [Why it was ruled out] |
| 3 | [Description] | Disproved | [Why it was ruled out] |

### Suggested Fix
- **File**: `path/to/file.ext:line_number`
- **Change**: [Description of the fix]
- **Risk**: [Low/Medium/High - potential side effects]

### Alternative Explanations Considered
[Anything the devils-advocate raised that wasn't fully resolved]
```

## Team Size Guidelines

| Symptom Clarity | Team Size | Composition |
|----------------|-----------|-------------|
| Somewhat clear, 2 plausible causes | 3 agents | 2 investigators + 1 skeptic |
| Unclear, 3+ plausible causes | 4 agents | 3 investigators + 1 skeptic |
| Very unclear, wide search needed | 5 agents | 4 investigators + 1 skeptic |

## Example Invocations

**Network timeout bug:**
```
/debug-team Users report intermittent 504 timeouts on the /api/checkout endpoint.
Occurs under moderate load, not reproducible locally.
```

**Data corruption:**
```
/debug-team Customer records showing duplicate entries after the nightly sync job.
Started after last week's deployment. No errors in logs.
```

**Test flakiness:**
```
/debug-team test_payment_webhook fails ~20% of the time in CI but passes locally.
No obvious timing dependency. Started failing 3 weeks ago.
```

## Anti-Patterns

- **Don't use for simple bugs**: If you can reproduce and diagnose in 5 minutes, use a single agent.
- **Don't let investigators ignore counter-evidence**: The skeptic's job is to catch this.
- **Don't skip the skeptic**: Without one, investigators tend toward confirmation bias.
- **Don't let the team run indefinitely**: If no convergence after thorough investigation, report the top 2 hypotheses with evidence and let the user decide.
- **Don't have investigators edit code**: This is a diagnostic tool. Fixes come after the report.
