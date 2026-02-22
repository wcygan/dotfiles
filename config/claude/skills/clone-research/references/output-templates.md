---
title: Output Templates
description: Complete templates for all 9 clone-research documents
tags: [templates, output, documents, format]
---

# Output Templates

Templates for all 9 documents. Each agent writes its owned documents using these templates.

---

## 01 — Product Thesis

**Owner**: Product Strategist

```markdown
---
type: clone-research
document: "Product Thesis"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 1
sequence: 01
---

# Product Thesis: {Company}

## North Star

**What they do**: {One sentence — what the product is}

**Who it's for**: {Primary customer segment}

**Why it wins**: {The core insight or unfair advantage}

**Mission statement**: "{Exact quote if available}" [Source](url)

## Company Snapshot

| Field | Value | Source |
|-------|-------|--------|
| Founded | {year} | {source} |
| Headquarters | {location} | {source} |
| Funding | {total raised, last round, investors} | {source} |
| Estimated employees | {range} | {source} |
| Estimated ARR | {range or "Not public"} | {source} |
| Category | {product category} | — |

## Value Proposition Canvas

| Element | Description |
|---------|-------------|
| **Customer jobs** | {What users are trying to accomplish} |
| **Pains** | {What frustrates them about current solutions} |
| **Gains** | {What outcomes they desire} |
| **Pain relievers** | {How {company} addresses pains} |
| **Gain creators** | {How {company} delivers gains} |

## Competitive Landscape

| Competitor | Positioning | Key Differentiator | Weakness vs {Company} |
|-----------|-------------|-------------------|----------------------|
| {competitor 1} | {positioning} | {differentiator} | {weakness} |
| {competitor 2} | {positioning} | {differentiator} | {weakness} |
| {competitor 3} | {positioning} | {differentiator} | {weakness} |

## Market Context

**Category maturity**: {Emerging / Growing / Mature / Declining}

**Key trends**:
1. {trend affecting this market}
2. {trend affecting this market}
3. {trend affecting this market}

**Clone opportunity thesis**: {2-3 sentences on why building a clone makes sense now — what gap exists, what has changed, or what segment is underserved}

**Xref:** Features detailed in [02-feature-priority-matrix.md](02-feature-priority-matrix.md). Revenue model in [07-revenue-pricing-model.md](07-revenue-pricing-model.md).

## Sources

- [Source Title](url) — description
```

---

## 02 — Feature Priority Matrix

**Owner**: UX Researcher

```markdown
---
type: clone-research
document: "Feature Priority Matrix"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 1
sequence: 02
---

# Feature Priority Matrix: {Company}

## Feature Inventory

| ID | Feature | Description | Priority | Effort | Impact | Tier |
|----|---------|-------------|----------|--------|--------|------|
| F1 | {feature} | {description} | P0 | {S/M/L/XL} | High | Free |
| F2 | {feature} | {description} | P0 | {S/M/L/XL} | High | Free |
| F3 | {feature} | {description} | P1 | {S/M/L/XL} | Medium | Pro |
| F4 | {feature} | {description} | P1 | {S/M/L/XL} | High | Pro |
| F5 | {feature} | {description} | P2 | {S/M/L/XL} | Medium | Pro |
| ... | ... | ... | ... | ... | ... | ... |

Target: 15-25 features. Priority assignment rationale:
- **P0**: Without this, no one would use the product
- **P1**: Users expect this within the first quarter
- **P2**: Differentiation opportunity
- **P3**: Nice-to-have, backlog

## Priority Summary

| Priority | Count | Features |
|----------|-------|----------|
| P0 | {N} | {F1, F2, ...} |
| P1 | {N} | {F3, F4, ...} |
| P2 | {N} | {F5, ...} |
| P3 | {N} | {...} |

## Feature Teardown Appendix

For each P0 feature, provide a brief teardown:

### F1: {Feature Name}

**What it does**: {description of behavior}
**How {company} implements it**: {observed implementation}
**Key interactions**: {notable UX patterns}
**Clone consideration**: {what to keep, what to improve}

### F2: {Feature Name}

(repeat for each P0 feature)

**Xref:** MVP scope derived from this in [03-mvp-scope-contract.md](03-mvp-scope-contract.md). User journeys reference feature IDs in [04-core-user-journeys.md](04-core-user-journeys.md).

## Sources

- [Source Title](url) — description
```

