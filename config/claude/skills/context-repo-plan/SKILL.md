---
name: context-repo-plan
description: >
  Turn a feature spec into an execution plan. Reads
  context/specs/<slug>/spec.md, arch/ maps, and repos.toml (if present).
  Produces specs/<slug>/plan.md as an ordered task DAG with per-task steps,
  migration ordering, compatibility windows, rollback points, and owners.
  Flags plans that cross ownership boundaries (monorepo). Forks to keep
  planning context isolated. Use after /context-repo-spec, or when a
  feature needs an ordered execution plan. Keywords: feature plan, task
  DAG, migration plan, context repo plan
disable-model-invocation: true
argument-hint: <feature-slug>
context: fork
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(fd *), Write, Edit
---

# /context-repo-plan

Turn `context/specs/<slug>/spec.md` into `context/specs/<slug>/plan.md`.
This is the highest-leverage skill in the suite — a well-ordered plan is
what makes a feature tractable.

**Slug**: `$ARGUMENTS`. If missing, list existing specs and ask which one.

Read `../context-repo/references/structure.md` for the plan format.

## Workflow

### 1. Locate and load

- Resolve `context/` as `$(git rev-parse --show-toplevel)/context`. Stop
  if missing.
- Read `context/specs/<slug>/spec.md`. Stop if missing — suggest
  `/context-repo-spec <slug>` first.
- Read `context/repos.toml` (if present), `context/arch/system-map.md`,
  `context/arch/infrastructure.md`, and any relevant
  `arch/projects/<name>.md` files for affected subprojects.
- Read `context/adrs/INDEX.md` and any ADRs that touch affected areas.

### 2. Inspect affected areas

For each area listed in the spec's "Affected areas":
- Glob the directories likely to change (relative to repo root)
- Read key files to understand current structure
- Note the test command from `repos.toml` if the area maps to a listed
  project; otherwise infer from repo-level tooling

Do not read unrelated parts of the repo. Scope discipline matters in a
forked context.

### 3. Build the task DAG

Think hard about ordering. The right order respects:

- **Producers before consumers.** If one module emits a new message type,
  that change lands before the module that consumes it.
- **Backward compatibility during rollout.** Never a step that breaks
  existing clients without a compatibility window.
- **Migrations first, code second, cleanup last.** Data migrations run
  before code that depends on them. Dropping old columns is a separate
  later step.
- **One area per task where possible.** Tasks that touch multiple
  unrelated areas are a warning sign — split them unless atomicity is
  truly required.
- **Rollback points.** After each atomic group, name the rollback procedure.

### 4. Draft `plan.md`

```markdown
# <Feature Title> — Execution Plan

## Ordering rationale
<2-4 sentences: why this order, what constraints drove it>

## Ownership
- Areas touched: <list of directories or project names>
- Teams involved: <from repos.toml owners, if applicable>
- Cross-team coordination needed: yes/no (flag if yes)

## Tasks

### 1. <area>: <short imperative title>
- **Files**: <paths or globs, relative to repo root>
- **Change**: <1-2 sentences>
- **Verify**: `<test command>`
- **Owner**: <from repos.toml or spec>
- **Depends on**: none | 1, 2
- **Rollback**: <how to back out this step alone>

### 2. ...

## Rollback points
- After step N: <state>, <what's safe to revert>

## Risk notes
- <migration is one-way>
- <feature flag required: <flag name>>
- <external dependency: <what, when>>

## Open questions (must resolve before execution)
- [ ] <question>
```

All file paths are relative to the repo root.

### 5. Flag cross-team plans (monorepos with repos.toml)

If the plan touches projects owned by different teams (per `repos.toml`
owners), add a prominent `## ⚠ Cross-team coordination` section. Never
assume a single-team review will work for multi-team changes.

### 6. Show the draft and ask for approval

Present the full plan. Ask: "Write to `context/specs/<slug>/plan.md`?"
Only write on explicit yes.

### 7. Write and report

- Write `plan.md` alongside `spec.md`
- If any "Open questions (must resolve)" exist, tell the user they must be
  resolved before `/context-repo-execute` will run
- Also copy (not symlink) the plan to `context/plans/active/<slug>.md`
  so active work is visible in one place
- Suggest next step: resolve open questions, then `/context-repo-execute <slug>`

## Hard rules

- No plan without a spec. If `spec.md` is missing, refuse.
- If `repos.toml` exists, never plan work for a project not listed. Ask
  the user to add it first.
- Never skip the ordering rationale section — if you can't explain why,
  the order is wrong.
- Never silently update an existing plan. If `plan.md` exists, show a diff
  and get explicit approval.
- All paths are relative to the repo root. No `../`, no absolutes.
- Plans with cross-team reach (monorepos) must be flagged, not hidden.

## References

- [`../context-repo/references/structure.md`](../context-repo/references/structure.md) — the `specs/<slug>/plan.md` format: task DAG, rollback points, risk notes.
- [`../context-repo/references/workflow.md`](../context-repo/references/workflow.md) — `plan` sits between `spec` and `execute`; see the "ship a feature" chain.

## Related skills

| Direction | Skill | Why |
|-----------|-------|-----|
| **Prerequisite** | `/context-repo-spec <slug>` | A plan requires an existing spec. Refuse if `spec.md` is missing. |
| Prerequisite (soft) | `/context-repo-map` | Planning accuracy depends on up-to-date `arch/` maps |
| **Next step** | `/context-repo-execute <slug>` | Work the plan. Blocks until all "must-resolve" open questions are closed. |
| Also useful | `/context-repo-adr review` | Check plan doesn't contradict accepted ADRs |
| Also useful | `/plan` | General-purpose planning skill — `/context-repo-plan` borrows ordering heuristics from it |

On completion, list any "must-resolve" open questions and suggest the user
answer them before running `/context-repo-execute <slug>`.
