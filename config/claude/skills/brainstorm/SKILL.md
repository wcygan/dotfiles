---
name: brainstorm
description: >
  Multi-agent brainstorming for software design decisions and architecture choices.
  Spawns parallel agents with differentiated roles (codebase explorer, trade-off analyst,
  devil's advocate) to evaluate options, surface blind spots, and produce structured
  analysis including trade-off matrices, pre-mortems, and ADR-ready summaries.
  Use when making architecture decisions, choosing between approaches, or evaluating
  trade-offs. Keywords: brainstorm, decision, trade-off, architecture, design, evaluate,
  options, approach, choose, pros cons, ADR, pre-mortem, WWHTBT
disable-model-invocation: true
argument-hint: [decision or question to explore]
---

# Brainstorm

Decision: **$ARGUMENTS**

## Agent Strategy

Every brainstorm uses 3 core agents in parallel, plus an optional specialist.

### Core Agents (always spawn)

| Agent | Role | Mandate |
|-------|------|---------|
| **Explorer** | Codebase & Context Analyst | Maps relevant code, existing patterns, constraints, prior decisions |
| **Analyst** | Trade-off Evaluator | Scores options against quality attributes, produces trade-off matrix + WWHTBT |
| **Critic** | Devil's Advocate | Assumes the "obvious" choice fails; runs pre-mortem; surfaces risks and biases |

### Optional Agent (spawn when relevant)

| Agent | When to spawn | Mandate |
|-------|---------------|---------|
| **Scout** | Unfamiliar tech, external solutions, or user says "what else?" | Researches alternatives nobody mentioned; finds external precedent |

References: [agent-roles](references/agent-roles.md)

## Execution

### 1. Frame the Decision

Before spawning agents, restate the decision clearly and identify:
- **Decision statement**: What exactly are we deciding?
- **Options on the table**: 2-4 obvious approaches (agents may add more)
- **Priority quality attributes**: Performance, security, maintainability, DX, operability, cost, scalability, availability
- **Constraints**: Timeline, team size, existing tech, compliance, budget

### 2. Spawn Agents in Parallel

Use Task tool — `subagent_type=Explore` for Explorer, `subagent_type=general-purpose` for Analyst/Critic/Scout. Give each their specific mandate and output format from reference files. Spawn all agents in ONE parallel call.

References: [workflow](references/workflow.md)

### 3. Synthesize

After all agents return, combine findings:
1. Cross-reference Explorer facts against Analyst scores
2. Check if Critic's pre-mortem reveals risks Analyst missed
3. Incorporate Scout alternatives if spawned
4. Resolve contradictions explicitly — state disagreements and what drives them

References: [output-templates](references/output-templates.md), [decision-frameworks](references/decision-frameworks.md)

## Output

Present findings in this order:
1. **TL;DR** — 2-3 sentence recommendation with confidence level
2. **Trade-off matrix** — options scored against weighted quality attributes
3. **WWHTBT** — what would have to be true for each option to succeed
4. **Pre-mortem & risks** — Critic findings, risk register, bias check
5. **Recommendation** — detailed reasoning + ADR-ready summary

References: [output-templates](references/output-templates.md)

## Anti-Patterns

- **Don't skip the framing step** — vague questions produce vague analysis
- **Don't let agents duplicate work** — Explorer inspects code, Analyst evaluates, Critic attacks; clear boundaries
- **Don't omit the devil's advocate** — false consensus is the #1 risk in agent-assisted brainstorming
- **Don't present raw agent outputs** — the synthesis is the value
- **Don't anchor on the first option** — always evaluate at least 3 approaches

References: [cognitive-biases](references/cognitive-biases.md)
