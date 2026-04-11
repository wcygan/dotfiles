---
name: context-decorate
description: Scan a codebase and place CLAUDE.md context files in directories that lack them. Spins up a team of subagents to parallelize the work — each agent covers a few directories and generates a succinct overview of the directory's purpose and key subdirectories. Use when onboarding to a new codebase, improving Claude context quality, annotating project structure, or scaffolding directory-level context for AI assistants. Keywords: context, CLAUDE.md, annotate, codebase, directory, onboard, decorate, scaffold context, context files.
disable-model-invocation: true
---

# Context Decorate

Populate a project with directory-level CLAUDE.md context files using a team of parallel subagents.

## Prerequisite Reading (always load first)

**Before** discovering directories, spawning agents, or writing any CLAUDE.md file — including when the user asks you to update or audit existing ones — load the CLAUDE.md authoring guidance from the `claude-code-best-practices` skill:

- [`claude-code-best-practices/references/writing-claude-md.md`](../claude-code-best-practices/references/writing-claude-md.md) — instruction-budget math, WHAT/WHY/HOW structure, progressive disclosure, universality rule, anti-patterns, author checklist.

Every file this skill produces is a CLAUDE.md and therefore burns the always-loaded instruction budget of any Claude session opened in that directory. The same rules that apply to a root-level CLAUDE.md apply here, scoped to the directory:

- **Universality within the directory**: only include rules that apply to essentially every task touching this directory. Sub-area rules belong in a deeper file, not here.
- **WHAT / WHY / HOW**: what lives here, why it exists, how a developer interacts with it.
- **No linter-style prose**: if a formatter or linter already enforces it, don't restate it.
- **No long inline code examples**: use `file:line` pointers.
- **Absolutely no auto-generated boilerplate** (no `/init`-style dumps).
- **Target ≤40 lines** — tighter than the root budget because parent CLAUDE.md files may already be loaded.

If the user asks to *search* existing CLAUDE.md files for problems, audit them against this same checklist and flag violations (bloat, task-specific rules, duplication of parent content, stale migration notes).

## When Invoked

Run `/context-decorate [path]` to scan `[path]` (default: current working directory) and create CLAUDE.md files in directories that don't already have one.

## Workflow

### 1. Discovery

Scan the target directory tree (max depth 2) and collect all subdirectories that:
- Do **NOT** already contain a `CLAUDE.md` file
- Are **NOT** in the skip list

**Always skip:**
- `node_modules`, `.git`, `vendor`, `bower_components`
- Any directory starting with `.` (hidden dirs like `.cache`, `.venv`, `.direnv`)
- `dist`, `build`, `target`, `out`, `.next`, `.nuxt`, `__pycache__`

References: [scanning](references/scanning.md)

### 2. Team Creation

Create a coordination team, then batch the discovered directories into groups of 2–4 and spawn one `general-purpose` agent per batch. All agents can write files concurrently since each covers a different set of directories.

References: [team-workflow](references/team-workflow.md)

### 3. Agent Work

Each agent receives a list of directory paths **and an explicit instruction to read `claude-code-best-practices/references/writing-claude-md.md` before writing anything**. For each directory the agent:
1. Reads the directory listing and key manifests (README, package.json, go.mod, Cargo.toml, etc.)
2. Samples source entry points to infer purpose
3. Writes a concise CLAUDE.md (under 40 lines) following the WHAT/WHY/HOW structure, universality rule, and anti-patterns from `writing-claude-md.md`

References: [content-guidelines](references/content-guidelines.md), [writing-claude-md](../claude-code-best-practices/references/writing-claude-md.md)

### 4. Completion

After all agents report back, summarize:
- Directories decorated (with file paths)
- Directories skipped (with reason)
- Total CLAUDE.md files created

Shut down the team and call `TeamDelete` to clean up.
