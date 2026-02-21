---
name: tauri
description: Tauri v2 + SvelteKit desktop/mobile app expert. Auto-loads when working with Tauri commands, tauri.conf.json, src-tauri/, #[tauri::command], invoke(), IPC, Tauri plugins, capabilities, permissions, WRY, TAO, tauri::Builder, tauri::State, Tauri events, channels, WebviewWindow, AppHandle, tauri-driver, or Tauri security patterns.
---

# Tauri v2 + SvelteKit

Tauri is a framework for building tiny, fast desktop and mobile apps. It combines a Rust backend (Core Process) with a frontend rendered in the OS's native webview — no bundled browser engine. Apps start under 600KB. We always use **SvelteKit** with `adapter-static` (SPA mode, `ssr = false`).

## Architecture Overview

```
SvelteKit Frontend (WebView)
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
- **WebView Process**: renders SvelteKit app using system webview (WKWebView/Edge WebView2/webkitgtk)
- **IPC**: message-passing via commands (`invoke`) and events — all routed through Core

## Project Structure

```
├── package.json
├── svelte.config.js          # adapter-static, fallback: 'index.html'
├── src/
│   ├── routes/
│   │   └── +layout.ts        # export const ssr = false
│   └── ...
└── src-tauri/
    ├── Cargo.toml
    ├── tauri.conf.json        # devUrl, frontendDist, app config
    ├── build.rs               # must call tauri_build::build()
    ├── src/
    │   ├── lib.rs             # Builder, commands, state
    │   └── main.rs            # desktop entry point
    ├── capabilities/
    │   └── default.json       # permission bindings per window
    ├── permissions/            # custom TOML permission definitions
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

## SvelteKit Setup Essentials

```js
// svelte.config.js
import adapter from '@sveltejs/adapter-static';
export default { kit: { adapter: adapter({ fallback: 'index.html' }) } };
```

```ts
// src/routes/+layout.ts
export const ssr = false;
```

```json
// tauri.conf.json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../build"
  }
}
```

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

- [Getting Started & SvelteKit](references/getting-started.md) — project creation, SvelteKit adapter-static setup, project structure
- [Architecture & Process Model](references/architecture.md) — multi-process design, WRY/TAO, crate ecosystem, size optimization
- [Inter-Process Communication](references/ipc.md) — commands, events, channels, brownfield vs isolation patterns
- [Security & Permissions](references/security.md) — capabilities, permissions, scopes, CSP, security lifecycle
- [Commands & Events](references/commands-and-events.md) — calling Rust from frontend, calling frontend from Rust, streaming
- [Development & Configuration](references/development.md) — config files, resources, state management, icons, dev workflow
- [Testing](references/testing.md) — IPC mocking, event mocking, window mocking, WebDriver, tauri-driver
