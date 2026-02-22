---
name: clone-research
description: >
  Comprehensive product research for building an MVP clone. Spawns 4 parallel research agents
  to produce 9 standardized documents: Product Thesis, Feature Priority Matrix, MVP Scope
  Contract, Core User Journeys, Domain Model, System Architecture, Revenue & Pricing Model,
  API Surface Spec, and Design System Brief. Use when planning a clone, building a competitor
  alternative, scoping an MVP, or analyzing a product to replicate. Keywords: clone, MVP,
  product research, teardown, feature matrix, domain model, reverse engineer, competitor clone
context: fork
disable-model-invocation: true
argument-hint: <product-name-or-url>
---

# Clone Research

Target: **$ARGUMENTS**

## Agent Strategy

Spawn 4 parallel research agents. Each produces 1-3 documents from external research.

| Agent | Role | Documents |
|-------|------|-----------|
| **Product Strategist** | Company, market, business model | 01-product-thesis, 07-revenue-pricing |
| **UX Researcher** | Features, flows, user needs | 02-feature-matrix, 03-mvp-scope, 04-user-journeys |
| **Technical Architect** | Stack, data model, APIs | 05-domain-model, 06-architecture, 08-api-surface |
| **Design Analyst** | Visual language, components | 09-design-system-brief |

All agents: `subagent_type: general-purpose`, `run_in_background: true`

References: [agent-roles](references/agent-roles.md)

## Execution

### 1. Parse Input

**Target: `$ARGUMENTS`**

If the target above is non-empty, use it immediately — do NOT ask the user to confirm or re-provide it. Parse it as follows:

- **URL** (starts with `http`): use as-is for WebFetch, extract company name from domain
- **Company name** (no URL): construct likely URLs (`https://{name}.com`, `https://www.{name}.com`)

If the target above is empty, ask the user what product to research and wait for their response.

Store:
- `COMPANY_NAME`: Human-readable name (e.g., "Linear")
- `PRIMARY_URL`: Main product URL (e.g., "https://linear.app")
- `SLUG`: kebab-case for directory (e.g., "linear")

Create output directory: `clone-research/{SLUG}/`

**IMPORTANT**: When a target is provided, begin Phase 2 immediately after parsing. Do not pause for user input.

References: [workflow](references/workflow.md)

### 2. Spawn Agents in Parallel

Spawn all 4 agents in ONE parallel Task tool call. Each agent receives:
- Company name and URL
- Their specific mandate and prompt template from agent-roles reference
- The relevant document templates from output-templates reference
- Document standards (naming, feature IDs, entity naming, confidence levels, citations)
- Research techniques for their specific role

Build each agent's prompt by:
1. Taking the prompt template from the agent-roles reference
2. Replacing `{COMPANY_NAME}`, `{PRIMARY_URL}`, `{OUTPUT_DIR}` with parsed values
3. Pasting the document templates they own from the output-templates reference
4. Including document standards and their research techniques

References: [agent-roles](references/agent-roles.md), [output-templates](references/output-templates.md), [document-standards](references/document-standards.md), [research-techniques](references/research-techniques.md)

### 3. Cross-Reference & Index

After all agents complete:

1. Read all 9 documents from `clone-research/{SLUG}/`
2. Write `clone-research/{SLUG}/00-INDEX.md` with executive summary, reading order, and cross-reference map
3. Verify feature IDs (F1, F2...) and entity names are consistent across documents
4. Note any inconsistencies in the INDEX under "Known Gaps"
5. Write `AGENTS.md` at the **project root** (current working directory) using the AGENTS template — includes operating instructions, domain model, architecture stack, and phased work plan (Phase 0 through 4) with per-phase checklists; this file is the primary context document for all future agents building the clone
6. Run `ln -s AGENTS.md CLAUDE.md` at the project root — creates a relative symlink so Claude Code auto-loads the context when opening the project; only ever edit AGENTS.md going forward

References: [workflow](references/workflow.md), [output-templates](references/output-templates.md)

## Output

9 research documents + index in `clone-research/{SLUG}/`, plus `AGENTS.md` and `CLAUDE.md` symlink at the **project root**:

```
./                               # Project root (current working directory)
  AGENTS.md                      # Project context: mission, scope, stack, work phases
  CLAUDE.md -> AGENTS.md         # Symlink — Claude Code auto-loads this; edit AGENTS.md only
  clone-research/{slug}/
    00-INDEX.md                  # Executive summary + reading order
    01-product-thesis.md         # North star, market, opportunity
    02-feature-priority-matrix.md  # Feature inventory P0-P3
    03-mvp-scope-contract.md     # In/out scope, roadmap phases
    04-core-user-journeys.md     # Personas, JTBD, step-by-step flows
    05-domain-model.md           # Entities, relationships, lifecycles
    06-system-architecture.md    # Observed + recommended stack
    07-revenue-pricing-model.md  # Tiers, gating, upgrade triggers
    08-api-surface-spec.md       # Endpoints, pagination, errors
    09-design-system-brief.md    # Colors, type, spacing, components
```

Present to user: file list, executive summary, gaps, and suggested reading order.

## Anti-Patterns

- **Don't use Explore agents**: Sub-agents need WebSearch and WebFetch for external research. Use `general-purpose` only.
- **Don't collapse agents**: Each agent has a distinct research lens. Combining them loses depth.
- **Don't fabricate data**: If information isn't found, say "Not publicly available" rather than guessing.
- **Don't skip citations**: Every factual claim must reference a source URL.
- **Don't run agents sequentially**: All 4 agents are independent — spawn them in parallel.
- **Don't skip the INDEX**: The cross-reference map is essential for downstream consumers.

## Example Invocations

```
/clone-research https://linear.app
/clone-research Notion
/clone-research https://www.figma.com
/clone-research Vercel
/clone-research Superhuman
```

## Notes

- Total runtime: typically 4-10 minutes depending on the target's web presence.
- All 4 agents run in background for maximum parallelism.
- If an agent fails or returns thin results, note the gap in the INDEX rather than blocking.
- For private/stealth companies with minimal web presence, agents will produce thinner reports — this is expected.
- Documents are consumed by builder agents downstream — consistency in naming, feature IDs, and entity names matters.
