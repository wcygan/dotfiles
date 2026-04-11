---
title: Content Guidelines
description: What to include in each generated CLAUDE.md context file
tags: [content, guidelines, CLAUDE.md, context, writing]
---

# Content Guidelines for CLAUDE.md Files

> **Read first**: [`claude-code-best-practices/references/writing-claude-md.md`](../../claude-code-best-practices/references/writing-claude-md.md). That file is the canonical source for CLAUDE.md authoring — this file layers directory-scoped conventions on top of it. When the two disagree, the best-practices reference wins.

## Why This Matters

Every CLAUDE.md you write is injected into every Claude Code session opened in that directory. It competes with the root CLAUDE.md, the skill instructions, and the system prompt for a finite instruction budget. Treat each line as expensive. If a piece of info can be discovered by reading the code, or is already covered by a parent CLAUDE.md, leave it out.

## Core Rules (inherited from writing-claude-md)

- **WHAT / WHY / HOW**: what's in the directory, why it exists, how a developer touches it.
- **Universality within scope**: only rules that apply to *essentially every* task in this directory. Sub-area specifics belong in a deeper CLAUDE.md or an `agent_docs/` file.
- **No linter prose**: formatting, naming, import order — leave to the linter.
- **No long inline code**: use `path/to/file.ext:42` pointers instead of pasting code.
- **No duplication of the parent CLAUDE.md**: if the root already says "this is a pnpm monorepo," don't repeat it.
- **No auto-generated boilerplate**: hand-write every line.

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
