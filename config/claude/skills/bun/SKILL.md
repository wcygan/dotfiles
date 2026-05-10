---
name: bun
description: Bun runtime and package manager — `bun --bun` flag rationale, `bunx` vs `npx`, `bun install`, `bun.lockb` lockfile rules, native dep gotchas, and the runtime-vs-package-manager distinction. Auto-loads when `bun.lockb` exists or when scripts use `bun`/`bunx`. Keywords bun, bunx, bun install, bun.lockb, bunfig, bun --bun.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch
---

# Bun

Bun is two things wearing one binary: a **JavaScript runtime** (Node-compatible, faster startup, native TS) and a **package manager / script runner** (drop-in for `npm`/`yarn`/`pnpm`). Most footguns come from confusing the two.

## When to apply this skill

| Signal | Action |
|---|---|
| `bun.lockb` exists in the project | Apply this skill's conventions |
| `package.json` scripts call `bun` or `bunx` | Apply this skill |
| User says "use Bun", "switch to Bun", "scaffold with Bun" | Apply this skill |
| Both `bun.lockb` and `package-lock.json` exist | Flag as a lockfile conflict — see Lockfile rules below |

## The `--bun` flag (the easy-to-miss one)

`bun run <script>` will happily start under Bun and then **delegate execution to Node** for tooling that spawns subprocesses (Vite, webpack, vinxi, esbuild wrappers, anything that does its own `process.argv[0]` introspection). The `--bun` flag forces Bun end-to-end.

Patch `package.json` scripts that wrap a tool you want to keep on Bun:

```json
{
  "scripts": {
    "dev":   "bun --bun vite dev",
    "build": "bun --bun vite build",
    "serve": "bun --bun vite preview"
  }
}
```

**Verify it took effect:** `bun run dev` then `ps -ef | grep -E '(node|bun)'` — the parent should be `bun`, not `node`. If you see `node` as the runtime, the flag is missing.

When you don't need it: pure scripts (`bun run lint`, `bun run test`) where the tool itself runs natively under Bun. The flag is only load-bearing when a wrapped CLI re-exec's into Node.

## `bunx` vs `npx` vs `bun x`

- **`bunx <pkg>`** — current canonical name. Same UX as `npx`, runs on Bun. Prefer this for one-off CLI invocations like scaffolders so the *scaffolder itself* runs on Bun.
- **`bun x <pkg>`** — older Bun (< 1.1) syntax. If `bunx` isn't found, upgrade Bun: `curl -fsSL https://bun.sh/install | bash`.
- **`npx <pkg>`** — works fine, but the spawned tool runs under Node. Use only when a CLI is known-incompatible with Bun.

## Lockfile rules

- `bun.lockb` is **binary** and authoritative. Commit it.
- Do **not** commit both `bun.lockb` and `package-lock.json` (or `pnpm-lock.yaml`, `yarn.lock`). Pick one. If migrating to Bun, delete the others.
- `bun install` is dramatically faster than `npm install` but reads the same `package.json`. There's no separate manifest.
- Reproducible installs in CI: `bun install --frozen-lockfile`.

## Install command

```sh
curl -fsSL https://bun.sh/install | bash
```

Verify: `bun --version`. Bump if you see < 1.1 (you'll lack `bunx`, `--frozen-lockfile`, and other flags this skill assumes).

## Native dep gotchas

Some native packages don't ship Bun-compatible prebuilt binaries:

- **`sharp`** — usually fine on recent Bun, but has had churn. If `bun install sharp` fails with a node-gyp error, fall back per-package: `npm install --prefix . sharp` (keeps Bun for the rest).
- **`better-sqlite3`** — historically rocky; check the project's issue tracker before assuming it works. Bun ships its own `bun:sqlite` built-in — prefer that for new projects.
- **anything with `node-gyp` postinstall** — diagnose per-case. Don't blanket-switch the whole project back to npm.

Diagnostic flow for a failing native install:

1. `bun install <pkg>` → see the actual error.
2. Search the package's GitHub issues for "bun" — usually a known thread.
3. If it's truly broken, `npm install --prefix . <pkg>` adds *just that one* dep via npm without touching Bun for the rest.

## `bunfig.toml` — usually skip it

`bunfig.toml` (project root) is optional. Only add it when you need to:
- Disable telemetry (`telemetry = false`)
- Set a custom registry (`registry = "..."`)
- Tune install cache or lockfile behavior

Most projects don't need one. Don't generate a placeholder.

## Bun built-ins worth knowing

When writing Bun-native code (not Node-compat code), reach for these instead of npm equivalents:

| Need | Bun built-in | npm equivalent it replaces |
|---|---|---|
| SQLite | `bun:sqlite` | `better-sqlite3` |
| Hashing / crypto | `Bun.password`, `Bun.hash` | `bcrypt`, `argon2` for passwords |
| File I/O | `Bun.file()`, `Bun.write()` | `fs/promises` |
| HTTP server | `Bun.serve()` | `express`, `fastify` (if no framework) |
| Test runner | `bun test` | `jest`, `vitest` |
| Env loading | automatic (`.env`, `.env.local`) | `dotenv` |

These only make sense for **Bun-only** code. If the file might run under Node (libraries, edge functions, tests in mixed CI), stick to Node-compat APIs.

## Runtime delegation pitfalls (debugging "why is this Node?")

Symptoms that a tool you thought was on Bun is actually on Node:

- `process.versions.bun` is `undefined` at runtime.
- `ps` shows `node` as the parent of your dev server.
- A package using Bun-only APIs (`Bun.file`, `bun:sqlite`) throws `ReferenceError`.

Causes, in rough order of frequency:

1. Missing `--bun` on the wrapping script.
2. The tool re-exec's via shebang (`#!/usr/bin/env node`) — `--bun` fixes this.
3. A globally-installed CLI was found before the local one — `bunx` instead of running a global.

## Canonical sources

- Bun quickstart: https://bun.com/docs/quickstart
- Bun CLI reference: https://bun.com/docs/cli/run
- Bun + TanStack Start: https://bun.com/docs/guides/ecosystem/tanstack-start

## Complements

- `tanstack-start` skill — TanStack Start framework (with Bun-aware notes in `project-setup.md` and `hosting-and-deployment.md`).
