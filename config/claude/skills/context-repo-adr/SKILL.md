---
name: context-repo-adr
description: >
  ADR lifecycle management for a context repo. Subcommands - new (capture a
  decision with context/consequences), list (regenerate adrs/INDEX.md with
  status), review (drift-check existing ADRs against current code and flag
  ones that appear reversed). ADRs are immutable; changes supersede via new
  ADR. Use when making a decision worth recording, or periodically to audit
  ADR drift. Keywords: ADR, architecture decision, decision record, adr
  review, adr drift, capture decision
disable-model-invocation: true
argument-hint: <new|list|review> [args]
allowed-tools: Read, Grep, Glob, Bash(git *), Write, Edit
---

# /context-repo-adr

ADR lifecycle for a context repo. Subcommands: `new`, `list`, `review`.

**Args**: `$ARGUMENTS`. First token is the subcommand.

Read `../context-repo/references/structure.md` for the ADR format and rules.

## Preconditions

- Must be run from inside a git repo. The context repo is at
  `$(git rev-parse --show-toplevel)/context`.
- `context/adrs/` must exist. Create it (with a seed `INDEX.md`) if missing.

## Subcommand: `new`

Capture a new decision.

### Workflow

1. **Interview the user** with AskUserQuestion. Ask 3-4 questions:
   - **Title** (free text): one-line imperative, <60 chars.
   - **Affects** (multi-select if `repos.toml` exists; free text otherwise):
     which parts of the repo this decision constrains. Monorepos pick from
     `[[projects]]` names; single-project repos pick affected directories
     or modules, or just "all".
   - **What's being decided** (free text): the choice in plain language.
   - **Alternatives considered** (free text): what else you rejected and why.

2. **Allocate the next number.** Scan `context/adrs/` for the highest
   existing `NNNN-*.md` file. Next is max + 1, zero-padded to 4 digits.
   Never reuse a number. Never renumber existing files.

3. **Generate slug** from the title: kebab-case, lowercased, first 4-6
   meaningful words.

4. **Draft the ADR** using the template:

```markdown
# NNNN: <Title>

- **Status**: Proposed
- **Date**: YYYY-MM-DD
- **Deciders**: <ask the user>
- **Affects**: <project names from repos.toml, or directories/modules, or "all">

## Context
<from interview>

## Decision
<from interview — one paragraph, plain language>

## Alternatives considered
- <alt 1>: <why rejected>
- <alt 2>: <why rejected>

## Consequences
### Positive
- ...
### Negative
- ...
### Neutral / things that become harder
- ...

## Follow-ups
- [ ] <task> — owner: @?
```

5. **Show the draft.** Ask: "Write to `context/adrs/NNNN-<slug>.md`?"
   Only write on explicit yes.

6. **Write the file.** Do not mark Accepted automatically — leave it as
   Proposed. The human promotes it to Accepted in a follow-up commit.

7. **Regenerate `INDEX.md`** (see `list` subcommand).

8. Report the new file path.

### Superseding an existing ADR

If the user's new decision supersedes an existing ADR:

1. Create the new ADR as above.
2. Ask for the number of the ADR being superseded.
3. Edit the old ADR **only** to change its status line from
   `Status: Accepted` to `Status: Superseded-by NNNN`. No other edits.
4. Add a line to the new ADR's front matter: `Supersedes: NNNN`.
5. Note in `memory/notes.md` (append-only).

## Subcommand: `list`

Regenerate `context/adrs/INDEX.md`.

1. Find all `context/adrs/NNNN-*.md` files, sorted by number.
2. Parse the front matter (Status, Date, Affects, Title).
3. Write:

```markdown
# ADR Index

Generated: YYYY-MM-DD

| # | Title | Status | Date | Affects |
|---|-------|--------|------|---------|
| 0001 | ... | Accepted | ... | api, web |
| 0002 | ... | Superseded-by 0007 | ... | api |
```

4. Show diff, confirm, write.

## Subcommand: `review`

Drift-check: find ADRs whose premises appear to have been reversed in code.

This is an **expensive operation**. Scope to accepted ADRs only. Do not
modify anything — only report.

1. Read all ADRs with `Status: Accepted` or `Status: Proposed`.
2. For each ADR, for each entry in its `Affects` list:
   - Resolve the affected scope: if `repos.toml` exists and the entry is
     a project name, use that project's `path`; otherwise treat it as a
     directory or the whole repo.
   - Extract 2-3 searchable claims from the Decision section (library
     names, config values, architectural verbs like "use", "avoid",
     "require").
   - Grep the affected scope for evidence that supports or contradicts
     each claim.
   - Check `git log` for commits that reference the ADR number.
3. Categorize each ADR:
   - **Supported** — evidence consistent with the decision
   - **Drift suspected** — evidence contradicts or is absent
   - **Inconclusive** — can't tell from a static scan
4. Produce a report (not a file — output to the user):

```
ADR Review — YYYY-MM-DD

Supported (N):
  0001, 0003, 0005

Drift suspected (N):
  0002: "use postgres for auth" — internal/auth/ now imports mysql driver
        (internal/auth/db.go:12). Consider new ADR.
  0007: "feature flag all launches" — new endpoint in routes/v2.go
        with no flag guard.

Inconclusive (N):
  0004: too abstract to verify automatically.
```

5. Suggest: "Run `/context-repo-adr new` to write a superseding ADR for
   any drift you confirm."

## Hard rules

- **Never edit an Accepted ADR's body.** Only the status line may be
  changed, and only to mark it Superseded.
- **Never reuse an ADR number.** Never renumber.
- **`review` is read-only.** Never write changes to ADRs or code during a
  review — only report.
- **Drift is suggested, not concluded.** The review output is a starting
  point for human judgment, not a source of truth.
- All paths are relative to the repo root. No `../`, no absolutes.

## References

- [`../context-repo/references/structure.md`](../context-repo/references/structure.md) — the ADR format (frontmatter, sections, numbering) and the immutability rule.
- [`../context-repo/references/workflow.md`](../context-repo/references/workflow.md) — ADRs are written at multiple points in the lifecycle (after `init`, after `map`, after `execute`); see the invocation chains.

## Related skills

| Direction | Skill | Why |
|-----------|-------|-----|
| **Often triggered by** | `/context-repo-map` | Infra/system mapping surfaces undocumented decisions worth capturing with `adr new` |
| **Often triggered by** | `/context-repo-execute` | Execution surfaces "we decided to X because Y" moments worth recording |
| **Triggered by** | `/context-repo-refresh` | Refresh flags drift; follow up with `adr review` to confirm, then `adr new` to supersede |
| Complements | `/context-repo-plan` | `plan` should read `adrs/INDEX.md` to avoid contradicting accepted decisions |
| Pattern sibling | `/refresh-claude-md` | Same shape as `adr review` but scoped to `CLAUDE.md` files |

After `adr new` or `adr list`, suggest no specific next step — ADRs are
asynchronous artifacts. After `adr review`, suggest `adr new` for each
confirmed drift to supersede the old decision.