---

## 03 — MVP Scope Contract

**Owner**: UX Researcher

```markdown
---
type: clone-research
document: "MVP Scope Contract"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 1
sequence: 03
---

# MVP Scope Contract: {Company} Clone

## The Must-Nail Feature

**Feature**: {The single most important feature to get right}

**Why**: {Reasoning — what makes this the make-or-break feature for user adoption}

**Xref:** See F{N} in [02-feature-priority-matrix.md](02-feature-priority-matrix.md).

## In Scope (v1.0)

| Feature ID | Feature | Effort | Acceptance Criteria |
|-----------|---------|--------|-------------------|
| F1 | {feature} | {S/M/L/XL} | {what "done" looks like} |
| F2 | {feature} | {S/M/L/XL} | {what "done" looks like} |
| ... | ... | ... | ... |

## Out of Scope (v1.0)

| Feature | Reason | Revisit When |
|---------|--------|-------------|
| {feature} | {why excluded} | {trigger to reconsider} |
| {feature} | {why excluded} | {trigger to reconsider} |

## Roadmap Phases

### Phase 1: MVP (v1.0)
- **Goal**: {primary goal}
- **Features**: F1, F2, F3, ...
- **Success metric**: {measurable outcome}

### Phase 2: Growth (v1.x)
- **Goal**: {primary goal}
- **Features**: F{N}, F{N+1}, ...
- **Success metric**: {measurable outcome}

### Phase 3: Scale (v2.0)
- **Goal**: {primary goal}
- **Features**: F{N}, ...
- **Success metric**: {measurable outcome}

## Effort Summary

| Phase | Feature Count | Estimated Effort |
|-------|-------------|-----------------|
| MVP | {N} | {total} |
| Growth | {N} | {total} |
| Scale | {N} | {total} |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| {risk} | H/M/L | H/M/L | {strategy} |

**Xref:** Domain entities in [05-domain-model.md](05-domain-model.md). Architecture decisions in [06-system-architecture.md](06-system-architecture.md).

## Sources

- [Source Title](url) — description
```

---

## 04 — Core User Journeys

**Owner**: UX Researcher

```markdown
---
type: clone-research
document: "Core User Journeys"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 1
sequence: 04
---

# Core User Journeys: {Company}

## Personas

| Persona | Role | Goal | Pain Point |
|---------|------|------|-----------|
| {persona 1} | {role/title} | {what they want to accomplish} | {primary frustration} |
| {persona 2} | {role/title} | {what they want to accomplish} | {primary frustration} |
| {persona 3} | {role/title} | {what they want to accomplish} | {primary frustration} |

## Jobs to Be Done (JTBD)

| # | Job Statement | Current Solution | Desired Outcome |
|---|--------------|-----------------|-----------------|
| 1 | When I {situation}, I want to {motivation}, so I can {outcome} | {what they use now} | {ideal state} |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |

## Journey 1: {Journey Name} (e.g., "First-Time Setup")

**Persona**: {persona name}
**Goal**: {what they're trying to accomplish}
**Features used**: F{N}, F{N}, F{N}

| Step | Action | Screen/Page | Notes |
|------|--------|------------|-------|
| 1 | {user action} | {where it happens} | {UX observation} |
| 2 | {user action} | {where it happens} | {UX observation} |
| 3 | {user action} | {where it happens} | {UX observation} |
| 4 | {user action} | {where it happens} | {UX observation} |
| 5 | {user action} | {where it happens} | {UX observation} |

**Friction points**: {where users struggle}
**Clone improvement opportunity**: {what to do better}

## Journey 2: {Journey Name} (e.g., "Core Workflow Loop")

(same format — repeat for 3-5 total journeys)

## Journey 3: {Journey Name}

(same format)

## Journey Map Summary

| Journey | Steps | Friction | Priority | Features |
|---------|-------|---------|----------|----------|
| {journey 1} | {N} | {H/M/L} | P0 | F1, F3 |
| {journey 2} | {N} | {H/M/L} | P0 | F2, F4 |
| {journey 3} | {N} | {H/M/L} | P1 | F5, F7 |

**Xref:** Features referenced by ID from [02-feature-priority-matrix.md](02-feature-priority-matrix.md). Entities from [05-domain-model.md](05-domain-model.md).

## Sources

- [Source Title](url) — description
```

