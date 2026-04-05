---
name: context-repo
description: >
  Conventions for context repos — a context/ directory that lives at the
  root of a code repo and holds decisions, architecture maps, specs, plans,
  and agent memory. Load when the current git repo contains a context/
  directory, or when the user mentions context repos, architecture decision
  records, cross-project planning, arch maps, or repo brain. Keywords:
  context repo, ADR, architecture decision record, arch map, system map,
  feature spec, cross-project plan, repo brain, agent memory
---

# Context Repo Convention

A **context repo** is a `context/` directory that lives at the root of a
code repo (not beside it). It is the repo's shared brain: decisions, maps,
specs, plans, and agent memory that don't belong in any source directory
but travel with the code in the same git clone.

## When you're in a repo with a context repo

If `$(git rev-parse --show-toplevel)/context` exists:

1. **Read `context/CLAUDE.md` first.** It is the north star for the repo.
2. **If `context/repos.toml` exists, read it.** The repo is a monorepo; the
   file lists every subproject with paths, owners, test commands, and
   dependencies. If the file is absent, the repo is a single project —
   operate on it as a whole.
3. **Consult `context/arch/` before assuming anything about the repo's
   shape.** The maps may be stale, but they're a faster starting point
   than re-reading the whole codebase.
4. **Check `context/adrs/INDEX.md`** when a decision seems load-bearing.
   Never invent a rationale that contradicts an accepted ADR without
   flagging it explicitly to the user.
5. **Log significant actions to `context/memory/notes.md`** — append-only,
   dated `## YYYY-MM-DD HH:MM`.

## Topic Routing

| Topic | Reference | When to load |
|-------|-----------|--------------|
| Directory layout, file formats, schemas | [structure](references/structure.md) | Creating or modifying any file under `context/` |
| Skill lifecycle, hand-off contracts, invocation chains | [workflow](references/workflow.md) | Choosing which `/context-repo-*` skill to run next, or understanding how they compose |

Load `structure.md` whenever you need to write files. Load `workflow.md`
whenever the user asks "what's next" or you need to decide which skill
comes after another.

## Available skills

All context-repo skills are user-invoked (`/context-repo-*`). You do not
auto-trigger them; suggest them when appropriate, and always suggest the
next skill in the workflow after completing one.

| Skill | Purpose | Typical predecessor | Typical successor |
|-------|---------|---------------------|-------------------|
| `/context-repo-init` | Scaffold a new `context/` inside the current repo | (none — entry point) | `/context-repo-map all` |
| `/context-repo-map [scope]` | Generate/refresh `arch/` docs | `/context-repo-init` or `/context-repo-refresh` | `/context-repo-spec` or `/context-repo-adr new` |
| `/context-repo-spec <slug>` | Interview-driven feature spec | `/context-repo-map` | `/context-repo-plan` |
| `/context-repo-plan <slug>` | Turn a spec into an ordered task DAG | `/context-repo-spec` | `/context-repo-execute` |
| `/context-repo-execute <slug>` | Work a plan on a feature branch | `/context-repo-plan` | `/context-repo-adr new` (if decisions emerged) |
| `/context-repo-adr <new\|list\|review>` | ADR lifecycle | any skill that surfaces a decision | — |
| `/context-repo-refresh` | Staleness audit (read-only) | — (runs periodically) | `/context-repo-map <scope>` on flagged files |

See `references/workflow.md` for the full lifecycle diagram, hand-off
contracts, and common invocation chains.

## Hard rules (never violate)

1. **`context/` lives at the root of the current git repo.** Never as a
   sibling directory. Never under `.claude/`. Resolve its location as
   `$(git rev-parse --show-toplevel)/context`.
2. **ADRs are immutable.** If a decision needs to change, write a new ADR
   that supersedes the old one. Do not edit accepted ADRs in place.
3. **Never invent files outside the documented layout.** The shape in
   `references/structure.md` is the contract. If you need a new location,
   propose it to the user first.
4. **Never silently overwrite `arch/` files.** Show a diff and get confirmation.
5. **`memory/notes.md` is append-only.** Never edit or delete prior entries.
6. **All paths are relative to the repo root.** No `../`, no absolutes.
7. **Do not commit secrets, binaries, or vendor directories** to the context
   repo. It must stay small and reviewable.
