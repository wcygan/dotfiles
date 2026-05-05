# Install & first scan (Bun)

End-to-end first-scan walkthrough. Translates the upstream README's `npx`/`pnpm` commands to Bun.

## 0. Preflight

```bash
bun --version           # require Bun
node --version          # require Node ≥22 (deepsec engines field)
```

If `node` is missing or <22, stop and tell the user. Bun cannot substitute for Node in the deepsec runtime.

## 1. Init (run from the repo you want to scan)

```bash
# cwd: <target-repo>
bunx deepsec init
```

This creates `.deepsec/` with the target repo registered as the first project and prints further instructions, including a `<id>` for the project's data dir.

## 2. Install deepsec into the harness

```bash
cd .deepsec
bun install
```

Resulting `.deepsec/` layout (relevant bits):

```
.deepsec/
├── node_modules/deepsec/SKILL.md      ← upstream skill the agent should read
├── data/<id>/
│   ├── SETUP.md                        ← bootstrap instructions
│   └── INFO.md                         ← agent-authored project context (starts as a stub)
└── package.json
```

## 3. Bootstrap INFO.md (the mandatory agent step)

This is the part the README delegates to a coding agent. Do it inline — do **not** ask the parent to do it.

1. Read `.deepsec/node_modules/deepsec/SKILL.md` (use Read, not bash cat).
2. Read `.deepsec/data/<id>/SETUP.md`.
3. Skim the **target repo** (one level up):
   - README.md
   - any AGENTS.md / CLAUDE.md / .cursor/rules
   - 5–10 representative source files (entry points, auth, middleware, data access)
4. Replace each section of `.deepsec/data/<id>/INFO.md`.

**Constraints on INFO.md** (from upstream guidance — load-bearing):

- Target **50–100 lines total**. Verbose context dilutes scan signal because INFO.md is injected into every batch.
- 3–5 examples per section. Not exhaustive enumeration.
- Name primitives (auth helpers, middleware, request validators) but **no line numbers** — they rot.
- Skip generic CWE categories — built-in matchers cover those. Cover only project-specific concerns.

## 4. Configure credentials

Two paths, in priority order:

**Local dev (preferred when available):** deepsec uses the user's existing Claude / Codex subscriptions automatically. No env vars needed. Don't override unless the user asks.

**Scaled / CI:** set the AI Gateway key.

```bash
# .env or shell
AI_GATEWAY_API_KEY=vck_...
```

That single key covers both Claude and Codex via the Vercel AI Gateway.

**Explicit override (advanced):** to bypass the gateway, set `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL` (or the OpenAI pair). Explicit values always beat `AI_GATEWAY_API_KEY` expansion.

## 5. Scan (cheap, no AI)

```bash
# cwd: .deepsec
bun run deepsec scan
```

Runs regex matchers across the target tree. Output: candidate sites in `data/<id>/`. Read the count back to the user; this drives the cost estimate for step 6.

## 6. Process (expensive — confirm first)

**STOP.** Before running this, surface the cost shape to the user:

- Candidate site count (from step 5)
- Default model is the strongest available at max thinking — runs can be $1k–$10k+ on large repos
- Idempotent and resumable, so an interrupted run isn't wasted

Only after explicit confirmation:

```bash
bun run deepsec process
```

## 7. Revalidate (optional, recommended)

```bash
bun run deepsec revalidate
```

Re-checks existing findings, also consults git history to drop findings that have already been fixed. Cuts false-positive rate.

## 8. Triage (optional, cheap classification)

```bash
bun run deepsec triage
```

Lightweight P0/P1/P2 pass with a smaller model.

## 9. Export

```bash
bun run deepsec export --format md-dir --out ./findings
```

Use a path **outside** `.deepsec/` so findings survive a clean install. `findings/` at the target repo root is a sensible default.

## Common first-scan failures

| Symptom | Cause | Fix |
|---|---|---|
| `bunx deepsec init` errors on Node version | Bun's bundled Node shim too old | Install Node ≥22 separately; bunx defers to it |
| `bun install` fails on workspace deps | User accidentally ran inside the **deepsec source repo** | `cwd` should be the user's `.deepsec/`, not vercel-labs/deepsec checkout |
| `process` exits immediately with no work | `scan` was never run, or scan output was wiped | Re-run `scan`; check `data/<id>/` |
| Auth errors despite `AI_GATEWAY_API_KEY` | Stale `ANTHROPIC_AUTH_TOKEN` in env wins over gateway | `unset ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL` |
