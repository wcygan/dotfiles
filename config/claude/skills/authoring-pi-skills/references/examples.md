# Worked pi skill examples

Four complete, copy-ready skills, ordered easiest → hardest to get right on a small model. Each shows the full `SKILL.md`. Clone the one closest to your task and adapt. Every one applies the three rules: low freedom, a validator, lean structure.

Table of contents:
- [1. commit-draft — read-only, self-check validator](#1-commit-draft)
- [2. changelog-since-tag — pure transform](#2-changelog-since-tag)
- [3. fish-shortcut — repo edit gated by a real test](#3-fish-shortcut)
- [4. repo-recon — read-only research with a fixed output shape](#4-repo-recon)

---

## 1. commit-draft

The canonical distillation example: read-only, mechanical, with a regex the model checks itself against. Safe to pilot — it never commits.

```markdown
---
name: commit-draft
description: Draft a Conventional Commits message for the staged changes and print it. Does not commit. Keywords commit message, conventional commit, staged diff.
---

# commit-draft

Produce one Conventional Commits message for the **staged** diff, then print it. Do **not** run `git commit`, push, or edit files.

## Procedure
1. Read staged changes: `git diff --staged --stat` then `git diff --staged`.
   If empty, print `No staged changes — run git add first.` and stop.
2. Pick exactly one type from: feat, fix, docs, refactor, test, chore, perf, build, ci.
3. Subject = `type(scope): summary` — imperative, lowercase, no trailing period, ≤ 50 chars. Omit `(scope)` if changes span many areas.
4. If multiple files or a non-obvious change, add a blank line then `- ` bullets explaining WHY, wrapped at 72 cols.

## Self-check before printing (revise if any fails)
- [ ] Subject matches ^(feat|fix|docs|refactor|test|chore|perf|build|ci)(\([a-z0-9._-]+\))?: .+
- [ ] Subject ≤ 50 chars, imperative, no trailing period
- [ ] type reflects the dominant change
- [ ] Body explains WHY, not a restatement of the diff

## Output
Print only the final message in one fenced text block — nothing else.
```

Why it works on a small model: closed type list, explicit empty-diff stop, a regex self-check, and an exact output contract.

---

## 2. changelog-since-tag

Pure git-history → markdown transform. No judgment beyond grouping by the type the commit already declares.

```markdown
---
name: changelog-since-tag
description: Generate a grouped markdown changelog from Conventional Commits between the latest tag and HEAD. Keywords changelog, release notes, git log, since tag.
---

# changelog-since-tag

## Procedure
1. Find the range: `git describe --tags --abbrev=0` is the previous tag (`PREV`). If it errors (no tags), use the first commit: `git rev-list --max-parents=0 HEAD`.
2. List commits: `git log PREV..HEAD --no-merges --pretty=format:'%s'`.
3. Bucket each subject by its Conventional Commits type into these sections, in this order, dropping empty sections:
   `### Features` (feat) · `### Fixes` (fix) · `### Performance` (perf) · `### Other` (everything else).
4. Within a section, one `- ` bullet per commit; strip the `type(scope): ` prefix; keep the summary verbatim.

## Self-check
- [ ] Every non-merge commit in the range appears exactly once
- [ ] No empty sections rendered
- [ ] Sections in the fixed order above

## Output
Print the changelog as markdown starting at `## PREV..HEAD`. Nothing else.
```

Why it works: the range commands are exact, the buckets are a closed set, and the self-check counts commits — a verifiable invariant.

---

## 3. fish-shortcut

A skill that **edits the repo**, made safe by a real validator (`make test-pre`). This is the highest-value shape — it offloads genuine work — but demands the tightest procedure. It hard-codes this repo's policy, so it's a *project* skill (`.pi/skills/` or `config/claude/skills/`), not a global one.

```markdown
---
name: fish-shortcut
description: Add a fish abbreviation to config/fish/conf.d/40-aliases.fish following this repo's policy, guarded by type -q, then validate. Keywords fish abbr, alias, 40-aliases, shortcut.
---

# fish-shortcut

Add one abbreviation. Input (from the prompt): the abbr name and its expansion.

## Procedure
1. Read `config/fish/conf.d/40-aliases.fish` to learn the existing block style.
2. Confirm the underlying tool is guarded: the new abbr must sit inside (or add) a `type -q <tool>` block. Never add an unguarded abbr.
3. Append the abbr in the matching tool's block:
   `abbr -a <name> '<expansion>'`
   Do not reorder or edit unrelated lines.
4. Validate: run `make test-pre`.
5. If it fails, read the error, fix only your addition, and re-run `make test-pre`. Repeat until green.

## Self-check (do not finish until all true)
- [ ] `make test-pre` exits 0
- [ ] The new abbr is inside a `type -q` guard for its tool
- [ ] Exactly one abbr added; no other lines changed (`git diff --stat` shows one file, small delta)

## Output
Print the `git diff` of the change and the final `make test-pre` result.
```

Why it works: the validator is a real command with a binary outcome, the "do not touch other lines" constraint is explicit, and the diff-stat self-check catches over-editing — the classic small-model failure on file edits.

---

## 4. repo-recon

Read-only research with a fixed output shape. Pilot with `--tools read,grep,find,ls` so it physically cannot write.

```markdown
---
name: repo-recon
description: Summarize an unfamiliar repo into a fixed-format brief — entry points, build/test commands, and layout. Read-only. Keywords repo summary, onboarding, recon, layout.
---

# repo-recon

Read-only. Do not edit or run build/test commands — only inspect.

## Procedure
1. Identify the stack: look for one of package.json, Cargo.toml, go.mod, pyproject.toml, flake.nix. Name the first you find.
2. Find the build/test entry: read the manifest's scripts/targets and any Makefile/justfile. Record the exact commands; if none found, write `unknown`.
3. List top-level source dirs: `git ls-files | awk -F/ '{print $1}' | sort -u`.
4. Find entry points: files named main.*, index.*, lib.*, or a `[[bin]]`/`bin` field.

## Output (fill every field; use `unknown` when not found)
```
Stack:      <name>
Build:      <command or unknown>
Test:       <command or unknown>
Top dirs:   <comma-separated>
Entrypoints:<comma-separated>
```
Print only this block.

## Self-check
- [ ] Every field present (a value or the literal `unknown`)
- [ ] No file was written or modified
```

Why it works: a rigid output template removes free-form drift, every field has a fallback so the model can't stall, and read-only tools enforce the safety claim at the harness level.

---

## Adapting one

When you clone an example, change in this order: `name` + `description` (triggering), the closed lists/commands (the procedure), the **validator** (must stay machine-checkable), and the output contract. If you can't write a validator, reread [skill-anatomy.md](skill-anatomy.md#routing-local-vs-frontier) — the task may belong on a frontier model.
