---
title: Brainstorm Workflow
description: Step-by-step orchestration for the brainstorming process
tags: [workflow, orchestration, steps, process]
---

# Brainstorm Workflow

## Step 1: Frame the Decision (Before Spawning Agents)

This is the most critical step. A poorly framed question produces confident-sounding but unhelpful analysis.

### Restate the decision clearly

Transform vague requests into precise decision statements:
- "Should we refactor this?" -> "Should we extract the payment processing logic from the monolithic OrderService into a separate module/service, given that we need to add Stripe and PayPal support in Q2?"

### Identify initial options

List 2-4 approaches that are obviously on the table. Agents will add more.

### Prioritize quality attributes

Which of these matter most for THIS decision?
- Performance (latency, throughput, resource usage)
- Security (attack surface, data protection, compliance)
- Maintainability (readability, testability, modularity)
- Developer experience (learning curve, debugging, onboarding)
- Operability (deployment, monitoring, incident response)
- Cost (infrastructure, development time, licensing)
- Scalability (horizontal, vertical, data growth)
- Availability (uptime, failover, degradation)

### State constraints

What's non-negotiable?
- Timeline
- Team size and expertise
- Existing technology commitments
- Compliance requirements
- Budget

---

## Step 2: Spawn Agents

### Always spawn (3 agents minimum):

**Explorer** (subagent_type: Explore):
```
Provide: decision statement, relevant code areas to inspect, what facts to gather
```

**Analyst** (subagent_type: general-purpose):
```
Provide: decision statement, list of options, priority quality attributes, constraints
```

**Critic** (subagent_type: general-purpose):
```
Provide: decision statement, which option seems to be "winning," pre-mortem instructions
```

### Conditionally spawn:

**Scout** (subagent_type: general-purpose) — when:
- Technology selection is involved
- The user asks "what else could we do?"
- The options are all variations of the same approach
- The domain is unfamiliar

### Spawn all agents in ONE parallel Task tool call

This is critical for performance. All agents are independent — they don't need each other's output.

### Agent prompts should include:

1. The full framed decision (from Step 1)
2. Their specific mandate and output format (from agent-roles.md)
3. Explicit boundaries (what NOT to do — prevents overlap)
4. Relevant starting points in the codebase (if known from the user's question)

---

## Step 3: Synthesize Findings

After all agents return:

### Cross-reference

- Do Explorer findings support or contradict Analyst scores?
- Does the Critic's pre-mortem reveal risks the Analyst missed?
- Did the Scout find options that change the trade-off landscape?

### Resolve contradictions

When agents disagree:
- State the disagreement explicitly
- Identify what assumptions drive the disagreement
- Use WWHTBT to frame it: "If Explorer is right that [X], then Option A; if Analyst is right that [Y], then Option B"

### Build the output

Follow the output template (see output-templates.md):
1. TL;DR recommendation
2. Trade-off matrix (synthesized from Analyst)
3. WWHTBT (synthesized from Analyst + Critic)
4. Risk register (from Critic)
5. ADR-ready summary

---

## Calibration Guidelines

### When to use 3 agents (default)

- Most architectural decisions
- Technology choice between 2-3 options
- Refactoring strategy decisions
- API design choices

### When to add the Scout (4 agents)

- Greenfield technology selection
- "We're stuck between bad options"
- Unfamiliar problem domain
- User explicitly asks for alternatives

### When NOT to brainstorm (just answer directly)

- Single correct answer exists (e.g., "which sort algorithm for 10 items?")
- Decision is easily reversible and low-impact
- User already knows what they want and just needs implementation help
