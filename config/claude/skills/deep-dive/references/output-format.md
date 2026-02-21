# Output Format: Layered Summary

Progressive disclosure — the reader gets value at every level of depth.

## Template

```markdown
# Deep Dive: [Topic]

## TL;DR
[3 sentences max. A reader who stops here should understand the core answer.]

## Key Findings
- [Finding 1 with `file:line` reference]
- [Finding 2 with `file:line` reference]
- [Finding 3 with `file:line` reference]
[5-8 bullets maximum]

## How It Works
[Narrative walkthrough of the primary flow. Include the annotated call chain
from the Tracer. Use code snippets for non-obvious logic.]

### Entry Point
`function_name` at `file.ext:line`
[What triggers this and what it does]

### Core Logic
[The interesting part — where the real work happens]

### Output / Side Effects
[What the result is, what state changes, what gets written/sent]

## File Map
| File | Purpose | Hot Spot? |
|------|---------|-----------|
| `path/to/file.ext` | [one-line description] | Yes/No |
[Include all files explored by any agent]

## Architecture
[ASCII diagram if the relationships are non-trivial]

```
[Component A] → [Component B] → [Component C]
       ↓                              ↑
[Component D] ─────────────────────────┘
```

[Brief explanation of the diagram]

## Why It's This Way
[Only if the Archaeologist was spawned. Key decisions and their motivation.]

## Connections
[Only if the Boundary Mapper was spawned. What connects to this and how.]

## Patterns & Conventions
- [Pattern 1 observed in this area]
- [Pattern 2 observed in this area]
[What a developer should know before modifying this code]

## Open Questions
- [What we didn't investigate]
- [Follow-up topics the user might want to explore]
```

## Depth Adaptation

Not every section is needed for every query. Adapt:

| Query depth | Include |
|------------|---------|
| Quick ("where is X?") | TL;DR + Key Findings + File Map |
| Standard ("how does X work?") | All core sections |
| Deep ("explain X in detail") | All sections + extended code snippets + architecture diagrams |

## Style Rules

- **File references**: Always `file.ext:line` format, backtick-wrapped
- **Code snippets**: Include only the relevant 5-15 lines, not entire functions
- **Diagrams**: ASCII only, keep under 10 lines
- **Bullets over prose**: For lists of facts, use bullets; for explanation, use prose
- **No hedging**: Say "X does Y" not "X appears to do Y" (the agents read the code)
