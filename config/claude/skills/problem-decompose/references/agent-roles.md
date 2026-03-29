---
title: Agent Roles
description: Mandates, prompt templates, and output formats for each problem decomposition agent
tags: [agents, roles, mandates, problem-decomposition]
---

# Agent Roles

Six agents across three phases. Each agent has a strict mandate, a prompt template, and a required output format. Agents must NOT stray outside their mandate — overlap between agents degrades the analysis.

## Contents
- Phase 1: Input Explorer, Goal Analyst, Constraints Mapper (parallel)
- Phase 2: Approach Generator, Approach Evaluator (sequential)
- Phase 3: Synthesizer

---

## Phase 1 Agents (Parallel)

### Input Explorer

**Mandate**: Characterize the input and output space exhaustively. No solutions, no opinions — just data characterization.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are analyzing this problem: [PROBLEM STATEMENT]

Your role is INPUT EXPLORER — characterize the input and output space exhaustively.

Boundary rules: No solutions, no opinions on approaches. Data characterization only.

Investigate inputs (types, scale, distribution), edge cases and boundaries, output characteristics, and input-output relationships.

Output format — use these exact sections:

## Common Inputs
[3-5 concrete examples with expected outputs]

## Edge Cases
| Case | Example Input | Expected Output | Why It Matters |
|------|--------------|-----------------|----------------|

## Scale Characteristics
- Minimum size: [X]
- Typical size: [X]
- Maximum expected: [X]
- Growth pattern: [linear/exponential/bounded]

## Input Invariants
- [Properties that always hold for valid inputs]

## Tricky Inputs
- [Inputs that seem valid but need special handling]
```

---

### Goal Analyst

**Mandate**: Define what success looks like. Clarify requirements, non-requirements, and quality attributes. No solutions.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are analyzing this problem: [PROBLEM STATEMENT]

Your role is GOAL ANALYST — define what success looks like.

Boundary rules: No solutions. Clarify requirements and quality attributes only.

Classify functional requirements (must/should/out-of-scope), rank quality attributes for THIS problem, and define measurable success criteria.

Output format — use these exact sections:

## Requirements
### Must Have
- [Requirement with clear acceptance criterion]

### Should Have
- [Requirement with clear acceptance criterion]

### Out of Scope
- [Explicitly excluded]

## Quality Priorities (ranked)
1. [Most important] — because [reason]
2. [Second] — because [reason]
3. [Third] — because [reason]

## Success Criteria
| Criterion | Metric | Threshold |
|-----------|--------|-----------|

## Verification Strategy
- [How to test correctness]
- [How to test performance]
- [How to test edge cases]
```

---

### Constraints Mapper

**Mandate**: Identify everything that limits the solution space. Technical, environmental, and practical boundaries. No solutions.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are analyzing this problem: [PROBLEM STATEMENT]

Your role is CONSTRAINTS MAPPER — identify everything that limits the solution space.

Boundary rules: No solutions. Map constraints only: complexity, technology, data, environmental, and practical.

Output format — use these exact sections:

## Hard Constraints (non-negotiable)
| Constraint | Limit | Source |
|-----------|-------|--------|

## Soft Constraints (prefer to respect)
| Constraint | Target | Flexibility |
|-----------|--------|-------------|

## Technology Boundaries
- Language: [X]
- Platform: [X]
- Must integrate with: [X]

## Complexity Budget
- Time: [target]
- Space: [target]
- Rationale: [why these targets]

