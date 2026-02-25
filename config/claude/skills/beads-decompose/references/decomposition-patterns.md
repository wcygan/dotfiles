---
title: Decomposition Patterns
description: Patterns and strategies for breaking product designs into beads task hierarchies
tags: [decomposition, planning, patterns, methodology]
---

# Decomposition Patterns

## Core Principle: Shippable Slices

Every epic should represent a **vertical slice** — a thin, end-to-end piece of functionality that delivers user value. Avoid horizontal slices that build an entire layer (e.g., "all database tables") without connecting to the user.

**Good**: "User can sign up with email" (touches DB, API, UI)
**Bad**: "Create all database schemas" (horizontal, no user value alone)

## Pattern 1: Feature Decomposition

For a new product feature:

```
Epic: User Authentication
├── Task: Design auth database schema (P1)
├── Task: Implement signup API endpoint (P1)
│   └── depends on: schema
├── Task: Implement login API endpoint (P1)
│   └── depends on: schema
├── Task: Build signup form UI (P2)
│   └── depends on: signup API
├── Task: Build login form UI (P2)
│   └── depends on: login API
├── Task: Add session management middleware (P1)
│   └── depends on: login API
├── Task: Write auth integration tests (P2)
│   └── depends on: signup API, login API
└── Task: Add rate limiting to auth endpoints (P3)
    └── depends on: signup API, login API
```

**Key moves:**
- Schema/infrastructure first (everything depends on it)
- API before UI (UI depends on API contract)
- Tests alongside or just after implementation
- Polish/hardening as lower priority

## Pattern 2: System Integration

For connecting to external systems or services:

```
Epic: Payment Processing Integration
├── Task: Spike — evaluate Stripe vs Square API (P1)
├── Task: Create payment service abstraction layer (P1)
│   └── depends on: spike
├── Task: Implement Stripe adapter (P1)
│   └── depends on: abstraction layer
├── Task: Add webhook handler for payment events (P1)
│   └── depends on: Stripe adapter
├── Task: Build checkout flow UI (P2)
│   └── depends on: Stripe adapter
├── Task: Handle payment failure/retry logic (P2)
│   └── depends on: webhook handler
└── Task: Add payment audit logging (P3)
    └── depends on: Stripe adapter
```

**Key moves:**
- Start with a spike when there are unknowns
- Abstraction layer before concrete implementation
- Webhook/async handling as separate concern
- Audit/observability as lower priority

## Pattern 3: Data Pipeline

For ETL, migrations, or data processing features:

```
Epic: Analytics Dashboard
├── Task: Define event schema and tracking plan (P1)
├── Task: Implement event collection API (P1)
│   └── depends on: schema
├── Task: Build event processing pipeline (P1)
│   └── depends on: collection API
├── Task: Create aggregation queries (P2)
│   └── depends on: processing pipeline
├── Task: Build dashboard API endpoints (P2)
│   └── depends on: aggregation queries
├── Task: Build dashboard UI components (P2)
│   └── depends on: dashboard API
└── Task: Add data retention/cleanup job (P3)
    └── depends on: processing pipeline
```

## Pattern 4: Refactoring / Migration

For restructuring existing code:

```
Epic: Migrate from REST to GraphQL
├── Task: Spike — inventory all REST endpoints (P1)
├── Task: Define GraphQL schema for core entities (P1)
│   └── depends on: spike
├── Task: Implement resolvers for read operations (P1)
│   └── depends on: schema
├── Task: Implement mutations for write operations (P1)
│   └── depends on: schema
├── Task: Add GraphQL endpoint alongside REST (P1)
│   └── depends on: resolvers, mutations
├── Task: Migrate frontend to GraphQL queries (P2)
│   └── depends on: GraphQL endpoint
├── Task: Add deprecation warnings to REST (P3)
│   └── depends on: frontend migration
└── Task: Remove REST endpoints (P4)
    └── depends on: deprecation warnings
```

**Key moves:**
- Always run old and new in parallel first
- Migrate consumers before removing old system
- Deprecation before removal

## Pattern 5: Multi-Agent Parallel Work

When designing for multiple agents working simultaneously:

```
Epic: E-Commerce Product Catalog
├── Task: Define product data model (P0)           ← MUST be first
├── Task: Implement product CRUD API (P1)           ← Agent A
│   └── depends on: data model
├── Task: Build product search/filter (P1)          ← Agent B (parallel)
│   └── depends on: data model
├── Task: Build product listing page (P2)           ← Agent C (parallel)
│   └── depends on: data model
├── Task: Build product detail page (P2)
│   └── depends on: CRUD API
├── Task: Add image upload handling (P2)
│   └── depends on: CRUD API
└── Task: Integration tests for catalog flow (P2)
    └── depends on: CRUD API, search, listing page
```

**Key moves:**
- Identify the critical path (data model → everything)
- Maximize parallel lanes by only adding true blocks
- Integration tests depend on all components they cover

## Sizing Guide

| Size | Duration | Decompose? |
|------|----------|------------|
| < 30 min | Trivial | No — single task |
| 30 min–2 hrs | Small | Task, maybe 2-3 subtasks |
| 2–8 hrs | Medium | Epic with 3-6 tasks |
| 1–3 days | Large | Epic with 6-12 tasks |
| > 3 days | Too big | Split into multiple epics |

## Anti-Patterns

**Over-decomposition**: Creating subtasks for trivial steps ("open file", "write function", "save file"). If it takes <30 min, it's one task.

**Over-constraining**: Adding `blocks` dependencies between tasks that could run in parallel. Only block when there's a true data/API dependency.

**Horizontal slicing**: "Build all models", "Build all controllers", "Build all views" — these prevent vertical integration and delay feedback.

**Missing spikes**: Diving into implementation when there are fundamental unknowns. Create a spike task first.

**Implicit dependencies**: Not modeling dependencies because "it's obvious". The graph is for agents — make it explicit.

## Labels for Cross-Cutting Concerns

Use labels to enable filtering across epics:

- `frontend`, `backend`, `database`, `api`, `infra`
- `security`, `performance`, `accessibility`
- `spike`, `testing`, `docs`
- `tech-debt`, `polish`