---

## 05 — Domain Model

**Owner**: Technical Architect

```markdown
---
type: clone-research
document: "Domain Model"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 1
sequence: 05
---

# Domain Model: {Company}

## Core Entities

| Entity | Description | Key Attributes | Relationships |
|--------|-------------|---------------|--------------|
| User | {description} | id, email, name, role | belongs to Workspace, creates Project |
| Workspace | {description} | id, name, slug, plan | has many Users, has many Projects |
| Project | {description} | id, name, status | belongs to Workspace, has many Tasks |
| {Entity} | {description} | {attributes} | {relationships} |
| ... | ... | ... | ... |

Target: 8-15 core entities.

## Entity Relationships

```
Workspace 1──* User (membership)
Workspace 1──* Project
Project    1──* Task
Task       *──1 User (assignee)
Task       *──* Label
Task       0..1──1 Task (parent, for subtasks)
```

Use ASCII notation: `1──*` (one-to-many), `*──*` (many-to-many), `0..1──1` (optional).

## Lifecycle States

For entities with status workflows:

### {Entity} Lifecycle

```
[Draft] → [Active] → [Completed]
                   → [Archived]
           [Active] → [Cancelled]
```

| State | Description | Transitions To | Trigger |
|-------|-------------|---------------|---------|
| Draft | {description} | Active | {what causes transition} |
| Active | {description} | Completed, Archived, Cancelled | {triggers} |
| Completed | {description} | Active (reopen) | {trigger} |

## Bounded Contexts

| Context | Core Entities | Aggregates | External Dependencies |
|---------|--------------|------------|----------------------|
| {e.g., Identity} | User, Session, Team | UserAggregate | — |
| {e.g., Project Management} | Project, Task, Label | ProjectAggregate | Identity |
| {e.g., Notification} | Notification, Preference | NotificationAggregate | Identity |
| {e.g., Billing} | Subscription, Invoice, Plan | SubscriptionAggregate | Identity |

**External Dependencies** column: list other bounded contexts this context depends on.
This drives cross-epic dependency wiring during build decomposition.

## Invariants & Business Rules

| Rule | Description | Entities Involved |
|------|-------------|------------------|
| {rule name} | {e.g., "A task must have exactly one assignee when in Active state"} | Task, User |
| {rule name} | {description} | {entities} |

## Confidence Notes

| Entity | Confidence | Evidence |
|--------|-----------|---------|
| {entity} | High | Visible in API/docs |
| {entity} | Medium | Inferred from UI/features |
| {entity} | Low | Assumed from patterns |

**Xref:** Entities map to API resources in [08-api-surface-spec.md](08-api-surface-spec.md). Architecture contexts in [06-system-architecture.md](06-system-architecture.md).

## Sources

- [Source Title](url) — description
```

---

## 06 — System Architecture

**Owner**: Technical Architect

