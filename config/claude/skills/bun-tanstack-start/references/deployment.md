# Deployment

TanStack Start builds via Nitro. Pick a preset per target — **do not** blanket-default to `bun`.

## Preset matrix

| Target | Nitro preset | Notes |
|---|---|---|
| Bun (self-hosted / container) | `bun` | Run `.output/server/index.mjs` with `bun`. Fastest cold start. |
| Node (generic) | `node-server` | Works everywhere but slower than Bun. Default fallback. |
| Vercel | `vercel` | **Incompatible with `bun` preset.** Always use `vercel`. |
| Cloudflare Workers | `cloudflare-pages` or `cloudflare-module` | No Node APIs — audit deps for `fs`, `crypto` usage. |
| Netlify | `netlify` | |

## Configure via env or `app.config.ts`

```ts
// app.config.ts
export default {
  server: { preset: process.env.NITRO_PRESET ?? 'node-server' },
}
```

Then `NITRO_PRESET=bun bun run build` for a Bun container, or rely on platform auto-detection (Vercel injects its own).

## Bun-specific server run

```sh
bun --bun .output/server/index.mjs
```

Add a `start` script:
```json
"start": "bun --bun .output/server/index.mjs"
```

## Gotchas

- `cloudflare-module` has no `node:fs` — adapt any file reads to imports or KV.
- Vercel's build system ignores `NITRO_PRESET` and forces `vercel`. Don't fight it.
- Static-only? Use `node-server` preset and front with a CDN; TanStack Start does not have a pure SPA export out of the box unless you disable SSR explicitly.
