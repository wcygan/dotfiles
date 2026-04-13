# Validation (grep recipes)

Run these before merging. Any hit is a violation — either justify it or fix it.

## No hex literals in component source

```sh
rg "#[0-9a-fA-F]{3,8}\b" src/ --type ts --type tsx --type css \
  | rg -v "src/styles/"  # theme block is the one allowed place
```

## No raw Tailwind color scales in components

```sh
rg -t tsx -t ts "\b(bg|text|border|ring|divide|from|via|to|placeholder|accent|caret|fill|stroke|shadow)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(50|100|200|300|400|500|600|700|800|900|950)\b" src/
```

Hits mean a semantic token should be used instead.

## No Tailwind config file

```sh
fd -t f "tailwind\.config\.(js|ts|cjs|mjs)"
```

Any result is wrong for v4 — configuration belongs in `@theme`.

## No v3-style CSS directives

```sh
rg "@tailwind (base|components|utilities)" src/
```

Any hit is stale v3 syntax. v4 uses a single `@import 'tailwindcss'`.

## No per-utility dark-mode color duplication

```sh
rg "dark:(bg|text|border)-(slate|gray|zinc|neutral|stone|red|blue|green|purple)-" src/
```

Any hit means the token flip isn't being used — fix per [dark-mode](./dark-mode.md).

## No arbitrary spacing values

```sh
rg "\b(p|m|gap|space-[xy])-\[\d+(px|rem|em)\]" src/
```

Prefer the spacing token scale. Arbitrary values are sometimes valid but should be rare.

## Checklist for Claude

- [ ] Ran hex grep: 0 hits in `src/` (outside `styles/`)
- [ ] Ran color-scale grep: 0 hits in `src/`
- [ ] Ran `tailwind.config.*` check: 0 files
- [ ] Ran `@tailwind` check: 0 hits
- [ ] Ran dark-mode duplication check: 0 hits
- [ ] All new colors added to `@theme` first

If any check fails, fix before calling the task complete.
