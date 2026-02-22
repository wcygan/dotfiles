---
title: Workflow
description: 3-phase orchestration for the clone-research skill
tags: [workflow, orchestration, phases, process]
---

# Workflow

3 phases: Parse Input, Parallel Research, Cross-Reference & Index.

---

## Phase 1: Parse Input

### Extract target from `$ARGUMENTS`

- **URL** (starts with `http`): use as-is for WebFetch, extract company name from domain
  - `https://linear.app` -> company name "Linear", URL as-is
  - `https://www.notion.so` -> company name "Notion", URL as-is
- **Company name** (no URL): construct likely URLs (`https://{name}.com`, `https://www.{name}.com`)
  - "Linear" -> try `https://linear.app`, `https://linear.com`
  - "Notion" -> try `https://notion.so`, `https://www.notion.so`
- **Empty**: Ask the user what product to research. Wait for response.

### Store parsed values

```
COMPANY_NAME = "Linear"           # Human-readable
PRIMARY_URL  = "https://linear.app"  # Main product URL
SLUG         = "linear"           # kebab-case for directory name
```

### Create output directory

```
clone-research/{SLUG}/
```

Use the Write tool to create files in this directory. Create it relative to the current working directory.

**IMPORTANT**: When `$ARGUMENTS` is provided, proceed immediately to Phase 2. Do not pause for user confirmation.

---

## Phase 2: Parallel Research

### Spawn all 4 agents in ONE parallel Task call

This is critical for performance. All agents are independent — they don't need each other's output.

```
Agent: Product Strategist
  subagent_type: general-purpose
  run_in_background: true
  Documents: 01-product-thesis.md, 07-revenue-pricing-model.md

Agent: UX Researcher
  subagent_type: general-purpose
  run_in_background: true
  Documents: 02-feature-priority-matrix.md, 03-mvp-scope-contract.md, 04-core-user-journeys.md

Agent: Technical Architect
  subagent_type: general-purpose
  run_in_background: true
  Documents: 05-domain-model.md, 06-system-architecture.md, 08-api-surface-spec.md

Agent: Design Analyst
  subagent_type: general-purpose
  run_in_background: true
  Documents: 09-design-system-brief.md
```

### Agent prompt construction

For each agent, build the prompt by:

1. Taking the prompt template from [agent-roles.md](agent-roles.md)
2. Replacing `{COMPANY_NAME}`, `{PRIMARY_URL}`, `{OUTPUT_DIR}` with parsed values
3. Pasting the relevant document templates from [output-templates.md](output-templates.md)
4. Including the document standards from [document-standards.md](document-standards.md)
5. Including the research techniques from [research-techniques.md](research-techniques.md) for their specific agent

### Wait for all agents to complete

Collect results from all 4 background agents. If any agent fails or returns thin results, note the gap rather than blocking.

---

## Phase 3: Cross-Reference & Index

After all agents complete:

### 1. Read all 9 documents

Read all documents from `clone-research/{SLUG}/` to verify they were written correctly.

### 2. Write the Index

Create `clone-research/{SLUG}/00-INDEX.md` using the INDEX template from [output-templates.md](output-templates.md):

- Write the executive summary based on findings from all agents
- Include the reading order (Tier 1 first, then Tier 2)
- Include the cross-reference map

### 3. Verify cross-references

Check that:
- Feature IDs (F1, F2...) used in docs 03, 04, 05, 08 match those defined in doc 02
- Entity names in docs 06 and 08 match those defined in doc 05
- Tier assignments in doc 07 align with tier column in doc 02

If inconsistencies are found, note them in the INDEX under a "Known Gaps" section rather than re-running agents.

### 4. Present summary to user

Show the user:
- List of all 10 files produced (including INDEX)
- Executive summary from the INDEX
- Any gaps or thin sections
- Suggested next steps (e.g., "Read 01-product-thesis.md first")

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Agent fails entirely | Note in INDEX, produce remaining 8 docs |
| Agent produces thin results | Include as-is, flag in INDEX |
| Company has no public info | Agents note "Not publicly available", produce best-effort docs |
| URL is unreachable | Fall back to WebSearch-only research |
| Output directory conflict | Append timestamp to slug: `{slug}-{YYYYMMDD}` |

---

## Timing Expectations

| Phase | Typical Duration |
|-------|-----------------|
| Phase 1 (Parse) | < 10 seconds |
| Phase 2 (Research) | 3-8 minutes |
| Phase 3 (Index) | 1-2 minutes |
| **Total** | **4-10 minutes** |

Phase 2 dominates runtime. All 4 agents run in parallel, so total time equals the slowest agent (typically the UX Researcher, which produces 3 documents).
