---
title: Workflow
description: Phase orchestration, dependency graph, and execution rules
tags: [workflow, orchestration, phases, dependencies]
---

# Workflow

## Dependency Graph

```
Phase 1 (parallel)              Phase 2 (sequential)          Phase 3
┌───────────────┐
│ Input Explorer │──┐
└───────────────┘  │
                   │
┌───────────────┐  ├──→ ┌────────────────────┐    ┌────────────────────┐    ┌──────────────┐
│ Goal Analyst  │──┤    │ Approach Generator │──→ │ Approach Evaluator │──→ │ Synthesizer  │
└───────────────┘  │    └────────────────────┘    └────────────────────┘    └──────────────┘
                   │
┌─────────────────┐│
│ Constraints     ││
│ Mapper          │┘
└─────────────────┘
```

**Rules**:
- Phase 1 agents run in ONE parallel Agent call
- Approach Generator WAITS for all Phase 1 agents to complete
- Approach Evaluator WAITS for Approach Generator to complete
- Synthesizer WAITS for Approach Evaluator to complete
- Never skip a phase

## Phase 1: Understanding

### What to include in each agent's prompt

**All Phase 1 agents get**:
- The framed problem statement (from Step 1)
- Any context the user provided (existing code, specs, URLs)
- Their specific mandate and output format from agent-roles.md
- The relevant analysis framework from analysis-frameworks.md

**Input Explorer also gets**:
- Known input examples if the user provided any
- Links to relevant data schemas or type definitions

**Goal Analyst also gets**:
- Any stated requirements or acceptance criteria
- Performance targets if mentioned

**Constraints Mapper also gets**:
- Technology stack information
- Deployment environment details
- Any stated complexity or resource limits

### Phase 1 completion check

Before proceeding to Phase 2, verify each Phase 1 agent produced:
- [ ] Input Explorer: Common inputs, edge cases, scale characteristics, input invariants
- [ ] Goal Analyst: Requirements (must/should/won't), quality priorities, success criteria
- [ ] Constraints Mapper: Hard constraints, soft constraints, complexity budget

If any output is thin or missing sections, note it as a gap — don't re-run the agent.

---

## Phase 2: Approaches

### Step A: Approach Generator

**Input**: All three Phase 1 outputs concatenated.

**Key instruction**: Approaches must be genuinely diverse. Check against the Strategy Diversity Checklist in analysis-frameworks.md. If the Generator produces 3 variations of the same idea, the analysis is degraded.

**Expected output**: 3-5 approaches, each with strategy, key insight, design, data structures, complexity, and trade-off profile.

### Step B: Approach Evaluator

**Input**: All Phase 1 outputs + Approach Generator output.

**Key instruction**: Evaluate against Phase 1 findings specifically. Every score must reference a Phase 1 finding. Generic evaluation ("this approach is fast") is not useful; specific evaluation ("this approach's O(n log n) meets the Goal Analyst's 'Should' target of <100ms for n=10^6") is.

**Expected output**: Comparison matrix, edge case coverage table, constraint compliance table, risk register.

### Phase 2 completion check

Before proceeding to Phase 3, verify:
- [ ] 3-5 distinct approaches generated
- [ ] Each approach evaluated against quality attributes, edge cases, and constraints
- [ ] Scores are justified with specific references to Phase 1 findings

---

## Phase 3: Synthesis

### What the Synthesizer receives

Concatenate ALL outputs from Phase 1 and Phase 2. The Synthesizer needs the full picture.

### What the Synthesizer produces

The final report using the template from output-templates.md. The Synthesizer is the ONLY agent that makes a recommendation.

### Synthesis quality checks

The Synthesizer must:
- Reference specific findings from each prior agent
- Explain disagreements between agents (not hide them)
- Justify the ranking with specific evidence
- Provide concrete implementation guidance (not vague "be careful" advice)

---

## Calibration: When to Use Which Depth

| Problem Complexity | Phases to Run | Total Agents |
|-------------------|---------------|--------------|
| **Simple** (clear inputs, obvious approach) | Don't use this skill — just solve it |  |
| **Moderate** (known space, 2-3 viable approaches) | All 3 phases | 6 |
| **Complex** (large input space, many approaches, unclear trade-offs) | All 3 phases, thorough | 6 |
| **Research-level** (novel problem, unclear if solvable) | Phase 1 only, then decide | 3 |

### Time budget guidance

| Phase | Expected duration | If taking too long |
|-------|------------------|-------------------|
| Phase 1 | 2-5 min per agent | Narrow the problem scope |
| Phase 2A | 3-5 min | Reduce to 3 approaches |
| Phase 2B | 3-5 min | Focus on top 3 quality attributes |
| Phase 3 | 2-3 min | Use minimal report template |

---

## Error Recovery

### Agent returns thin output
- Note the gap in the synthesis
- Do NOT re-run — diminishing returns
- The Synthesizer should call out "insufficient data for [X]"

### Approaches are too similar
- This usually means Phase 1 over-constrained the problem
- The Synthesizer should note this and suggest broadening constraints

### Agents contradict each other
- This is VALUABLE — don't suppress it
- The Synthesizer should present both perspectives and explain what drives the disagreement
- Frame as: "If [assumption A], then Approach X; if [assumption B], then Approach Y"
