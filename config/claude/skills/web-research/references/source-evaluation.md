# Source Evaluation & Citation Reference

How to assess source quality, handle conflicting information, and cite properly.

## Official Documentation First

**Always start with official documentation.** Before searching blogs, Reddit, or third-party tutorials, find and read the official docs for the subject. This is the single most important research habit.

### Why Official Docs Are the Starting Point

- They define the **canonical mental model** — how the creators intend the thing to be understood
- They contain the **accurate API surface** — function signatures, config options, defaults
- They reflect the **current state** — maintained projects update docs with each release
- They provide **migration guides** — when behavior changes between versions, docs explain how
- They set the **baseline** — you need to know the official story before you can evaluate practitioner deviations from it

### How to Find Official Docs

For any subject, search in this order:

1. **Project homepage**: `{project name}` — most link to docs directly
2. **Docs subdomain**: `docs.{project}.com` or `{project}.dev`
3. **GitHub/GitLab repo**: README, `/docs` directory, wiki
4. **Language/framework docs**: e.g., `doc.rust-lang.org`, `react.dev`, `go.dev`
5. **Specifications**: RFCs, W3C specs, ECMA standards, IETF drafts
6. **Man pages / CLI help**: `--help` output, man page content referenced in search results

### What to Extract from Official Docs

When reading official documentation, capture:

- **Purpose statement**: What problem does this solve? (usually in the introduction)
- **Core concepts**: The vocabulary and mental model (glossary, concepts pages)
- **Getting started**: The canonical happy path
- **API reference**: Exact behavior, parameters, return values, defaults
- **Configuration**: Available options and their effects
- **Version/changelog**: What's new, what's deprecated, what's removed
- **Known limitations**: Often buried in FAQ, troubleshooting, or "caveats" sections
- **Recommended patterns**: Official best practices or style guides

### When Official Docs Are Insufficient

Official docs don't cover everything. Specifically look beyond them for:

- **Real-world performance characteristics** — docs rarely discuss scale limits honestly
- **Ecosystem opinions** — which plugins/extensions are actually good
- **Migration pain** — adoption stories from practitioners
- **Comparisons with alternatives** — projects don't objectively compare themselves to competitors
- **Edge cases and bugs** — community discussions surface what docs miss
- **Operational concerns** — monitoring, debugging, failure modes in production

Even when docs are insufficient, **anchor your report in what the docs say** and frame practitioner experience as supplementary evidence.

---

## Source Quality Hierarchy

Not all sources are equal. Use this hierarchy when sources conflict:

| Tier | Source Type | Trust Level | Example |
|------|-----------|-------------|---------|
| 1 | Official documentation | Highest | Language specs, framework docs, RFCs |
| 2 | Primary research/benchmarks | High | Peer-reviewed papers, reproducible benchmarks |
| 3 | Authoritative practitioners | High | Core team members, recognized experts with track records |
| 4 | Quality blog posts | Medium | Well-reasoned posts with evidence, from known authors |
| 5 | Community consensus | Medium | Widely upvoted answers, repeated across multiple threads |
| 6 | Individual opinions | Low | Single blog post, single Reddit comment |
| 7 | Marketing material | Lowest | Vendor comparisons, sponsored content |

### When Lower-Tier Sources Beat Higher Ones

- **Recency**: A 2026 blog post may be more accurate than 2022 official docs if the docs haven't been updated
- **Practical experience**: Official docs show the happy path; a production postmortem shows reality
- **Edge cases**: Docs cover common usage; community discussions surface edge cases
- **Honest assessment**: Independent reviewers may be more honest than vendor documentation

## Evaluating Individual Sources

Before citing a source, assess:

### Credibility Signals (positive)
- Author has verifiable expertise (core contributor, published author, recognized in community)
- Post includes reproducible examples or data
- Claims are specific and falsifiable (not vague)
- Post acknowledges limitations and trade-offs
- Multiple independent sources corroborate the claim
- Published by a reputable organization

