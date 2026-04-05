---
name: context-repo-init
description: >
  Scaffold a new context/ directory at the root of the current git repo.
  Generates CLAUDE.md, README.md, and the standard arch/adrs/specs/plans/memory
  layout. Detects monorepo subprojects (apps/, packages/, services/, etc.)
  and offers to generate repos.toml. Use when starting a new repo or
  adopting the context-repo convention on an existing one. Keywords: init
  context repo, scaffold context, new context repo, bootstrap context,
  create context repo
disable-model-invocation: true
allowed-tools: Read, Glob, Bash(git *), Bash(ls *), Bash(fd *), Bash(pwd), Bash(mkdir *), Write
---

# /context-repo-init

Scaffold a new `context/` directory at the root of the current git repo.

The full convention is in `../context-repo/references/structure.md` — read
it before writing any files.

## Workflow

### 1. Resolve the target

Run `git rev-parse --show-toplevel`. If it fails, **stop** and tell the
user: "context-repo-init must be run from inside a git repo. `cd` into
the repo you want to document and re-run."

The target is always `<repo-root>/context/`. Never `../context`, never
`.claude/context`, never anywhere else.

Confirm with the user before proceeding: "I'll scaffold a context repo
at `<repo-root>/context/`. Continue?"

### 2. Refuse if `context/` already exists

If `<repo-root>/context/` exists, stop. Tell the user and suggest
`/context-repo-refresh` instead. Do not overwrite.

### 3. Detect whether this is a monorepo

A repo is treated as a monorepo (and gets a `repos.toml`) only if it has
**two or more** distinct subprojects. Look for top-level directories
containing their own manifest:

```bash
fd -H -t f --max-depth 3 \
  '^(package\.json|Cargo\.toml|pyproject\.toml|go\.mod|build\.gradle(\.kts)?|pom\.xml)$' \
  <repo-root>
```

Group results by their parent directory. A candidate subproject is any
directory (other than the repo root itself) that contains a manifest and
looks like a self-contained unit: `apps/<name>`, `packages/<name>`,
`services/<name>`, `crates/<name>`, `cmd/<name>`, etc.

- **Zero or one** subprojects beyond the root → single-project repo. Skip
  `repos.toml` entirely.
- **Two or more** → monorepo candidate. Show the user the list and ask:
  "I detected these subprojects: `<list>`. Generate `repos.toml` to track
  them? (y/n)" Only generate on explicit yes.

Do NOT guess. If inference is uncertain, ask.

### 4. Create the directory tree

```
context/
├── CLAUDE.md
├── README.md
├── repos.toml              # monorepos only
├── arch/
│   ├── system-map.md       # stub
│   ├── infrastructure.md   # stub
│   └── projects/           # monorepos only — empty, populated by /context-repo-map
├── adrs/
│   └── INDEX.md            # "No ADRs yet."
├── specs/                  # empty
├── plans/
│   ├── active/             # empty, with .gitkeep
│   └── archive/            # empty, with .gitkeep
└── memory/
    └── notes.md            # "# Agent Notes\n\n(append-only)\n"
```

### 5. Generate `repos.toml` (monorepos only)

Use the schema from `references/structure.md`. For each detected
subproject, populate `name`, `path` (relative to repo root, never `../`),
and `purpose` (from README first line if present). Populate `language`,
`test`, `lint`, `entry_points` only where the manifest makes it obvious.
Leave uncertain fields absent.

Add a top-of-file comment:

```toml
# Edit this file by hand. It is the source of truth for this monorepo's
# subprojects. Every /context-repo-* skill reads it first when present.
# Paths are relative to the repo root. Never use `../`.
```

### 6. Generate `CLAUDE.md`

Keep it short:

```markdown
# <repo name>

<1-2 sentence description, pulled from root README.md if possible>

## Where to look
- Architecture: `context/arch/system-map.md`
- Decisions: `context/adrs/INDEX.md`
- Active plans: `context/plans/active/`
- Feature specs: `context/specs/`
<!-- monorepos only: -->
- Subprojects: `context/repos.toml`

## Invariants
- ADRs are immutable; supersede via new ADR.
- `context/arch/` is regenerated, never hand-patched silently.
- `context/memory/notes.md` is append-only.
- All paths in this repo are relative to the repo root.
```

### 7. Generate `README.md`

Human-oriented. Explain what the context repo is, that it lives inside
the code repo (not beside it), how to use it, and which skills exist.
A short version of `references/structure.md`.

### 8. Do not touch git

The repo is already a git repo. Do **not** run `git init`, `git add`, or
`git commit`. The user reviews the scaffold and commits it themselves.

### 9. Report

Print:
- Absolute path to the new `context/` directory
- Whether `repos.toml` was generated (and the detected subprojects, if so)
- Fields that need human review (marked as `# TODO` comments)
- Next step: "Review `context/CLAUDE.md`"
  - Monorepo: "and `context/repos.toml`, then run `/context-repo-map all`"
  - Single project: "then run `/context-repo-map all`"

## Hard rules

- **Never create `context/` outside the current git repo's root.** If not
  in a git repo, refuse.
- **Never create `context/` under `.claude/`.** That directory is for
  harness config only.
- **Never overwrite an existing `context/` directory.**
- **Never run `git init`, `git add`, or `git commit`.** This skill only
  writes files — the user owns version control.
- **Never guess subprojects.** Ask the user to confirm before generating
  `repos.toml`.
- Do not write secrets, tokens, or machine-specific paths into any file.

## References

- [`../context-repo/references/structure.md`](../context-repo/references/structure.md) — directory layout, `repos.toml` schema, ADR/spec/plan formats, hard invariants. **Read before generating any file.**
- [`../context-repo/references/workflow.md`](../context-repo/references/workflow.md) — where `init` sits in the lifecycle and which skill to run next.

## Related skills

| Direction | Skill | Why |
|-----------|-------|-----|
| **Next step** | `/context-repo-map all` | After init, generate `arch/` docs from the current repo |
| **Also useful early** | `/context-repo-adr new` | Capture foundational decisions that motivated creating the context repo |
| Later | `/context-repo-spec <slug>` | First feature once maps exist |
| Maintenance | `/context-repo-refresh` | Audit staleness after the repo has been in use for a while |

On completion, always suggest `/context-repo-map all` as the next step.
