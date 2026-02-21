---
title: Getting Started & SvelteKit
description: Project creation, SvelteKit adapter-static setup, project structure, and prerequisites
tags: [getting-started, sveltekit, project-structure, adapter-static, create-tauri-app]
---

# Getting Started & SvelteKit

## Project Creation

```bash
# Recommended
npm create tauri-app@latest

# Alternatives
sh <(curl https://create.tauri.app/sh)
yarn create tauri-app
pnpm create tauri-app
cargo install create-tauri-app --locked
```

## SvelteKit Setup (Required)

Tauri requires SPA mode via `@sveltejs/adapter-static`. SSR/SSG with prerendering won't work because Tauri APIs aren't available during the build phase.

### 1. Install adapter-static

```bash
npm install --save-dev @sveltejs/adapter-static
```

### 2. Configure SvelteKit (`svelte.config.js`)

```javascript
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      fallback: 'index.html',
    }),
  },
};

export default config;
```

The `fallback: 'index.html'` is critical — it enables SPA mode so all routes are handled client-side.

### 3. Disable SSR (`src/routes/+layout.ts`)

```typescript
export const ssr = false;
```

This allows `window`-dependent APIs (like Tauri's `invoke`) to work without client-side guards.

### 4. Configure Tauri (`tauri.conf.json`)

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../build"
  }
}
```

Adapt `npm` to your package manager. The `frontendDist` points to SvelteKit's build output directory.

## Project Structure

```
.
├── package.json
├── svelte.config.js
├── vite.config.ts
├── src/
│   ├── routes/
│   │   ├── +layout.ts          # ssr = false
│   │   └── +page.svelte
│   ├── lib/
│   └── app.html
└── src-tauri/
    ├── Cargo.toml
    ├── Cargo.lock               # commit this
    ├── build.rs                 # must call tauri_build::build()
    ├── tauri.conf.json          # primary config, CLI marker
    ├── src/
    │   ├── lib.rs               # Builder, commands, state, mobile entry
    │   └── main.rs              # desktop entry: app_lib::run()
    ├── capabilities/
    │   └── default.json         # permission bindings
    ├── permissions/             # custom TOML permission definitions
    └── icons/
        ├── icon.png
        ├── icon.icns
        └── icon.ico
```

### Key Files

- **`tauri.conf.json`**: primary config — app identifier, dev server URL, build commands, window settings. Also serves as CLI marker to locate the Rust project.
- **`build.rs`**: must contain `tauri_build::build()` for the build system.
- **`lib.rs`**: Rust code + mobile entry point (`#[cfg_attr(mobile, tauri::mobile_entry_point)]`).
- **`main.rs`**: desktop entry point — calls `app_lib::run()` to share logic with mobile.
- **`capabilities/`**: permission files that control which commands are accessible from JavaScript.

### How It Works

The framework operates like static web hosting: SvelteKit compiles to static files first, then the Rust project bundles those files during compilation. The frontend build is entirely standard — nothing Tauri-specific.

## Development Commands

```bash
# Start dev mode (hot reload + Rust rebuild)
npm run tauri dev

# Build release binary
npm run tauri build

# Generate app icons from source image
npm run tauri icon

# Mobile dev
npx tauri android dev
npx tauri ios dev
npx tauri ios dev 'iPhone 15'
```

### Dev Mode Notes

- `tauri dev` watches `src-tauri/` and rebuilds on changes
- First build is slow (compiling all dependencies); subsequent builds are incremental
- Web Inspector: right-click "Inspect" or `Cmd+Option+I` (macOS) / `Ctrl+Shift+I` (Win/Linux)
- Use `.taurignore` (`.gitignore` syntax) in `src-tauri/` to exclude paths from file watching
- Disable watching with `--no-watch`

### Source Control

- **Commit**: `src-tauri/Cargo.lock`, `src-tauri/Cargo.toml`
- **Exclude**: `src-tauri/target/`

## Further Reading

- https://v2.tauri.app/start/
- https://v2.tauri.app/start/project-structure/
- https://v2.tauri.app/start/frontend/sveltekit/
- https://v2.tauri.app/start/prerequisites/
