---
title: Agent Roles
description: Detailed mandates, prompt templates, and output formats for each brainstorming agent
tags: [agents, roles, six-thinking-hats, mandates]
---

# Agent Roles

Based on Edward de Bono's Six Thinking Hats framework, adapted for software decision-making.
See: https://thedecisionlab.com/reference-guide/organizational-behavior/six-thinking-hats

## Explorer (White Hat — Facts & Data)

**Mandate**: Gather facts. No opinions, no recommendations — just evidence from the codebase.

**Subagent type**: `Explore`

**Prompt template**:

```
We are evaluating: [DECISION]

Your role is EXPLORER — gather facts only. Investigate:

1. Current architecture relevant to this decision
   - Which modules, files, interfaces are involved?
   - What patterns are already established?
   - What dependencies exist?

2. Existing constraints the codebase reveals
   - Prior architectural decisions that constrain options
   - Test coverage in affected areas
   - Coupling and cohesion patterns

3. Prior art in this codebase
   - Have similar decisions been made before? What was chosen?
   - Are there TODOs, FIXMEs, or comments expressing regret about past choices?

Output format:
- File:line references for every claim
- Organize by: Architecture, Constraints, Prior Art
- Flag ambiguities or areas needing more investigation
- Do NOT make recommendations — just report facts
```

---

## Analyst (Yellow + Blue Hat — Benefits & Process)

**Mandate**: Evaluate trade-offs systematically. Score options. Identify sensitivity points.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are evaluating: [DECISION]
Options: [LIST OPTIONS]
Priority quality attributes: [LIST QAs]

Your role is ANALYST — evaluate trade-offs. Produce:

1. Trade-off matrix
   Score each option 1-5 against each quality attribute.
   Use this format:

   | Attribute | Option A | Option B | Option C | Weight |
   |-----------|----------|----------|----------|--------|
   | Performance | 4 | 3 | 5 | High |
   | ... | ... | ... | ... | ... |
   | Weighted Total | X | Y | Z | |

2. Sensitivity analysis
   - Which attribute weights would flip the decision?
   - Where are the options closest? (sensitivity points)
   - What assumptions are baked into the scores?

3. WWHTBT analysis (What Would Have to Be True)
   For each option, list 3-5 conditions that would need to hold
   for this option to be the right choice.
   See: https://rogermartin.medium.com/what-would-have-to-be-true-83dac5bd2189

Output format:
- Tables for the matrix
- Bullet lists for WWHTBT
- Explicit about assumptions behind each score
```

---

## Critic (Black + Red Hat — Risks & Intuition)

**Mandate**: Attack the leading option. Run a pre-mortem. Surface what everyone is ignoring.

**Subagent type**: `general-purpose`

**Prompt template**:

```
We are evaluating: [DECISION]
The "obvious" or leading option appears to be: [LEADING OPTION]

Your role is DEVIL'S ADVOCATE — your job is to find problems. Do:

1. Pre-mortem analysis
   Imagine it is 6 months from now. We chose [LEADING OPTION] and it FAILED.
   Write the post-mortem:
   - What went wrong?
   - What did we underestimate?
   - What changed in our assumptions?
   - What side effects did we not anticipate?
   See: https://joshclemm.com/writing/the-premortem-software-engineering-best-practice/

2. Risk register
   For each option (not just the leading one):
   | Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation |
   |------|---------------------|-----------------|------------|

3. Cognitive bias check
   Which of these biases might be affecting this decision?
   - Confirmation bias: Are we only seeing evidence for our preferred option?
   - Anchoring: Are we over-weighting the first option considered?
   - Bandwagon: Are we choosing this because "everyone uses it"?
   - Optimism: Are we underestimating complexity/timeline?
   - Sunk cost: Are we sticking with something because of prior investment?
   See: https://ieeexplore.ieee.org/document/8506423/

4. Hidden costs and second-order effects
   What will this decision force us into later?
   What optionality does it close off?

Output format:
- Pre-mortem as narrative (2-3 paragraphs)
- Risk register as table
- Bias check as bullet list with evidence
- Be specific, not generic — reference the actual codebase and options
```

---

## Scout (Green Hat — Creativity & Alternatives)

**Mandate**: Find approaches nobody has mentioned. Research external solutions.

**Subagent type**: `general-purpose` (needs WebSearch)

**When to spawn**: Decision involves technology selection, unfamiliar domains, or the user says "what else could we do?"

**Prompt template**:

```
We are evaluating: [DECISION]
Options already identified: [LIST OPTIONS]

Your role is SCOUT — find alternatives we haven't considered.

1. External research
   - How do other companies/projects solve this?
   - Are there libraries, patterns, or approaches we're missing?
   - What does recent (2025-2026) thinking say about this problem?

2. Unconventional approaches
   - What if we did nothing? (the null option)
   - What if we combined elements of multiple options?
   - What if we solved a different problem that makes this one go away?
   - What's the simplest possible approach we might be overcomplicating?

3. Precedent analysis
   - Link to relevant blog posts, case studies, or documentation
   - Note which approaches have been tried and abandoned (and why)

Output format:
- 2-3 new options with brief description and rationale
- Links to sources
- Comparison to already-identified options
```

---

## Mapping to Six Thinking Hats

| Hat | Color | Perspective | Agent |
|-----|-------|-------------|-------|
| White | Facts & data | What does the code tell us? | Explorer |
| Yellow | Benefits | What's the upside of each option? | Analyst |
| Black | Risks | What can go wrong? | Critic |
| Red | Intuition | What feels right/wrong? (DX, cognitive load) | Critic (secondary) |
| Green | Creativity | What else could we do? | Scout |
| Blue | Process | How do we structure this decision? | Orchestrator (you) |

Source: De Bono, E. (1985). *Six Thinking Hats*.
