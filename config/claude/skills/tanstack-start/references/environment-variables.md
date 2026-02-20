# TanStack Start — Environment Variables

## VITE_ Prefix for Client-Accessible Vars

Variables prefixed with `VITE_` are embedded into the client bundle at build time.

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_NAME=My App
DATABASE_URL=postgresql://...  # Server-only (no VITE_ prefix)
SESSION_SECRET=...              # Server-only
```

```typescript
// In any file (client or server)
const apiUrl = import.meta.env.VITE_API_URL

// Server-only (process.env)
const dbUrl = process.env.DATABASE_URL
```

## .env File Hierarchy

Files are loaded in order (later files override earlier):

```
.env                    # Base defaults (committed to repo, no secrets)
.env.development        # Dev-only overrides
.env.production         # Production overrides
.env.local              # Machine-local overrides (gitignored)
.env.development.local  # Machine-local dev overrides (gitignored)
.env.production.local   # Machine-local prod overrides (gitignored)
```

### .gitignore

```
.env.local
.env.*.local
```

## Type Safety

### src/env.d.ts

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_STRIPE_PUBLIC_KEY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// Node.js process.env types
declare namespace NodeJS {
  interface ProcessEnv {
    DATABASE_URL: string
    SESSION_SECRET: string
    STRIPE_SECRET_KEY: string
    NODE_ENV: 'development' | 'production' | 'test'
  }
}
```

## Runtime Validation with Zod

```typescript
// src/env.ts (server-only, imported with *.server.ts pattern)
import { z } from 'zod'

const serverEnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  SESSION_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
})

const clientEnvSchema = z.object({
  VITE_API_URL: z.string().url().optional(),
  VITE_APP_NAME: z.string().default('My App'),
})

export const env = serverEnvSchema.parse(process.env)
export const clientEnv = clientEnvSchema.parse(import.meta.env)
```

## Runtime Client Env Vars via Server Functions

When you need client env vars that can't be known at build time:

```typescript
export const getClientConfigFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    return {
      apiUrl: process.env.API_URL,  // Set at runtime, not build time
      featureFlags: JSON.parse(process.env.FEATURE_FLAGS ?? '{}'),
    }
  })

// Load in root loader
export const Route = createRootRouteWithContext()({
  loader: async () => {
    return { config: await getClientConfigFn() }
  },
})
```

## Static NODE_ENV Replacement

```typescript
// In Vite config, NODE_ENV is statically replaced in server builds
// Use this for dead code elimination
if (process.env.NODE_ENV === 'development') {
  // This code is removed in production builds
  console.log('Debug mode')
}
```

## Platform-Specific Runtime Vars

### Cloudflare Workers (Bindings)

```typescript
// Cloudflare uses bindings, not process.env
export const getDataFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    const { env } = getCloudflareContext()
    const data = await env.MY_KV.get('key')  // KV binding
    const secret = env.SECRET_VALUE           // Secret binding
    return data
  })
```

### Vercel / Netlify

Environment variables set in dashboard are available via `process.env` in server code and via `VITE_` prefix for client code.

## Common Gotchas

1. **VITE_ vars are baked in at build time** — changing them requires a rebuild
2. **process.env in client code is undefined** — always use `import.meta.env`
3. **Don't use VITE_ for secrets** — they appear in the client bundle
4. **.env.local is gitignored by default** — each developer needs their own
5. **Env vars in server functions are evaluated at request time** — safe for secrets
6. **TypeScript won't error on missing env vars** — use runtime validation (Zod)

## Example: Full Setup

```bash
# .env (committed — no secrets)
VITE_APP_NAME=My TanStack App
VITE_API_BASE_URL=http://localhost:3000

# .env.local (gitignored — machine secrets)
DATABASE_URL=postgresql://user:pass@localhost/mydb
SESSION_SECRET=development-secret-at-least-32-chars
STRIPE_SECRET_KEY=sk_test_...
```

```typescript
// src/env.server.ts — validate on startup
import { z } from 'zod'

export const env = z.object({
  DATABASE_URL: z.string(),
  SESSION_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().optional(),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
}).parse(process.env)
```
