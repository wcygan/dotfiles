---
name: web-research
description: >
  Research any topic via web search and synthesize findings into a structured, actionable report.
  Spawns parallel research agents to gather diverse perspectives, cross-references sources,
  and progressively builds context from fundamentals to nuance. Use when investigating a technology,
  comparing approaches, evaluating tools, understanding best practices, or learning about any
  technical or non-technical topic. Keywords: research, web search, investigate, compare, evaluate,
  learn, best practices, how does, what is, pros cons, trade-offs, state of the art
context: fork
disable-model-invocation: true
argument-hint: [topic to research]
---

# Web Research

Research a topic thoroughly using web search, synthesize findings from multiple sources and perspectives, and present a progressively-built report that starts with fundamentals and builds to nuanced analysis.

**Target: `$ARGUMENTS`**

If the target above is non-empty, begin research immediately. If empty, ask the user what to research.

## Workflow

### 1. Scope the Research

Parse `$ARGUMENTS` to identify:

- **Core topic**: The central subject to investigate
- **Implicit questions**: What the user likely wants to know (how, why, trade-offs, alternatives)
- **Context clues**: Any technology stack, version, or constraint mentioned

Define 3-5 research questions that together would give a comprehensive understanding. Order them from foundational to advanced.

### 2. Parallel Research Phase

Spawn 2-3 research agents in parallel using the Task tool (`subagent_type: general-purpose`, `run_in_background: true`). Each agent takes a different research angle.

Read [research-methodology.md](references/research-methodology.md) for detailed agent prompts and search strategies.

**Agent assignments** (adapt based on topic):

| Agent | Angle | Focus |
|-------|-------|-------|
| Agent 1: Foundations | Official sources, documentation, specs | What it is, how it works, canonical usage |
| Agent 2: Practitioner Perspective | Blog posts, tutorials, conference talks, Reddit/HN | Real-world experience, gotchas, opinions |
| Agent 3: Comparative Analysis | Alternatives, benchmarks, trade-off discussions | How it compares, when to use what |

Each agent must follow the source evaluation and citation rules in [source-evaluation.md](references/source-evaluation.md).

### 3. Collect and Cross-Reference

After all agents complete:

1. Read their outputs
2. Identify areas of **agreement** (high-confidence findings)
3. Identify areas of **disagreement** (flag as contested, present both sides)
4. Note **gaps** where information was thin or unavailable
5. Resolve contradictions by preferring higher-quality sources (see [source-evaluation.md](references/source-evaluation.md))

### 4. Synthesize the Report

Build the report progressively using the structure in [synthesis-patterns.md](references/synthesis-patterns.md). The key principle: **start simple, add layers**.

Present the final report to the user using this structure:

```markdown
# Research: {topic}

## TL;DR
{3-5 bullet points capturing the most important takeaways. A busy reader should get 80% of the value here.}

## Foundations
{What it is, why it exists, core concepts. Assume the reader is smart but unfamiliar.}

## How It Works
{Mechanics, architecture, key patterns. Include code/config examples where applicable.}

## The Practitioner View
{What real users say. Common patterns, surprising gotchas, hard-won lessons from production use. Include direct quotes or paraphrases with attribution.}

## Trade-offs & Alternatives
{Honest comparison with alternatives. When to use this vs something else. Present as a decision framework, not a recommendation.}

## Best Practices
{Industry consensus on how to use it well. Distinguish between "universally agreed" and "one school of thought."}

## Gotchas & Caveats
{Things that bite people. Version-specific issues, common misconfigurations, performance cliffs, security considerations.}

## Open Questions & Evolving Areas
{What's still being figured out. Active debates, upcoming changes, areas where best practices haven't solidified.}

## Sources
{All sources cited in the report, grouped by type}

### Official Documentation
- [Title](url) — {brief note on what was used from this source}

### Blog Posts & Tutorials
- [Title](url) — {author, date if known, brief note}

### Community Discussions
- [Title](url) — {platform, date if known, brief note}

### Research & Benchmarks
- [Title](url) — {brief note}
```

### 5. Quality Check

Before presenting the report, verify:

- [ ] Every factual claim has a cited source
- [ ] Contested points present multiple perspectives
- [ ] The report builds progressively (a reader can stop at any section and have a coherent understanding)
- [ ] Code examples are realistic and runnable (not pseudo-code unless labeled)
- [ ] Dates and versions are noted where relevant
- [ ] No hallucinated URLs — only cite pages actually fetched or found via search

## Example Invocations

```
/web-research Rust async best practices 2025
/web-research Kubernetes ingress controller comparison
/web-research PostgreSQL connection pooling strategies
/web-research when to use SQLite vs Postgres for web apps
/web-research state of WebAssembly for server-side 2026
/web-research nix flakes best practices and common patterns
```

## Anti-Patterns

- **Don't present a single perspective as truth**: Always note when something is opinion vs consensus
- **Don't skip the foundations**: Even for advanced topics, ground the reader first
- **Don't fabricate sources**: If you can't find info, say so — gaps are data
- **Don't overwhelm with quantity**: Prioritize signal over completeness
- **Don't ignore recency**: Note when information might be outdated
- **Don't skip practitioner voices**: Official docs tell you how; practitioners tell you what actually works