### Warning Signals (reduce trust)
- No author attribution
- Vendor blog comparing their product to competitors
- No dates or version numbers mentioned
- Sweeping claims without evidence ("X is always better than Y")
- Content appears AI-generated without expert review
- Single anecdotal experience generalized to universal advice

### Red Flags (do not cite without heavy caveats)
- Contradicted by official documentation
- Contains factual errors you can verify
- Heavily promotional with affiliate links
- Outdated by more than 2 years for fast-moving topics
- From a known unreliable source

## Handling Conflicting Information

When sources disagree, do **not** silently pick a winner. Instead:

### 1. Present the Disagreement Explicitly

```markdown
**Contested**: Whether to use pattern X or Y is debated.

- **In favor of X**: [Author A](url) argues that X is better for {reason},
  based on their experience at {company}. This view is shared by
  [Author B](url) who benchmarked both approaches.

- **In favor of Y**: [Author C](url) makes the case for Y, noting that
  {counterargument}. The official docs [recommend Y](url) for {scenario}.

- **Resolution factors**: The choice likely depends on {factor 1} and
  {factor 2}. If your situation involves {context}, X is probably better.
  If {other context}, lean toward Y.
```

### 2. Identify Why Sources Disagree

Common reasons for conflicting information:
- **Different versions**: Feature changed between versions
- **Different contexts**: Advice for small apps vs large apps
- **Different priorities**: Performance-focused vs simplicity-focused
- **Outdated info**: One source is stale
- **Genuine disagreement**: Experts legitimately disagree

### 3. Use Confidence Levels

Attach confidence to synthesized claims:

| Confidence | Meaning | Evidence Needed |
|-----------|---------|----------------|
| **High** | Near-consensus, well-documented | 3+ independent sources agree, or official docs confirm |
| **Medium** | Likely correct, some caveats | 2+ sources agree, but limited counter-evidence exists |
| **Low** | Plausible but uncertain | Single source, or sources conflict significantly |
| **Speculative** | Informed guess | No direct sources; extrapolated from related information |

## Citation Format

### Inline Citations

Use inline markdown links with context:

```markdown
According to the [Rust Async Book](url), the recommended approach is...

[Jane Smith's analysis](url) of 50 production deployments found that...

The [official migration guide](url) (updated January 2026) recommends...
```

### Source Notes

When citing, include contextual information that helps the reader assess the source:

```markdown
- [Title](url) — Jane Smith, Senior Engineer at Company X, March 2025.
  Based on 2 years of production experience with 10M+ requests/day.

- [Title](url) — Official documentation, last updated February 2026.
  Covers v3.x; earlier versions have different behavior.

- [Title](url) — Reddit discussion, 847 upvotes, January 2026.
  Top comment is from a core maintainer confirming the approach.
```

### What Not to Cite

- Do not invent URLs — only cite pages you actually fetched or found via WebSearch
- Do not cite a source for common knowledge ("HTTP uses TCP")
- Do not cite marketing pages as technical evidence
- If you cannot find a source for a claim, say "commonly reported but I could not find a primary source" rather than fabricating a citation

## Representing Opinions vs Facts

### Facts (cite and move on)
```markdown
PostgreSQL supports JSON columns via the `jsonb` type ([docs](url)).
```

### Consensus opinions (present as expert agreement)
```markdown
Most practitioners recommend connection pooling for production PostgreSQL
deployments ([Source 1](url), [Source 2](url), [Source 3](url)).
```

### Contested opinions (present both sides)
```markdown
Whether to use an ORM or raw SQL is actively debated. [Author A](url)
advocates for ORMs citing developer productivity, while [Author B](url)
argues raw SQL gives better performance and debuggability.
```

### Minority opinions (present as counterpoint)
```markdown
While most teams use {X}, [Author](url) makes a compelling case for {Y},
noting that {specific argument}. This is a minority position but worth
considering if {specific context applies}.
```
