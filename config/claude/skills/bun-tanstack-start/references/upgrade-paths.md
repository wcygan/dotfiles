# Upgrade Paths & Drift Watch

TanStack Start and Bun both move fast. Re-verify these anchors when versions change:

## Things to re-check on upgrade

1. **Plugin import path**: `@tanstack/react-start/plugin/vite` has moved before — confirm with the linked docs below.
2. **CSS import syntax**: `@import 'tailwindcss' source('../')` is current Tailwind v4 convention. A v5 syntax may differ.
3. **`?url` suffix for stylesheets**: this is Vite behavior; unlikely to change but verify in `__root.tsx`.
4. **Nitro preset names**: check `cloudflare-pages` vs `cloudflare-module` on the latest Nitro docs.
5. **Route tree generator output**: if `routeTree.gen.ts` stops being generated, the `tanstackStart()` plugin is likely misordered or outdated.
6. **`bun --bun` flag**: still required; if Bun auto-forces itself someday, remove it.

## Canonical sources to WebFetch when in doubt

- https://tanstack.com/start/latest/docs/framework/react/getting-started
- https://bun.com/docs/guides/ecosystem/tanstack-start
- https://tanstack.com/start/latest/docs/framework/react/guide/tailwind-integration
- https://tailwindcss.com/docs/installation/using-vite
- https://nitro.unjs.io/deploy (preset list)

## Red flags that mean "re-read the docs before editing"

- `tailwind.config.js` exists → this skill's assumptions are broken; stop and reconcile.
- Plugin order differs from this skill's canonical ordering → verify against current TanStack Start docs before "fixing".
- `@tailwind base;` appears in CSS → project is still on v3; either upgrade or switch to the older `tailwind` skill.
