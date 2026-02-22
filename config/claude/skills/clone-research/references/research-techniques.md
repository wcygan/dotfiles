---
title: Research Techniques
description: Targeted search strategies and query patterns for each research agent
tags: [research, search, queries, websearch, webfetch]
---

# Research Techniques

Each agent performs 8-12 targeted searches. This file provides the query patterns organized by agent role.

## Common Rules

- Start with the company's own website and docs
- Use quotes for exact-match company names: `"{company}"`
- Cross-reference claims across 2+ sources before asserting High confidence
- If a query returns nothing useful after 2 attempts, note "Not publicly available" and move on
- Prioritize breadth — cover all template sections rather than going deep on one

## Product Strategist Queries

Focus: company background, market position, business model, pricing.

| # | Query Pattern | Purpose |
|---|---------------|---------|
| 1 | `WebFetch {homepage_url}` | Extract tagline, hero messaging, value prop |
| 2 | `"{company}" about founded funding investors` | Company background, funding history |
| 3 | `"{company}" pricing plans tiers` | Pricing page or pricing announcements |
| 4 | `WebFetch {pricing_url}` (if found) | Detailed tier breakdown |
| 5 | `"{company}" revenue ARR valuation` | Revenue signals |
| 6 | `"{company}" vs` | Competitor comparison pages, positioning |
| 7 | `"{company}" mission vision values` | Company narrative |
| 8 | `"{company}" acquisition partnership` | Strategic moves |
| 9 | `"{company}" market share {category}` | Market position |
| 10 | `"{company}" investor funding round 2024 2025 2026` | Recent funding |

### What to Extract

- North star / mission statement
- Target customer segments
- Revenue model (SaaS, usage-based, freemium, etc.)
- Competitive positioning (who they compare themselves to)
- Funding stage and trajectory

## UX Researcher Queries

Focus: features, user flows, onboarding, reviews, user sentiment.

| # | Query Pattern | Purpose |
|---|---------------|---------|
| 1 | `WebFetch {homepage_url}/features` or `/product` | Feature inventory |
| 2 | `WebFetch {homepage_url}/signup` or `/register` | Signup flow friction |
| 3 | `"{company}" features list` | Feature pages, comparison pages |
| 4 | `"{company}" review G2 Capterra` | User reviews, ratings |
| 5 | `site:reddit.com "{company}" review experience` | Unfiltered user sentiment |
| 6 | `"{company}" changelog "what's new" updates 2025 2026` | Recent feature updates |
| 7 | `"{company}" onboarding experience demo walkthrough` | Onboarding patterns |
| 8 | `site:youtube.com "{company}" demo tutorial` | Product demos |
| 9 | `"{company}" complaints limitations frustration` | Pain points |
| 10 | `"{company}" alternative switching from` | Why users leave |
| 11 | `"{company}" mobile app review iOS Android` | Mobile experience |
| 12 | `"{company}" keyboard shortcuts power user` | Power user features |

### What to Extract

- Complete feature inventory (name + description + tier)
- Core user workflow / usage loop
- Signup-to-value friction count
- Top 5 user complaints (from reviews/Reddit)
- Key UX patterns (navigation, search, shortcuts, real-time)
- Recent feature velocity (updates per month)

## Technical Architect Queries

Focus: tech stack, API design, data model signals, architecture patterns.

| # | Query Pattern | Purpose |
|---|---------------|---------|
| 1 | `"{company}" API documentation developer docs` | API docs |
| 2 | `WebFetch {api_docs_url}` (if found) | API structure, endpoints, auth |
| 3 | `"{company}" engineering blog tech stack architecture` | Architecture posts |
| 4 | `site:stackshare.io "{company}"` | StackShare profile |
| 5 | `"{company}" open source github` | OSS projects, language signals |
| 6 | `"{company}" hiring engineer job posting` | Stack from job descriptions |
| 7 | `"{company}" infrastructure scale performance` | Infrastructure details |
| 8 | `"{company}" security SOC compliance GDPR` | Security posture |
| 9 | `"{company}" webhook integration real-time sync` | Integration architecture |
| 10 | `"{company}" data model schema entities` | Data model signals |
| 11 | `"{company}" GraphQL REST API design` | API style |
| 12 | `"{company}" offline local-first sync` | Sync architecture |

### What to Extract

- Technology table (frontend, backend, DB, infra) with confidence levels
- API type (REST/GraphQL/gRPC), auth method, rate limits
- Architecture pattern (monolith vs micro, SSR vs SPA)
- Key entities visible from API (resources = domain model hints)
- Sync strategy (real-time, polling, local-first)
- Data format patterns (pagination, error format, envelope)

## Design Analyst Queries

Focus: visual language, design system, component patterns, responsive design.

| # | Query Pattern | Purpose |
|---|---------------|---------|
| 1 | `WebFetch {homepage_url}` | Visual analysis of landing page |
| 2 | `"{company}" design system styleguide` | Published design system |
| 3 | `WebFetch {design_system_url}` (if found) | Component inventory |
| 4 | `"{company}" brand guidelines logo` | Brand identity |
| 5 | `"{company}" dark mode theme` | Theme support |
| 6 | `"{company}" mobile responsive app design` | Mobile/responsive approach |
| 7 | `"{company}" accessibility WCAG` | Accessibility standards |
| 8 | `"{company}" UI component library` | Component framework |
| 9 | `site:dribbble.com "{company}"` | Design artifacts |
| 10 | `"{company}" design team designer hiring` | Design culture signals |

### What to Extract

- Color palette (primary, secondary, accent, semantic)
- Typography (font families, scale, weights)
- Spacing system (base unit if detectable)
- Key components (buttons, forms, cards, modals, navigation)
- Layout patterns (sidebar, top-nav, responsive breakpoints)
- Icon style (outline, filled, custom, library)
- Dark mode implementation
- Motion/animation patterns
