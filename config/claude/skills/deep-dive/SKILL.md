---
name: deep-dive
description: >
  Deep dive into a codebase to understand specific topics, patterns, or
  implementations. Spawns parallel agents with distinct investigation strategies
  (breadth-first mapping, depth-first tracing, optional history/boundary analysis)
  then synthesizes findings into a layered summary. Use for understanding how
  something works, exploring unfamiliar code, or building a mental model of a
  large system. Keywords: deep dive, explore, understand, how does, architecture,
  codebase exploration, trace, investigate, mental model
disable-model-invocation: true
argument-hint: [topic or question about the codebase]
---

# Deep Dive

Investigate: **$ARGUMENTS**

## Agent Strategy

Every deep dive uses two core agents in parallel, plus optional specialists based on the query.

### Core Agents (always spawn)

| Agent | Role | Strategy |
|-------|------|----------|
| **Scout** | Breadth-first explorer | Maps file structure, identifies hot spots, builds topology |
| **Tracer** | Depth-first investigator | Picks entry points, follows call chains deep into the stack |

### Optional Agents (spawn when relevant)

| Agent | When to spawn | Strategy |
|-------|---------------|----------|
| **Archaeologist** | Query involves "why", history, or decisions | Digs through git blame/log for intent behind code |
| **Boundary Mapper** | Query involves integrations, APIs, or "what connects to" | Maps module boundaries, API surfaces, integration seams |

References: [breadth-first-agent](references/breadth-first-agent.md), [depth-first-agent](references/depth-first-agent.md), [context-archaeologist](references/context-archaeologist.md), [boundary-mapper](references/boundary-mapper.md)

## Decision: Which Agents to Spawn

Read the user's query and decide:

1. **Always** spawn Scout + Tracer (2 agents minimum)
2. Add **Archaeologist** if the query asks *why* something exists, when it changed, or what motivated a design
3. Add **Boundary Mapper** if the query asks about connections, integration points, API surfaces, or module interactions
4. **Maximum 4 agents** — never more

## Execution

### 1. Analyze the Query

Before spawning agents, identify:
- **Target area**: What part of the codebase to explore
- **Depth level**: Quick overview vs. deep investigation
- **Query type**: "How does X work?" vs. "Why is X like this?" vs. "What connects to X?"

### 2. Spawn Agents in Parallel

Use Task tool with `subagent_type=Explore` for each agent. Give each agent:
- The user's query for context
- Their specific investigation strategy (from reference files)
- Concrete starting points if you can infer them from the query

### 3. Synthesize

After all agents return, combine their findings using the Investigation Summarizer approach.

References: [investigation-summarizer](references/investigation-summarizer.md), [output-format](references/output-format.md)

## Output

Present findings in the **layered format** — TL;DR first, then progressively detailed sections. The user should get the gist from the first 3 sentences and can read deeper as needed.

References: [output-format](references/output-format.md)

## Anti-Patterns

- **Don't spawn 4 agents for a simple "where is X defined?" question** — use Grep directly
- **Don't let agents read the same files** — Scout maps topology, Tracer goes deep; they cover different ground
- **Don't skip the synthesis step** — raw agent outputs are disjointed; the summary is the value
- **Don't present findings without file:line references** — every claim needs a source
