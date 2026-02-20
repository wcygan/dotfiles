# TanStack Start — Import Protection

Import protection prevents server-only code from leaking into the client bundle and vice versa.

## Automatic File Patterns

TanStack Start automatically enforces these patterns:

| Pattern | Client behavior | Server behavior |
|---------|----------------|-----------------|
| `*.server.*` | Build error | Allowed |
| `*.client.*` | Allowed | Build error |
| Imports from `@tanstack/react-start/server` | Build error | Allowed |

```typescript
// db.server.ts — automatically blocked on client
import { PrismaClient } from '@prisma/client'
export const db = new PrismaClient()

// analytics.client.ts — automatically blocked on server
import mixpanel from 'mixpanel-browser'
export const track = (event: string) => mixpanel.track(event)
```

## File Markers (Explicit)

Add explicit markers at the top of files:

```typescript
// Force server-only
import '@tanstack/react-start/server-only'

// Force client-only
import '@tanstack/react-start/client-only'
```

These throw a build error if imported from the wrong environment.

## Behavior Modes

```typescript
// app.config.ts
export default defineConfig({
  tsr: {
    importProtection: {
      // 'error': Build error (default for production)
      // 'mock': Replace with empty module (useful for dev)
      mode: 'error',
    },
  },
})
```

## Custom Deny Rules

```typescript
export default defineConfig({
  tsr: {
    importProtection: {
      customDenyRules: [
        // Prevent server DB client from reaching client bundle
        {
          pattern: '@prisma/client',
          target: 'client',
          message: 'Prisma must only be used in server functions',
        },
        // Prevent file pattern
        {
          pattern: /\.server\.(ts|js)$/,
          target: 'client',
        },
      ],
    },
  },
})
```

## onViolation Callback

```typescript
export default defineConfig({
  tsr: {
    importProtection: {
      onViolation: ({ importedId, importer, target }) => {
        console.error(`Import violation: ${importedId} imported in ${target} bundle from ${importer}`)
        // Can throw to fail build, or log to monitoring
      },
    },
  },
})
```

## Scoping / Exclusions

```typescript
export default defineConfig({
  tsr: {
    importProtection: {
      exclude: [
        // Allow specific files to bypass protection
        '**/test/**',
        '**/mocks/**',
      ],
    },
  },
})
```

## Common Pitfalls

### ❌ Side-effect imports survive tree shaking

```typescript
// WRONG: Even if you don't use db, the import keeps the module alive
import { db } from './db.server'

// The db.server module is in the client bundle because it was imported
// even if all exports are tree-shaken
```

### ❌ Re-exports bypass pattern matching

```typescript
// utils.ts (no .server suffix)
export { db } from './db.server'  // Re-exports bypass automatic protection

// CORRECT: Use explicit marker
import '@tanstack/react-start/server-only'
export { db } from './db.server'
```

### ✅ Correct pattern for shared utilities

```typescript
// src/utils/format.ts — safe for both environments
export function formatDate(date: Date) { ... }

// src/utils/db.server.ts — server-only
import '@tanstack/react-start/server-only'
export async function queryDB(sql: string) { ... }
```

## Full Configuration Reference

```typescript
export default defineConfig({
  tsr: {
    importProtection: {
      mode: 'error' | 'mock',
      customDenyRules: Array<{
        pattern: string | RegExp,
        target: 'client' | 'server',
        message?: string,
      }>,
      exclude: string[],
      onViolation?: (info: {
        importedId: string,
        importer: string,
        target: 'client' | 'server',
      }) => void,
    },
  },
})
```
