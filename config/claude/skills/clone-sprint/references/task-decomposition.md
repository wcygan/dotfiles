---
title: Task Decomposition
description: Transforms clone-research output into a beads task DAG with rich descriptions
tags: [decomposition, task-dag, research, bounded-context, vertical-slice, epics]
---

# Task Decomposition

## Overview

This document defines how the orchestrator reads the 9 clone-research documents and
produces a beads task DAG. The key principles:

1. **Bounded contexts → epics** (from doc 05)
2. **P0 features → subtasks grouped by context** (from doc 02)
3. **Vertical slices, not horizontal layers** — each task is a complete feature
4. **Rich descriptions** — embed enough context that agents rarely read research docs
5. **Scaffold epic blocks everything** — project structure lands first

## Research Document Mapping

Each research document contributes specific data to task creation:

| Research Doc | Role in Decomposition |
|-------------|----------------------|
| `00-INDEX.md` | Executive summary → agent preamble; cross-reference map → DAG validation; known gaps → skip missing docs |
| `01-product-thesis.md` | Project context for agent preamble (what we're building and why) |
| `02-feature-priority-matrix.md` | Feature IDs, priorities, effort estimates → subtask creation and ordering |
| `03-mvp-scope-contract.md` | Acceptance criteria, in/out scope → task acceptance field, scope guard |
| `04-core-user-journeys.md` | User flows → journey-aware task ordering (login before dashboard) |
| `05-domain-model.md` | Bounded contexts → epics; entities/aggregates → task domain context |
| `06-system-architecture.md` | Recommended stack → agent preamble; file structure conventions → suggested file targets |
| `07-revenue-pricing-model.md` | Pricing features → billing context tasks (if P0) |
| `08-api-surface-spec.md` | Endpoints → API task descriptions, request/response schemas |
| `09-design-system-brief.md` | Design tokens, component specs → UI task descriptions |

### Effort Scale Mapping

Clone-research uses single-letter effort codes (`S`, `M`, `L`, `XL`). Clone-sprint
labels use two-letter codes for clarity in beads. Map when creating tasks:

| Research (doc 02) | Beads Label | Meaning |
|-------------------|-------------|---------|
| S | `sm` | < 1 week |
| M | `md` | 1-2 weeks |
| L | `lg` | 2-4 weeks |
| XL | `xl` | > 4 weeks |

## Step 1: Extract Bounded Contexts (Doc 05)

Read `05-domain-model.md` and extract each bounded context:

```
Bounded Contexts found:
- Auth (entities: User, Session, Credential)
- Workspace (entities: Workspace, Member, Invitation)
- Project (entities: Project, Task, Comment)
- Billing (entities: Subscription, Plan, Invoice)
- Notification (entities: Notification, Preference)
```

Each bounded context becomes an **epic** in beads.

## Step 2: Extract P0 Features (Doc 02)

Read `02-feature-priority-matrix.md` and collect all P0 (must-have) features:

```
P0 Features:
- F1: User Registration/Login (effort: MD, context: Auth)
- F2: Create Workspace (effort: MD, context: Workspace)
- F3: Invite Members (effort: LG, context: Workspace)
- F4: Create Project (effort: SM, context: Project)
- F5: Task CRUD (effort: LG, context: Project)
- F6: Stripe Billing (effort: XL, context: Billing)
```

Map each feature to its bounded context. Features that span contexts get assigned
to the context that owns the primary entity.

## Step 3: Create Scaffold Epic

The scaffold epic is always created first and blocks all other epics:

```bash
SCAFFOLD_ID=$(bd create "Project Scaffold" -t epic -p 1 --label "scaffold,infra" \
  --description "$(cat <<'DESC'
## Project Scaffold

Initialize project structure, database configuration, and design system foundation.
Must complete before any feature work begins.

### From doc 06 (System Architecture):
- Framework: {recommended framework}
- Database: {recommended database}
- Directory structure: {recommended layout}

### From doc 09 (Design System Brief):
- CSS framework: {recommended}
- Color tokens: {primary, secondary, etc.}
- Typography scale: {font family, sizes}
- Component library: {if recommended}

### Subtasks:
1. Initialize project with framework CLI
2. Configure database connection + initial migration
3. Set up design system tokens + base layout
4. Configure CI pipeline
5. Add linting, formatting, test runner
DESC
)"
)
```

Scaffold subtasks:

```bash
bd create "Scaffold: Project Init — infra" -p 1 --label "scaffold,infra,sm" \
  --description "Initialize {framework} project, configure TypeScript/linting"

bd create "Scaffold: Database Setup — data" -p 1 --label "scaffold,data,sm" \
  --description "Configure {database}, create connection pool, initial migration"

bd create "Scaffold: Design System Foundation — ui" -p 1 --label "scaffold,ui,sm" \
  --description "Set up {css-framework}, configure tokens from doc 09, base layout"

bd create "Scaffold: CI Pipeline — infra" -p 1 --label "scaffold,infra,sm" \
  --description "GitHub Actions: lint, type-check, test, build"
```

## Step 4: Create Feature Epics

For each bounded context with P0 features, create an epic that depends on scaffold:

```bash
EPIC_ID=$(bd create "Auth System" -t epic -p 1 --label "auth" \
  --description "$(cat <<'DESC'
## Bounded Context: Authentication

### Entities (from doc 05):
- User { id, email, passwordHash, name, avatar, createdAt, updatedAt }
- Session { id, userId, token, expiresAt, createdAt }
- Credential { id, userId, provider, providerUserId }

### Aggregates:
- UserAggregate: User + Session + Credential

### Domain Rules:
- Passwords must be >= 8 chars, hashed with bcrypt
- Sessions expire after 7 days
- One active session per device

### Features (from doc 02):
- F1: Registration/Login (P0, MD)
- F7: Password Reset (P1, SM)
- F12: OAuth Login (P2, MD)
DESC
)"
)

# Scaffold blocks this epic
bd dep add $EPIC_ID $SCAFFOLD_ID
```

## Step 5: Create Feature Subtasks

Each P0 feature becomes a subtask under its epic. The task description is **rich** —
it embeds all context the builder agent needs.

### Rich Description Template

```markdown
## Feature: {Feature Name}

### Context
{One-paragraph summary from doc 01 product thesis — why this feature matters}

### Entities (from doc 05)
- {Entity} { field: type, field: type, ... }
- {Entity} { field: type, field: type, ... }

### API Endpoints (from doc 08)
- {METHOD} {path} — {request schema} → {response schema}
- {METHOD} {path} — {request schema} → {response schema}

### Acceptance Criteria (from doc 03)
- [ ] {criterion 1}
- [ ] {criterion 2}
- [ ] {criterion 3}

### User Flow (from doc 04)
1. User {action}
2. System {response}
3. User sees {outcome}

### Design Tokens (from doc 09)
- {component}: {token values}
- {component}: {token values}

### Suggested File Targets (inferred from doc 06 conventions)
- {path/to/file.ext} — {purpose}
- {path/to/file.ext} — {purpose}

### Xref
- 02: {feature ID} ({priority}, effort: {effort})
- 03: {section reference}
- 08: {endpoint reference}
```

### Example: Login Form Task

```bash
bd create "Auth: Login Form — fullstack" -p 1 \
  --label "auth,fullstack,md" \
  --acceptance "$(cat <<'ACC'
- [ ] Email + password form with client-side validation
- [ ] POST /api/auth/login endpoint with bcrypt comparison
- [ ] HttpOnly session cookie set on success (7-day expiry)
- [ ] Error states: invalid credentials (401), rate limit (429)
- [ ] Redirect to /dashboard on successful login
- [ ] Loading state on submit button
ACC
)" \
  --design "$(cat <<'DESIGN'
Stack: Next.js App Router + Prisma + PostgreSQL
Auth: Session-based with HttpOnly cookies (no JWT)
Validation: Zod schemas shared between client/server
DESIGN
)" \
  --description "$(cat <<'DESC'
## Feature: Login Form

### Context
Core authentication flow. Users must log in to access any workspace functionality.
This is the entry point for all returning users (from doc 01).

### Entities (from doc 05)
- User { id: uuid, email: string, passwordHash: string, name: string, createdAt: datetime }
- Session { id: uuid, userId: uuid, token: string, expiresAt: datetime }

### API Endpoints (from doc 08)
- POST /api/auth/login — { email: string, password: string } → { user: User }
  - Sets HttpOnly cookie with session token
  - 401 if credentials invalid
  - 429 if rate limited (5 attempts per 15 min)

### User Flow (from doc 04)
1. User navigates to /login
2. User enters email and password
3. User clicks "Sign In"
4. System validates credentials against User table
5. System creates Session record
6. System sets HttpOnly cookie
7. System redirects to /dashboard

### Design Tokens (from doc 09)
- Card: rounded-lg border bg-card p-6 shadow-sm
- Input: h-10 w-full rounded-md border border-input px-3
- Button (primary): bg-primary text-primary-foreground h-10 px-4 rounded-md
- Error text: text-sm text-destructive
- Link: text-sm text-muted-foreground underline-offset-4 hover:underline

### Suggested File Targets (inferred from doc 06 conventions)
- src/app/login/page.tsx — Login page component
- src/app/api/auth/login/route.ts — Login API endpoint
- src/lib/auth.ts — Auth utilities (hash, verify, session)
- src/lib/validations/auth.ts — Zod schemas for auth
- prisma/migrations/XXXX_auth/migration.sql — User + Session tables

### Xref
- 02-feature-priority-matrix.md: F1 (P0, effort: MD)
- 03-mvp-scope-contract.md: Section "Authentication" acceptance criteria
- 08-api-surface-spec.md: POST /api/auth/login
DESC
)"
```

## Step 6: Wire Dependencies

Dependencies follow the user journey flow (doc 04) and data model relationships:

### Dependency Rules

1. **Scaffold blocks all feature epics** — always
2. **Within an epic**: tasks that produce data schemas block tasks that consume them
3. **Between epics**: follow entity relationships from doc 05
   - If Workspace has `ownerId → User`, then Auth epic blocks Workspace epic
4. **Journey ordering** (doc 04): login before dashboard, create-workspace before invite

### Example Dependency Graph

```
Project Scaffold (bd-0001)
├── blocks → Auth System (bd-0002)
│   ├── Auth: Registration — fullstack (bd-0002.1)
│   ├── Auth: Login — fullstack (bd-0002.2) [blocked-by bd-0002.1]
│   └── Auth: Session Middleware — api (bd-0002.3) [blocked-by bd-0002.2]
├── blocks → Workspace System (bd-0003) [also blocked-by bd-0002]
│   ├── Workspace: Create — fullstack (bd-0003.1)
│   ├── Workspace: Invite Members — fullstack (bd-0003.2) [blocked-by bd-0003.1]
│   └── Workspace: Settings — fullstack (bd-0003.3) [blocked-by bd-0003.1]
└── blocks → Project System (bd-0004) [also blocked-by bd-0003]
    ├── Project: Create — fullstack (bd-0004.1)
    ├── Project: Task CRUD — fullstack (bd-0004.2) [blocked-by bd-0004.1]
    └── Project: Comments — fullstack (bd-0004.3) [blocked-by bd-0004.2]
```

```bash
# Scaffold blocks everything
bd dep add bd-0002 bd-0001
bd dep add bd-0003 bd-0001
bd dep add bd-0004 bd-0001

# Cross-context dependencies
bd dep add bd-0003 bd-0002    # Workspace needs Auth
bd dep add bd-0004 bd-0003    # Project needs Workspace

# Intra-epic dependencies
bd dep add bd-0002.2 bd-0002.1   # Login needs Registration
bd dep add bd-0002.3 bd-0002.2   # Middleware needs Login
```

## Step 7: Validate the DAG

After creating all tasks and dependencies:

```bash
# Check for cycles
bd swarm validate $SCAFFOLD_ID --verbose

# Verify ready tasks are only scaffold subtasks
READY=$(bd ready --json)
echo "$READY" | jq '.[].title'
# Should show only scaffold tasks (nothing else is unblocked)

# Overall stats
bd stats --json
```

## Decomposition Anti-Patterns

### DO NOT: Decompose by Layer

```
BAD:
- "Create all database migrations"
- "Build all API endpoints"
- "Create all React components"
```

This creates cross-agent file conflicts and prevents independent testing.

### DO NOT: Create Thin Tasks

```
BAD:
- "Create User model"  (no API, no UI, no tests)
- "Add login button"   (no handler, no endpoint)
```

Each task must be a complete, testable vertical slice.

### DO NOT: Skip Rich Descriptions

```
BAD:
bd create "Login form" -p 1
```

Without entity definitions, API specs, design tokens, and file targets, the builder
agent will guess — and guess wrong.

### DO NOT: Create More Than ~30 Tasks for MVP

If the DAG has >30 tasks, features are too granular. Combine related features
into broader slices. A typical MVP has 4-6 epics with 3-5 tasks each.

## Effort Calibration

From doc 02's effort estimates (mapped via the effort scale above):

| Research Effort | Beads Label | Expected Subtasks | Sprint Estimate |
|-----------------|-------------|-------------------|-----------------|
| S | `sm` | 1-2 tasks | 1 sprint |
| M | `md` | 2-4 tasks | 1-2 sprints |
| L | `lg` | 4-6 tasks | 2-3 sprints |
| XL | `xl` | 6-8 tasks | 3-4 sprints |

Each sprint handles 2-3 tasks (from different contexts when possible).
