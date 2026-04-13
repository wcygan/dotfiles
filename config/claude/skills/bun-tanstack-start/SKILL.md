---
name: bun-tanstack-start
description: Opinionated scaffolding and wiring for Bun + TanStack Start apps. Encodes exact create/run commands, Vite plugin order, Tailwind v4 CSS import pattern, `__root.tsx` stylesheet injection, server functions, and Nitro deployment presets. Auto-loads when package.json contains `@tanstack/react-start` or the user asks to create/set up/configure a TanStack Start project with Bun. Complements the general `tanstack-start` and `tailwind` skills by being stack-specific and command-exact. Keywords bun, bunx, tanstack start, vite, nitro, createFileRoute, createServerFn, __root, SSR, react-start.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch
---

# Bun + TanStack Start (Opinionated Stack)

Stack-specific mechanics for shipping a TanStack Start app on **Bun** with **Tailwind v4**. This is the *how to wire it up* skill — the *design tokens* skill owns visual consistency, and `frontend-aesthetic` owns taste.

This skill is **low-freedom**: the commands and config snippets below are load-bearing and easy to get wrong from memory. Use them verbatim.

## When to use this skill

| Signal | Action |
|---|---|
| `package.json` has `@tanstack/react-start` | Apply this skill's conventions automatically |
| User says "new app" / "scaffold" / "set up TanStack Start" | Use [create-and-run](references/create-and-run.md) |
| User adds a route / touches `src/routes/` | Apply [routing](references/routing.md) conventions |
| User writes server logic | Use [server-functions](references/server-functions.md) |
| User asks about deployment / Vercel / Cloudflare | See [deployment](references/deployment.md) |
| `bun.lockb` but scripts missing `--bun` flag | Flag and patch — see [create-and-run](references/create-and-run.md) |

## Non-negotiables (the six easy-to-miss things)

1. **Scaffold with the TanStack CLI via `bunx`**: `bunx @tanstack/cli create my-app`. Do not hand-roll.
2. **Force Bun as the runtime** in scripts with `bun --bun`. Without the flag, Bun delegates to Node and the runtime advantage evaporates.
3. **Vite plugin order**: `tsConfigPaths() → tanstackStart() → viteReact() → tailwindcss()`. Order matters.
4. **Tailwind v4 CSS entry** uses `@import 'tailwindcss' source('../')` — not `@tailwind base/components/utilities` (v3 syntax) and not a `tailwind.config.js` file (v4 is CSS-first).
5. **Inject the stylesheet via the root route** using `?url` import + `head.links` — *not* a plain `import './styles.css'`.
6. **Nitro `bun` preset is incompatible with Vercel.** Pick presets per target; don't blanket-set it.

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

## References

- [create-and-run](references/create-and-run.md) — exact scaffold + run commands
- [vite-config](references/vite-config.md) — plugin order, env handling
- [routing](references/routing.md) — `__root.tsx`, `createFileRoute`, loaders, consistency
- [server-functions](references/server-functions.md) — `createServerFn`, middleware, auth
- [deployment](references/deployment.md) — Nitro preset matrix, Bun vs Node runtime
- [upgrade-paths](references/upgrade-paths.md) — drift watch for TanStack/Bun releases

## External canonical docs

- Bun + TanStack Start guide: https://bun.com/docs/guides/ecosystem/tanstack-start
- TanStack Start getting started: https://tanstack.com/start/latest/docs/framework/react/getting-started
- Bun quickstart: https://bun.com/docs/quickstart
- TanStack Start Tailwind integration: https://tanstack.com/start/latest/docs/framework/react/guide/tailwind-integration
- Tailwind v4 Vite install: https://tailwindcss.com/docs/installation/using-vite

## Complements

- `tanstack-start` skill — general framework reference (API catalog, routing concepts)
- `tailwind` skill — general Tailwind v4 reference
- `tailwind-v4-tokens` skill — token system layered on top
- `frontend-aesthetic` skill — visual direction
