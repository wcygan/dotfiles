---
name: problem-decompose
description: >
  Decomposes complex problems via phased multi-agent analysis before implementation.
  Explores input space, maps constraints, generates and evaluates approaches, produces
  a ranked recommendation report. Use for algorithm design, system design, or any task
  where deep understanding matters more than jumping to code.
  Keywords: problem decomposition, analyze, input space, edge cases, algorithm,
  system design, approach evaluation, pre-implementation, decompose
disable-model-invocation: true
argument-hint: [problem description or link to problem statement]
effort: high
---

# Problem Decompose

Problem: **$ARGUMENTS**

## Progress Tracking

Copy this checklist and update as you progress:

```
Problem Decomposition Progress:
- [ ] Frame: Restate problem, classify, identify initial approaches
- [ ] Phase 1: Input Explorer (parallel)
- [ ] Phase 1: Goal Analyst (parallel)
- [ ] Phase 1: Constraints Mapper (parallel)
- [ ] Phase 1 gate: Verify all outputs have required sections
- [ ] Phase 2A: Approach Generator (3-5 distinct approaches)
- [ ] Phase 2B: Approach Evaluator (comparison matrix + edge case coverage)
- [ ] Phase 2 gate: Verify diversity and evidence-backed scores
- [ ] Phase 3: Synthesizer (final report)
- [ ] Deliver report to user
```

## Overview

Three-phase analysis producing a comprehensive problem report before any code is written.

### Phase 1: Understanding (3 agents, parallel)

- **Input Explorer** — characterizes the input space, common cases, edge cases, boundaries
- **Goal Analyst** — clarifies what success looks like, functional and non-functional requirements
- **Constraints Mapper** — identifies technical, performance, and environmental constraints

### Phase 2: Approaches (2 agents, sequential)

- **Approach Generator** — proposes 3-5 solution approaches informed by Phase 1
- **Approach Evaluator** — evaluates each approach against Phase 1 findings

### Phase 3: Synthesis (1 agent)

- **Synthesizer** — cross-references all findings, ranks approaches, produces final report

## Execution

### 1. Frame the Problem

Before spawning agents, restate the problem clearly:

- **Problem statement**: What exactly are we solving? Transform vague requests into precise statements.
- **Known inputs/outputs**: What do we know about the data or system boundaries?
- **Domain**: What category does this fall into? Use problem-categories.md to classify.
- **Initial gut approaches**: Any obvious starting points the agents should be aware of.

If `$ARGUMENTS` is empty or too vague to act on, ask the user for a specific problem statement before proceeding.

If the problem is described in an existing file, spec, or URL, read it first and extract the above.

References: [problem-categories](references/problem-categories.md)

### 2. Phase 1 — Understanding (Parallel)

Spawn all 3 Phase 1 agents in ONE parallel Agent tool call. Each agent gets:

- The framed problem statement from Step 1
- Their specific mandate and output format from agent-roles.md
- Any known context (existing code, requirements, constraints the user mentioned)
- The relevant analysis framework from analysis-frameworks.md

Use `subagent_type: general-purpose` for all three.

**Input Explorer**: Characterize what goes in and comes out. Common cases, edge cases, degenerate inputs, scale characteristics.

**Goal Analyst**: Define success. What must the solution do? What is explicitly out of scope? What quality attributes matter most?

**Constraints Mapper**: Identify what limits the solution space. Time/space complexity targets, technology constraints, existing system interfaces, compatibility requirements.

References: [agent-roles](references/agent-roles.md), [analysis-frameworks](references/analysis-frameworks.md)

**Phase 1 gate** — Before proceeding, verify each agent produced its required sections:
- Input Explorer: Common inputs, edge cases, scale characteristics, input invariants
- Goal Analyst: Must/Should/Won't requirements, quality priorities, success criteria
- Constraints Mapper: Hard constraints, soft constraints, complexity budget

If any output is thin, note it as a gap for the Synthesizer — don't re-run the agent.

### 3. Phase 2 — Approaches (Sequential)

After Phase 1 completes:

**Step A — Approach Generator**: Spawn with all Phase 1 outputs. It proposes 3-5 genuinely distinct approaches (not variations of one idea). Each approach should include the core algorithm/pattern, data structures, and high-level architecture.

**Step B — Approach Evaluator**: After the Generator finishes, spawn with:
- All Phase 1 outputs (inputs, goals, constraints)
- The Generator's proposed approaches
- Instructions to score each approach against the goal dimensions and constraint boundaries

The Evaluator produces a comparison matrix and identifies which edge cases each approach handles or struggles with.

References: [agent-roles](references/agent-roles.md), [workflow](references/workflow.md)

**Phase 2 gate** — Before synthesis, verify:
- 3-5 genuinely distinct approaches (not variations of one idea)
- Each approach scored with specific references to Phase 1 findings
- Edge case coverage table populated for all approaches

### 4. Phase 3 — Synthesis

Spawn the **Synthesizer** with ALL prior phase outputs. It produces the final report by:

1. Cross-referencing approaches against edge cases from the Input Explorer
2. Verifying approaches meet goals from the Goal Analyst
3. Confirming approaches respect constraints from the Constraints Mapper
4. Incorporating the Evaluator's comparison matrix
5. Resolving any contradictions between agents explicitly
6. Producing a ranked recommendation with implementation guidance

References: [output-templates](references/output-templates.md)

## Output

Present the final report using the structured template:

1. **TL;DR** — recommended approach in 2-3 sentences with confidence level
2. **Problem Profile** — input characteristics, goals, constraints summary
3. **Approach Comparison** — matrix scoring each approach against quality attributes
4. **Edge Case Coverage** — which approaches handle which edge cases
5. **Recommendation** — ranked approaches with rationale
6. **Implementation Guidance** — suggested first steps, key decisions, what to prototype first

References: [output-templates](references/output-templates.md)

## Anti-Patterns

- **Don't skip Phase 1** — jumping to approaches without understanding the problem is the #1 source of rework
- **Don't let agents duplicate work** — each agent has a clear mandate; the Input Explorer doesn't evaluate approaches, the Goal Analyst doesn't characterize inputs
- **Don't present raw agent outputs** — the synthesis is the value; raw outputs are working material
- **Don't over-decompose simple problems** — if the problem is trivially understood, just solve it
- **Don't anchor on the first approach** — the Generator must produce genuinely diverse options
- **Don't skip the Evaluator** — without evaluation against Phase 1 findings, approaches are just guesses
