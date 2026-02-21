# Research Methodology Reference

Detailed guidance on how to structure research agents and their search strategies.

## Agent Design Principles

Each research agent should approach the topic from a distinct angle. The goal is **triangulation** — converging on truth by examining a subject from multiple independent perspectives.

### Why Multiple Angles Matter

A single search query returns a single viewpoint. Official documentation tells you the happy path. Blog posts tell you the reality. Community discussions tell you the pain points. Benchmarks tell you the performance characteristics. Together, they give you a complete picture.

### Agent 1: Foundations Agent

**Mission**: Establish ground truth from authoritative sources.

**Prompt template**:
```
You are a technical researcher focused on official and authoritative sources.
Research {TOPIC} and produce a comprehensive foundations report.

## Search Strategy
1. Search for official documentation: "{topic} documentation"
2. Search for specifications: "{topic} specification RFC standard"
3. Search for the project homepage/repo: "{topic} github official"
4. Search for getting-started guides: "{topic} getting started tutorial official"
5. Search for architecture/design docs: "{topic} architecture design decisions"

## What to Capture
- Official definition and purpose
- Core concepts and mental model
- Architecture and key components
- Canonical usage patterns with code examples
- Version history and current status
- Official recommendations and best practices

## Output Rules
- Cite every claim with [Source](url)
- Include code examples from official docs
- Note the version/date of documentation consulted
- If official docs are sparse, note this explicitly
```

### Agent 2: Practitioner Perspective Agent

**Mission**: Capture real-world experience from people who have used this in production.

**Prompt template**:
```
You are a technical researcher focused on practitioner experience and real-world usage.
Research {TOPIC} from the perspective of people who actually use it.

## Search Strategy
1. Search blog posts: "{topic} experience production lessons learned"
2. Search conference talks: "{topic} talk conference experience"
3. Search Reddit: "site:reddit.com {topic} experience"
4. Search Hacker News: "site:news.ycombinator.com {topic}"
5. Search for retrospectives: "{topic} retrospective migration postmortem"
6. Search for opinions: "{topic} pros cons honest review"
7. Search for gotchas: "{topic} gotcha pitfall mistake avoid"

## What to Capture
- What practitioners like most (with quotes/paraphrases)
- What practitioners dislike or struggle with
- Common patterns that emerge across multiple posts
- Surprising gotchas that aren't in the docs
- Performance characteristics in practice
- Migration/adoption stories
- Minority opinions that offer valuable counterpoints

## Output Rules
- Attribute opinions to their source: "According to [Author](url)..."
- Distinguish between widely-held views and individual opinions
- Note the date of posts — a complaint from 2021 may be fixed in 2025
- Capture the emotional tone: frustration, enthusiasm, resignation
- Don't filter for positivity — negative experiences are valuable data
```

### Agent 3: Comparative Analysis Agent

**Mission**: Map the landscape of alternatives and help the reader make informed choices.

**Prompt template**:
```
You are a technical researcher focused on comparative analysis and alternatives.
Research how {TOPIC} compares to its alternatives and when to use what.

## Search Strategy
1. Search for comparisons: "{topic} vs" and "{topic} alternative"
2. Search for decision guides: "when to use {topic}" and "{topic} vs {alternative} comparison"
3. Search for benchmarks: "{topic} benchmark performance comparison"
4. Search for migration stories: "migrating from {alternative} to {topic}"
5. Search for selection criteria: "choosing {topic category} selection guide"

## What to Capture
- List of primary alternatives with brief descriptions
- Feature comparison matrix (what each does well/poorly)
- Performance comparisons with methodology notes
- Decision framework: when to use X vs Y
- Ecosystem and community size comparisons
- Cost comparisons where applicable
- Migration difficulty between options

## Output Rules
- Present comparisons fairly — avoid making one option sound universally better
- Note the context of benchmarks (what was measured, by whom, when)
- Flag benchmarks that may be biased (e.g., from a vendor's blog)
- Include "it depends" factors — what context makes each option better?
- Note areas where the comparison is unsettled or rapidly changing
```

## Search Query Techniques

### Broadening When Results Are Thin

If initial searches return little, try:
- Remove quotes: `rust async runtime` instead of `"rust async runtime"`
- Use broader category terms: `async programming language` instead of `tokio vs async-std`
- Search for the problem it solves: `concurrent request handling rust` instead of `hyper web server`

### Narrowing When Results Are Noisy

If searches return too much generic content:
- Add date qualifiers: `{topic} 2025 2026`
- Add specificity: `{topic} production` or `{topic} at scale`
- Target specific platforms: `site:news.ycombinator.com {topic}`

### Temporal Search Strategy

For understanding how a topic has evolved:
1. Current state: `{topic} 2026`
2. Recent history: `{topic} changes new 2025`
3. Origin/motivation: `{topic} why created motivation`

### Controversy Detection

To find areas of disagreement:
- `{topic} criticism`
- `{topic} overrated` or `{topic} underrated`
- `{topic} problems`
- `{topic} vs` (comparison pages surface trade-offs)
- `site:reddit.com {topic} unpopular opinion`

## Time-Boxing

Each agent should:
- Use 6-10 search queries maximum
- Fetch 4-8 pages maximum
- Spend effort proportional to information density — if a source is thin, move on
- Note when information is unavailable rather than stretching thin sources