```markdown
---
type: clone-research
document: "System Architecture"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 1
sequence: 06
---

# System Architecture: {Company}

## Observed Stack

| Layer | Technology | Confidence | Evidence |
|-------|-----------|-----------|---------|
| Frontend framework | {e.g., React} | {H/M/L} | {source} |
| Frontend language | {e.g., TypeScript} | {H/M/L} | {source} |
| Backend language | {e.g., Go} | {H/M/L} | {source} |
| Backend framework | {e.g., Gin} | {H/M/L} | {source} |
| Database (primary) | {e.g., PostgreSQL} | {H/M/L} | {source} |
| Database (cache) | {e.g., Redis} | {H/M/L} | {source} |
| Search | {e.g., Elasticsearch} | {H/M/L} | {source} |
| Message queue | {e.g., Kafka} | {H/M/L} | {source} |
| Cloud provider | {e.g., AWS} | {H/M/L} | {source} |
| CDN | {e.g., Cloudflare} | {H/M/L} | {source} |
| Real-time | {e.g., WebSockets} | {H/M/L} | {source} |

## Architecture Patterns

| Pattern | Observed | Evidence |
|---------|----------|---------|
| Monolith vs microservices | {observation} | {evidence} |
| SSR vs SPA vs hybrid | {observation} | {evidence} |
| REST vs GraphQL vs gRPC | {observation} | {evidence} |
| Multi-tenant vs single-tenant | {observation} | {evidence} |
| Real-time sync strategy | {observation} | {evidence} |
| Offline/local-first | {observation} | {evidence} |

## Recommended Clone Architecture

Based on observations, the recommended architecture for a clone:

### Frontend

| Choice | Recommendation | Rationale |
|--------|---------------|-----------|
| Framework | {recommendation} | {why} |
| Language | TypeScript | Standard for modern web |
| State management | {recommendation} | {why} |
| Styling | {recommendation} | {why} |
| Real-time | {recommendation} | {why} |

### Backend

| Choice | Recommendation | Rationale |
|--------|---------------|-----------|
| Language | {recommendation} | {why} |
| Framework | {recommendation} | {why} |
| API style | {recommendation} | {why} |
| Database | {recommendation} | {why} |
| Cache | {recommendation} | {why} |
| Auth | {recommendation} | {why} |

### Infrastructure

| Choice | Recommendation | Rationale |
|--------|---------------|-----------|
| Hosting | {recommendation} | {why} |
| CI/CD | {recommendation} | {why} |
| Monitoring | {recommendation} | {why} |

## Key Architecture Decisions

| Decision | Options | Recommendation | Trade-off |
|----------|---------|---------------|-----------|
| {decision} | {options} | {pick} | {what you give up} |
| {decision} | {options} | {pick} | {what you give up} |

**Xref:** Domain contexts from [05-domain-model.md](05-domain-model.md). API design in [08-api-surface-spec.md](08-api-surface-spec.md).

## Sources

- [Source Title](url) — description
```

---

## 07 — Revenue & Pricing Model

**Owner**: Product Strategist

```markdown
---
type: clone-research
document: "Revenue & Pricing Model"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 2
sequence: 07
---

# Revenue & Pricing Model: {Company}

## Pricing Tiers

| Tier | Price | Billing | Target |
|------|-------|---------|--------|
| {Free/Starter} | {price} | {monthly/annual} | {persona} |
| {Pro/Team} | {price} | {monthly/annual} | {persona} |
| {Enterprise} | {price} | {monthly/annual} | {persona} |

**Pricing model**: {per seat / per workspace / usage-based / flat rate}
**Annual discount**: {percentage if offered}
**Free trial**: {duration and scope}

## Feature Gating

| Feature | Free | Pro | Enterprise |
|---------|------|-----|-----------|
| {feature} | {limit or check} | {limit or check} | {limit or check} |
| {feature} | {limit or check} | {limit or check} | {limit or check} |
| {feature} | {limit or check} | {limit or check} | {limit or check} |

## Upgrade Triggers

| Trigger | From | To | Mechanism |
|---------|------|-----|----------|
| {e.g., "Hit 10 member limit"} | Free | Pro | {banner/modal/email} |
| {e.g., "Need SSO"} | Pro | Enterprise | {sales contact} |
| {e.g., "Need audit log"} | Pro | Enterprise | {feature gate} |

## Revenue Signals

| Signal | Value | Confidence | Source |
|--------|-------|-----------|--------|
| Estimated ARR | {amount} | {H/M/L} | {source} |
| Estimated customers | {count} | {H/M/L} | {source} |
| Avg deal size | {amount} | {H/M/L} | {source} |
| Growth rate | {percentage} | {H/M/L} | {source} |

## Clone Pricing Recommendation

| Tier | Suggested Price | Rationale |
|------|----------------|-----------|
| Free | {price} | {reasoning vs competitor} |
| Pro | {price} | {reasoning vs competitor} |
| Enterprise | {price} | {reasoning vs competitor} |

**Positioning vs {Company}**: {cheaper / same / premium — and why}

**Xref:** Feature gating aligns with [02-feature-priority-matrix.md](02-feature-priority-matrix.md) tier column. Upgrade triggers visible in [04-core-user-journeys.md](04-core-user-journeys.md).

## Sources

- [Source Title](url) — description
```

