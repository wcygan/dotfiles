# Form Factor Checklist

Use this checklist for Tauri Start Demo responsive styling tasks.

## Breakpoints

- Desktop: `> 900px`, with devtools and multi-column layouts allowed at `>= 1024px`.
- Tablet/iPad: `621px-900px`, usually a sticky top nav plus one-column page content.
- Phone: `<= 620px`, compact app header, horizontal nav, one-column content, reduced type and spacing.
- Narrow phone: `<= 380px`, reduce title/nav/card padding again.

Adjust exact breakpoints to the app, but keep the rule simple and explain it if changed.

## CSS Patterns

Use these patterns when they fit the existing code:

```css
:root {
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
}

input {
  min-width: 0;
}

svg {
  flex: 0 0 auto;
}
```

Pair safe-area variables with:

```tsx
{
  name: 'viewport',
  content: 'width=device-width, initial-scale=1, viewport-fit=cover',
}
```

For grids and flex layouts:

- Use `minmax(0, 1fr)` for shrinkable grid columns.
- Use `min-width: 0` on containers that hold long text, inputs, paths, code, or flex children.
- Use `overflow-wrap: anywhere` for code, filesystem paths, timestamps, and IPC output.
- Avoid `100vh` alone; pair with `100dvh` where full-height shells are used.
- Prefer `scrollbar-gutter: stable` for desktop scroll containers.
- Keep touch targets around `40px-44px` minimum height.

## App-Specific Layout

For `tauri-start-demo`:

- Desktop can keep `.app-shell` as a two-column grid with `.sidebar` and `.workspace`.
- At tablet width, switch `.app-shell` to one column, keep `.sidebar` sticky at the top, and keep `.nav-list` as three equal columns.
- At phone width, keep `.sidebar` compact and sticky, shrink `.brand-mark` and headings, make `.nav-list` a horizontal scroll/flex row, and reduce `.workspace`, `.panel`, `.runtime-meter`, and `.status-strip` spacing.
- Make `.dashboard-grid`, `.architecture-band`, `.optimization-grid`, `.sqlite-workbench`, `.sqlite-summary`, and event rows collapse to one column before they crowd.
- Gate TanStack devtools to desktop-only when it overlaps app content in visual checks.

## Tauri Config

- Lower `src-tauri/tauri.conf.json` `minWidth`/`minHeight` only when desktop shell resizing should exercise responsive breakpoints.
- Keep `devUrl`, `frontendDist`, Portless settings, and security settings unchanged unless the task specifically requires them.
- Do not add custom titlebar/window decoration changes for responsive styling. If custom chrome is requested, use the official Tauri window customization docs and verify drag regions and platform behavior.

## Visual Acceptance

Check each viewport:

- No horizontal overflow: `document.documentElement.scrollWidth === document.documentElement.clientWidth`.
- No text clipped inside buttons, nav items, cards, input fields, or code blocks.
- No devtools or floating controls covering app content on phone/tablet.
- First phone viewport shows app identity, nav, current page title, and at least one meaningful content block.
- Tablet layout should feel like a real tablet layout, not a stretched phone or cramped desktop.
- Desktop should remain dense and efficient after responsive changes.

## Verification Commands

Use the repo's package manager and scripts:

```bash
bun run typecheck
bun run lint
bun run check
bun run test
bun run build
cargo check --manifest-path src-tauri/Cargo.toml
```

Browser checks can use `agent-browser`:

```bash
agent-browser --session tauri-mobile set viewport 390 844
agent-browser --session tauri-mobile open http://tauri-start-demo.localhost
agent-browser --session tauri-mobile eval '({scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth})'
agent-browser --session tauri-mobile screenshot /tmp/tauri-mobile.png
```

Repeat for `768x1024` and `1280x800`, and open major routes such as `/`, `/architecture`, and `/performance`.
