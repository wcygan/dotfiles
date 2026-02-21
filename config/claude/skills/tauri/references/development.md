---
title: Development & Configuration
description: Config files, platform overrides, resources/assets, state management, icons, dev workflow
tags: [configuration, tauri-conf, cargo-toml, resources, state, icons, development]
---

# Development & Configuration

## Configuration Files

Three primary config files: `tauri.conf.json`, `Cargo.toml`, and `package.json`.

### tauri.conf.json

Supported formats: JSON (default), JSON5, TOML (via feature flags).

**Enable JSON5:**

```toml
# Cargo.toml
[build-dependencies]
tauri-build = { version = "2.0.0", features = ["config-json5"] }

[dependencies]
tauri = { version = "2.0.0", features = ["config-json5"] }
```

**Example configuration:**

```json
{
  "build": {
    "devUrl": "http://localhost:5173",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../build"
  },
  "bundle": {
    "active": true,
    "icon": ["icons/app.png"]
  },
  "app": {
    "windows": [
      {
        "title": "MyApp"
      }
    ]
  },
  "plugins": {}
}
```

### Platform-Specific Overrides

Tauri merges platform-specific files using JSON Merge Patch (RFC 7396). Arrays are **replaced**, not merged.

Filenames:
- `tauri.linux.conf.json` / `Tauri.linux.toml`
- `tauri.windows.conf.json` / `Tauri.windows.toml`
- `tauri.macos.conf.json` / `Tauri.macos.toml`
- `tauri.android.conf.json` / `Tauri.android.toml`
- `tauri.ios.conf.json` / `Tauri.ios.toml`

### CLI Config Extension

Build variants without duplicating full config:

```bash
npm run tauri build -- --config src-tauri/tauri.beta.conf.json
```

```json
{
  "productName": "My App Beta",
  "identifier": "com.myorg.myappbeta"
}
```

### Cargo.toml

```toml
[package]
name = "app"
version = "0.1.0"
description = "A Tauri App"
edition = "2021"
rust-version = "1.57"

[build-dependencies]
tauri-build = { version = "2.0.0" }

[dependencies]
serde_json = "1.0"
serde = { version = "1.0", features = ["derive"] }
tauri = { version = "2.0.0", features = [] }
```

`tauri dev` and `tauri build` automatically manage required Cargo features based on `tauri.conf.json`.

### package.json

```json
{
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "tauri": "tauri"
  },
  "dependencies": {
    "@tauri-apps/api": "^2.0.0",
    "@tauri-apps/cli": "^2.0.0"
  }
}
```

The `"tauri"` script entry is required only when using npm.

## Resources / Assets

Resources are additional files bundled with the app, stored in `$RESOURCE/` with preserved directory structure.

### Array Syntax

```json
{
  "bundle": {
    "resources": [
      "./path/to/file.txt",
      "some-folder/",
      "resources/**/*.md"
    ]
  }
}
```

### Object Syntax (Fine Control)

```json
{
  "bundle": {
    "resources": {
      "resources/": "",
      "docs/**/*md": "website-docs/"
    }
  }
}
```

### Resolving Resource Paths

**Rust:**

```rust
let resource_path = app.path().resolve("lang/de.json", BaseDirectory::Resource)?;
let json = std::fs::read_to_string(&resource_path).unwrap();
```

**JavaScript (requires FS plugin + permissions):**

```javascript
import { resolveResource } from '@tauri-apps/api/path';
import { readTextFile } from '@tauri-apps/plugin-fs';

const resourcePath = await resolveResource('lang/de.json');
const content = JSON.parse(await readTextFile(resourcePath));
```

**Required permissions:**

```json
{
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    "fs:allow-resource-read-recursive"
  ]
}
```

### Resource Scoping

```json
{
  "identifier": "fs:scope",
  "allow": ["$RESOURCE/**/*"],
  "deny": ["$RESOURCE/secret.txt"]
}
```

## State Management

### Basic Setup

```rust
use tauri::{Builder, Manager};

struct AppData {
    welcome_message: &'static str,
}

fn main() {
    Builder::default()
        .setup(|app| {
            app.manage(AppData { welcome_message: "Welcome!" });
            Ok(())
        })
        .run(tauri::generate_context!())
        .unwrap()
}
```

### Thread Safety / Interior Mutability

Tauri wraps state in `Arc` internally — no `Arc` needed. Use `Mutex` for mutable state:

```rust
use std::sync::Mutex;

#[derive(Default)]
struct AppState {
    counter: u32,
}

fn main() {
    Builder::default()
        .setup(|app| {
            app.manage(Mutex::new(AppState::default()));
            Ok(())
        })
        .run(tauri::generate_context!())
        .unwrap()
}
```

### Accessing State in Commands

**Synchronous:**

```rust
#[tauri::command]
fn increase_counter(state: State<'_, Mutex<AppState>>) -> u32 {
    let mut state = state.lock().unwrap();
    state.counter += 1;
    state.counter
}
```

**Async (must return Result):**

```rust
#[tauri::command]
async fn increase_counter(state: State<'_, Mutex<AppState>>) -> Result<u32, ()> {
    let mut state = state.lock().unwrap(); // use std::sync::Mutex in async
    state.counter += 1;
    Ok(state.counter)
}
```

### Accessing State Outside Commands

```rust
use tauri::{Window, WindowEvent, Manager};

fn on_window_event(window: &Window, _event: &WindowEvent) {
    let state = window.app_handle().state::<Mutex<AppState>>();
    let mut state = state.lock().unwrap();
    state.counter += 1;
}
```

### Async Mutex Guidance

Prefer `std::sync::Mutex` in async code. Only use `tokio::sync::Mutex` when holding the lock across `.await` points (e.g., database connections).

### Type Safety Note

Mismatched state types cause **runtime panics**, not compile errors. Use type aliases:

```rust
type AppState = Mutex<AppStateInner>;
```

## App Icons

### Generate Icons

```bash
npm run tauri icon          # uses ./app-icon.png
npm run tauri icon my.png   # custom source
npm run tauri icon -o out/  # custom output dir
```

Start with at least 1024x1024 PNG or SVG source.

### Configuration

```json
{
  "bundle": {
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

### Platform Requirements

| Platform | Format | Notes |
|----------|--------|-------|
| macOS | `icon.icns` | Application bundle icon |
| Windows | `icon.ico` | 16, 24, 32, 48, 64, 256px layers |
| Linux | `*.png` | Multiple size variants |
| iOS | PNG (no transparency) | Specific sizes required |
| Android | PNG (with transparency) | Density-specific sizes |

## Mobile Development

```bash
npx tauri android dev
npx tauri ios dev
npx tauri ios dev 'iPhone 15'
```

For iOS physical device, the frontend must listen on `TAURI_DEV_HOST`:

```javascript
import { defineConfig } from 'vite';
const host = process.env.TAURI_DEV_HOST;

export default defineConfig({
  clearScreen: false,
  server: {
    host: host || false,
    port: 1420,
    strictPort: true,
    hmr: host ? { protocol: 'ws', host, port: 1421 } : undefined,
  },
});
```

The `--open` flag launches Xcode or Android Studio instead of simulator/device deployment.

## Further Reading

- https://v2.tauri.app/develop/
- https://v2.tauri.app/develop/configuration-files/
- https://v2.tauri.app/develop/resources/
- https://v2.tauri.app/develop/state-management/
- https://v2.tauri.app/develop/icons/
