---
allowed-tools: Read, Write, mcp__sequential-thinking__sequentialthinking
description: Apply five why's root cause analysis to a problem
---

## Context

- Problem description: $ARGUMENTS
- Session ID: !`gdate +%s%N`
- Analysis file: /tmp/five-whys-$SESSION_ID.md

## Your task

PROCEDURE five_whys_analysis():

STEP 1: Initialize analysis

- Parse the problem statement from $ARGUMENTS
- Create structured analysis document
- Set iteration counter to 1

STEP 2: Iterative questioning loop
FOR iteration IN [1, 2, 3, 4, 5]:

- ASK: "Why does [current problem/answer] occur?"
- THINK deeply about potential causes
- IDENTIFY the most likely cause
- DOCUMENT the answer with supporting reasoning
- UPDATE current_answer = this iteration's answer
- IF root cause is clearly identified before iteration 5:
  - BREAK from loop

STEP 3: Synthesize findings

- REVIEW the chain of causes
- IDENTIFY the root cause (typically the final "why" answer)
- ANALYZE systemic issues revealed
- GENERATE actionable recommendations

STEP 4: Create comprehensive report

- Problem statement
- Five why's chain with reasoning
- Root cause identification
- Contributing factors
- Recommended solutions
- Preventive measures

STEP 5: Save analysis

- Write complete analysis to /tmp/five-whys-$SESSION_ID.md
- Present summary to user
- Highlight key insights and next steps

## Analysis structure

```markdown
# Five Why's Analysis

## Problem Statement

[Original problem description]

## Analysis Chain

### Why 1: [First why question]

**Answer**: [First answer]
**Reasoning**: [Supporting evidence and logic]

### Why 2: [Second why question based on answer 1]

**Answer**: [Second answer]
**Reasoning**: [Supporting evidence and logic]

[Continue for all iterations...]

## Root Cause

[Identified root cause with explanation]

## Recommendations

1. Immediate actions
2. Long-term solutions
3. Preventive measures

## Next Steps

[Actionable items based on analysis]
```

## Best practices

- Ask "why" about the answer from the previous iteration
- Focus on process and system failures, not individual blame
- Look for actionable root causes within your control
- Consider multiple contributing factors
- Validate assumptions with evidence when possible

## Example

Problem: "Website is slow"

1. Why? → Server response time is high
2. Why? → Database queries are taking too long
3. Why? → Queries aren't using indexes
4. Why? → Recent schema changes removed indexes
5. Why? → No index validation in deployment process
   Root cause: Missing deployment validation checks
