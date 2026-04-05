# Context Repo Structure

A **context repo** is a `context/` directory that lives at the root of a
code repo (not beside it). It holds decisions, architecture maps, specs,
plans, and agent memory — the artifacts that don't belong in source
directories but travel with the code in the same git clone.

The guiding principle: **context travels with the code**. One `git clone`
gets you both. If a project grows to include multiple related subprojects,
they live as subdirectories of the same repo (monorepo model) — never as
separate cloned repos coordinated by a sibling `context/`.

## Layout

```
my-repo/                         # any code repo (single project or monorepo)
├── .git/
├── context/                     # <— this is the context repo
│   ├── CLAUDE.md                # North star. Agents read this first.
│   ├── README.md                # Human overview of what lives here.
│   ├── repos.toml               # Optional. Only when the repo is a monorepo.
│   ├── arch/
│   │   ├── system-map.md        # System diagram + invariants.
│   │   ├── infrastructure.md    # DB/queue/cache/cloud/external services.
│   │   └── projects/<name>.md   # Per-subproject summary (monorepos only).
│   ├── adrs/
│   │   ├── NNNN-<slug>.md       # Immutable. Supersede via new ADR.
│   │   └── INDEX.md             # Generated index with status.
│   ├── specs/<feature-slug>/
│   │   ├── spec.md              # What & why.
│   │   └── plan.md              # How. Ordered task DAG.
│   ├── plans/
│   │   ├── active/              # In-flight plans. Delete on merge.
│   │   └── archive/             # Dated. Historical reference only.
│   └── memory/
│       └── notes.md             # Append-only. Dated entries.
├── src/                         # or apps/, packages/, cmd/, etc.
├── README.md
└── ...
```

`context/` **must not** live under `.claude/`. That directory is for the
Claude Code harness config; `context/` is human-reviewable architecture
documentation that belongs at repo root next to `README.md`.

## `repos.toml` — optional monorepo manifest

Present only when the repo hosts multiple distinct subprojects (apps,
services, packages) that have different languages, test commands, or
owners. Single-project repos omit this file entirely, and skills operate
on the whole repo as one unit.

```toml
version = 1

[workspace]
name = "my-product"
description = "Customer-facing product and supporting services."

[[projects]]
name = "api"
path = "apps/api"             # relative to repo root
purpose = "Public HTTP API and auth"
owners = ["platform"]
language = "go"
test = "go test ./..."
lint = "golangci-lint run"
entry_points = ["cmd/server/main.go"]
depends_on = ["shared"]

[[projects]]
name = "web"
path = "apps/web"
purpose = "Customer-facing SPA"
owners = ["frontend"]
language = "typescript"
test = "pnpm test"
lint = "pnpm lint"
depends_on = ["api"]

[[projects]]
name = "shared"
path = "packages/shared"
purpose = "Shared types, protobuf definitions"
owners = ["platform"]
language = "proto"
```

Required per-project fields: `name`, `path`, `purpose`. Everything else is
optional but recommended — skills use them to run the right commands per
subproject.

**Path rule:** `path` is always relative to the repo root. Never `../`.
Never absolute. A `path` that escapes the repo root is an error.

## ADR format

```markdown
# NNNN: Title (imperative, <60 chars)

- **Status**: Proposed | Accepted | Superseded-by NNNN | Deprecated
- **Date**: YYYY-MM-DD
- **Deciders**: @alice, @bob
- **Affects**: api, web          # project names from repos.toml, or "all"

## Context
What forced the decision. Constraints, pressures, alternatives considered.

## Decision
The choice, in plain language. One paragraph.

## Consequences
Positive, negative, and neutral. Include what becomes harder.

## Follow-ups
- [ ] Concrete task @owner
```

Numbering is strictly sequential. Never renumber. To change a decision,
write a new ADR and mark the old one `Status: Superseded-by NNNN`.

## Spec format (`specs/<slug>/spec.md`)

