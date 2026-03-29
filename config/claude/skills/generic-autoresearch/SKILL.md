---
name: generic-autoresearch
description: >
  Iterates autonomously on a knowledge goal — one research question per iteration, validate findings,
  accumulate into a growing knowledge artifact, repeat until coverage is complete.
  Use when deeply researching a non-code topic, exploring a domain, evaluating approaches,
  modeling an application, or building structured knowledge on any subject.
  Keywords: autoresearch, research, iterate, knowledge, domain, explore, deep dive, learn, evaluate, model
disable-model-invocation: true
context: fork
effort: high
argument-hint: [topic] [max=N] [depth=standard|deep]
---

# Generic Autoresearch

Autonomous non-code research loop. ONE research question per iteration, web-validated findings, accumulate or discard, repeat.

Complementary to `/autoresearch` (code metrics) and `/web-research` (single-pass synthesis). This skill iteratively deepens understanding across multiple passes, building a knowledge artifact that grows richer with each iteration.

## Current context

```
Date: !`date +%Y-%m-%d`
Working directory: !`basename $(pwd)`
```

## Arguments

Parse `$ARGUMENTS`:
- **topic**: What to research (required)
- **max=N**: Iteration cap (default: 8)
- **depth=standard|deep**: Controls coverage checklist size (standard: 6-8 items, deep: 10-14 items)

If no topic provided, stop with an error.

## Protocol

Copy this checklist and update as you progress:

```
Generic Autoresearch Progress:
- [ ] Phase 1: Frame (define scope, generate coverage checklist, establish baseline understanding)
- [ ] Phase 2: Plan (rank research questions by expected impact)
- [ ] Phase 3: Loop (iterate until coverage complete or max reached)
- [ ] Phase 4: Report (final synthesized knowledge artifact)
```

### Phase 1: Frame

1. Restate the topic as a clear **research objective** (what the user will know after this completes)
2. Identify the **topic type** to select the right coverage template:
   - **Domain exploration**: understanding a field, technology, or concept
   - **Approach evaluation**: comparing strategies, architectures, or methods
   - **Application modeling**: designing a system, product, or workflow
   - **Skill development**: learning how to improve at something
   - **General inquiry**: anything else
3. Generate the **coverage checklist** — a list of specific aspects that must be addressed for the research to be complete

References: [coverage-model](references/coverage-model.md)

4. Do ONE initial web search to establish **baseline understanding** — what's easily available vs what requires digging
5. Write the initial `.autoresearch-knowledge.md` file with:
   - Research objective
   - Coverage checklist (all items unchecked)
   - Baseline findings
   - Source log (URLs with brief descriptions)

### Phase 2: Plan

1. Read `.autoresearch-knowledge.md` (learn from current state)
2. For each uncovered checklist item, estimate:
   - **Expected difficulty**: easy (1 search), moderate (2-3 searches), hard (requires cross-referencing)
   - **Dependencies**: does covering X require first covering Y?
3. Rank items: easy + high-impact first, hard + niche last
4. Identify likely source categories per item (official docs, practitioner blogs, academic papers, community discussions)

### Phase 3: Loop

Each iteration:

1. Read `.autoresearch-knowledge.md` and `.autoresearch-results.tsv` (learn from past iterations)
2. Select the highest-priority uncovered checklist item
3. Formulate 1-2 targeted search queries
4. Execute web searches (WebSearch) and fetch key pages (WebFetch)
5. Evaluate source quality and extract findings

References: [loop-protocol](references/loop-protocol.md)

6. **Validate findings**:
   - Claim supported by 2+ independent sources? -> **validated** (add to knowledge artifact)
   - Claim from 1 credible source only? -> **provisional** (add with caveat, flag for future validation)
   - Claim contradicted by other sources? -> **contested** (present both sides)
   - No useful findings? -> **gap** (note it, move on)
7. Update `.autoresearch-knowledge.md`:
   - Add validated/provisional/contested findings under the relevant checklist item
   - Check off the item if sufficiently covered
   - Update the source log
8. Append result to `.autoresearch-results.tsv`

**On 3 consecutive gaps**: re-evaluate approach. Try different search strategies, broader framing, or adjacent topics. If still stuck after 1 more attempt, mark those items as "insufficient sources available" and move on.

**Stop conditions** (any of):
- All checklist items covered
- Max iterations reached
- 3 consecutive gap iterations with no recovery

### Phase 4: Report

Present the final knowledge artifact to the user:

```markdown
## Generic Autoresearch Results

**Topic**: <research objective>
**Iterations**: <completed> / <max>
**Coverage**: <checked items> / <total items> (<percentage>%)
**Depth**: <standard|deep>

### Coverage Summary
- [x] <item>: <1-sentence summary of findings>
- [x] <item>: <1-sentence summary>
- [ ] <item>: <why uncovered — insufficient sources / out of scope / blocked by X>

### Knowledge Artifact

<The full synthesized findings, organized by coverage checklist items.
Each section includes:
- Key findings (validated claims with source citations)
- Provisional findings (single-source claims, flagged)
- Contested areas (conflicting information, both sides presented)
- Practical implications (so what? what does this mean for the user?)>

### Source Quality Summary
- **High confidence**: <N> findings from 2+ independent sources
- **Provisional**: <N> findings from single credible source
- **Contested**: <N> areas with conflicting information

### Sources
<All URLs cited, grouped by type:>

#### Official / Authoritative
- [Title](url) — <brief note>

#### Practitioner / Experience
- [Title](url) — <brief note>

#### Community / Discussion
- [Title](url) — <brief note>

### Iteration Log
<Summary of what each iteration explored and found>

### Suggested Follow-Up
- <What to research next if the user wants to go deeper>
- <Related topics that surfaced during research>
- <Questions that emerged but were out of scope>
```

## Results log format

Tab-separated, one row per iteration in `.autoresearch-results.tsv`:

```
iteration	checklist_item	sources_found	findings_status	description
```

Status values: `validated`, `provisional`, `contested`, `gap`, `skipped`

## Safety

- NEVER fabricate sources or URLs — only cite pages actually found via search
- NEVER present provisional findings as validated
- NEVER skip contradictory evidence — contested claims must show both sides
- If a topic veers into harmful territory (weapons, exploitation, etc.), stop and explain why
- Always note when information might be outdated (check publication dates)

## Anti-Patterns

- **Don't boil the ocean**: Each iteration tackles ONE checklist item, not everything at once
- **Don't repeat failed searches**: Read the results log; try different queries or angles
- **Don't mistake quantity for quality**: 2 validated findings beat 10 unverified claims
- **Don't ignore the "so what"**: Every finding should connect to practical implications
- **Don't abandon structure**: Even if findings are sparse, maintain the checklist-driven organization

## Example Invocations

```
/generic-autoresearch "event-driven architecture patterns for distributed systems"
/generic-autoresearch "how to design a CLI tool UX" max=12 depth=deep
/generic-autoresearch "Rust vs Go for network services — when to pick which"
/generic-autoresearch "improving Claude Code skills — patterns and anti-patterns"
/generic-autoresearch "building a personal knowledge management system"
/generic-autoresearch "OAuth 2.1 changes and migration considerations"
```
