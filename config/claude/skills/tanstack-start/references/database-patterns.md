# TanStack Start — Database Patterns

## Core Pattern: DB Access via Server Functions

The only way to access a database in TanStack Start is through server functions (or server routes). Database clients must live in `.server.ts` files.

```typescript
// src/db/client.server.ts — NEVER imported on client
import { PrismaClient } from '@prisma/client'

declare global {
  var __prisma: PrismaClient | undefined
}

// Reuse in development to avoid connection exhaustion
export const db = globalThis.__prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== 'production') globalThis.__prisma = db
```

## File Organization

```
src/
  db/
    client.server.ts     # DB client (server-only)
    schema.prisma        # Prisma schema
  features/
    posts/
      queries.server.ts  # DB query helpers (server-only)
      functions.ts       # Server functions (isomorphic entry, calls server-only code)
      schemas.ts         # Zod schemas (shared, isomorphic)
```

## Recommended Database Providers

### Neon (Serverless Postgres)

Best for serverless deployments (Cloudflare, Vercel, Netlify).

```bash
npm install @neondatabase/serverless drizzle-orm drizzle-kit
```

```typescript
// src/db/client.server.ts
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'
import * as schema from './schema'

const sql = neon(process.env.DATABASE_URL!)
export const db = drizzle(sql, { schema })
```

```typescript
// src/db/schema.ts
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core'

export const posts = pgTable('posts', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  title: text('title').notNull(),
  content: text('content').notNull(),
  published: boolean('published').default(false),
  createdAt: timestamp('created_at').defaultNow(),
})
```

### Prisma + Postgres

Traditional ORM for complex schemas.

```bash
npm install prisma @prisma/client
npx prisma init
```

```typescript
// src/db/client.server.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient }
export const db = globalForPrisma.prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db
```

### Convex

Real-time database with built-in server functions.

```bash
npm install convex
npx convex dev
```

```typescript
// convex/posts.ts
import { query, mutation } from './_generated/server'
import { v } from 'convex/values'

export const list = query({
  handler: async (ctx) => ctx.db.query('posts').collect(),
})

export const create = mutation({
  args: { title: v.string(), content: v.string() },
  handler: async (ctx, args) => ctx.db.insert('posts', args),
})
```

```typescript
// Use in TanStack Start server functions
export const getPostsFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    return await fetchQuery(api.posts.list)
  })
```

### Drizzle + Turso (SQLite Edge)

Good for Cloudflare Workers.

```bash
npm install drizzle-orm @libsql/client drizzle-kit
```

```typescript
// src/db/client.server.ts
import { createClient } from '@libsql/client'
import { drizzle } from 'drizzle-orm/libsql'

export const db = drizzle(
  createClient({ url: process.env.TURSO_URL!, authToken: process.env.TURSO_TOKEN! })
)
```

## CRUD Server Functions Pattern

```typescript
// src/features/posts/functions.ts
import { createServerFn } from '@tanstack/react-start'
import { zodValidator } from '@tanstack/zod-adapter'
import { z } from 'zod'
import { db } from '../../db/client.server'
import { posts } from '../../db/schema'
import { eq } from 'drizzle-orm'

export const getPostsFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    return await db.select().from(posts).orderBy(posts.createdAt)
  })

export const getPostFn = createServerFn({ method: 'GET' })
  .validator(zodValidator(z.object({ id: z.string() })))
  .handler(async ({ data }) => {
    const [post] = await db.select().from(posts).where(eq(posts.id, data.id))
    if (!post) throw notFound()
    return post
  })

export const createPostFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(z.object({
    title: z.string().min(1),
    content: z.string().min(1),
  })))
  .handler(async ({ data }) => {
    const [post] = await db.insert(posts).values(data).returning()
    return post
  })

export const updatePostFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(z.object({
    id: z.string(),
    title: z.string().min(1).optional(),
    content: z.string().min(1).optional(),
  })))
  .handler(async ({ data: { id, ...update } }) => {
    const [post] = await db.update(posts).set(update).where(eq(posts.id, id)).returning()
    return post
  })

export const deletePostFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(z.object({ id: z.string() })))
  .handler(async ({ data }) => {
    await db.delete(posts).where(eq(posts.id, data.id))
    return { success: true }
  })
```

## Transactions

```typescript
export const transferFundsFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(z.object({
    fromId: z.string(),
    toId: z.string(),
    amount: z.number().positive(),
  })))
  .handler(async ({ data }) => {
    return await db.transaction(async (tx) => {
      await tx.update(accounts)
        .set({ balance: sql`balance - ${data.amount}` })
        .where(eq(accounts.id, data.fromId))

      await tx.update(accounts)
        .set({ balance: sql`balance + ${data.amount}` })
        .where(eq(accounts.id, data.toId))
    })
  })
```

## Connection Pooling for Serverless

For serverless environments, use PgBouncer or connection poolers:

```typescript
// Neon handles this automatically with @neondatabase/serverless
// For Prisma + serverless:
export const db = new PrismaClient({
  datasourceUrl: process.env.DATABASE_URL_POOLED,  // PgBouncer URL
})
```
