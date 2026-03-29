# Output Format: Layered Summary

Progressive disclosure — the reader gets value at every level of depth.

## Sections

- TL;DR (always) — 3 sentences max
- Key Findings (always) — 5-8 bullets with `file:line`
- How It Works (always) — narrative walkthrough with call chain
- File Map (always) — table of explored files
- Architecture (when non-trivial) — ASCII diagram
- Why It's This Way (when Archaeologist spawned) — decisions and motivation
- Connections (when Boundary Mapper spawned) — integration map
- Patterns & Conventions (when relevant) — what to know before modifying
- Open Questions (always) — unexplored areas and follow-ups

## Template

```markdown
# Deep Dive: [Topic]

## TL;DR
[3 sentences max. A reader who stops here should understand the core answer.]

## Key Findings
- [Finding 1 with `file:line` reference]
- [Finding 2 with `file:line` reference]
- [Finding 3 with `file:line` reference]

## How It Works

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

## Architecture
[ASCII diagram if the relationships are non-trivial]

```
[Component A] → [Component B] → [Component C]
       ↓                              ↑
[Component D] ─────────────────────────┘
```

## Why It's This Way
[Only if the Archaeologist was spawned.]

## Connections
[Only if the Boundary Mapper was spawned.]

## Patterns & Conventions
- [Pattern 1 observed in this area]
- [Pattern 2 observed in this area]

## Open Questions
- [What we didn't investigate]
- [Follow-up topics the user might want to explore]
```

## Depth Adaptation

| Query depth | Include |
|------------|---------|
| Quick ("where is X?") | TL;DR + Key Findings + File Map |
| Standard ("how does X work?") | All core sections |
| Deep ("explain X in detail") | All sections + extended code snippets + architecture |

## Style Rules

- **File references**: Always `file.ext:line` format, backtick-wrapped
- **Code snippets**: Only the relevant 5-15 lines, not entire functions
- **Diagrams**: ASCII only, keep under 10 lines
- **Bullets over prose**: For lists of facts, use bullets; for explanation, use prose
- **No hedging**: Say "X does Y" not "X appears to do Y" (the agents read the code)
