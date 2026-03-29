---
title: Analysis Frameworks
description: Structured analysis approaches for problem decomposition agents
tags: [analysis, frameworks, methodology, structured-thinking]
---

# Analysis Frameworks

Reusable analysis structures that agents apply based on the problem category. Each framework is a lens — agents pick the relevant ones, not all of them.

## Contents
- Input/Output Analysis (Input Explorer)
- Goal Decomposition (Goal Analyst)
- Constraint Analysis (Constraints Mapper)
- Approach Generation (Approach Generator)
- Evaluation Framework (Approach Evaluator)

---

## Input/Output Analysis (Input Explorer)

Systematic characterization of the problem's data boundaries.

### Step 1: Type Signature

Define the abstract input and output types:
```
f(input_1: Type, input_2: Type, ...) -> OutputType
```

### Step 2: Example Matrix

Build a 2D matrix of input characteristics:

| Dimension | Minimal | Typical | Large | Adversarial |
|-----------|---------|---------|-------|-------------|
| Size | [ex] | [ex] | [ex] | [ex] |
| Shape | [ex] | [ex] | [ex] | [ex] |
| Values | [ex] | [ex] | [ex] | [ex] |
| Structure | [ex] | [ex] | [ex] | [ex] |

### Step 3: Boundary Identification

For each input parameter, identify:
- **Zero/empty**: What happens with no input?
- **One**: Single element behavior
- **Two**: Minimum for pairwise interactions
- **Max**: Upper bound behavior
- **Just past max**: What breaks?
- **Negative/invalid**: Error behavior

### Step 4: Equivalence Classes

Group inputs that should produce the same *kind* of output:
- Class A: [description] — representative example
- Class B: [description] — representative example
- Transitions between classes are where bugs hide

---

## Goal Decomposition (Goal Analyst)

Structured approach to turning vague goals into testable criteria.

### The MoSCoW Framework

| Priority | Question | Example |
|----------|----------|---------|
| **Must** | What makes it correct? | "Returns sorted output" |
| **Should** | What makes it good? | "Runs in O(n log n)" |
| **Could** | What makes it great? | "Handles streaming input" |
| **Won't** | What's explicitly out of scope? | "Distributed execution" |

### Quality Attribute Decomposition

For each relevant quality attribute, define:

```
Attribute: [name]
  Stimulus: [what triggers measurement]
  Measure: [how we quantify it]
  Target: [acceptable threshold]
  Priority: [H/M/L relative to other attributes]
  Conflict: [which other attributes it trades off against]
```

### Acceptance Criteria Pattern

Write criteria in Given/When/Then format:
```
GIVEN [precondition about input state]
WHEN [action or function call]
THEN [observable outcome with specific values]
```

---

## Constraint Analysis (Constraints Mapper)

### The Constraint Stack

Analyze constraints from most rigid to most flexible:

```
Level 1: Laws of physics / mathematics
  └── Can't sort faster than O(n log n) comparison-based
  └── CAP theorem trade-offs

Level 2: Platform / technology
  └── Language features available
  └── Runtime memory limits
  └── Network bandwidth

Level 3: Requirements / SLA
  └── Response time targets
  └── Uptime requirements
  └── Compliance rules

Level 4: Team / organizational
  └── Familiarity with approaches
  └── Time to implement
  └── Maintenance burden

Level 5: Preferences / conventions
  └── Code style
  └── Library choices
  └── Architecture patterns
```

Higher levels cannot be negotiated. Lower levels can be if the trade-off is worthwhile.

### Constraint Interaction Matrix

When two constraints might conflict:

| Constraint A | Constraint B | Conflict? | Resolution |
|-------------|-------------|-----------|------------|
| O(n) time | O(1) space | Yes | Trade space for time or vice versa |
| Real-time latency | Exactly-once | Possible | At-least-once + idempotency |

---

## Approach Generation (Approach Generator)

### Strategy Diversity Checklist

When generating approaches, ensure diversity across these dimensions:

| Dimension | Spectrum |
|-----------|----------|
| **Time vs Space** | CPU-heavy ↔ Memory-heavy |
| **Preprocessing** | None ↔ Heavy upfront cost |
| **Exactness** | Exact ↔ Approximate |
| **Complexity** | Simple/brute-force ↔ Sophisticated/optimal |
| **Paradigm** | Iterative ↔ Recursive ↔ Declarative |
| **Architecture** | Monolithic ↔ Decomposed ↔ Pipeline |

At least 3 of these dimensions should vary across the proposed approaches.

### Approach Description Structure

For each approach, answer:
1. **What's the key insight?** (One sentence that captures why this works)
2. **What data structure enables it?** (The central organizing structure)
3. **Where does the work happen?** (Upfront, per-query, or amortized)
4. **What's the invariant?** (What property does the approach maintain)

### Known Pattern Matching

Check if the problem maps to known patterns:

| Pattern | Signature | Canonical Approach |
|---------|-----------|-------------------|
| Two pointer | Sorted array, find pair | Left/right convergence |
| Sliding window | Contiguous subarray/substring | Expand/contract window |
| Divide and conquer | Can split problem in half | Recursive halving |
| Greedy | Local optimal = global optimal | Sorted processing |
| Backtracking | Explore and prune | DFS with constraint checks |
| Topological | Dependencies/ordering | DFS/BFS on DAG |
| Union-Find | Grouping/connectivity | Disjoint set forest |
| Interval scheduling | Start/end times | Sort by end time |

---

## Evaluation Framework (Approach Evaluator)

### Scoring Rubric

Apply consistently across approaches:

**Performance (1-5)**:
- 5: Optimal complexity, cache-friendly, minimal allocation
- 4: Near-optimal, good constants
- 3: Acceptable complexity, reasonable constants
- 2: Sub-optimal but might work for expected scale
- 1: Unacceptable complexity for the problem size

**Correctness confidence (1-5)**:
- 5: Trivially correct, well-known algorithm
- 4: Correctness is clear with simple proof/argument
- 3: Correctness requires careful implementation
- 2: Subtle edge cases make correctness hard to verify
- 1: Correctness depends on unverified assumptions

**Implementation effort (1-5, inverted — 5 = easiest)**:
- 5: Straightforward, <1 hour
- 4: Clear path, a few hours
- 3: Requires some design decisions
- 2: Complex, multiple components to coordinate
- 1: Research-level difficulty

### Edge Case Stress Test

For each approach × edge case combination, determine:
1. **Natural handling**: The approach handles it without special code
2. **Special-case needed**: Requires an if/else or guard clause
3. **Redesign needed**: Approach fundamentally can't handle it

Count the results. Approaches with more "natural handling" entries are more robust.
