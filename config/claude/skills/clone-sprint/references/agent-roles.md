---
title: Agent Roles
description: Builder agent types, selection criteria, and prompt templates for clone-sprint
tags: [agents, builder, prompt-templates, worktree, parallel]
---

# Agent Roles

## Overview

Clone-sprint spawns builder agents via the `Task` tool with `isolation: worktree`.
Each agent receives a rich prompt composed from research documents and task metadata.
This document defines the 5 builder types, their selection criteria, and prompt templates.

All builders use `subagent_type: "general-purpose"` — the type distinction is in the
prompt content, not the agent infrastructure.

## Agent Types

### 1. Fullstack Builder

**When used:** Default for vertical feature slices that span data + API + UI.

**Primary concern:** Complete, testable feature within one bounded context.

**Implementation order:**
1. Database schema/migration
2. Data access layer (ORM model, queries)
3. API endpoint (route, validation, handler)
4. UI component (page, form, data fetching)
5. Tests (unit for logic, integration for API)

**File scope:** All files within the bounded context's directory subtree.

### 2. Data Builder

**When used:** Schema-only tasks — migrations, seed data, data access layers.
Typically used for scaffold database setup or complex schema tasks.

**Primary concern:** Correct migrations, type-safe data access, seed data.

**Implementation order:**
1. Migration file
2. ORM model / type definitions
3. Data access functions (CRUD)
4. Seed data (if applicable)
5. Tests (migration up/down, query correctness)

**File scope:** `prisma/`, `drizzle/`, `src/db/`, `src/models/`, or equivalent.

### 3. API Builder

**When used:** API-only tasks — routes, middleware, validation. Used when API
complexity justifies a dedicated agent (e.g., webhook handlers, OAuth flows).

**Primary concern:** Correct request/response handling, validation, error codes.

**Implementation order:**
1. Request/response schemas (Zod, io-ts, etc.)
2. Route handler
3. Middleware (auth, rate limiting)
4. Integration tests (happy path + error cases)

**File scope:** `src/api/`, `src/routes/`, `src/middleware/`, or equivalent.

### 4. UI Builder

**When used:** Frontend-only tasks — components, pages, styles. Used when the
API already exists and UI is the remaining work.

**Primary concern:** Correct component composition, design token usage, accessibility.

**Implementation order:**
1. Shared components (if new)
2. Page component
3. Data fetching / state management
4. Styles (design tokens from doc 09)
5. Tests (component rendering, user interaction)

**File scope:** `src/app/`, `src/components/`, `src/styles/`, or equivalent.

### 5. Infra Builder

**When used:** Scaffolding, CI, configuration. Used for the scaffold epic and
any infrastructure-specific tasks (Docker, CI pipelines, env config).

**Primary concern:** Correct configuration, reproducible builds, security.

**Implementation order:**
1. Configuration files
2. Build scripts / CI workflows
3. Environment variable handling
4. Documentation (if required by task)

**File scope:** Root config files, `.github/`, `scripts/`, `docker/`, or equivalent.

## Agent Selection Logic

```
Given a task with labels [context, layer, effort]:

if layer == "infra":
    agent_type = "Infra Builder"
elif layer == "data":
    agent_type = "Data Builder"
elif layer == "api":
    agent_type = "API Builder"
elif layer == "ui":
    agent_type = "UI Builder"
else:  # "fullstack" or unspecified
    agent_type = "Fullstack Builder"
```

## Prompt Structure

Every builder agent receives a prompt composed of three sections:

### Section 1: Common Preamble

Shared by all agent types. Provides project-wide context.

