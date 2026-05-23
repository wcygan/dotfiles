---
name: portless
description: "Use when configuring, debugging, or documenting Portless for local development: stable named .localhost URLs, portless CLI usage, HTTPS/local CA setup, custom TLD or LAN mode, Tailscale sharing, monorepo or git worktree routing, package.json/portless.json configuration, static aliases, hosts cleanup, or replacing localhost port numbers in dev scripts."
---

# Portless

Use this skill to route local development servers through Portless: stable named URLs such as `https://myapp.localhost` instead of fragile `localhost:<port>` links.

## Default Approach

- Prefer the least invasive repo change: add `portless.json` or a `package.json` `"portless"` key before rewriting many scripts.
- Keep the underlying app command visible. For package scripts, prefer `portless` plus a separate real script such as `dev:app` when Turborepo or recursive package scripts are involved.
- Use `portless run <cmd>` when the app name should be inferred from the repo, package, config, or git worktree.
- Use `portless <name> <cmd>` when the URL name must be explicit and no inference is wanted.
- Use `portless alias <name> <port>` for services not started by Portless, such as Docker containers.
- Treat Portless as development-only config unless the user explicitly asks for production-adjacent sharing such as Tailscale Funnel.

## Safety

- Ask before running commands that can prompt for admin privileges or modify system state: first-run trust flows, `portless trust`, `portless clean`, `portless hosts sync`, `portless hosts clean`, and `portless service install/uninstall`.
- Do not run `portless prune --force` or `portless <name> ... --force` unless the user asks to kill or take over existing processes.
- Expect HTTPS on port 443 by default. Use `--no-tls`, `-p <port>`, or custom certs only when the local environment requires it.
- Remember that Portless is pre-1.0. Prefer a globally installed version for consistent local state, or pin a project dev dependency when reproducibility matters more than shared machine state.

## Workflow

1. Inspect the repo first: `package.json`, workspace files, existing dev scripts, framework config, and any hardcoded localhost URLs.
2. Load the relevant reference file from the map below. For most implementation work, start with `references/getting-started.md` and `references/configuration.md`.
3. Choose stable hostnames. Use subdomains for multi-service apps, and account for git worktree prefixes when using `portless run`.
4. Add the smallest durable config: `portless.json`, a `"portless"` key, or a script update.
5. Handle framework edge cases: Vite/webpack API proxy `changeOrigin`, Next.js LAN `allowedDevOrigins`, Expo/React Native LAN networking, custom TLD, or Tailscale sharing.
6. Verify without unnecessary system changes first: inspect scripts/config, run `portless --help` or `portless --version` when installed, then run the app only when the user wants live validation.

## Reference Map

- `references/getting-started.md`: install, basic run modes, subdomains, worktrees, custom TLDs, requirements.
- `references/github-repository.md`: README-only details such as LAN mode, Tailscale/Funnel sharing, repo development commands, Safari/DNS, and proxying between Portless apps.
- `references/why.md`: reasons to adopt Portless and which pain points it solves.
- `references/commands.md`: command syntax, flags, lifecycle commands, aliases, proxy/service controls, hosts, and bypass mode.
- `references/https.md`: default HTTPS/HTTP2 behavior, local CA trust, custom certs, and disabling TLS.
- `references/configuration.md`: `portless.json`, package.json `"portless"`, monorepo discovery, config precedence, env vars, state files, and port assignment.

## Common Config Shapes

Single app, inferred name:

```json
{
  "scripts": {
    "dev": "next dev"
  }
}
```

Run with:

```sh
portless
```

Explicit app URL in a script:

```json
{
  "scripts": {
    "dev": "portless run next dev"
  }
}
```

Turborepo-friendly package:

```json
{
  "scripts": {
    "dev": "portless",
    "dev:app": "next dev"
  },
  "portless": { "name": "myapp", "script": "dev:app" }
}
```

Monorepo root overrides:

```json
{
  "apps": {
    "apps/web": { "name": "myapp" },
    "apps/api": { "name": "api.myapp" }
  }
}
```

## Sources

- https://portless.sh/
- https://github.com/vercel-labs/portless
- https://portless.sh/why
- https://portless.sh/commands
- https://portless.sh/https
- https://portless.sh/configuration
