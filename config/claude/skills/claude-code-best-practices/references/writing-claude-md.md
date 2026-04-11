---
title: Writing a Good CLAUDE.md
canonical_url: https://www.humanlayer.dev/blog/writing-a-good-claude-md
fetch_before_acting: true
---

# Writing a Good CLAUDE.md

> Before authoring or refactoring a `CLAUDE.md`, WebFetch https://www.humanlayer.dev/blog/writing-a-good-claude-md for the latest HumanLayer guidance.

## Table of Contents

- [Why CLAUDE.md Is Special](#why-claudemd-is-special)
- [The Instruction Budget](#the-instruction-budget)
- [What to Include: WHAT / WHY / HOW](#what-to-include-what--why--how)
- [Progressive Disclosure via `agent_docs/`](#progressive-disclosure-via-agent_docs)
- [Universality Rule](#universality-rule)
- [Anti-Patterns](#anti-patterns)
- [Why Claude Sometimes "Ignores" CLAUDE.md](#why-claude-sometimes-ignores-claudemd)
- [Author Checklist](#author-checklist)
- [Worked Examples](#worked-examples)

## Why CLAUDE.md Is Special

`CLAUDE.md` is **the only file that, by default, is injected into every Claude Code conversation** in a project. Every line competes for space in a finite instruction budget, and every line is paid for whether or not the current task needs it.

LLMs are stateless functions with frozen weights — they only know what you put in the context. `CLAUDE.md` is the lever for teaching Claude things it can't infer from the code itself.

## The Instruction Budget

Frontier LLMs follow roughly **150–200 instructions with reasonable consistency**. Claude Code's system prompt already burns ~50 of those. That leaves ~100–150 for your repo — and those slots are shared across *all* sessions on *all* tasks.

- Aim for `CLAUDE.md` **under ~300 lines** (HumanLayer's own is under 60).
- Every line should earn its spot. If it's only relevant to one task area, it doesn't belong at the top level.
- Prefer one strong rule over three weak variants of the same rule.

## What to Include: WHAT / WHY / HOW

A good `CLAUDE.md` answers three questions succinctly:

- **WHAT** — the tech stack, project structure, and a codebase map (especially critical in monorepos where Claude has to pick between packages).
- **WHY** — the purpose of the project and of its major components. Claude can read code; it cannot read intent.
- **HOW** — the practical workflow: package manager, how to run tests, how to lint, how to verify a change is actually done.

If a section isn't clearly WHAT/WHY/HOW-at-the-project-level, it probably belongs in a deeper reference file.

## Progressive Disclosure via `agent_docs/`

Don't cram specialized guidance into `CLAUDE.md`. Create an `agent_docs/` (or similar) directory with topic-scoped markdown files and **reference them from `CLAUDE.md` by path**. Claude loads them on demand when a task actually touches that area.

Good candidates for extraction:
- Build and release procedures
- Test layout and conventions
- Architecture deep-dives
- Area-specific coding rules (DB schema, auth, frontend styling, etc.)
- Migration notes and historical context

The `CLAUDE.md` should read like a router: *"If you're doing X, read `agent_docs/x.md`."*

## Universality Rule

**If a rule only applies to a subset of tasks, it does not belong in `CLAUDE.md`.**

Counter-example: a database schema instruction loaded in every session will distract the model when it's editing frontend styles. Worse, the built-in system reminder tells Claude the `CLAUDE.md` context *"may or may not be relevant to your tasks"* — so irrelevant rules are actively filtered out, while still consuming budget.

Rule of thumb: if two unrelated contributors would both benefit from a line, keep it. Otherwise, extract it.

## Anti-Patterns

- **Using CLAUDE.md as a linter.** *"Never send an LLM to do a linter's job."* Formatting, naming, import order, unused vars — all of this belongs in Biome / ESLint / ruff / gofmt, not in prose rules Claude has to remember.
- **Running `/init` and shipping the output.** The auto-generated default is low-quality and bloated. Manual authoring beats it every time.
- **Long inline code examples.** They rot the moment the code changes. Use `file:line` references instead.
- **Task-specific guidance at the top level.** Move it to `agent_docs/`.
- **Duplicating README content.** The README is for humans; `CLAUDE.md` is for agents. Different audiences, different emphasis.
- **Walls of "always do X / never do Y" rules** without a *why*. Claude generalizes poorly from rules it doesn't understand.
- **Stale historical notes.** If the migration is done, delete the note.

## Why Claude Sometimes "Ignores" CLAUDE.md

Anthropic wraps the injected `CLAUDE.md` in a system reminder telling the model the content *may or may not be relevant*. This is deliberate: it lets the model filter out irrelevant instructions so a bloated `CLAUDE.md` doesn't poison every task.

The practical consequence: **the more universally applicable your content is, the more reliably Claude will follow it**. Task-specific rules are the first thing the model drops.

## Author Checklist

Before merging changes to a `CLAUDE.md`:

- [ ] Under ~300 lines (ideally much less)
- [ ] Covers WHAT, WHY, and HOW at the project level
- [ ] Every top-level rule applies to essentially *every* session in this repo
- [ ] Task-specific guidance lives in `agent_docs/` (or equivalent), not here
- [ ] No linter-style rules a formatter/linter already enforces
- [ ] No long inline code examples — use `file:line` pointers
- [ ] No stale migration notes or one-off historical context
- [ ] Not auto-generated from `/init`
- [ ] Not a copy of the README

## Worked Examples

### Good: minimal router

```markdown
# MyProject

## What
TypeScript monorepo, pnpm workspaces. Packages live under `packages/`.
Primary apps: `apps/web` (Next.js), `apps/api` (Fastify).

## Why
Internal billing platform. Correctness and auditability trump velocity.

## How
- Install: `pnpm install`
- Test: `pnpm test` (Vitest, must be green before commit)
- Lint: `pnpm lint` (Biome — do not hand-fix what Biome can fix)
- Verify a change: run the test suite for the touched package, then `pnpm build`.

## Deeper docs
- Architecture: `agent_docs/architecture.md`
- Billing domain rules: `agent_docs/billing.md`
- DB migrations: `agent_docs/migrations.md`
```

### Bad: bloated and task-specific

```markdown
# MyProject

When writing React components, always use function components, never classes.
Use Tailwind utility classes. Prefer `clsx` over template strings. Never use
`any` in TypeScript. When touching the billing service, remember that invoices
must be stamped in UTC and the `stamp_utc` column is NOT NULL. Migrations
should be written with `pnpm db:migrate`. Do not forget to update the OpenAPI
spec when you change a route. Here is an example handler:

```ts
export const handler = async (req, res) => { /* 40 lines of example */ }
```

...and so on for 600 more lines.
```

Problems: linter territory (React/Tailwind/TS rules), task-specific (billing UTC, OpenAPI), long code example (rots fast), and way over budget — Claude will filter most of it out anyway.

## Applying This to This Repo

This dotfiles repo already uses a two-tier pattern:
- Personal global: `~/.claude/CLAUDE.md` — tight and universal (philosophy, commit rules, CLI prefs, jj policy, sub-agent policy).
- Project: `config/claude/skills/CLAUDE.md` and `dotfiles/CLAUDE.md` — larger, mixes universal policy with specialized playbooks.

When either file drifts past ~300 lines or starts accumulating task-specific sections (fish-aliases implementation, direnv perf tuning, per-tool playbooks), extract those sections into topic files and leave a one-line pointer. That keeps the always-loaded budget for rules that matter on *every* turn.
