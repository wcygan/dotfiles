# Package Picker (@preview)

Task → canonical package. Browse the full universe at https://typst.app/universe.

Versions shown are known-good as of early 2026; newer versions usually work but **pin per-import** — `@preview/<name>:<version>` requires the exact version be on the user's system or downloadable. When unsure, check the universe page for the latest. LLM priors frequently hallucinate versions; always verify.

## Contents

- [Diagrams and plots](#diagrams-and-plots)
- [Slides](#slides)
- [Tables](#tables)
- [Code blocks](#code-blocks)
- [Algorithms](#algorithms)
- [Science and math](#science-and-math)
- [Documentation](#documentation)
- [Glossaries and acronyms](#glossaries-and-acronyms)
- [Layout helpers](#layout-helpers)
- [CVs and résumés](#cvs-and-résumés)

## Diagrams and plots

| Task | Package | Example import |
|---|---|---|
| General 2D drawing (TikZ-like) | `cetz` | `#import "@preview/cetz:0.3.2"` |
| Plots (line/bar/scatter/heatmap) | `cetz-plot` | `#import "@preview/cetz-plot:0.1.1"` |
| Commutative diagrams, graphs | `fletcher` | `#import "@preview/fletcher:0.5.5": diagram, node, edge` |
| Circuit diagrams | `circuiteria` | `#import "@preview/circuiteria:0.1.0"` |
| Chemical structures | `chem-par` / `conchord` | — |
| Trees | `syntree` / `cetz-tree` | — |

**cetz + fletcher** is the mainline combo. Fletcher builds on cetz, so you import both.

## Slides

| Task | Package | Notes |
|---|---|---|
| Modern slides (preferred) | `touying` | `#import "@preview/touying:0.5.5": *` — rich themes, animations, cetz integration |
| Legacy slides | `polylux` | Still common, has pdfpc speaker-note support |

**Recommendation:** use touying for new slide decks. Polylux is in maintenance mode.

## Tables

| Task | Package | Notes |
|---|---|---|
| Booktabs-style professional tables | `tablex` | `#import "@preview/tablex:0.0.9": tablex, cellx` — more control than built-in |
| Grid layout with merging | `tabled` | Newer alternative |
| Built-in `table(...)` | — | Fine for simple cases; use `stroke: (x, y) => ...` for custom borders |

Start with the built-in `#table(...)`. Only reach for `tablex` when you need merged cells, colored rows, or complex borders.

## Code blocks

| Task | Package | Notes |
|---|---|---|
| Syntax-highlighted code with line numbers, annotations | `codly` | `#import "@preview/codly:1.2.0": *` — decorator pattern; pairs with built-in raw blocks |
| Language-tagged raw blocks | built-in | ```` ```python\n...\n``` ```` — syntax highlighting comes for free |

## Algorithms

| Task | Package |
|---|---|
| Pseudocode (algorithm2e-style) | `algorithmic` or `lovelace` |

## Science and math

| Task | Package |
|---|---|
| Physics notation (bra-ket, tensors) | `physica` |
| Quantum circuits | `quill` |
| SI units | `unify` or `metro` |
| Theorems, proofs, lemma environments | `ctheorems` or `thmbox` |

## Documentation

| Task | Package |
|---|---|
| Typst package documentation (function signatures, examples) | `tidy` |
| Generic manuals with running headers | `hydra` (section-aware headers) |

`tidy` is the standard for documenting your own packages.

## Glossaries and acronyms

| Task | Package |
|---|---|
| Glossaries, acronyms with forward/back links | `glossarium` |

## Layout helpers

| Task | Package |
|---|---|
| Drop caps | `droplet` |
| Custom bookmarks, outlines | `outrageous` |
| Indented "notebook"-style code + prose | `gentle-clues` (callouts: info, warning, etc.) |
| Tables of contents with customization | built-in `outline()` first; `indenta` for extra control |
| Page-aware headers/footers | `hydra` |

## CVs and résumés

Templates, not libraries — start with one from the universe:

- `modernpro` / `modern-cv` — 1-page modern CVs
- `basic-resume` — clean minimal
- `chic-cv` — two-column with sidebar

All are `#import "@preview/<name>:<version>": *` + `#show: resume.with(...)`.

## Rules for using packages

1. **Pin the version.** `@preview/cetz:0.3.2` not `@preview/cetz`. Typst will refuse unpinned imports.
2. **First import fetches and caches.** `typst compile` will download to `~/.cache/typst/packages/`. Offline builds need pre-warmed cache.
3. **Check compatibility.** A package pinned to cetz 0.2 won't run against cetz 0.3 automatically. Read the package's README for cetz/Typst version requirements.
4. **Don't hallucinate.** If unsure of a version, check https://typst.app/universe/package/<name> or `ls ~/.cache/typst/packages/preview/<name>/`. LLMs routinely invent versions.
5. **@local for in-progress packages.** Develop at `~/.local/share/typst/packages/local/<name>/<version>/` and import as `@local/<name>:<version>`.
