---
name: context-repo-spec
description: >
  Interview-driven feature spec writer. Produces
  context/specs/<slug>/spec.md with problem statement, goals, non-goals,
  affected areas, constraints, and open questions. Uses AskUserQuestion to
  extract intent. Use when starting a new feature or change and you want
  a reviewable spec before planning. Keywords: feature spec, context repo
  spec, new feature, write spec
disable-model-invocation: true
argument-hint: <feature-slug>
allowed-tools: Read, Grep, Glob, Bash(git *), Write
---

# /context-repo-spec

Interview the user and produce `context/specs/<slug>/spec.md`.

**Slug**: `$ARGUMENTS`. Must be kebab-case, short, no spaces. If missing or
invalid, ask the user for one before proceeding.

Read `../context-repo/references/structure.md` for the spec format.

## Workflow

### 1. Locate the context repo and validate the slug

- Resolve `context/` as `$(git rev-parse --show-toplevel)/context`. Stop
  if it doesn't exist.
- Validate slug: `^[a-z0-9][a-z0-9-]*$`, length 3-40.
- If `context/specs/<slug>/spec.md` already exists, stop and tell the user
  to pick a different slug or delete the existing spec.

### 2. Read context to prime the interview

- `context/CLAUDE.md`
- `context/repos.toml` (if present — tells you the monorepo subprojects)
- `context/arch/system-map.md` (if present) — so you understand the shape
- `context/arch/infrastructure.md` (if present)
- `context/adrs/INDEX.md` (if present) — so you don't propose something
  that contradicts an accepted ADR

### 3. Interview the user with AskUserQuestion

Ask 3-5 questions, informed by what you read. Good question shapes:

1. **Problem** (free text via "Other"): "Who hurts today, how often, and
   what's the current workaround?"
2. **Primary outcome** (multiple choice, multi-select): list plausible
   success metrics based on what you read.
3. **Affected areas** — if `repos.toml` exists, multi-select from the
   listed projects; otherwise free text for directories or modules.
4. **Non-goals** (free text): "What do you explicitly NOT want in this
   change?"
5. **Constraints** (multiple choice, multi-select): feature flag required?
   backward compatible? migration window? SLO impact?

Adapt the questions to the request. Do not ask more than 5.

### 4. Draft `spec.md`

Use the format from `references/structure.md`:

```markdown
# <Feature Title>

## Problem
<from interview>

## Goals
- <measurable>
- <measurable>

## Non-goals
- <explicit>

## Affected areas
- <project or directory>: <what changes>
- <project or directory>: <what changes>

## Constraints
- <from interview + ADR review>

## Open questions
- [ ] <question> — owner: @?
- [ ] ...
```

Mark anything you had to guess with `[inferred]`. Humans need to be able to
see what came from them vs. you.

### 5. Show the draft and ask for approval

Show the full draft to the user. Ask: "Write this to
`context/specs/<slug>/spec.md`?" Only write on explicit yes.

### 6. Write the file and report

- Create `context/specs/<slug>/` directory
- Write `spec.md`
- Print path and suggest next step: `/context-repo-plan <slug>`

## Hard rules

- Never skip the interview. No spec without at least one round of questions.
- Never write a spec that contradicts an accepted ADR without flagging it
  explicitly in the "Open questions" section.
- Never invent affected areas. Confirm them via the interview.
- Do not touch files outside `context/specs/<slug>/`.
- All paths in the spec are relative to the repo root. No `../`.
- If the user's request is already a plan (not a problem), stop and ask
  whether they want `/context-repo-plan` instead.

## References

- [`../context-repo/references/structure.md`](../context-repo/references/structure.md) — the `specs/<slug>/spec.md` format and the rules about where it lives.
- [`../context-repo/references/workflow.md`](../context-repo/references/workflow.md) — how `spec` feeds `plan` and what the "ship a feature" flow looks like end-to-end.

## Related skills

| Direction | Skill | Why |
|-----------|-------|-----|
| **Prerequisite** | `/context-repo-init` | `context/` must exist |
| Prerequisite (soft) | `/context-repo-map` | Fresh arch maps make the interview sharper and affected-area selection accurate |
| **Next step** | `/context-repo-plan <slug>` | Turn the spec into an ordered task DAG |
| Also useful | `/context-repo-adr review` | Run before writing to catch constraints from accepted ADRs |
| Also useful | `/create-feature-spec` | General-purpose spec skill that `/context-repo-spec` may delegate prose structure to |

On completion, always suggest `/context-repo-plan <slug>` as the next step.
