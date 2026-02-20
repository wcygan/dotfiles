---
title: Content Guidelines
description: What to include in each generated CLAUDE.md context file
tags: [content, guidelines, CLAUDE.md, context, writing]
---

# Content Guidelines for CLAUDE.md Files

## Target Structure (under 40 lines)

```markdown
# <Directory Name>

<1–2 sentence overview of what this directory is for and why it exists.>

## Contents

- `subdir/` — one-line description of what lives there
- `filename.ext` — one-line description of what it does

## Usage

<How this directory fits into the larger project: what reads from it, what writes to
it, when a developer would touch it.>
```

## What to Read Before Writing

Scan these files (if they exist) to infer purpose — stop reading once you have enough:

1. `README.md` or `README.rst`
2. `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `build.gradle`
3. `Makefile`, `justfile`
4. First 30 lines of `index.*`, `main.*`, `mod.*`, `lib.*`
5. Any `.md` files present

## Writing Principles

- **Audience**: A developer or AI agent unfamiliar with this directory who needs to orient fast
- **Concise**: Under 40 lines total — ruthlessly cut anything not essential
- **No duplication**: Don't re-state information already in the parent CLAUDE.md
- **Present tense**: "This directory contains…", "Use this when…"
- **Factual**: Only describe what you can observe; no speculation about future plans
- **Contents list**: Include key subdirectories and non-obvious files; skip boilerplate files

## Example — Good Output

```markdown
# src/api

HTTP handler layer for the REST API. All route registrations and request/response
shapes live here; business logic is delegated to `src/services/`.

## Contents

- `handlers/` — one handler file per resource (users, orders, products)
- `middleware/` — auth, logging, and rate-limiting middleware
- `router.go` — registers all routes and attaches middleware chain

## Usage

Entry point is `router.go`, called once from `main.go` at startup. Add new endpoints
by creating a handler in `handlers/` and registering it in `router.go`.
```

## Example — Bad Output (avoid)

```markdown
# src/api

This directory has some Go files for the API. There are handlers and middleware.
It is used by the application.
```

Bad because: vague, no structure, no actionable information about where to add things.
