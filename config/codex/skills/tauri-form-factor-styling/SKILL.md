---
name: tauri-form-factor-styling
description: Use when Codex needs to style, restyle, or review the Tauri Start Demo or a similar Tauri v2 + TanStack Start React app across desktop, tablet/iPad, and mobile phone form factors. Triggers include responsive layout work, mobile styling that looks bad, safe-area or viewport issues, Tauri desktop window constraints, tablet/phone navigation, horizontal overflow, screenshots at multiple viewport sizes, and requests to make a Tauri app look correct on Desktop, iPad, and Mobile.
---

# Tauri Form Factor Styling

## Purpose

Make conservative, testable responsive styling changes for this Tauri/TanStack Start application without turning the app into a redesign project. Preserve the existing routes, panels, design language, and native Tauri window chrome unless the user explicitly asks for a new interaction model.

## Workflow

1. Inspect the app before editing: read `src/styles.css`, `src/routes/__root.tsx`, route components under `src/routes/`, `src-tauri/tauri.conf.json`, `package.json`, and `git status --short`.
2. Read [references/form-factor-checklist.md](references/form-factor-checklist.md) before making CSS, viewport, navigation, or Tauri window-size changes.
3. Prefer small CSS/layout changes over markup rewrites. Keep repeated panels, route files, and runtime logic intact unless the layout cannot be fixed safely in CSS.
4. Use official docs when checking Tauri behavior: start with `https://v2.tauri.app/learn/window-customization/` and `https://v2.tauri.app/reference/webview-versions/`. Avoid custom titlebar or drag-region changes unless the user requested native window customization.
5. Implement mobile-first safeguards that are easy to reason about:
   - Add `viewport-fit=cover` when safe-area padding is used.
   - Use `env(safe-area-inset-*)` for sticky headers and bottom padding.
   - Set `min-width: 0` on shrinkable content and use `overflow-wrap: anywhere` for code/paths.
   - Use stable dimensions for cards, meters, buttons, nav items, and grids so content does not resize the layout.
   - Keep phone navigation compact; do not let a vertical nav consume the first screen.
6. Verify in a real browser at minimum:
   - Phone: `390x844`
   - Tablet/iPad: `768x1024`
   - Desktop: `1280x800`
   - Run a JS overflow check such as `document.documentElement.scrollWidth === document.documentElement.clientWidth`.
7. Run the project checks that match the files changed. For this repo, default to `bun run typecheck`, `bun run lint`, `bun run check`, `bun run test`, `bun run build`, and `cargo check --manifest-path src-tauri/Cargo.toml` when Tauri config or Rust-adjacent behavior changed.

## Styling Rules

- Keep native Tauri window chrome by default. Only touch custom titlebar APIs, `data-tauri-drag-region`, decorations, or window controls when asked.
- Treat Desktop, Tablet, and Phone as layout form factors, not separate apps. Avoid user-agent sniffing.
- Keep desktop dense and work-focused. Use side navigation and multi-column grids where they fit.
- Use a top sticky navigation band on tablet when the desktop sidebar no longer fits.
- Use a compact horizontal phone nav, reduced heading sizes, smaller panel padding, and one-column content on phones.
- Hide development overlays or move them away from content on phone/tablet screenshots when they interfere with the app UI.
- Prefer existing colors, radii, typography, lucide icons, and component classes. Do not introduce decorative backgrounds, marketing-style hero sections, or broad palette shifts for a responsive fix.
- Ensure the first phone viewport shows the app identity, navigation, page title, and meaningful content instead of only chrome/navigation.

## Final Response

Report the files changed, verification commands, and viewport checks. Mention if any checks were skipped or if unrelated dirty files already existed.
