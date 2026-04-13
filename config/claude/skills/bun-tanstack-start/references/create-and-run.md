# Create and Run

## Scaffold

```sh
bunx @tanstack/cli create my-app
cd my-app
bun install
```

Prefer `bunx` over `npx` so the scaffolder itself runs on Bun. Do not use `create-vite` + manual TanStack Start wiring — the CLI sets up Nitro, route tree generation, and dev-server HMR correctly.

## Force Bun as the runtime

Bun will happily launch and then delegate execution to Node for tooling that spawns subprocesses. The `--bun` flag forces Bun end-to-end.

Patch `package.json`:

```json
{
  "scripts": {
    "dev":   "bun --bun vite dev",
    "build": "bun --bun vite build",
    "serve": "bun --bun vite preview",
    "start": "bun --bun node .output/server/index.mjs"
  }
}
```

Check: `bun run dev` prints a Vite banner. Then `ps` should show `bun` as the parent, not `node`.

## Run

```sh
bun run dev     # dev with HMR
bun run build   # build to .output/
bun run serve   # preview the production build
```

## When `bunx` is not available

Older Bun versions use `bun x`. If the user has < 1.1, upgrade first: `curl -fsSL https://bun.sh/install | bash`.

## Gotchas

- `bun install` is faster than `npm install` but some native deps (`sharp`, `better-sqlite3`) may need fallback to `npm install --prefix` — diagnose per-case, don't blanket-switch.
- Do not commit `bun.lockb` *and* `package-lock.json`. Delete the npm lockfile; Bun's is authoritative.
- `bunfig.toml` is optional — add only when you need custom install/telemetry flags.

## Canonical source

https://bun.com/docs/guides/ecosystem/tanstack-start