---

## 08 — API Surface Spec

**Owner**: Technical Architect

```markdown
---
type: clone-research
document: "API Surface Spec"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 2
sequence: 08
---

# API Surface Spec: {Company}

## API Overview

| Aspect | Details |
|--------|---------|
| API style | {REST / GraphQL / gRPC / None public} |
| Base URL | {if documented} |
| Authentication | {API key / OAuth / JWT / Bearer token} |
| Rate limiting | {limits if documented} |
| Versioning | {URL path / header / none} |
| Documentation | {URL and quality assessment} |

## Resource Endpoints

| Resource | Method | Endpoint | Description | Feature |
|----------|--------|----------|-------------|---------|
| {Entity} | GET | /api/{entities} | List all | F{N} |
| {Entity} | POST | /api/{entities} | Create | F{N} |
| {Entity} | GET | /api/{entities}/:id | Get one | F{N} |
| {Entity} | PATCH | /api/{entities}/:id | Update | F{N} |
| {Entity} | DELETE | /api/{entities}/:id | Delete | F{N} |
| ... | ... | ... | ... | ... |

Map resources to domain entities from [05-domain-model.md](05-domain-model.md).

## Pagination Pattern

| Aspect | Observed |
|--------|----------|
| Style | {cursor / offset / page-number} |
| Default page size | {N} |
| Max page size | {N} |
| Response fields | {next_cursor, has_more, total_count, etc.} |

## Error Format

```json
{
  "error": {
    "code": "{error_code}",
    "message": "{human-readable message}",
    "details": {}
  }
}
```

| HTTP Status | Meaning | Example |
|-------------|---------|---------|
| 400 | Bad request | Invalid field value |
| 401 | Unauthorized | Missing/expired token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not found | Resource doesn't exist |
| 429 | Rate limited | Too many requests |

## Webhook Events (if supported)

| Event | Payload | Trigger |
|-------|---------|---------|
| {entity}.created | {key fields} | {when fired} |
| {entity}.updated | {key fields} | {when fired} |
| {entity}.deleted | {key fields} | {when fired} |

## SDK & Integration Support

| Language/Platform | Official SDK | Quality |
|------------------|-------------|---------|
| {JavaScript/TypeScript} | {Yes/No} | {assessment} |
| {Python} | {Yes/No} | {assessment} |
| {Go} | {Yes/No} | {assessment} |
| {Ruby} | {Yes/No} | {assessment} |

## Clone API Recommendations

| Decision | Recommendation | Rationale |
|----------|---------------|-----------|
| API style | {recommendation} | {why} |
| Auth method | {recommendation} | {why} |
| Pagination | {recommendation} | {why} |
| Error format | {recommendation} | {why} |
| Versioning | {recommendation} | {why} |

**Xref:** Resources map to entities in [05-domain-model.md](05-domain-model.md). Architecture context in [06-system-architecture.md](06-system-architecture.md).

## Sources

- [Source Title](url) — description
```

---

## 09 — Design System Brief

**Owner**: Design Analyst

