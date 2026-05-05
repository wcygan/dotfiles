---
title: Getting Started & TanStack Start
description: Scaffolding a Bun + TanStack Start frontend, wiring Tauri on top, SPA-mode requirement, project structure, prerequisites
tags: [getting-started, tanstack-start, bun, spa, project-structure, create-tauri-app]
---

# Getting Started & TanStack Start

This skill assumes Bun + TanStack Start as the frontend. The recommended path is **scaffold the frontend first, then add Tauri to it** — `create-tauri-app` does not ship a TanStack Start template.

## 1. Scaffold the TanStack Start frontend

```bash
bunx @tanstack/cli create my-app
cd my-app
bun install
```

Patch `package.json` scripts to force Bun end-to-end (see the `bun-tanstack-start` skill for the rationale):

```json
{
  "scripts": {
    "dev": "bun --bun vite dev",
    "build": "bun --bun vite build",
    "serve": "bun --bun vite preview"
  }
}
```

## 2. Switch the frontend to SPA mode

Tauri loads a **static** frontend bundle at runtime — there is no Nitro server. Enable SPA mode on the TanStack Start Vite plugin so the build emits static HTML/JS:

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import tsConfigPaths from 'vite-tsconfig-paths'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tsConfigPaths(),
    tanstackStart({ spa: { enabled: true } }),
    viteReact(),
    tailwindcss(),
  ],
})
```

Plugin order (`tsConfigPaths → tanstackStart → viteReact → tailwindcss`) is the same as the `bun-tanstack-start` skill.

Why SPA mode: in default (SSR) mode, TanStack Start outputs a Nitro server bundle to `.output/server/` and Tauri has nothing static to load. SPA mode emits a prerendered shell + client bundle into `.output/public/` instead.

## 3. Add Tauri to the project

```bash
bun add -D @tauri-apps/cli
bunx @tauri-apps/cli@latest init
```

Answer the prompts:

- **frontend dev command** → `bun run dev`
- **frontend build command** → `bun run build`
- **dev server URL** → `http://localhost:3000`
- **frontend dist path** → `../.output/public`

After scaffolding, run `bun run build` once and check the actual output directory (`ls .output/` or `ls dist/`) — the dir varies by TanStack Start version. Update `frontendDist` to match if it differs.

Install the JS API:

```bash
bun add @tauri-apps/api
```

## 4. Wire `tauri.conf.json`

```json
{
  "build": {
    "beforeDevCommand": "bun run dev",
    "beforeBuildCommand": "bun run build",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../.output/public"
  }
}
```

## Project Structure

```
.
├── package.json
├── vite.config.ts                # SPA-mode tanstackStart + plugin chain
├── src/
│   ├── routes/
│   │   ├── __root.tsx            # createRootRoute + app.css ?url link
│   │   └── index.tsx             # createFileRoute('/')
│   ├── styles/
│   │   └── app.css               # @import 'tailwindcss' source('../')
│   └── components/
└── src-tauri/
    ├── Cargo.toml
    ├── Cargo.lock                # commit this
    ├── build.rs                  # must call tauri_build::build()
    ├── tauri.conf.json           # primary config, CLI marker
    ├── src/
    │   ├── lib.rs                # Builder, commands, state, mobile entry
    │   └── main.rs               # desktop entry: app_lib::run()
    ├── capabilities/
    │   └── default.json          # permission bindings
    ├── permissions/              # custom TOML permission definitions
    └── icons/
        ├── icon.png
        ├── icon.icns
        └── icon.ico
```

### Key Files

- **`tauri.conf.json`**: primary config — app identifier, dev server URL, build commands, window settings. Also serves as CLI marker to locate the Rust project.
- **`vite.config.ts`**: SPA-mode `tanstackStart`. The single most common failure mode for Tauri + TanStack Start is forgetting `spa: { enabled: true }` and getting a Nitro server bundle that Tauri cannot load.
- **`src/routes/__root.tsx`**: links `app.css` via `?url` import (see `bun-tanstack-start`). Single source of truth for the app shell.
- **`build.rs`**: must contain `tauri_build::build()` for the build system.
- **`lib.rs`**: Rust code + mobile entry point (`#[cfg_attr(mobile, tauri::mobile_entry_point)]`).
- **`main.rs`**: desktop entry point — calls `app_lib::run()` to share logic with mobile.
- **`capabilities/`**: permission files that control which commands are accessible from JavaScript.

### How It Works

The framework operates like static web hosting: TanStack Start (in SPA mode) compiles to static files first, then the Rust project bundles those files during compilation. The frontend build is entirely standard — nothing Tauri-specific.

## Development Commands

```bash
# Start dev mode (hot reload + Rust rebuild)
bun run tauri dev

# Build release binary
bun run tauri build

# Generate app icons from source image
bun run tauri icon
```

For mobile (`bunx tauri android dev` / `bunx tauri ios dev`), see [development.md](development.md#mobile-development).

### Dev Mode Notes

- `tauri dev` watches `src-tauri/` and rebuilds on changes
- First build is slow (compiling all dependencies); subsequent builds are incremental
- Web Inspector: right-click "Inspect" or `Cmd+Option+I` (macOS) / `Ctrl+Shift+I` (Win/Linux)
- Use `.taurignore` (`.gitignore` syntax) in `src-tauri/` to exclude paths from file watching
- Disable watching with `--no-watch`

### Source Control

- **Commit**: `src-tauri/Cargo.lock`, `src-tauri/Cargo.toml`, the Bun lockfile (`bun.lock` on Bun ≥1.2, `bun.lockb` on older)
- **Exclude**: `src-tauri/target/`, `.output/`, `node_modules/`

## Further Reading

- https://v2.tauri.app/start/
- https://v2.tauri.app/start/project-structure/
- https://v2.tauri.app/start/prerequisites/
- https://tanstack.com/start/latest/docs/framework/react/getting-started
- https://tanstack.com/start/latest/docs/framework/react/guide/spa-mode
- https://bun.com/docs/guides/ecosystem/tanstack-start
