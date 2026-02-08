# UX Review Report Template

Use this exact structure for the final synthesized report. Fill every section.

---

```markdown
# UX Review Report: [Application Name]

**Date**: [Date]
**URL**: [Target URL]
**Reviewed by**: AI UX Review Team (6 specialist agents)

---

## Executive Summary

[3-5 sentences: What is the overall UX health of this application? What are the biggest
strengths? What are the most critical problems? What's the single most impactful change
the developer could make?]

---

## Scores Overview

| Dimension | Score (1-10) | Summary |
|-----------|:---:|---------|
| First Impression | X | [One sentence] |
| Information Architecture | X | [One sentence] |
| User Flows | X | [One sentence] |
| Visual Design | X | [One sentence] |
| Accessibility | X | [One sentence] |
| Copy & Microcopy | X | [One sentence] |
| **Overall** | **X** | **[One sentence]** |

---

## Top 5 Critical Issues

### 1. [Issue Title]
**Impact**: [Who is affected and how]
**Evidence**: [What we observed — reference specific pages/elements]
**Fix**: [Specific, actionable recommendation]
**Effort**: [Quick fix / Small task / Medium task / Large task]

### 2. [Issue Title]
...

[Repeat for top 5]

---

## Quick Wins (< 30 minutes each)

These high-impact, low-effort fixes should be tackled first:

| # | Fix | Location | Impact | Est. Time |
|---|-----|----------|--------|-----------|
| 1 | [Specific change] | [Page/Component] | [What improves] | [Minutes] |
| 2 | ... | ... | ... | ... |

---

## Sprint Plan

### Sprint 1: Foundation (1-2 days)
High-impact structural fixes that other improvements depend on.

- [ ] [Task 1 — specific and actionable]
- [ ] [Task 2]
- [ ] ...

### Sprint 2: Core UX (2-3 days)
Major usability improvements to key user flows.

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] ...

### Sprint 3: Polish (3-5 days)
Visual consistency, copy improvements, and accessibility.

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] ...

### Sprint 4: Enhancement (ongoing)
Lower-priority improvements and nice-to-haves.

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] ...

---

## Detailed Findings

### Conversion & First Impression
[Consolidated findings from First Impression and relevant User Flow insights]

### Navigation & Discoverability
[Consolidated findings from Information Architecture]

### User Flows & Task Completion
[Consolidated findings from User Flow agent]

### Visual Design & Consistency
[Consolidated findings from Visual Design agent]

### Accessibility
[Consolidated findings from Accessibility agent]

### Copy & Content
[Consolidated findings from Copy Review agent]

---

## Strengths (Keep These)

Things that are working well — don't break these while fixing other issues:

- [Strength 1]
- [Strength 2]
- [Strength 3]

---

## Methodology

This review was conducted by 6 specialized AI agents, each using Playwright CLI to
browse the live application. Each agent analyzed the app through a distinct lens
(first impression, information architecture, user flows, visual design, accessibility,
and copy quality). Findings were synthesized and prioritized using an impact × effort
matrix optimized for solo developer workflows.

**Limitations**:
- This is an automated heuristic review, not a user study with real participants
- Some subjective design assessments may differ from target audience preferences
- Dynamic/authenticated flows may not be fully tested without credentials
- Performance metrics are approximate (not lab-grade Lighthouse scores)
```