```markdown
---
type: clone-research
document: "Design System Brief"
target: "{company}"
date: "{YYYY-MM-DD}"
tier: 2
sequence: 09
---

# Design System Brief: {Company}

## Color Palette

| Role | Value | Usage |
|------|-------|-------|
| Primary | {hex} | {where used} |
| Secondary | {hex} | {where used} |
| Accent | {hex} | {where used} |
| Background | {hex} | {main bg} |
| Surface | {hex} | {cards, modals} |
| Text primary | {hex} | {body text} |
| Text secondary | {hex} | {muted text} |
| Success | {hex} | — |
| Warning | {hex} | — |
| Error | {hex} | — |
| Info | {hex} | — |

**Dark mode**: {Yes / No / System-follows}

## Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| Headings | {font family} | {sizes} | {weights} |
| Body | {font family} | {base size} | {weight} |
| Code/mono | {font family} | {size} | {weight} |
| UI labels | {font family} | {size} | {weight} |

**Type scale**: {ratio if detectable, e.g., 1.25 major third}

## Spacing & Layout

| Property | Value |
|----------|-------|
| Base unit | {e.g., 4px / 8px} |
| Grid system | {e.g., 12-column, CSS grid} |
| Max content width | {e.g., 1200px} |
| Sidebar width | {e.g., 240px} |
| Border radius | {e.g., 4px, 8px} |

## Component Inventory

| Component | Variants | Notable Patterns |
|-----------|----------|-----------------|
| Button | {primary, secondary, ghost, danger} | {size variants, loading state} |
| Input | {text, select, textarea, search} | {validation style, placeholder} |
| Card | {default, elevated, bordered} | {hover effects} |
| Modal/Dialog | {sizes} | {overlay, animation} |
| Navigation | {sidebar, topbar, breadcrumb} | {collapse behavior} |
| Table/List | {default, compact, striped} | {sorting, selection} |
| Toast/Alert | {success, error, warning, info} | {position, auto-dismiss} |
| Avatar | {sizes, group} | {fallback} |
| Badge/Tag | {colors, sizes} | {removable} |
| Dropdown | {single, multi, combobox} | {search, grouping} |
| Tooltip | {positions} | {delay, max width} |
| Tabs | {default, pill, underline} | {responsive behavior} |

## Icon Style

| Property | Value |
|----------|-------|
| Style | {outline / filled / duotone} |
| Library | {Lucide / Heroicons / custom / etc.} |
| Size convention | {e.g., 16px, 20px, 24px} |
| Stroke width | {if outline} |

## Motion & Animation

| Pattern | Duration | Easing |
|---------|----------|--------|
| Page transition | {ms} | {easing} |
| Modal open/close | {ms} | {easing} |
| Hover effects | {ms} | {easing} |
| Loading states | {description} | — |

## Responsive Breakpoints

| Name | Width | Layout Change |
|------|-------|--------------|
| Mobile | {e.g., < 640px} | {description} |
| Tablet | {e.g., 640-1024px} | {description} |
| Desktop | {e.g., > 1024px} | {description} |

## Clone Design Recommendations

| Decision | Recommendation | Rationale |
|----------|---------------|-----------|
| Component library | {e.g., shadcn/ui, Radix} | {why} |
| CSS approach | {e.g., Tailwind, CSS Modules} | {why} |
| Icon set | {recommendation} | {why} |
| Font stack | {recommendation} | {why} |

**Xref:** Components support features in [02-feature-priority-matrix.md](02-feature-priority-matrix.md). Layout integrates with [06-system-architecture.md](06-system-architecture.md) frontend choices.

## Sources

- [Source Title](url) — description
```

---

## AGENTS.md (Generated by Orchestrator)

This file is written after all agents complete and the INDEX is written. It synthesizes key findings into a project context file for future AI-assisted development. `CLAUDE.md` is created as a relative symlink pointing to it.

The template includes: essential operating instructions for AI agents, domain context from the research, and explicit work phases so agents know what has been done and what to build next.

