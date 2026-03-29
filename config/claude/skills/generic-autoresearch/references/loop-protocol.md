---
title: Research Loop Protocol
description: The critical rules governing each iteration of the generic autoresearch loop
tags: [loop, protocol, iteration, rules, validation]
---

# Research Loop Protocol

## Critical Rules

1. **One checklist item per iteration.** Research one aspect, validate it, record results. Not multiple.
2. **Read before searching.** Every iteration starts by reading `.autoresearch-knowledge.md` and `.autoresearch-results.tsv` to understand current state.
3. **Source-based validation only.** No "this seems right." Every claim needs a URL. Two independent sources = validated; one source = provisional.
4. **Record before moving on.** Update the knowledge artifact and results log immediately after each iteration. Don't batch.
5. **Automatic gap handling.** No useful sources found? Log as `gap`, try a different angle next iteration. Don't spin.
6. **Simplicity wins.** A clean 2-sentence finding from 2 good sources beats a rambling paragraph from 1 blog post.
7. **The results log is memory.** Read it each iteration. Don't repeat search queries that already returned nothing.
8. **When stuck, pivot.** After 2 consecutive gaps: reframe the question, broaden scope, try adjacent topics. After 3: mark and move on.

## Iteration Anatomy

```
Iteration N:
1. READ   — .autoresearch-knowledge.md + .autoresearch-results.tsv
2. SELECT — Pick highest-priority uncovered checklist item
3. QUERY  — Formulate 1-2 targeted search queries (different from prior iterations)
4. SEARCH — WebSearch for each query
5. FETCH  — WebFetch the 2-3 most promising results
6. EXTRACT — Pull key findings, note source quality
7. VALIDATE — Categorize: validated / provisional / contested / gap
8. UPDATE — Write findings to knowledge artifact, check off item if covered
9. LOG    — Append to .autoresearch-results.tsv
```

## Search Strategy Progression

If initial queries don't yield results, escalate:

1. **Direct query**: "event sourcing schema evolution"
2. **Question form**: "how do teams handle schema changes in event sourced systems"
3. **Practitioner angle**: "event sourcing schema migration real world experience"
4. **Problem angle**: "event sourcing versioning challenges problems"
5. **Adjacent topic**: "CQRS event store migration patterns" (broaden scope)
6. **Specific platforms**: "event sourcing schema evolution Axon" or "EventStoreDB versioning"

## Source Quality Tiers

| Tier | Source Type | Trust Level | Example |
|------|-----------|-------------|---------|
| 1 | Official docs, specs, RFCs | High | IETF RFC, language spec, tool documentation |
| 2 | Peer-reviewed, established publishers | High | IEEE, ACM, O'Reilly, major tech blogs |
| 3 | Practitioner blogs, conference talks | Medium | Staff eng blogs, QCon/StrangeLoop talks |
| 4 | Community discussions (with upvotes/engagement) | Medium | HN threads, Reddit, Stack Overflow |
| 5 | Individual opinions, undated content | Low | Random Medium posts, undated blogs |

**Rules:**
- A Tier 1-2 source alone = provisional (upgrade to validated with a second independent source)
- A Tier 3-4 source alone = provisional
- A Tier 5 source alone = not sufficient (find better sources)
- Two independent Tier 1-4 sources agreeing = validated
- Two sources disagreeing = contested (present both)

## Handling Contradictions

When sources disagree:

1. Note the contradiction explicitly
2. Check publication dates — newer may supersede older
3. Check authority — official docs override blog posts
4. If still unclear, present both positions with context:
   ```
   **Contested**: Source A (official docs, 2025) states X, while Source B
   (practitioner blog, 2026) reports Y in production. The discrepancy may
   reflect [theory vs practice / version differences / different scale].
   ```

## Knowledge Artifact Format

Each checklist item in the artifact should follow this template:

```markdown
### [Checklist Item Title]

**Status**: validated | provisional | contested | gap

**Key findings:**
- Finding 1 ([Source A](url), [Source B](url))
- Finding 2 ([Source C](url))

**Practical implications:**
- What this means for the user's goals

**Caveats:**
- Any limitations, recency concerns, or gaps in the evidence
```
