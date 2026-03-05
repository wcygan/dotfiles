---
title: Output Templates
description: Structured output formats for problem decomposition reports
tags: [output, templates, report, synthesis]
---

# Output Templates

## Final Report Template

The Synthesizer produces this report. Every section is mandatory.

```markdown
# Problem Decomposition: [Problem Name]

## TL;DR

**Recommended approach**: [Approach Name] — [1 sentence why]
**Confidence**: [High/Medium/Low] — [1 sentence about main uncertainty]
**Key risk**: [The #1 thing that could make this wrong]

## Problem Profile

### Input Space
- **Common case**: [brief description with example]
- **Scale**: [typical size / max expected]
- **Key edge cases**: [top 3, one line each]

### Goals (ranked)
1. [Most important quality attribute] — [threshold]
2. [Second] — [threshold]
3. [Third] — [threshold]

### Hard Constraints
- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## Approaches Considered

### [Approach 1 Name] — Recommended
**Strategy**: [1-2 sentences]
**Complexity**: Time O(?), Space O(?)
**Strengths**: [bullet list]
**Weaknesses**: [bullet list]

### [Approach 2 Name]
**Strategy**: [1-2 sentences]
**Complexity**: Time O(?), Space O(?)
**Why not #1**: [specific reason]

### [Approach 3 Name]
**Strategy**: [1-2 sentences]
**Complexity**: Time O(?), Space O(?)
**Why not #1**: [specific reason]

## Comparison Matrix

| Quality Attribute | Weight | Approach 1 | Approach 2 | Approach 3 |
|-------------------|--------|-----------|-----------|-----------|
| [Attr 1]          | [H/M/L]| [1-5]    | [1-5]    | [1-5]    |
| [Attr 2]          | [H/M/L]| [1-5]    | [1-5]    | [1-5]    |
| **Weighted Total**|        | **X**    | **Y**    | **Z**    |

## Edge Case Coverage

| Edge Case | Approach 1 | Approach 2 | Approach 3 |
|-----------|-----------|-----------|-----------|
| [case]    | [handles/needs special logic/fails] | ... | ... |

**Coverage gap**: [Any edge cases no approach handles well]

## Recommendation

**Choose**: [Approach Name]

**Because**:
- [Reason 1 — reference to comparison matrix]
- [Reason 2 — reference to edge case coverage]
- [Reason 3 — reference to constraint compliance]

**Despite**:
- [Acknowledged weakness 1]
- [Acknowledged weakness 2]

**Revisit this if**:
- [Condition that would change the recommendation]

## Implementation Guidance

### Start with
1. [First thing to build / prototype]
2. [Second step]
3. [Third step]

### Key decisions during implementation
- [Decision 1]: [options and recommendation]
- [Decision 2]: [options and recommendation]

### Tests to write first
1. [Test for primary happy path]
2. [Test for most dangerous edge case]
3. [Test for performance threshold]

### What to spike first
- [Area of uncertainty worth prototyping before committing]
```

---

## Minimal Report (for simpler problems)

When the problem is straightforward, use this compressed format:

```markdown
# Problem Decomposition: [Problem Name]

## TL;DR
**Go with [Approach]** because [reason]. [Complexity]. [Key edge case to watch].

### Quick Comparison
| | Approach A | Approach B |
|--|-----------|-----------|
| Complexity | O(?) | O(?) |
| Handles [key edge] | Yes/No | Yes/No |
| [Key quality] | [rating] | [rating] |

### Edge Cases to Handle
- [Case 1]: [how]
- [Case 2]: [how]

### Start With
1. [First step]
2. [Test to write]
```

---

## Scoring Guide

Use consistent scoring across all agents:

### Quality Attribute Scores (1-5)

| Score | Meaning |
|-------|---------|
| 5 | Excellent — naturally optimized for this attribute |
| 4 | Good — handles it well with minor trade-offs |
| 3 | Adequate — meets requirements but not a strength |
| 2 | Weak — requires significant effort or workarounds |
| 1 | Poor — fundamentally misaligned with this attribute |

### Weight Levels

| Weight | Meaning |
|--------|---------|
| H (High) | Non-negotiable, primary decision driver |
| M (Medium) | Important but some flexibility |
| L (Low) | Nice-to-have, won't drive the decision |

### Confidence Levels

| Level | Meaning |
|-------|---------|
| High | Clear winner, robust across assumptions |
| Medium | Likely best, but sensitive to 1-2 assumptions |
| Low | Slight edge, could change with more information |

### Edge Case Handling

| Status | Meaning |
|--------|---------|
| Handles | Works correctly without special logic |
| Special-case | Needs explicit handling but is solvable |
| Fails | Approach cannot handle this case; redesign needed |