```markdown
# Builder Agent: {agent_name}

## Task
- **ID:** {task_id}
- **Title:** {task_title}
- **Type:** {agent_type}
- **Priority:** {priority}

## Project Context

### What We're Building (from doc 01)
{One-paragraph product thesis}

### Stack (from doc 06)
- Framework: {framework}
- Language: {language}
- Database: {database}
- CSS: {css_framework}
- Package Manager: {package_manager}

### Domain Context (from doc 05)
**Bounded Context:** {context_name}
**Entities:**
{entity_definitions}

**Aggregates:**
{aggregate_definitions}

**Domain Rules:**
{domain_rules}

## Commit Conventions
- Prefix: `feat({context}):` for features, `fix({context}):` for fixes
- One commit per logical change
- All tests must pass before committing
- Format and lint before committing

## Constraints
- Work ONLY in your worktree — do not modify files outside your bounded context
- Write tests for all business logic
- Follow the existing project structure (from doc 06)
- Use design tokens from doc 09 for all UI work
- Do NOT install new dependencies without noting them in your completion message
```

### Section 2: Type-Specific Instructions

Appended based on agent type.

#### Fullstack Builder Instructions

```markdown
## Implementation Instructions (Fullstack)

You are building a complete vertical slice. Follow this order strictly:

1. **Schema First:** Create or update the database migration for entities listed below.
   Ensure foreign keys, indexes, and constraints are correct.

2. **Data Access:** Create the ORM model and data access functions. Export typed
   query functions (create, read, update, delete as needed).

3. **API Endpoint:** Create the route handler with:
   - Input validation (use Zod or equivalent from project stack)
   - Auth middleware (if the endpoint requires authentication)
   - Proper HTTP status codes and error responses
   - JSON response matching the API spec below

4. **UI Component:** Create the page/component with:
   - Form handling and client-side validation
   - Data fetching (server components or client hooks as appropriate)
   - Loading, error, and empty states
   - Design tokens from the spec below

5. **Tests:** Write at minimum:
   - Unit test for data access functions
   - Integration test for the API endpoint
   - Component render test for the UI

### API Specification
{endpoints_from_doc_08}

### Acceptance Criteria
{acceptance_from_doc_03}

### Design Tokens
{design_tokens_from_doc_09}

### File Targets
{file_targets_from_doc_06}
```

#### Data Builder Instructions

```markdown
## Implementation Instructions (Data)

You are building the data layer. Focus on correctness and type safety.

1. **Migration:** Create the migration file. Include:
   - Table creation with all columns, types, and constraints
   - Foreign keys with ON DELETE behavior
   - Indexes for frequently queried columns
   - Migration rollback (down migration)

2. **ORM Model:** Create/update the model definition:
   - All fields with correct types
   - Relations to other models
   - Validation at the model level

3. **Data Access Functions:** Export typed CRUD functions:
   - Create: accept validated input, return created entity
   - Read: by ID, by unique fields, list with pagination
   - Update: partial update, return updated entity
   - Delete: soft delete if applicable

4. **Seed Data:** If the task requires initial data:
   - Create realistic seed data (not "test123")
   - Make seed idempotent (upsert, not insert)

5. **Tests:**
   - Migration up/down test
   - CRUD function tests with test database
   - Edge cases: unique constraints, foreign key violations

### Entity Definitions
{entities_from_doc_05}

### File Targets
{file_targets_from_doc_06}
```

#### API Builder Instructions

```markdown
## Implementation Instructions (API)

You are building API endpoints. Focus on correctness, validation, and error handling.

1. **Schemas:** Define request/response schemas:
   - Zod (or project equivalent) for runtime validation
   - TypeScript types derived from schemas
   - Document edge cases in schema comments

2. **Route Handler:** Implement the endpoint:
   - Parse and validate request body/params/query
   - Call data access layer (do NOT write raw SQL)
   - Return proper HTTP status codes
   - Include error response bodies

3. **Middleware:** Add/configure middleware:
   - Auth check (if protected endpoint)
   - Rate limiting (if specified)
   - CORS (if needed)

4. **Tests:**
   - Happy path: valid request → expected response
   - Validation: invalid input → 400 with error details
   - Auth: unauthenticated → 401, unauthorized → 403
   - Edge cases: not found (404), conflict (409)

### API Specification
{endpoints_from_doc_08}

### Acceptance Criteria
{acceptance_from_doc_03}

### File Targets
{file_targets_from_doc_06}
```

