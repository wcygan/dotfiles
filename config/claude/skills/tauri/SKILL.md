---
name: tauri
description: Tauri v2 + Bun + TanStack Start (SPA mode) desktop/mobile app expert. Auto-loads when working with Tauri commands, tauri.conf.json, src-tauri/, #[tauri::command], invoke(), IPC, Tauri plugins, capabilities, permissions, WRY, TAO, tauri::Builder, tauri::State, Tauri events, channels, WebviewWindow, AppHandle, tauri-driver, Tauri security patterns, frontendDist, bunx tauri, bun --bun, or TanStack Start SPA mode for a Tauri webview.
---

# Tauri v2 + Bun + TanStack Start

Tauri is a framework for building tiny, fast desktop and mobile apps. It combines a Rust backend (Core Process) with a frontend rendered in the OS's native webview — no bundled browser engine. Apps start under 600KB.

This skill assumes **Bun + TanStack Start in SPA mode**. Tauri loads a static frontend bundle at runtime, so SSR/Nitro is disabled. For framework wiring (Vite plugin order, Tailwind v4, `__root.tsx`), see the `bun-tanstack-start` skill. **Server functions / loaders / Effect TS guidance from that skill do not apply here**: there is no Nitro server in a Tauri app. All "backend" work happens in Rust via Tauri commands.

## Architecture Overview

```
TanStack Start Frontend (WebView, SPA, static)
      │  invoke() / events / channels
      ▼
┌─────────────────────────┐
│  Tauri Core Process     │  Rust — owns OS access, state, IPC routing
│  (tauri::Builder)       │
└─────────────────────────┘
      │
      ├── WRY: cross-platform webview rendering
      └── TAO: window creation & management
```

- **Core Process (Rust)**: entry point, OS access, state, IPC hub, security enforcement
- **WebView Process**: renders the prebuilt TanStack Start SPA using system webview (WKWebView/Edge WebView2/webkitgtk)
- **IPC**: message-passing via commands (`invoke`) and events — all routed through Core

## Project Structure

```
├── package.json                  # bun --bun vite scripts
├── vite.config.ts                # tsConfigPaths → tanstackStart({ spa }) → viteReact → tailwindcss
├── src/
│   ├── routes/
│   │   ├── __root.tsx            # links app.css via ?url import
│   │   └── index.tsx             # createFileRoute('/')
│   └── styles/
│       └── app.css               # @import 'tailwindcss' source('../')
└── src-tauri/
    ├── Cargo.toml
    ├── tauri.conf.json           # devUrl, frontendDist, app config
    ├── build.rs                  # must call tauri_build::build()
    ├── src/
    │   ├── lib.rs                # Builder, commands, state
    │   └── main.rs               # desktop entry point
    ├── capabilities/
    │   └── default.json          # permission bindings per window
    ├── permissions/              # custom TOML permission definitions
    └── icons/
```

## Quick Command Reference

| Rust API | Purpose |
|----------|---------|
| `#[tauri::command]` | Define a command callable from frontend |
| `tauri::generate_handler![cmd1, cmd2]` | Register commands with Builder |
| `tauri::Builder::default().manage(state)` | Register managed state |
| `State<'_, T>` | Access managed state in commands |
| `AppHandle` | Access app handle in commands |
| `WebviewWindow` | Access calling window in commands |
| `tauri::ipc::Channel<T>` | Stream data to frontend |
| `tauri::ipc::Response` | Return raw bytes efficiently |
| `app.emit("event", payload)` | Emit global event to frontend |
| `app.emit_to("label", "event", payload)` | Emit to specific window |

| JS/TS API (`@tauri-apps/api`) | Purpose |
|-------------------------------|---------|
| `invoke('cmd', { args })` | Call a Rust command |
| `listen('event', handler)` | Listen for backend events |
| `emit('event', payload)` | Emit event to backend |
| `Channel<T>` | Receive streamed data from Rust |

## TanStack Start Setup Essentials

Tauri requires a **static SPA bundle**. Enable SPA mode on the TanStack Start Vite plugin so there is no Nitro server and the build emits static HTML/JS that Tauri can load from disk.

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
    tanstackStart({ spa: { enabled: true } }), // disables SSR/Nitro for Tauri
    viteReact(),
    tailwindcss(),
  ],
})
```

```json
// src-tauri/tauri.conf.json
{
  "build": {
    "beforeDevCommand": "bun run dev",
    "beforeBuildCommand": "bun run build",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../.output/public"
  }
}
```

The dev port and `frontendDist` path are the only Tauri-specific knobs. See [getting-started](references/getting-started.md) for the full walkthrough including how to verify the actual build-output directory for your TanStack Start version.

## Security Model (Capability-Based)

```
Permissions (TOML) → Capabilities (JSON/TOML) → Runtime Authority
     what ops            bind to windows         enforce at runtime
```

- Frontend is **untrusted** by default — all backend access requires explicit capability grants
- Commands must be listed in capability files to be callable from JS
- Scopes (allow/deny) provide fine-grained resource boundaries
- Isolation pattern adds AES-GCM encrypted IPC for high-security apps

## Release Build Optimization

```toml
# src-tauri/Cargo.toml
[profile.release]
codegen-units = 1
lto = true
opt-level = "s"
panic = "abort"
strip = true
```

## References

- [Getting Started & TanStack Start](references/getting-started.md) — scaffold (Bun + TanStack Start, then add Tauri), SPA-mode wiring, project structure
- [Architecture & Process Model](references/architecture.md) — multi-process design, WRY/TAO, crate ecosystem, size optimization
- [Inter-Process Communication](references/ipc.md) — commands, events, channels, brownfield vs isolation patterns
- [Security & Permissions](references/security.md) — capabilities, permissions, scopes, CSP, security lifecycle
- [Commands & Events](references/commands-and-events.md) — calling Rust from frontend, calling frontend from Rust, streaming
- [Development & Configuration](references/development.md) — config files, resources, state management, icons, dev workflow
- [Testing](references/testing.md) — IPC mocking, event mocking, window mocking, WebDriver, tauri-driver

## Companion Skills

- **`bun-tanstack-start`** — frontend stack reference (Vite plugin order, Tailwind v4, `__root.tsx`). Load whenever touching `src/`, `vite.config.ts`, or `package.json`.
- **`tailwind`** / **`tailwind-v4-tokens`** — styling.
- **`idiomatic-rust`** / **`async-rust`** — Rust side of `src-tauri/`.
