# Synthesis Patterns Reference

How to progressively build context and present research findings in a digestible way.

## The Progressive Disclosure Principle

The report should work like a funnel: wide at the top (simple, high-level), narrow at the bottom (specific, nuanced). A reader should be able to stop at any section and have a coherent — if incomplete — understanding.

### Layer 1: TL;DR (10 seconds)
The reader gets 80% of the value in 3-5 bullet points. Each bullet is a complete thought. If they read nothing else, they can make a basic decision or hold a conversation.

**Good TL;DR bullet**:
```markdown
- Connection pooling (via PgBouncer or built-in) is essential for production
  Postgres — raw connections don't scale past ~100 concurrent users
```

**Bad TL;DR bullet**:
```markdown
- Connection pooling is important for databases
```

### Layer 2: Foundations (2 minutes)
The reader understands what this thing is, why it exists, and the core mental model. No jargon that hasn't been introduced. This section should make sense to a smart generalist.

**Techniques**:
- Define terms on first use
- Use analogies to familiar concepts
- Explain the "why" before the "how"
- One concept per paragraph

### Layer 3: How It Works (5 minutes)
The reader understands the mechanics. Include code examples, diagrams (described in text), and concrete illustrations. This section assumes the reader understood Layer 2.

**Techniques**:
- Start with the common/default case
- Show a minimal working example
- Then layer in configuration, options, and customization
- Use "here's the simple version... here's what changes at scale" structure

### Layer 4: Practitioner View (5 minutes)
The reader understands what real usage looks like. This is where opinions, experiences, and gotchas live. The reader should come away thinking "now I know what to watch out for."

**Techniques**:
- Lead with the most common real-world pattern
- Quote or paraphrase practitioners with attribution
- Group experiences by theme (performance, DX, debugging, etc.)
- Distinguish "everyone agrees" from "some people find"

### Layer 5: Trade-offs & Nuance (5 minutes)
The reader can make an informed decision. Present alternatives fairly. Provide a decision framework, not a recommendation (unless the consensus is overwhelming).

**Techniques**:
- Use comparison tables for structured data
- Present decision criteria as questions ("If you need X, consider Y")
- Acknowledge that context matters
- Include the "it depends" factors explicitly

## Structuring Information Within Sections

### The Inverted Pyramid

Within each section, put the most important information first:

```
Most important finding
├── Supporting detail
├── Supporting detail
└── Example or evidence

Second most important finding
├── Supporting detail
└── Example or evidence

Additional context
└── Edge case or nuance
```

### Tables for Structured Comparisons

When comparing options, tools, or approaches, use tables:

```markdown
| Factor | Option A | Option B | When It Matters |
|--------|----------|----------|----------------|
| Performance | Faster for reads | Faster for writes | High-throughput systems |
| Complexity | Simpler setup | More configuration | Team experience level |
| Ecosystem | Larger community | Better docs | Long-term maintenance |
```

Always include a "When It Matters" or "Context" column to help the reader apply the comparison to their situation.

### Callout Patterns

Use emphasis to signal information type:

```markdown
**Key insight**: {The single most important thing in this section}

**Common pattern**: {What most people do}

**Gotcha**: {Something that catches people off guard}

**Contested**: {Where experts disagree — both sides presented}

**Note**: {Version-specific or context-specific information}
```

## Connecting the Dots

### Cross-Referencing Within the Report

Tie sections together so the report reads as a narrative, not a collection of fragments:

```markdown
## Trade-offs & Alternatives

As noted in the Foundations section, {topic} was designed for {use case}.
This design choice means it excels at {strength} but struggles with {weakness},
which is why practitioners (see Practitioner View) often reach for {alternative}
when {specific context}.
```

### Building on Previous Context

Each section should reference what came before without repeating it:

```markdown
## Gotchas & Caveats

Given the architecture described above (single-writer, multiple-reader),
the most common gotcha is...
```

### Signposting for Skimmers

Use section intros that tell the reader what they'll learn:

```markdown
## How It Works

This section covers the three core concepts you need to understand:
connection lifecycle, query planning, and the write-ahead log.
```

## Handling Different Topic Types

### Technology Evaluation Topics
*"Should we use X?"*

Emphasize: trade-offs, alternatives, decision framework, real-world experience.
De-emphasize: exhaustive feature lists, historical background.

### How-To Topics
*"How does X work?"*

Emphasize: mechanics, code examples, common patterns, gotchas.
De-emphasize: alternatives (mention briefly), market landscape.

### Comparison Topics
*"X vs Y"*

Emphasize: fair comparison matrix, decision criteria, context-dependent recommendations.
De-emphasize: deep dives into either option individually (link to further reading).

### State-of-the-Art Topics
*"What's the current state of X?"*

Emphasize: recent developments, active debates, evolving best practices, what's changed recently.
De-emphasize: settled fundamentals (summarize briefly).

## Quality Signals in the Final Report

A well-synthesized report should have:

- **No orphan claims**: Every statement either cites a source or is labeled as common knowledge
- **No false consensus**: Disagreements are surfaced, not papered over
- **No recency blindness**: Dates and versions are noted for time-sensitive information
- **Progressive depth**: Each section adds a layer; none repeat previous sections
- **Actionable framing**: The reader finishes knowing what to do, not just what exists
- **Honest gaps**: "I couldn't find information on X" is better than silence or speculation
