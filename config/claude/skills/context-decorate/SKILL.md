---
name: context-decorate
description: Scan a codebase and place CLAUDE.md context files in directories that lack them. Spins up a team of subagents to parallelize the work — each agent covers a few directories and generates a succinct overview of the directory's purpose and key subdirectories. Use when onboarding to a new codebase, improving Claude context quality, annotating project structure, or scaffolding directory-level context for AI assistants. Keywords: context, CLAUDE.md, annotate, codebase, directory, onboard, decorate, scaffold context, context files.
disable-model-invocation: true
---

# Context Decorate

Populate a project with directory-level CLAUDE.md context files using a team of parallel subagents.

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

Each agent receives a list of directory paths. For each directory the agent:
1. Reads the directory listing and key manifests (README, package.json, go.mod, Cargo.toml, etc.)
2. Samples source entry points to infer purpose
3. Writes a concise CLAUDE.md (under 40 lines) with a purpose overview, contents list, and usage notes

References: [content-guidelines](references/content-guidelines.md)

### 4. Completion

After all agents report back, summarize:
- Directories decorated (with file paths)
- Directories skipped (with reason)
- Total CLAUDE.md files created

Shut down the team and call `TeamDelete` to clean up.
