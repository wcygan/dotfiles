# Context Repo Workflow

How the `/context-repo-*` skills fit together. Each skill has a single
responsibility and hands off to the next — no skill does the job of
another.

All skills operate on `$(git rev-parse --show-toplevel)/context` — the
`context/` directory at the root of the current git repo. If
`context/repos.toml` exists, the repo is treated as a monorepo with
multiple subprojects; otherwise skills treat the repo as a single
project.

## The canonical lifecycle

```
  ┌─────────────────────┐
  │ /context-repo-init  │  1. Scaffold context/ inside the current repo
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ /context-repo-map   │  2. Generate arch/ (infrastructure, system,
  └──────────┬──────────┘      per-project when monorepo)
             │
             ▼
  ┌─────────────────────┐
  │ /context-repo-adr   │  3. (optional) Capture decisions surfaced by
  │   new               │      mapping
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ /context-repo-spec  │  4. Start a feature: interview → spec.md
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ /context-repo-plan  │  5. Spec → plan.md (ordered task DAG)
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ /context-repo-      │  6. Work the plan with checkpoints + memory log
  │   execute           │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ /context-repo-adr   │  7. (optional) Record decisions that emerged
  │   new               │      during work
  └─────────────────────┘

  ╔═════════════════════╗
  ║ Ongoing maintenance ║
  ╠═════════════════════╣
  ║ /context-repo-      ║  Weekly/monthly: detect stale arch/ and ADR drift
  ║   refresh           ║  → re-run /context-repo-map on flagged files
  ║ /context-repo-adr   ║  After refresh: audit ADRs for reversal
  ║   review            ║
  ╚═════════════════════╝
```

## Hand-off contract (inputs → outputs)

| Skill | Requires | Reads | Writes |
|-------|----------|-------|--------|
| `/context-repo-init` | cwd inside a git repo; no existing `context/` | repo root, package manifests, subproject directories (if monorepo) | `context/` tree, `CLAUDE.md`, `README.md`, `repos.toml` (monorepos only) |
| `/context-repo-map` | `context/` exists | repo tree, manifests, configs, `repos.toml` (if present) | `arch/infrastructure.md`, `arch/system-map.md`, `arch/projects/<name>.md` (monorepos only) |
| `/context-repo-spec` | `context/` exists (arch/ helpful) | `arch/`, `adrs/` (to avoid contradicting), `repos.toml` (if present) | `specs/<slug>/spec.md` |
| `/context-repo-plan` | `specs/<slug>/spec.md` | spec, `arch/`, `adrs/`, affected code paths | `specs/<slug>/plan.md`, `plans/active/<slug>.md` |
| `/context-repo-execute` | `plan.md` with no open questions; clean working tree | `plan.md`, repo tree | commits on a feature branch, `memory/notes.md` (append), deletes `plans/active/<slug>.md` on completion |
| `/context-repo-adr new` | `context/adrs/` | existing ADRs (for numbering), `repos.toml` (if present, for Affects list) | `adrs/NNNN-<slug>.md`, updates `adrs/INDEX.md` |
| `/context-repo-adr list` | `adrs/*.md` | all ADRs | `adrs/INDEX.md` |
| `/context-repo-adr review` | `adrs/*.md` | ADRs, repo tree (grep) | nothing (read-only report) |
| `/context-repo-refresh` | `context/` exists | all of `context/`, repo tree, `git log` | nothing (read-only report with suggested next skills) |

## Invocation chains (common flows)

**New repo → ready to work:**

```
cd into a git repo
  → /context-repo-init
  → review CLAUDE.md and (if monorepo) repos.toml manually
  → /context-repo-map all
  → review arch/ diffs
  → /context-repo-adr new   (for any foundational decisions)
```

**Ship a feature:**

```
/context-repo-spec <slug>
  → /context-repo-plan <slug>
  → resolve any "Open questions (must resolve)"
  → /context-repo-execute <slug>
  → review the feature branch, open a PR
  → /context-repo-adr new   (if execution surfaced a decision)
```

**Periodic maintenance (weekly/monthly):**

```
/context-repo-refresh
  → /context-repo-map <scope>   for each STALE flag
  → /context-repo-adr review
  → /context-repo-adr new       to supersede any confirmed drift
```

**Resume interrupted execution:**

```
/context-repo-execute <slug>   (auto-detects last-completed task
                                from memory/notes.md)
```

## Isolation model (fork vs inline)

| Skill | Mode | Why |
|-------|------|-----|
| `/context-repo-init` | inline | interactive scaffolding, needs conversation |
| `/context-repo-map` | fork | heavy exploration across the repo |
| `/context-repo-spec` | inline | interview-driven, needs AskUserQuestion |
| `/context-repo-plan` | fork | heavy analysis of spec + arch + code |
| `/context-repo-execute` | inline | interactive checkpoints between tasks |
| `/context-repo-adr` | inline | interview for `new`, quick read for `list/review` |
| `/context-repo-refresh` | fork (Explore) | read-only audit, lots of grep/log |

## Delegation to other global skills

Context repo skills wrap, not replace, these general-purpose skills:

- `/context-repo-spec` → can delegate structured prose to `/create-feature-spec`
- `/context-repo-plan` → borrows ordering heuristics from `/plan`
- `/context-repo-execute` → delegates per-task execution to `/incremental-execution` when present
- `/context-repo-adr review` → pattern mirrors `/refresh-claude-md` but scoped to ADRs

## Hard invariants across all skills

These are restated from `structure.md` because every skill must enforce
them:

1. **`context/` lives inside the code repo it describes.** Never as a
   sibling directory. Never under `.claude/`. Always at repo root.
2. **ADRs are immutable.** Only the status line may be edited (to
   `Superseded-by NNNN`). Never edit an accepted ADR's body.
3. **`arch/` is diff-before-write.** Never silently overwrite.
4. **`memory/notes.md` is append-only.** Never edit or delete prior entries.
5. **`plans/active/` is garbage-collected.** Delete merged plans.
6. **`repos.toml` is authoritative when present.** If the file exists,
   skills only act on listed projects. If it's absent, skills treat the
   whole repo as one project.
7. **All paths are relative to the repo root.** No `../`, no absolutes.
8. **Never auto-push or auto-commit to remote.** Humans own the push step.
9. **No secrets in the context repo.** Only env var names, never values.