```markdown
---
type: clone-research
document: "AGENTS"
target: "{company}"
date: "{YYYY-MM-DD}"
---

# AGENTS.md — {Company} Clone

> **CLAUDE.md is a symlink to this file. Edit AGENTS.md only.**
> Research completed {YYYY-MM-DD}. Use this file as your primary context before starting any work.

## Mission

Build a {Company} clone: {what they do — one sentence from product thesis}.

**Primary target**: {who it's for — from 01-product-thesis}
**Core value prop**: {why it wins / unfair advantage — from 01-product-thesis}
**Clone opportunity**: {why a clone makes sense now — from 01-product-thesis}

---

## Operating Instructions

These rules apply to all agents working on this project:

**Development loop**: Write test → implement minimal solution → tests pass → format/lint → commit atomically. Never skip failing tests.

**Scope discipline**: Before implementing any feature, check [03-mvp-scope-contract.md](clone-research/{SLUG}/03-mvp-scope-contract.md). If it's not in scope for the current phase, do not build it.

**Naming**: Use exact entity names from the domain model (see below) in all code, schemas, and API routes. Do not invent synonyms.

**Feature IDs**: Reference features by their F-number (F1, F2, …) from [02-feature-priority-matrix.md](clone-research/{SLUG}/02-feature-priority-matrix.md) in PRs, tasks, and comments.

**Commits**: One logical change per commit. All tests green. Message format: `type(scope): description` (e.g., `feat(auth): add email/password login`).

**Sub-agents**: Use 2–3 parallel agents for exploration, research, and code-quality audits. Never have two agents edit the same file.

---

## Domain Model

Core entities — use these names exactly in code:

{For each of the 5–8 most important entities from 05-domain-model, write one line:}
- **{Entity}**: {one-sentence description of what it represents}
- **{Entity}**: {one-sentence description}
- …

Key relationships:
{2–4 most important relationships as plain English, e.g. "A Workspace has many Members; a Member belongs to exactly one Workspace."}

Full model: [05-domain-model.md](research/05-domain-model.md)

---

## Architecture

### Stack

| Layer | Choice | Source |
|-------|--------|--------|
| Frontend | {recommendation} | [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) |
| Backend | {recommendation} | [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) |
| Database | {recommendation} | [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) |
| Auth | {recommendation} | [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) |
| Real-time | {recommendation or "N/A"} | [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) |
| Hosting | {recommendation} | [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) |

### Key Decisions

{2–4 non-obvious architectural choices from 06-system-architecture, e.g.:}
- **{Decision}**: {choice and brief rationale}
- **{Decision}**: {choice and brief rationale}

Full spec: [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) · API patterns: [08-api-surface-spec.md](clone-research/{SLUG}/08-api-surface-spec.md)

---

## Work Phases

Progress is tracked here. Update this section as phases complete.

### Phase 0 — Research ✅ Complete

All 9 research documents produced. See [clone-research/{SLUG}/00-INDEX.md](clone-research/{SLUG}/00-INDEX.md) for executive summary.

### Phase 1 — Scaffold

**Goal**: Runnable skeleton with CI, auth, and empty shell for each major domain entity.

**Done when**:
- [ ] Repo initialized with chosen stack
- [ ] CI pipeline green (lint, type-check, test)
- [ ] Auth working (sign up / log in / log out)
- [ ] Database schema matches domain model entities
- [ ] Empty CRUD routes exist for each core entity

**Must-read before starting**: [03-mvp-scope-contract.md](clone-research/{SLUG}/03-mvp-scope-contract.md), [05-domain-model.md](clone-research/{SLUG}/05-domain-model.md), [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md)

### Phase 2 — MVP Core

**Goal**: The must-nail feature works end-to-end for the primary persona.

**Must-nail feature**: {feature name — from 03-mvp-scope-contract}

**In scope (P0 features)**:
{List each P0 feature ID and name from 03-mvp-scope-contract, one per line as a checkbox}
- [ ] F{N}: {feature name}
- [ ] F{N}: {feature name}
- …

**Done when**: A new user can complete the primary journey in [04-core-user-journeys.md](clone-research/{SLUG}/04-core-user-journeys.md) without hitting a dead end.

### Phase 3 — Growth Features

**Goal**: P1 features that users expect within the first quarter.

**In scope (P1 features)**:
{List each P1 feature ID and name from 03-mvp-scope-contract}
- [ ] F{N}: {feature name}
- [ ] F{N}: {feature name}
- …

**Done when**: All P1 features pass acceptance criteria from [03-mvp-scope-contract.md](clone-research/{SLUG}/03-mvp-scope-contract.md).

### Phase 4 — Launch Ready

**Goal**: Production-quality: billing, onboarding, monitoring, design polish.

- [ ] Pricing tiers implemented (see [07-revenue-pricing-model.md](clone-research/{SLUG}/07-revenue-pricing-model.md))
- [ ] Design system applied (see [09-design-system-brief.md](clone-research/{SLUG}/09-design-system-brief.md))
- [ ] Error handling and observability in place
- [ ] Performance acceptable under realistic load
- [ ] Security review passed

---

## Research Index

| # | Document | What it answers |
|---|----------|----------------|
| 00 | [00-INDEX.md](clone-research/{SLUG}/00-INDEX.md) | Executive summary and reading order |
| 01 | [01-product-thesis.md](clone-research/{SLUG}/01-product-thesis.md) | What {Company} is and why it wins |
| 02 | [02-feature-priority-matrix.md](clone-research/{SLUG}/02-feature-priority-matrix.md) | Feature inventory with P0–P3 priorities |
| 03 | [03-mvp-scope-contract.md](clone-research/{SLUG}/03-mvp-scope-contract.md) | What to build first and what to skip |
| 04 | [04-core-user-journeys.md](clone-research/{SLUG}/04-core-user-journeys.md) | How users interact with the product |
| 05 | [05-domain-model.md](clone-research/{SLUG}/05-domain-model.md) | Core entities and relationships |
| 06 | [06-system-architecture.md](clone-research/{SLUG}/06-system-architecture.md) | Recommended tech stack |
| 07 | [07-revenue-pricing-model.md](clone-research/{SLUG}/07-revenue-pricing-model.md) | Pricing tiers and monetization |
| 08 | [08-api-surface-spec.md](clone-research/{SLUG}/08-api-surface-spec.md) | API design patterns |
| 09 | [09-design-system-brief.md](clone-research/{SLUG}/09-design-system-brief.md) | Visual language and components |
```

