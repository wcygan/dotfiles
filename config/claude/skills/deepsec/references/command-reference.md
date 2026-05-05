# Command reference

All commands run from inside `.deepsec/` unless noted. Bun substitutions in **bold**.

| Command | What it does | Cost | Notes |
|---|---|---|---|
| `bunx deepsec init` | Creates `.deepsec/` and registers the current repo | free | **Run from target repo root**, not `.deepsec/` |
| **`bun install`** | Installs the `deepsec` package + workspace deps | free | Inside `.deepsec/` |
| **`bun run deepsec scan`** | Regex matchers find candidate sites | free, fast | No AI; safe to re-run |
| **`bun run deepsec process`** | AI investigation; emits findings + recommendation | **$$–$$$$$** | Confirm cost before running. Idempotent / resumable |
| **`bun run deepsec triage`** | P0/P1/P2 classification with a cheaper model | $ | Optional but useful |
| **`bun run deepsec revalidate`** | Re-checks findings, drops ones git history shows fixed | $ | Cuts FP rate noticeably |
| **`bun run deepsec enrich`** | Adds git committer info; ownership data with a plugin | free–$ | |
| **`bun run deepsec report`** | Markdown + JSON summary for one project | free | |
| **`bun run deepsec export --format md-dir --out <path>`** | Per-finding markdown directory | free | Use a path **outside** `.deepsec/` |
| **`bun run deepsec export --format json --out <path>`** | Per-finding JSON | free | Machine-readable |
| **`bun run deepsec metrics`** | Cross-project counts: severities, vuln types, TPs | free | |
| **`bun run deepsec status`** | Snapshot of project mirror state | free | |
| **`bun run deepsec sandbox <cmd> --project-id <id> --sandboxes N --concurrency M`** | Fan a command across Vercel Sandbox microVMs | $$+infra | Out of scope for this skill — point user to upstream `docs/vercel-setup.md` |

## Pipeline order (recommended)

```
init  →  bun install  →  bootstrap INFO.md  →  scan  →  [user confirms cost]
      →  process  →  revalidate  →  triage  →  export
```

`triage` and `revalidate` are commutative; either order works.

## Flags worth knowing

- **`--project-id <id>`** — every command takes this when multiple projects share a `.deepsec/`. Default is the first registered project.
- **`--format md-dir | json`** on `export` — md-dir for humans, json for tooling.
- **`--out <path>`** on `export` — required for non-default output paths. Will overwrite without prompt; refuse to clobber existing dirs without explicit user confirmation.
- **`AI_GATEWAY_API_KEY`** env — single key for Claude + Codex. Beats explicit `ANTHROPIC_*` only if those are unset.

## Resumption semantics

`process` is idempotent: kill it, restart it, it picks up from the last completed batch. Useful when:

- The user closes the terminal accidentally
- A batch fails on a single file (rest of the run continues)
- A scan takes hours and the user wants to checkpoint progress

Don't add retry wrappers — the CLI already handles this.

## What NOT to run from this skill

These need explicit user authorization with cost context:

- `process` (touched on above)
- `revalidate` (cheap-ish but still bills tokens)
- Any `sandbox <cmd>` — provisions microVMs, billed per minute
- `export` with `--out` pointing at a non-empty directory — risk of clobbering prior findings
