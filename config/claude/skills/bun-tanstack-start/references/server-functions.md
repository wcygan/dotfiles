# Server Functions

`createServerFn` is TanStack Start's RPC primitive. Code inside it never ships to the client.

## Basic pattern

```ts
// src/server/posts.ts
import { createServerFn } from '@tanstack/react-start'
import { z } from 'zod'

export const createPost = createServerFn({ method: 'POST' })
  .validator(z.object({ title: z.string().min(1) }))
  .handler(async ({ data }) => {
    const post = await db.post.create({ data })
    return post
  })
```

Call from any component or loader:

```ts
const post = await createPost({ data: { title: 'Hello' } })
```

## Method choice

- `GET` — readable, cacheable, loader-friendly
- `POST` — mutations, anything with side effects (default choice for writes)

## Middleware

```ts
import { createMiddleware } from '@tanstack/react-start'

const authMiddleware = createMiddleware().server(async ({ next }) => {
  const user = await getUser()
  if (!user) throw new Response('Unauthorized', { status: 401 })
  return next({ context: { user } })
})

export const updateProfile = createServerFn({ method: 'POST' })
  .middleware([authMiddleware])
  .handler(async ({ context, data }) => {
    return db.user.update({ where: { id: context.user.id }, data })
  })
```

## Gotchas

- Do not import server-only modules (filesystem, database client) from a route component's top level. Either wrap in `createServerFn` or use a loader.
- Validators run on both client and server (bundling-time) — keep them pure and dependency-light.
- Thrown `Response` objects propagate as HTTP responses; thrown `Error`s become 500s.