> **Note on paths**: `AGENTS.md` lives at the project root. All links use `clone-research/{SLUG}/` prefix pointing to the research directory produced by the skill. Replace `{SLUG}` with the actual kebab-case name (e.g., `clone-research/linear/`).

---

## 00 — INDEX (Generated by Orchestrator)

This document is written by the orchestrator after all agents complete, not by an agent.

```markdown
---
type: clone-research
document: "Index"
target: "{company}"
date: "{YYYY-MM-DD}"
sequence: 00
---

# Clone Research: {Company}

> Research completed {YYYY-MM-DD}. 9 documents produced by 4 parallel research agents.

## Executive Summary

{3-5 bullet points summarizing the key findings:}
- **What they do**: {one sentence}
- **Why they win**: {core advantage}
- **Clone opportunity**: {why a clone makes sense}
- **Key risk**: {biggest challenge}
- **Recommended approach**: {one sentence on strategy}

## Reading Order

### Start Here (Tier 1 — Non-Negotiable)
1. [01-product-thesis.md](01-product-thesis.md) — What the product is and why it wins
2. [02-feature-priority-matrix.md](02-feature-priority-matrix.md) — Complete feature inventory with priorities
3. [03-mvp-scope-contract.md](03-mvp-scope-contract.md) — What to build first and what to skip
4. [04-core-user-journeys.md](04-core-user-journeys.md) — How users actually use the product
5. [05-domain-model.md](05-domain-model.md) — Data entities and relationships
6. [06-system-architecture.md](06-system-architecture.md) — Technical stack and clone architecture

### Then Read (Tier 2 — High Value)
7. [07-revenue-pricing-model.md](07-revenue-pricing-model.md) — Pricing tiers and revenue model
8. [08-api-surface-spec.md](08-api-surface-spec.md) — API design and endpoints
9. [09-design-system-brief.md](09-design-system-brief.md) — Visual language and components

## Cross-Reference Map

| Document | Depends On | Feeds Into |
|----------|-----------|-----------|
| 01 Product Thesis | — | 03, 07 |
| 02 Feature Matrix | — | 03, 04, 05, 08, 09 |
| 03 MVP Scope | 01, 02 | 06 |
| 04 User Journeys | 02 | 05 |
| 05 Domain Model | 02, 04 | 06, 08 |
| 06 Architecture | 03, 05 | 08 |
| 07 Revenue Model | 01, 02 | — |
| 08 API Surface | 05, 06 | — |
| 09 Design System | 02, 06 | — |
```