#### UI Builder Instructions

```markdown
## Implementation Instructions (UI)

You are building frontend components. Focus on design fidelity and user experience.

1. **Components:** Build from smallest to largest:
   - Shared primitives (if new ones needed)
   - Feature-specific components
   - Page composition

2. **Data Fetching:** Connect to existing API:
   - Server components for initial data (if Next.js/Remix)
   - Client hooks for mutations and dynamic data
   - Loading skeletons matching final layout

3. **Styling:** Apply design tokens exactly:
   - Use project's CSS framework classes
   - Match spacing, colors, typography from spec
   - Responsive: mobile-first, test at 375px and 1280px

4. **States:** Handle all UI states:
   - Loading (skeleton or spinner)
   - Empty (helpful message + CTA)
   - Error (user-friendly message + retry)
   - Success (confirmation + next action)

5. **Tests:**
   - Component renders without error
   - Interactive elements respond to user actions
   - Form validation shows correct error messages

### User Flow
{flow_from_doc_04}

### Design Tokens
{design_tokens_from_doc_09}

### Acceptance Criteria
{acceptance_from_doc_03}

### File Targets
{file_targets_from_doc_06}
```

#### Infra Builder Instructions

```markdown
## Implementation Instructions (Infra)

You are building project infrastructure. Focus on correctness, security, and reproducibility.

1. **Configuration:** Create/update config files:
   - Use environment variables for secrets (never hardcode)
   - Document required env vars in .env.example
   - Use sensible defaults for development

2. **Build/CI:** Set up pipelines:
   - Install dependencies
   - Lint + type check
   - Run tests
   - Build for production
   - Use caching where possible

3. **Security:**
   - No secrets in code or config files
   - Restrict permissions (least privilege)
   - Pin dependency versions

4. **Documentation:**
   - README setup instructions (if scaffold)
   - Environment variable documentation
   - Development workflow notes

### Architecture Spec
{architecture_from_doc_06}

### File Targets
{file_targets_from_doc_06}
```

### Section 3: Task-Specific Content

The task description from beads (created during decomposition) is appended verbatim.
This contains the entity definitions, API endpoints, acceptance criteria, design tokens,
and file targets specific to this task.

```markdown
## Task Description

{task.description}

## Acceptance Criteria

{task.acceptance}

## Design Notes

{task.design}
```

## Spawning Agents

The orchestrator spawns agents via the `Task` tool:

```python
Task(
    name="builder-{context}-{feature_slug}",
    description="Build {feature} in {context}",
    subagent_type="general-purpose",
    isolation="worktree",
    prompt=compose_prompt(
        preamble=common_preamble(project_context, task),
        instructions=type_instructions(agent_type, task),
        task_content=task.description + task.acceptance + task.design
    )
)
```

### Naming Convention

Agent names follow: `builder-{bounded_context}-{feature_slug}`

Examples:
- `builder-auth-login`
- `builder-workspace-create`
- `builder-billing-stripe`
- `builder-scaffold-init`

### Parallel Limits

**Hard limit: 3 agents per sprint.**

Reasons:
- Merge conflicts scale quadratically with agent count
- Context window pressure from monitoring multiple agents
- Diminishing returns past 3 concurrent builders

**Soft guideline: 2 agents from different contexts.**

This minimizes file overlap. Only go to 3 if all tasks are in distinct contexts.

## Agent Completion

When a builder agent finishes, it should report:

1. **Files modified** — list of files created or changed
2. **Tests passing** — confirmation that all tests pass
3. **Dependencies added** — any new packages installed
4. **Blockers found** — any issues discovered during implementation
5. **Commit summary** — list of commits made in the worktree

The orchestrator uses this report to inform merge strategy and sprint reporting.
