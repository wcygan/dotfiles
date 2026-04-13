# Vite Config

## Plugin order (load-bearing)

```ts
import { defineConfig } from 'vite'
import tsConfigPaths from 'vite-tsconfig-paths'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tsConfigPaths(),   // 1. Resolve `@/*` aliases before anything else
    tanstackStart(),   // 2. Generate the route tree, inject server entry
    viteReact(),       // 3. React fast-refresh transforms
    tailwindcss(),     // 4. Tailwind v4 Vite plugin last — consumes all CSS
  ],
})
```

**Why order matters**: `tsConfigPaths` must run before `tanstackStart` so generated route imports resolve. `tailwindcss()` must run last so every CSS module passes through it (including ones authored by earlier plugins).

## Env vars

- Client-visible env must be prefixed `VITE_` (Vite convention).
- Server-only env reads directly from `process.env` inside server functions or loaders.
- Never leak `SERVER_*` secrets by importing a config module from a route component — use `createServerFn` to gate server-only reads.

## Path aliases

`tsconfig.json`:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  }
}
```

`vite-tsconfig-paths` picks this up automatically — do not duplicate aliases in `vite.config.ts`.

## Build output

Default output is `.output/` (Nitro convention). Do not commit; add to `.gitignore` and deploy from a build step.
