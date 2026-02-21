---
title: Output Templates
description: Structured output formats for brainstorming results
tags: [output, templates, ADR, matrix, WWHTBT]
---

# Output Templates

## Complete Brainstorm Output

### 1. TL;DR (always first)

```
## TL;DR

**Recommendation**: [Option X] — [1 sentence why]
**Confidence**: [High/Medium/Low] — [1 sentence about main uncertainty]
**Key risk**: [The #1 thing that could make this wrong]
```

### 2. Trade-off Matrix

```
## Trade-off Analysis

| Quality Attribute | Weight | Option A | Option B | Option C |
|-------------------|--------|----------|----------|----------|
| [Attr 1]          | [H/M/L]| [1-5]   | [1-5]   | [1-5]   |
| [Attr 2]          | [H/M/L]| [1-5]   | [1-5]   | [1-5]   |
| ...               | ...    | ...      | ...      | ...      |
| **Weighted Total**|        | **X**   | **Y**    | **Z**    |

**Sensitivity**: [Which weight changes would flip the decision?]
**Key assumption**: [What's the biggest assumption in these scores?]
```

### 3. WWHTBT Analysis

```
## What Would Have to Be True

### For Option A to be the best choice:
- [Condition 1 about codebase/architecture]
- [Condition 2 about team/timeline]
- [Condition 3 about requirements/scale]
**Reality check**: [Are these conditions likely true?]

### For Option B to be the best choice:
- [Condition 1]
- [Condition 2]
- [Condition 3]
**Reality check**: [Are these conditions likely true?]
```

### 4. Pre-Mortem & Risk Register

```
## Pre-Mortem: What If [Leading Option] Fails?

[2-3 paragraph narrative from the Critic agent describing the failure scenario]

### Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Affects |
|---|------|-----------|--------|------------|---------|
| 1 | [Risk] | H/M/L | H/M/L | [Strategy] | Option A |
| 2 | [Risk] | H/M/L | H/M/L | [Strategy] | All |
| ...| ... | ... | ... | ... | ... |

### Cognitive Bias Check
- **[Bias name]**: [How it might be affecting this decision]
```

### 5. Recommendation & ADR Summary

```
## Recommendation

**Choose**: [Option X]

**Because**:
- [Reason 1 — reference to trade-off matrix]
- [Reason 2 — reference to WWHTBT conditions being met]
- [Reason 3 — reference to risk mitigation]

**Despite**:
- [Acknowledged downside 1]
- [Acknowledged downside 2]

**Revisit this decision if**:
- [Condition 1 that would change the calculus]
- [Condition 2]

---

## ADR-Ready Summary

### ADR: [Decision Title]

**Status**: Proposed

**Context**: [2-3 sentences on what forces led to this decision]

**Decision**: [What we chose and the primary reason]

**Alternatives Considered**:
- [Option B]: Rejected because [reason]
- [Option C]: Rejected because [reason]

**Consequences**:
- Positive: [list]
- Negative: [list]
- Risks: [list]

**Review Triggers**: [When to revisit]
```

---

## Minimal Output (for simpler decisions)

When the decision is straightforward, use a compressed format:

```
## TL;DR

**Go with [Option X]** because [reason].

### Quick comparison

| | Option A | Option B |
|--|---------|---------|
| [Key attr 1] | [assessment] | [assessment] |
| [Key attr 2] | [assessment] | [assessment] |
| Main risk | [risk] | [risk] |

### Watch out for
- [Risk 1 from Critic]
- [Risk 2 from Critic]

### Revisit if
- [Condition]
```
