# TanStack Start — Project Setup

## CLI Scaffold (Recommended)

```bash
npx create @tanstack/start@latest my-app
cd my-app
npm install
npm run dev
```

## Manual Setup

### package.json

```json
{
  "scripts": {
    "dev": "vinxi dev",
    "build": "vinxi build",
    "start": "vinxi start"
  },
  "dependencies": {
    "@tanstack/react-start": "latest",
    "@tanstack/react-router": "latest",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "vinxi": "latest"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.0.0",
    "vite": "^6.0.0"
  }
}
```

### app.config.ts (Vite Config)

```typescript
import { defineConfig } from '@tanstack/react-start/config'
import viteTsConfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  vite: {
    plugins: [
      // NOTE: viteReact() is added automatically by tanstackStart()
      // Do NOT manually add it before tanstackStart()
      viteTsConfigPaths(),
    ],
  },
  // Optional: SSR options
  routers: {
    ssr: {
      entry: './src/ssr.tsx',
    },
    client: {
      entry: './src/client.tsx',
    },
  },
})
```

> **Critical**: If adding `@vitejs/plugin-react`, it MUST come AFTER `tanstackStart()` in the plugin order, or use `defineConfig` which handles this automatically.

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
npm run build   # Production build
npm run start   # Start production server
```
