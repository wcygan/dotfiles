---
name: context-repo-refresh
description: >
  Staleness audit for a context repo. Diffs the current repo tree against
  arch/ maps and ADRs, surfaces files that have changed significantly
  since the map was generated, and proposes targeted updates. Read-only —
  never writes automatically. Forks to keep the scan isolated. Use
  periodically (weekly/monthly) or after large merges. Keywords: refresh
  context repo, drift check, staleness audit, arch drift, context rot
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(fd *)
---

# /context-repo-refresh

Audit a context repo for staleness. Produces a report — never writes.

Read `../context-repo/references/structure.md` for file locations.

## Workflow

### 1. Locate the context repo

Resolve `context/` as `$(git rev-parse --show-toplevel)/context`. Stop
if missing.

### 2. Establish baselines

For each file under `context/arch/`:
- `git log -1 --format=%cI <path>` → baseline timestamp
- Record the most recent commit hash that touched it

For each ADR under `context/adrs/` with `Status: Accepted`:
- Baseline timestamp = the ADR's `Date` header

### 3. Measure churn since baseline

Detect mode from `context/repos.toml`:

- **Monorepo** (`repos.toml` present): for each `[[projects]]`, measure
  churn in its `path` with `git log --since=<baseline> --oneline --stat -- <path>`.
- **Single project** (no `repos.toml`): measure churn across the whole
  repo with `git log --since=<baseline> --oneline --stat`.

Count commits, files touched, and which top-level directories saw the
most activity. Note any commits with messages referencing an ADR number
(`ADR-0007`, `#0007`, etc.).

### 4. Detect suspected drift

Flag a map stale if:
- The map file is older than 30 days **and** the scope it describes has
  seen >10 commits since.
- A top-level directory named in `arch/projects/<name>.md` (monorepo) or
  `arch/system-map.md` (single project) no longer exists.
- A dependency mentioned in `arch/infrastructure.md` is no longer in any
  package manifest.
- An ADR's `Affects` scope has commits touching files that mention the
  ADR's opposing alternatives (heuristic — flag, don't conclude).

### 5. Produce the report

Output to the user (not a file):

```
Context Repo Refresh — YYYY-MM-DD

## Arch maps
- arch/infrastructure.md — STALE (generated 67 days ago; 143 commits
  since). Suggested: /context-repo-map infra
- arch/projects/api.md — STALE (generated 45 days ago; apps/api saw 89
  commits, major churn in internal/auth/). Suggested:
  /context-repo-map project api
- arch/projects/web.md — FRESH (12 days, 7 commits, low churn).
- arch/system-map.md — UNKNOWN (never updated since init).

## ADRs
- 0002 "use postgres for auth" — DRIFT SUSPECTED. internal/auth now
  imports github.com/go-sql-driver/mysql (internal/auth/db.go:9).
  Suggested: /context-repo-adr review, then /context-repo-adr new if
  confirmed.
- 0005 "feature flag all launches" — SUPPORTED. Recent endpoints all
  reference the `flags.Enabled` helper.
- 0007, 0008, 0009 — no affected-scope activity since; nothing to audit.

## plans/active
- active/migrate-auth.md — 42 days old. If this work is done, delete the
  file. If not, consider whether the plan is still accurate.

## memory/notes.md
- Last append: 8 days ago. (Healthy if no work has run; investigate if
  execution has happened without logging.)

## Suggested actions (priority order)
1. /context-repo-map project api
2. /context-repo-adr review    (then decide on 0002)
3. /context-repo-map infra
4. Review plans/active/migrate-auth.md
```

In single-project mode, omit the `project <name>` suggestions and use
repo-wide map scopes instead.

### 6. Do not write anything

This skill is **read-only**. It never touches files. The report is input
for the human to decide what to run next.

## Hard rules

- **Read-only.** Never edit, create, or delete files.
- **Drift is suspected, not concluded.** All flags are hypotheses for
  human review.
- **Never run the suggested skills automatically.** Just list them.
- Do not scan outside the current repo root. No `../`, no absolutes.
- If `repos.toml` exists, do not scan paths not listed as
  `[[projects]]` `path` entries (plus top-level config).
- Do not attempt to read secrets or environment files for values — only
  check for presence/absence of configuration keys.

## References

- [`../context-repo/references/structure.md`](../context-repo/references/structure.md) — what "fresh" looks like for each artifact type (`arch/`, `adrs/`, `plans/active/`, `memory/`).
- [`../context-repo/references/workflow.md`](../context-repo/references/workflow.md) — the "periodic maintenance" chain; refresh is the entry point, map + adr are the remediation.

## Related skills

| Direction | Skill | Why |
|-----------|-------|-----|
| **Remediation** | `/context-repo-map <scope>` | Regenerate any maps flagged STALE. Run one scope at a time for reviewable diffs. |
| **Remediation** | `/context-repo-adr review` | Deeper drift analysis on ADRs refresh suspected |
| Follow-up | `/context-repo-adr new` | Supersede ADRs whose drift is confirmed |
| Pair with | `/loop` | `/loop 7d /context-repo-refresh` schedules weekly audits |
| Pattern sibling | `/refresh-claude-md` | Same read-only audit pattern applied to `CLAUDE.md` files |

The report ends with "Suggested actions (priority order)" — present these
as concrete next commands for the user, never run them automatically.
