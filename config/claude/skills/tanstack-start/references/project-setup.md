# TanStack Start — Project Setup

## CLI Scaffold (Recommended)

```bash
npx @tanstack/cli@latest create my-app
cd my-app
npm install
npm run dev
```

On Bun: `bunx @tanstack/cli create my-app` (the CLI runs on Bun and emits Bun-aware scripts). See the `bun` skill for `--bun` flag and lockfile rules.

## Manual Setup

### package.json

```json
{
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "serve": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-start": "latest",
    "@tanstack/react-router": "latest",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "latest",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.0.0",
    "vite": "^6.0.0",
    "vite-tsconfig-paths": "latest"
  }
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite'
import tsConfigPaths from 'vite-tsconfig-paths'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    tsConfigPaths(),   // 1. Resolve `@/*` aliases before anything else
    tanstackStart(),   // 2. Generate the route tree, inject server entry
    viteReact(),       // 3. React fast-refresh transforms (NOT auto-injected)
  ],
})
```

> **Plugin order is load-bearing.** `tsConfigPaths` must run before `tanstackStart` so generated route imports resolve. `viteReact()` is **not** auto-injected by `tanstackStart()` — add it explicitly. If you also use Tailwind v4, append `tailwindcss()` from `@tailwindcss/vite` last so every CSS module flows through it (see `tailwind-and-styling.md`).

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src", "app.config.ts"]
}
```

### src/router.tsx

```typescript
import { createRouter as createTanStackRouter } from '@tanstack/react-router'
import { routerWithQueryClient } from '@tanstack/react-router-with-query'
import { QueryClient } from '@tanstack/react-query'
import { routeTree } from './routeTree.gen'

export function createRouter() {
  const queryClient = new QueryClient()

  const router = createTanStackRouter({
    routeTree,
    context: { queryClient },
    defaultPreload: 'intent',
    defaultPreloadStaleTime: 0,
    scrollRestoration: true,
  })

  return routerWithQueryClient(router, queryClient)
}

declare module '@tanstack/react-router' {
  interface Register {
    router: ReturnType<typeof createRouter>
  }
}
```

### src/routes/__root.tsx

```typescript
import {
  createRootRouteWithContext,
  HeadContent,
  Outlet,
  Scripts,
} from '@tanstack/react-router'
import type { QueryClient } from '@tanstack/react-query'
import appCss from '../styles/app.css?url'

/// <reference types="vite/client" />

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { title: 'My App' },
    ],
    links: [{ rel: 'stylesheet', href: appCss }],
  }),
  component: RootComponent,
  // Required when any child route has ssr: false
  // shellComponent: ShellComponent,
})

function RootComponent() {
  return (
    <html lang="en">
      <head>
        <HeadContent />
      </head>
      <body>
        <Outlet />
        <Scripts />
      </body>
    </html>
  )
}
```

### src/client.tsx

```typescript
import { StartClient } from '@tanstack/react-start/client'
import { createRouter } from './router'
import ReactDOM from 'react-dom/client'

const router = createRouter()

ReactDOM.hydrateRoot(document, <StartClient router={router} />)
```

### src/ssr.tsx

```typescript
import { createStartHandler, defaultStreamHandler } from '@tanstack/react-start/server'
import { createRouter } from './router'

export default createStartHandler({
  createRouter,
})(defaultStreamHandler)
```

## TanStack Router Plugin (File-Based Routing)

Add to vite config to enable auto route-tree generation:

```typescript
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'

// In vite plugins array (inside defineConfig vite.plugins):
TanStackRouterVite({ target: 'react', autoCodeSplitting: true })
```

This watches `src/routes/` and auto-generates `src/routeTree.gen.ts`.

## Development Server

```bash
npm run dev     # Start dev server (default: http://localhost:3000)
npm run build   # Production build to .output/
npm run serve   # Preview the production build
```

In production, run the Nitro output directly: `node .output/server/index.mjs` (or `bun --bun .output/server/index.mjs` on Bun). See `hosting-and-deployment.md` for preset matrix.
