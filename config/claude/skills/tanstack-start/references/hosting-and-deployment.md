# TanStack Start — Hosting & Deployment

## Cloudflare Workers / Pages

### Install

```bash
npm install --save-dev @cloudflare/vite-plugin
```

### app.config.ts

```typescript
import { defineConfig } from '@tanstack/react-start/config'
import { cloudflare } from '@cloudflare/vite-plugin'

export default defineConfig({
  vite: {
    plugins: [
      cloudflare(),
    ],
  },
})
```

### wrangler.jsonc

```jsonc
{
  "name": "my-app",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "pages_build_output_dir": ".output/public",
  "kv_namespaces": [
    { "binding": "MY_KV", "id": "..." }
  ],
  "vars": {
    "APP_URL": "https://my-app.pages.dev"
  }
}
```

### Deploy

```bash
npm run build
npx wrangler pages deploy
```

### Access Cloudflare Bindings

```typescript
import { getCloudflareContext } from '@cloudflare/vite-plugin/cloudflare-context'

export const getKvFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    const { env } = getCloudflareContext()
    return await env.MY_KV.get('key')
  })
```

---

## Netlify

### Install

```bash
npm install --save-dev @netlify/vite-plugin-tanstack-start
```

### app.config.ts

```typescript
import { defineConfig } from '@tanstack/react-start/config'
import netlify from '@netlify/vite-plugin-tanstack-start'

export default defineConfig({
  vite: {
    plugins: [netlify()],
  },
})
```

### netlify.toml

```toml
[build]
  command = "npm run build"
  publish = ".output/public"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/*"
  to = "/.netlify/functions/server"
  status = 200
```

### Deploy

```bash
npm run build
netlify deploy --prod
```

---

## Vercel

### Install

```bash
npm install --save-dev nitropack
```

### app.config.ts

```typescript
import { defineConfig } from '@tanstack/react-start/config'
import nitro from '@tanstack/react-start/plugin/nitro'

export default defineConfig({
  vite: {
    plugins: [
      nitro({ preset: 'vercel' }),
    ],
  },
})
```

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".output/public"
}
```

Deploy via Vercel dashboard (auto-detects from vercel.json) or:

```bash
npx vercel deploy
```

---

## Railway

Railway auto-detects TanStack Start via Nitro. No special configuration required.

### Procfile (optional)

```
web: node .output/server/index.mjs
```

### Environment Variables

Set in Railway dashboard:
- `DATABASE_URL`
- `SESSION_SECRET`
- `PORT` (Railway provides this automatically)

---

## Node.js / Docker

### Build

```bash
npm run build
# Output: .output/server/index.mjs
```

### Dockerfile

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.output ./.output
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
ENV PORT=3000

CMD ["node", ".output/server/index.mjs"]
```

### docker-compose.yml

```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
      SESSION_SECRET: your-secret-here
    depends_on: [db]
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

---

## Bun

Requires React 19+.

### app.config.ts

```typescript
import { defineConfig } from '@tanstack/react-start/config'
import nitro from '@tanstack/react-start/plugin/nitro'

export default defineConfig({
  vite: {
    plugins: [
      nitro({ preset: 'bun' }),
    ],
  },
})
```

### Run

```bash
npm run build
bun run .output/server/index.mjs
```

---

## Nitro (Generic)

For other deployment targets via Nitro presets:

```typescript
import nitro from '@tanstack/react-start/plugin/nitro'

export default defineConfig({
  vite: {
    plugins: [
      nitro({
        preset: 'aws-lambda',  // or 'azure', 'firebase', 'deno-deploy', etc.
      }),
    ],
  },
})
```

Available presets: `node`, `node-server`, `bun`, `cloudflare-module`, `vercel`, `vercel-edge`, `netlify`, `netlify-edge`, `aws-lambda`, `azure`, `firebase`, `deno-deploy`, `static`

### FastResponse Optimization (Nitro)

```typescript
nitro({
  experimental: {
    openAPI: true,
  },
  // Faster response: send headers before body
  fastResponse: true,
})
```
