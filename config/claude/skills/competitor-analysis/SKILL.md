---
name: competitor-analysis
description: >
  Comprehensive competitor research using a 7-agent team. Spawns parallel research agents
  for product, marketing, UX, and technical analysis, then sequential synthesis agents for
  MVP spec, go-to-market strategy, and competitive landscape. Use when evaluating a competitor,
  planning a new product, or scoping an MVP. Keywords: competitor, competitive analysis,
  market research, product research, MVP, go-to-market, GTM, teardown, product teardown
context: fork
disable-model-invocation: true
argument-hint: [url-or-company-name]
---

# Competitor Analysis

Orchestrate 7 research agents to produce a comprehensive competitor teardown. Phase 1 runs 4 parallel research agents (Product, Marketing, UX, Technical). Phase 2 runs 3 sequential synthesis agents (MVP Spec, GTM Strategy, Competitive Landscape) that build on Phase 1 findings.

## Workflow

### 1. Parse Input

**Target: `$ARGUMENTS`**

If the target above is non-empty, use it immediately — do NOT ask the user to confirm or re-provide it. Parse it as follows:

- **URL** (starts with `http`): use as-is for WebFetch, extract company name from domain
- **Company name** (no URL): construct likely URLs (`https://{name}.com`, `https://www.{name}.com`)

If the target above is empty, ask the user what competitor to analyze and wait for their response.

Store the parsed values:
- `COMPANY_NAME`: Human-readable name (e.g., "Linear")
- `PRIMARY_URL`: Main product URL (e.g., "https://linear.app")

**IMPORTANT**: When a target is provided, begin Phase 2 immediately after parsing. Do not pause for user input.

### 2. Phase 1 — Parallel Research Agents

Spawn 4 agents in parallel using the Task tool. Each agent is `general-purpose` (needs WebSearch + WebFetch). Run all 4 with `run_in_background: true` for maximum parallelism.

Read [REFERENCE.md](REFERENCE.md) first to get the detailed research checklists and output templates for each agent.

#### Agent 1: Product Overview

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a product research analyst. Research {COMPANY_NAME} ({PRIMARY_URL}) and produce
a comprehensive product overview.

Follow the "Product Overview Agent" template in the reference below. Use WebSearch and
WebFetch to gather information. Cite sources for every claim.

{paste Product Overview section from REFERENCE.md}
```

#### Agent 2: Marketing Analysis

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a marketing strategist. Research {COMPANY_NAME}'s marketing and positioning.

Follow the "Marketing Analysis Agent" template in the reference below. Use WebSearch and
WebFetch to analyze their marketing channels, messaging, and content strategy.

{paste Marketing Analysis section from REFERENCE.md}
```

#### Agent 3: UX Analysis

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a UX researcher. Analyze the user experience of {COMPANY_NAME} ({PRIMARY_URL}).

Follow the "UX Analysis Agent" template in the reference below. Use WebFetch to walk
through their signup flow, onboarding, and core product experience.

{paste UX Analysis section from REFERENCE.md}
```

#### Agent 4: Technical Stack

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a technical researcher. Investigate the technology stack behind {COMPANY_NAME}.

Follow the "Technical Stack Agent" template in the reference below. Use WebSearch and
WebFetch to analyze their tech choices, APIs, architecture signals, and engineering culture.

{paste Technical Stack section from REFERENCE.md}
```

### 3. Collect Phase 1 Results

Wait for all 4 background agents to complete. Read their output files to collect results.

Compile a **Phase 1 Summary** containing the key findings from each agent. This summary feeds into Phase 2 agents.

### 4. Phase 2 — Sequential Synthesis Agents

Phase 2 agents run sequentially because each builds on prior results. These are NOT background agents — wait for each to complete before spawning the next.

Read [REFERENCE.md](REFERENCE.md) for detailed templates.

#### Agent 5: MVP Specification

```
subagent_type: general-purpose
```

Prompt:

```
You are a product strategist. Based on the competitor research below, define an MVP
specification for a product that competes with {COMPANY_NAME}.

## Phase 1 Research Findings
{paste compiled Phase 1 findings}

Follow the "MVP Specification Agent" template in the reference below.

{paste MVP Specification section from REFERENCE.md}
```

#### Agent 6: Go-to-Market Strategy

```
subagent_type: general-purpose
```

Prompt:

```
You are a go-to-market strategist. Based on the competitor research and MVP spec below,
design a go-to-market strategy for competing with {COMPANY_NAME}.

## Phase 1 Research Findings
{paste compiled Phase 1 findings}

## MVP Specification
{paste Agent 5 output}

Follow the "Go-to-Market Strategy Agent" template in the reference below.

{paste GTM Strategy section from REFERENCE.md}
```

#### Agent 7: Competitive Landscape

```
subagent_type: general-purpose
```

Prompt:

```
You are a market analyst. Based on all prior research, map the competitive landscape
around {COMPANY_NAME} and identify differentiation opportunities.

## Phase 1 Research Findings
{paste compiled Phase 1 findings}

## MVP Specification
{paste Agent 5 output}

## Go-to-Market Strategy
{paste Agent 6 output}

Follow the "Competitive Landscape Agent" template in the reference below.

{paste Competitive Landscape section from REFERENCE.md}
```

### 5. Final Synthesis

Combine all 7 agent outputs into a single report. Present to the user with this structure:

```markdown
# Competitor Teardown: {COMPANY_NAME}

## Executive Summary
[3-5 bullet points: what they do, how they win, where they're vulnerable]

## Table of Contents
1. Product Overview
2. Marketing Analysis
3. UX Analysis
4. Technical Stack
5. MVP Specification
6. Go-to-Market Strategy
7. Competitive Landscape

---

[Agent 1 output — Product Overview]

---

[Agent 2 output — Marketing Analysis]

---

[Agent 3 output — UX Analysis]

---

[Agent 4 output — Technical Stack]

---

[Agent 5 output — MVP Specification]

---

[Agent 6 output — Go-to-Market Strategy]

---

[Agent 7 output — Competitive Landscape]

---

## Key Takeaways

### Top 3 Opportunities
1. [Biggest gap or underserved segment]
2. [Second opportunity]
3. [Third opportunity]

### Top 3 Risks
1. [Biggest risk in competing]
2. [Second risk]
3. [Third risk]

### Recommended Next Steps
1. [Most important action]
2. [Second action]
3. [Third action]
```

## Example Invocations

```
/competitor-analysis https://linear.app
/competitor-analysis Notion
/competitor-analysis https://www.figma.com
/competitor-analysis Vercel
```

## Anti-Patterns

- **Don't skip Phase 1 before Phase 2**: Synthesis agents need research findings to produce useful output. Never run Phase 2 agents without passing them Phase 1 results.
- **Don't use Explore agents**: Sub-agents need WebSearch and WebFetch for external research. Use `general-purpose` only.
- **Don't collapse agents**: Each agent has a distinct research lens. Combining them loses depth.
- **Don't fabricate data**: If an agent can't find information (e.g., pricing not public), it should say so explicitly rather than guessing.
- **Don't skip citations**: Every factual claim must reference a source URL or page.
- **Don't run Phase 2 in parallel**: Agent 6 needs Agent 5's output, Agent 7 needs both.

## Notes

- Total runtime is typically 3-8 minutes depending on the target's web presence.
- Phase 1 agents run in background for parallelism; Phase 2 agents run sequentially.
- If a Phase 1 agent fails or returns thin results, note the gap in the final report rather than blocking Phase 2.
- For private/stealth companies with minimal web presence, agents will produce thinner reports — this is expected.