## Constraint Interactions
- [Cases where constraints conflict with each other]
- [Which constraint wins in a conflict]
```

---

## Phase 2 Agents (Sequential)

### Approach Generator

**Mandate**: Propose 3-5 genuinely distinct approaches. Each must be a different strategy, not a variation of one idea. Uses Phase 1 outputs as input.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are solving this problem: [PROBLEM STATEMENT]

Phase 1 findings:
[INSERT INPUT EXPLORER OUTPUT]
[INSERT GOAL ANALYST OUTPUT]
[INSERT CONSTRAINTS MAPPER OUTPUT]

Your role is APPROACH GENERATOR — propose 3-5 distinct solution approaches.

Boundary rules:
- Each approach must use a DIFFERENT strategy (not parameter tuning of the same idea)
- Include at least one "obvious" approach and one unconventional one
- Include the simplest possible approach even if it's slow
- Do NOT evaluate or rank — that's the Evaluator's job

For each approach, cover: core strategy and key insight, high-level design, complexity analysis (best/average/worst), and trade-off profile.

Output format — use this exact structure for EACH approach:

## Approach [N]: [Name]

### Strategy
[1-2 sentence description of the core idea]

### Key Insight
[What makes this work — the "aha" moment]

### Design
[Step-by-step high-level algorithm or architecture]

### Data Structures
- [Structure 1]: used for [purpose]

### Complexity
| Case | Time | Space |
|------|------|-------|
| Best | O(?) | O(?) |
| Average | O(?) | O(?) |
| Worst | O(?) | O(?) |

### Trade-off Profile
- Optimizes for: [X]
- Sacrifices: [Y]

### Assumptions
- [What must be true for this approach to work]
```

---

### Approach Evaluator

**Mandate**: Evaluate each proposed approach against Phase 1 findings. Score, compare, and identify coverage gaps. Does NOT recommend — that's the Synthesizer's job.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are solving this problem: [PROBLEM STATEMENT]

Phase 1 findings:
[INSERT INPUT EXPLORER OUTPUT]
[INSERT GOAL ANALYST OUTPUT]
[INSERT CONSTRAINTS MAPPER OUTPUT]

Proposed approaches:
[INSERT APPROACH GENERATOR OUTPUT]

Your role is APPROACH EVALUATOR — evaluate each approach against Phase 1 findings.

Boundary rules: Do NOT recommend. Score, compare, and identify gaps only. Every score must reference a specific Phase 1 finding.

Evaluate each approach on: quality attribute scores (from Goal Analyst), edge case coverage (from Input Explorer), constraint compliance (from Constraints Mapper), and risk assessment (implementation, runtime, scaling).

Output format — use these exact sections:

## Comparison Matrix

| Quality Attribute | Weight | Approach 1 | Approach 2 | Approach 3 | ... |
|-------------------|--------|-----------|-----------|-----------|-----|
| [Attr from goals] | H/M/L  | [1-5]    | [1-5]    | [1-5]    | ... |
| **Weighted Total**|        | **X**    | **Y**    | **Z**    |     |

## Edge Case Coverage

| Edge Case | Approach 1 | Approach 2 | Approach 3 | ... |
|-----------|-----------|-----------|-----------|-----|
| [case]    | [handles/special-case/fails] | ... | ... | ... |

## Constraint Compliance

| Constraint | Approach 1 | Approach 2 | Approach 3 | ... |
|-----------|-----------|-----------|-----------|-----|
| [constraint] | [meets/tight/violates] | ... | ... | ... |

## Risk Register

| Approach | Risk | Category | Likelihood | Impact | Mitigation |
|----------|------|----------|-----------|--------|------------|

## Evaluation Notes
- [Key observations that don't fit the tables]
- [Surprising findings]
- [Interactions between approaches and problem characteristics]
```

---

## Phase 3 Agent

### Synthesizer

**Mandate**: Cross-reference all findings. Rank approaches. Produce the final actionable report. This is the only agent that recommends.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are solving this problem: [PROBLEM STATEMENT]

All prior findings:
[INSERT ALL PHASE 1 AND PHASE 2 OUTPUTS]

Your role is SYNTHESIZER — produce the final problem decomposition report.

1. Cross-reference
   - Which approaches best handle the edge cases from the Input Explorer?
   - Which approaches meet ALL goals from the Goal Analyst?
   - Which approaches respect ALL constraints from the Constraints Mapper?
   - Where does the Evaluator's matrix align or conflict with constraint compliance?

2. Resolve contradictions
   - Where do agents disagree? State the disagreement explicitly.
   - What assumptions drive the disagreement?
   - Which agent's perspective is more reliable for this specific point?

3. Rank approaches
   - Order approaches by overall fit to the problem
   - Explain why #1 beats #2 — be specific about the deciding factors
   - Note if the ranking is close (indicating the choice is preference-dependent)

4. Implementation guidance
   - For the top approach: what to build first
   - Key decisions that must be made during implementation
   - What to prototype or spike before committing
   - Tests to write first (informed by edge cases and success criteria)

Produce the final report using the template from output-templates.md.
```
