---
name: context-repo-map
description: >
  Generate or refresh architecture maps in a context repo. Scopes - all,
  infra (databases, queues, caches, cloud, external services), system
  (repo-wide system map), project <name> (per-subproject summary, monorepos
  only). Inspects the current git repo, reads context/repos.toml when
  present, writes to context/arch/. Always shows a diff before applying.
  Use when the context repo is new, after a significant change, or when
  agents keep missing context about the repo or its infrastructure stack.
  Keywords: map infrastructure, arch map, system map, project summary,
  generate arch docs, infrastructure inventory, tech stack inventory
disable-model-invocation: true
argument-hint: <scope: all|infra|system|project <name>>
context: fork
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(fd *), Bash(ls *), Bash(cat *), Bash(wc *), Write, Edit
---

# /context-repo-map

Generate or refresh architecture maps in `context/arch/`. Forks because
map generation is exploration-heavy and shouldn't pollute the main
conversation.

**Scope**: `$ARGUMENTS`. Valid values:
- `all` — infrastructure + system map + per-project summaries (if monorepo)
- `infra` — only `arch/infrastructure.md`
- `system` — only `arch/system-map.md`
- `project <name>` — only `arch/projects/<name>.md` (requires `repos.toml`)

If `$ARGUMENTS` is missing, default to `all` and confirm with the user.

Read `../context-repo/references/structure.md` before writing anything.

## Workflow

### 1. Locate the context repo

Run `git rev-parse --show-toplevel`. The context repo is at
`<repo-root>/context`. If it doesn't exist, stop and tell the user to run
`/context-repo-init`.

### 2. Detect mode (single project vs monorepo)

- If `context/repos.toml` exists, parse it. Each `[[projects]]` entry
  defines a subproject with a `path` relative to the repo root.
- If `context/repos.toml` is absent, treat the whole repo as one project.
  The `project <name>` scope is unavailable in this mode; `all` skips the
  per-project step.

### 3. Inspect the repo

All paths below are relative to the repo root. Never use `../` to escape.
Never read files outside the repo root.

**For `infra` scope** — scan the repo tree (or, in monorepo mode, each
listed project path) for:
- `docker-compose.y*ml`, `compose.y*ml` → extracted services
- `Dockerfile*` → base images, exposed ports
- `k8s/`, `kubernetes/`, `deploy/`, `helm/` → manifests
- `.env.example`, `config/*.y*ml`, `config/*.toml` → env var names (never values)
- `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml` → dependencies
  matching known infra libs (pg, mysql, redis, rabbitmq, kafka, nats, s3,
  opensearch, clickhouse, etc.)
- `README.md` → first 50 lines

Produce `arch/infrastructure.md` with sections:
- **Databases** (kind, which part of the repo uses it, connection env var name)
- **Queues / streams**
- **Caches**
- **Object storage**
- **External APIs** (by hostname, pulled from `.env.example`)
- **Cloud services** (AWS/GCP/Azure clients detected)
- **Observability** (Prometheus, OTel, Datadog, Sentry)
- **Open questions** (things the scan couldn't resolve — for human review)

**For `project <name>` scope** (monorepo only) — produce
`arch/projects/<name>.md` with:
- **Purpose** (1 sentence, from `repos.toml`)
- **Location** (path from `repos.toml`, relative to repo root)
- **Entry points** (main files, binaries)
- **Key modules / packages** (top-level directories with 1-line descriptions)
- **External interfaces** (HTTP routes, gRPC services, CLI commands, exported libs)
- **Infrastructure dependencies** (from infra scan)
- **Test command** (from `repos.toml`)
- **How to run locally** (if inferable)
- **Owners** (from `repos.toml`)

**For `system` scope** — produce `arch/system-map.md` with:
- **Mermaid diagram** showing components as nodes and their dependencies
  as edges. In monorepo mode, nodes are subprojects from `repos.toml`
  (using `depends_on`). In single-project mode, nodes are top-level
  modules/packages inferred from the code.
- **Request flow** for the most common end-to-end path
- **Cross-cutting invariants** (3-5 bullets — things that are true
  everywhere in the repo and must not be violated)
- **Deployment topology** (what deploys where, from infra scan)

### 4. Show a diff before writing

For each file to be written:
- If the file doesn't exist, show the new content and ask "Create?"
- If it exists, generate the new content into a temp buffer, show the diff
  against the existing file, and ask "Apply?"
- Never silently overwrite.

### 5. Write accepted changes

Write files individually. After each write, tell the user the path.

### 6. Report

- List of files created/updated/skipped
- Open questions surfaced in the scan (the human's next action)
- Suggested next step: `/context-repo-adr new` if the scan revealed
  undocumented decisions, or `/context-repo-spec <slug>` if a feature is next.

## Hard rules

- Do not read or write anything outside the current repo root.
- Do not include secret values — only env var names.
- Do not invent dependencies. If the scan is uncertain, say so in the
  "Open questions" section.
- Always diff-before-write. Silent overwrites are banned.
- Do not touch files outside `context/arch/`.
- `project <name>` scope requires `repos.toml`. If absent, refuse and
  explain.

## References

- [`../context-repo/references/structure.md`](../context-repo/references/structure.md) — the `arch/` file formats (`system-map.md`, `infrastructure.md`, `projects/<name>.md`) and the `repos.toml` schema.
- [`../context-repo/references/workflow.md`](../context-repo/references/workflow.md) — when to run `map` in the lifecycle (after `init`, after `refresh`, before `spec`).

## Related skills

| Direction | Skill | Why |
|-----------|-------|-----|
| **Prerequisite** | `/context-repo-init` | Must exist; `map` writes into the scaffold |
| **Triggered by** | `/context-repo-refresh` | Reports which maps are stale; run `map` with the suggested scope |
| **Next step** | `/context-repo-spec <slug>` | Use the fresh maps to frame a feature |
| Also useful | `/context-repo-adr new` | The scan often surfaces decisions worth recording (especially during `infra` scope) |
| Also useful | `/context-repo-adr review` | Drift-check ADRs against the newly regenerated maps |

After generating maps, surface any decisions found in "Open questions" and
suggest `/context-repo-adr new` for the important ones.
