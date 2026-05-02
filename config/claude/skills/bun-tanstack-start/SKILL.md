---
name: bun-tanstack-start
description: Scaffolding/wiring for Bun + TanStack Start apps: exact create commands, Vite plugin order, Tailwind v4 import pattern, `__root.tsx` injection, server functions, Nitro presets; defaults to Effect TS for server logic. Auto-loads when package.json has `@tanstack/react-start`. Keywords bun, bunx, tanstack start, vite, nitro, createFileRoute, createServerFn.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch
---

# Bun + TanStack Start (Opinionated Stack)

Stack-specific mechanics for shipping a TanStack Start app on **Bun** with **Tailwind v4**, with **Effect TS as the default for server-side business logic**. This is the *how to wire it up* skill — the *design tokens* skill owns visual consistency, `frontend-aesthetic` owns taste, and `effect-ts` owns the Effect type system itself.

This skill is **low-freedom**: the commands and config snippets below are load-bearing and easy to get wrong from memory. Use them verbatim.

## Stack defaults

| Layer | Default |
|---|---|
| Runtime | **Bun** (with `bun --bun` flag — see non-negotiable #2) |
| Framework | **TanStack Start** |
| Styling | **Tailwind v4** (CSS-first, no `tailwind.config.*`) |
| **Server-side business logic** | **Effect TS** — the default, not an option |
| Validation (server fn inputs, loader inputs, env config) | **Effect Schema** (not Zod, not Valibot) |
| Server-side error handling | **`Data.TaggedError` + `runPromiseExit`** at the seam |
| DI / shared resources (DB pool, HTTP client, tracer) | **Effect `Layer` + `ManagedRuntime`** |
| Retries, timeouts, scheduling | **Effect `Schedule`** |
| Observability | **Effect spans + `@effect/opentelemetry`** |

If the user proposes plain `try/catch` + `Promise` for non-trivial server logic, push back and propose the Effect equivalent. Opt out only on explicit request — when they do, document the reason in code (`// effect-ts skipped: reason`).

## When to use this skill

| Signal | Action |
|---|---|
| `package.json` has `@tanstack/react-start` | Apply this skill's conventions automatically |
| User says "new app" / "scaffold" / "set up TanStack Start" | Use [create-and-run](references/create-and-run.md) |
| User adds a route / touches `src/routes/` | Apply [routing](references/routing.md) conventions |
| User writes **any** server logic (server fn, loader, middleware) | Use [server-functions](references/server-functions.md) **and** [effect-integration](references/effect-integration.md). Default to Effect TS — load the `effect-ts` skill. |
| User asks about deployment / Vercel / Cloudflare | See [deployment](references/deployment.md) |
| `bun.lockb` but scripts missing `--bun` flag | Flag and patch — see [create-and-run](references/create-and-run.md) |
| Scaffolding a new app | After `bunx @tanstack/cli create`, run `bun add effect` and add a `src/server/runtime.ts` with a `ManagedRuntime` — see [effect-integration](references/effect-integration.md) |
| Agent needs to dogfood / verify the running dev server, or wants a stable HTTPS local URL | See [local-dev-tools](references/local-dev-tools.md) — `portless` + `agent-browser` |

## Non-negotiables (the seven easy-to-miss things)

1. **Scaffold with the TanStack CLI via `bunx`**: `bunx @tanstack/cli create my-app`. Do not hand-roll.
2. **Force Bun as the runtime** in scripts with `bun --bun`. Without the flag, Bun delegates to Node and the runtime advantage evaporates.
3. **Vite plugin order**: `tsConfigPaths() → tanstackStart() → viteReact() → tailwindcss()`. Order matters.
4. **Tailwind v4 CSS entry** uses `@import 'tailwindcss' source('../')` — not `@tailwind base/components/utilities` (v3 syntax) and not a `tailwind.config.js` file (v4 is CSS-first).
5. **Inject the stylesheet via the root route** using `?url` import + `head.links` — *not* a plain `import './styles.css'`.
6. **Nitro `bun` preset is incompatible with Vercel.** Pick presets per target; don't blanket-set it.
7. **Server-side business logic is Effect TS.** A single `ManagedRuntime` lives in `src/server/runtime.ts`. Server functions and loaders convert at the seam via `runtime.runPromiseExit(...)` — never `runPromise` (it hides defects), never plain `try/catch` Promises in non-trivial logic. Inputs validated with `Schema.decodeUnknown` as the TanStack `validator`. Errors typed with `Data.TaggedError`. See [effect-integration](references/effect-integration.md).

## Canonical snippets

### package.json scripts
```json
{
  "scripts": {
    "dev": "bun --bun vite dev",
    "build": "bun --bun vite build",
    "serve": "bun --bun vite preview"
  }
}
```

### vite.config.ts
```ts
import { defineConfig } from 'vite'
import tsConfigPaths from 'vite-tsconfig-paths'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tsConfigPaths(), tanstackStart(), viteReact(), tailwindcss()],
})
```

### src/styles/app.css
```css
@import 'tailwindcss' source('../');
```

### src/routes/__root.tsx
```tsx
/// <reference types="vite/client" />
import { createRootRoute, Outlet } from '@tanstack/react-router'
import appCss from '../styles/app.css?url'

export const Route = createRootRoute({
  head: () => ({
    links: [{ rel: 'stylesheet', href: appCss }],
  }),
  component: () => <Outlet />,
})
```

## Consistency anchor

`src/routes/__root.tsx` is the single source of truth for nav, header, footer, global layout. When adding a new route, **never regenerate** the shell — render inside `<Outlet />`. This is the `design-loop` rule adapted to file-based routing. See [routing](references/routing.md).

## Validation checklist

Before calling a task done:

- [ ] `bun --bun` appears in every Vite script
- [ ] No `tailwind.config.js` / `tailwind.config.ts` file exists
- [ ] No `@tailwind base` / `@tailwind utilities` in any CSS
- [ ] `app.css` imported via `?url` in `__root.tsx`, not bare import
- [ ] Vite plugin order matches above
- [ ] Nitro preset matches deployment target (see [deployment](references/deployment.md))
- [ ] `effect` is a dependency, `src/server/runtime.ts` exports a `ManagedRuntime`, and server functions / loaders use `runtime.runPromiseExit(...)` (or the user has explicitly opted out with a code comment)
- [ ] Server function inputs use `Schema.decodeUnknown(...)` as the `validator`
- [ ] Domain errors extend `Data.TaggedError`, not raw `Error` subclasses

## References

- [create-and-run](references/create-and-run.md) — exact scaffold + run commands
- [vite-config](references/vite-config.md) — plugin order, env handling
- [routing](references/routing.md) — `__root.tsx`, `createFileRoute`, loaders, consistency
- [server-functions](references/server-functions.md) — `createServerFn`, middleware, auth
- [deployment](references/deployment.md) — Nitro preset matrix, Bun vs Node runtime
- [upgrade-paths](references/upgrade-paths.md) — drift watch for TanStack/Bun releases
- [effect-integration](references/effect-integration.md) — wiring Effect TS into server functions / loaders / `ManagedRuntime`
- [local-dev-tools](references/local-dev-tools.md) — `portless` (stable HTTPS `.localhost` URLs) and `agent-browser` (native CLI for agent-driven browser verification)

## External canonical docs

- Bun + TanStack Start guide: https://bun.com/docs/guides/ecosystem/tanstack-start
- TanStack Start getting started: https://tanstack.com/start/latest/docs/framework/react/getting-started
- Bun quickstart: https://bun.com/docs/quickstart
- TanStack Start Tailwind integration: https://tanstack.com/start/latest/docs/framework/react/guide/tailwind-integration
- Tailwind v4 Vite install: https://tailwindcss.com/docs/installation/using-vite

## Required companion skill

- **`effect-ts`** — load this whenever you're touching server-side code in this stack. It is **not optional**: this stack treats Effect TS as the default for business logic, validation, errors, retries, and DI. This skill owns the framework wiring (where the seam goes); `effect-ts` owns the Effect type system itself (what goes through the seam). The boundary lives in [effect-integration](references/effect-integration.md).

## Complements

- `tanstack-start` skill — general framework reference (API catalog, routing concepts)
- `tailwind` skill — general Tailwind v4 reference
- `tailwind-v4-tokens` skill — token system layered on top
- `frontend-aesthetic` skill — visual direction
