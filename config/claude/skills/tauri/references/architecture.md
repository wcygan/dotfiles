---
title: Architecture & Process Model
description: Multi-process architecture, WRY/TAO foundation, crate ecosystem, app size optimization
tags: [architecture, process-model, wry, tao, size, optimization, webview]
---

# Architecture & Process Model

## Multi-Process Architecture

Tauri uses a multi-process architecture (like modern browsers) with two main components:

### Core Process (Rust)

- Application entry point with exclusive OS-level access
- Responsibilities:
  - Create/manage windows, system-tray menus, notifications
  - Route all IPC through a central hub
  - Manage global state (settings, database connections)
  - Intercept, filter, and manipulate IPC messages
- Rust provides memory safety via Ownership without runtime overhead

### WebView Process

- Renders UI through OS-provided WebView libraries
- Executes HTML, CSS, and JavaScript
- **Dynamically linked at runtime** — not bundled, reducing app size significantly
- Platform implementations:
  - **Windows**: Microsoft Edge WebView2
  - **macOS**: WKWebView
  - **Linux**: webkitgtk

### Benefits

1. **Resilience**: component failures don't crash the whole app
2. **Performance**: better multi-core CPU utilization
3. **Isolation**: processes restart independently
4. **Security**: limited permissions per process reduce attack surface

## Foundation Libraries

| Library | Purpose |
|---------|---------|
| **WRY** (Webview Rendering Library) | Cross-platform webview rendering (Windows, macOS, Linux) |
| **TAO** (Application Window Library) | Window creation and management (desktop + iOS + Android) |

## Core Crates

| Crate | Function |
|-------|----------|
| `tauri` | Central crate — runtimes, macros, utilities, config, script injection, API hosting |
| `tauri-runtime` | Glue layer between Tauri and webview libraries |
| `tauri-macros` | Generates context, handler, and command macros |
| `tauri-utils` | Shared utilities — config parsing, CSP injection, asset management |
| `tauri-build` | Build-time macro application |
| `tauri-codegen` | Embeds/hashes assets; parses config at compile time |
| `tauri-runtime-wry` | System-level interactions (printing, monitor detection) |

## Tooling Ecosystem

- **JavaScript/TypeScript API** (`@tauri-apps/api`): typed frontend-backend communication
- **Bundler**: cross-platform app builder for macOS, Windows, Linux
- **CLI**: both Rust (`cli.rs`) and JavaScript (`cli.js`) CLIs
- **create-tauri-app**: scaffolding tool
- **Plugin Architecture**: extensibility through Rust/JavaScript plugin pairs

## Message-Passing IPC

All communication between frontend and backend uses **asynchronous message passing**. Messages are serialized and routed through the Core process, which can reject malicious requests before execution. This is safer than shared memory or direct function access.

Two primitives:
- **Commands** (`invoke`): request-response pattern, like `fetch`
- **Events**: fire-and-forget, unidirectional

## App Size Optimization

### Cargo Profile (`src-tauri/Cargo.toml`)

**Stable toolchain:**

```toml
[profile.dev]
incremental = true

[profile.release]
codegen-units = 1
lto = true
opt-level = "s"
panic = "abort"
strip = true
```

**Nightly toolchain (additional):**

```toml
[profile.release]
trim-paths = "all"
rustflags = ["-Cdebuginfo=0", "-Zthreads=8"]
```

### Settings Explained

| Setting | Purpose |
|---------|---------|
| `codegen-units = 1` | Better LLVM optimization (slower compile) |
| `lto = true` | Link-time optimization across crate boundaries |
| `opt-level = "s"` | Optimize for size (`"s"` > `"z"` > `"3"` for size/perf tradeoff) |
| `panic = "abort"` | Remove unwinding machinery |
| `strip = true` | Remove debug symbols |
| `trim-paths = "all"` | Remove path info (nightly only) |

### Remove Unused Commands (Tauri 2.4+)

```json
{
  "build": {
    "removeUnusedCommands": true
  }
}
```

Eliminates commands not permitted in capability files. Best results when specifying individual commands rather than using defaults in ACL configuration.

Requires: `tauri@2.4`, `tauri-build@2.1`, `tauri-plugin@2.1`, `tauri-cli@2.4`.

### Security Advantage of System WebView

Tauri deliberately does not bundle a WebView. OS WebView maintainers deploy security patches faster than individual developers bundling Chromium. This trades some developer convenience for reduced vulnerability exposure and dramatically smaller app size.

## Licensing

MIT or Apache-2.0.

## Further Reading

- https://v2.tauri.app/concept/architecture/
- https://v2.tauri.app/concept/process-model/
- https://v2.tauri.app/concept/size/
- https://v2.tauri.app/concept/