```markdown
# <Feature Title>

## Problem
Who hurts, how often, why now.

## Goals
- Measurable outcome 1
- Measurable outcome 2

## Non-goals
- Explicitly out of scope

## Affected areas
- apps/api: new endpoints, migration
- apps/web: new route, API client update
- packages/shared: new protobuf messages

## Constraints
- Must ship behind feature flag
- No breaking changes to public API

## Open questions
- [ ] Q1 — owner: @alice
```

On a single-project repo, "Affected areas" is just a list of directories
or modules. On a monorepo, use project names from `repos.toml`.

## Plan format (`specs/<slug>/plan.md`)

```markdown
# <Feature Title> — Execution Plan

## Ordering rationale
Why this order matters (migrations first, compatibility windows, etc).

## Tasks

### 1. packages/shared: add new protobuf messages
- Files: packages/shared/proto/feature.proto
- Verify: `buf build`
- Owner: @alice
- Depends on: none

### 2. apps/api: implement handler behind flag
- Files: apps/api/internal/feature/*.go
- Verify: `go test ./internal/feature/...`
- Owner: @alice
- Depends on: 1

### 3. apps/web: wire up UI
- Files: apps/web/src/routes/feature/*
- Verify: `pnpm test`
- Owner: @bob
- Depends on: 2

## Rollback points
After step 2, rollback is: revert commit, leave shared/proto in place.

## Risk notes
- Migration in step 2 is forward-compatible only — no rollback of data.
```

All task paths are relative to the repo root.

## Invariants (enforced by skills)

1. **`context/` lives inside the code repo it describes.** Never as a
   sibling directory. Never under `.claude/`. Always at repo root.
2. **ADRs are immutable.** Changes are new ADRs that supersede the old one.
3. **`arch/` is regenerated, never silently patched.** `/context-repo-map`
   always shows a diff before writing.
4. **`plans/active/` is garbage-collected.** Delete merged plans; don't
   archive in place. `plans/archive/` is for historical curiosity only.
5. **`memory/notes.md` is append-only.** Entries are dated
   `## YYYY-MM-DD HH:MM` and never edited after write.
6. **`repos.toml` is authoritative when present.** If the file exists,
   every skill reads it first and only acts on listed projects. If it's
   absent, skills treat the repo as a single project rooted at the repo
   root.
7. **All paths are relative to the repo root.** No `../`, no absolutes.
8. **No secrets, binaries, or vendor dirs.** The context repo must stay
   small, reviewable, and shareable.

## Update discipline

| Artifact    | Who updates            | How                                       |
|-------------|------------------------|-------------------------------------------|
| repos.toml  | Human                  | Manual edit, reviewed in PR               |
| arch/       | Agent + human          | `/context-repo-map` then review diff      |
| adrs/       | Human (agent-assisted) | `/context-repo-adr new`, reviewed         |
| specs/      | Human + agent          | `/context-repo-spec` interview            |
| plans/      | Agent                  | `/context-repo-plan` → reviewed → execute |
| memory/     | Agent                  | Append-only during execution              |

## Why this shape

- **Context co-located with code** — one clone, one source of truth. No
  separate repo to keep in sync, no sibling-layout coordination.
- **Flat, predictable paths** — agents don't need to search. Every skill
  knows exactly where to read and write: `$(git rev-parse --show-toplevel)/context`.
- **Immutable history (ADRs)** — prevents the "confidently-cites-reversed-decision"
  failure mode.
- **Human review gates** — `arch/` and `specs/` are regenerated with diffs,
  not silent rewrites, so staleness is visible.
- **Append-only memory** — agent memory that edits itself self-poisons;
  append-only sidesteps that entirely.
- **Delete-on-merge plans** — `plans/active/` stays small; completed work
  lives in git history, not in a directory that grows forever.
- **Optional monorepo manifest** — `repos.toml` only appears when it earns
  its keep. Single-project repos stay ceremony-free.
