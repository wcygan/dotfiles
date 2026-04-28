# Local dev tools (agent-friendly)

Two Vercel Labs CLIs that pair well with this stack when an **agent** (or human) needs to dog-food the running dev server. Both are optional — the stack runs fine without them — but they remove specific friction the moment you start asking an agent to "go check the page."

## portless — stable named `.localhost` URLs

> https://github.com/vercel-labs/portless

Replaces `http://localhost:<random-port>` with a deterministic `https://<name>.localhost`.

**Why it matters for this stack**

- **Stable target for agents.** An agent can hardcode `https://myapp.localhost` in test commands, screenshots, and `agent-browser` calls without first scraping the Vite dev-server's "Local: http://localhost:5173" line out of stdout. The URL is derived from the project name, not the port the OS happens to hand out.
- **HTTPS by default with an auto-trusted local CA.** TanStack Start renders cookies, headers, and redirects under SSR; secure-context features (Service Workers, WebAuthn, `SameSite=None; Secure` cookies, `crossOriginIsolated`) only behave production-like over HTTPS. Plain `http://localhost` silently diverges.
- **Vite-aware.** portless auto-injects `--port` and `--host` for frameworks that ignore `PORT` (Vite is on that list). Our canonical scripts (`bun --bun vite dev`) work unchanged — portless wraps the command.
- **CI-safe.** In non-TTY / `CI=1` environments it exits with a clear error instead of prompting for sudo on port 443. Fine for local agent runs; don't bake it into CI without `--no-tls`.

**How to wire it in (optional)**

```bash
# One-off, no script change
bunx portless        # runs the `dev` script → https://<project>.localhost

# Or pin per-project
bun add -d portless
# then: bunx portless
```

Optional `portless.json` next to `package.json`:
```json
{ "name": "myapp" }
```

**When *not* to reach for it**

- Just typing the URL once yourself — overkill.
- Anything that runs in CI without a TTY (use the bare dev script).
- Stacks where you've already standardized on a different proxy (Caddy, Traefik, ngrok). Don't stack proxies.

## agent-browser — native CLI for browser automation

> https://github.com/vercel-labs/agent-browser

Fast Rust CLI built specifically for AI agent loops: each step is a discrete shell command with text output, instead of a long-lived Node/Playwright process the agent has to keep alive across turns.

**Why it matters for this stack**

- **Closes the verification loop.** TanStack Start is SSR-first; type-checks and tests don't catch hydration mismatches, missing stylesheet links from `__root.tsx`, broken loaders, or layout regressions. An agent can navigate, screenshot, and assert against the actual rendered page in one command.
- **Cheap per-invocation.** Native binary, low startup overhead — important when an agent issues many short commands across a session rather than one long script.
- **Pinned Chrome via Chrome for Testing** (`agent-browser install`). Reproducible across machines and CI; no "works on my Chrome 142, breaks on 141" surprises.
- **Already wired into this user's skill set.** The `agent-browser` skill auto-loads on browser-automation requests and is preferred over generic web tools.

**Typical agent loop on this stack**

1. `bun --bun vite dev` (or `bunx portless` for a stable URL).
2. `agent-browser` navigates `https://myapp.localhost` (or `http://localhost:<port>`).
3. Screenshot / extract / click / assert.
4. Edit code → HMR → repeat from step 2.

**When *not* to reach for it**

- Unit/integration tests that don't need a real browser — use Vitest/Bun's test runner.
- One-off "does the page load" check the user can do in their own browser.
- Headless E2E suites that already use Playwright in CI — keep them; don't fork the toolchain.

## Pairing them

`portless` gives the agent a deterministic HTTPS target; `agent-browser` gives it a cheap way to drive that target. Together they remove the two papercuts that show up the moment an agent tries to verify its own UI work on this stack: "what port is it on this run?" and "how do I drive a browser from a single shell command?"

Neither is required. Reach for them when the workflow is **agent-driven dogfooding of the dev server**, not when a human is just running `bun --bun vite dev` in one terminal.
