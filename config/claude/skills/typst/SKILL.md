---
name: typst
description: Typst 0.13+ typesetting expert. Auto-loads when working with .typ files, Typst markup, show/set/let rules, figures, math mode, counters, state, context blocks, @preview packages, templates, tinymist LSP, or typst compile/watch. Corrects outdated idioms from pre-0.12 training data. Keywords typst, .typ, typesetting, LaTeX alternative, show rule, set rule, let binding, content block, context block, counter, state, figure, bibliography, @preview, tinymist, typst compile, typst watch, cetz, touying, polylux, fletcher, Hayagriva.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch
---

# Typst (0.13+)

Typst is a markup-based typesetting system. Single-binary compiler, incremental compilation, CSS-like show/set rules instead of LaTeX macro hell.

**Pin this skill to Typst 0.13.x idioms.** LLM training data is typically pre-0.12 and will emit deprecated forms. The version-drift reference is the load-bearing piece — consult it before writing non-trivial Typst.

## Three modes (the thing Claude conflates)

| Mode | Enter with | Inside, you write |
|---|---|---|
| **Markup** | default, `[...]` | prose, `#heading[...]`, `@label` refs |
| **Code** | `#expr`, `{...}` | expressions, `let`, `if`, `for`, function calls |
| **Math** | `$...$` | math; multi-char names auto-treated as words, single letters as variables |

Inside markup you need `#` before a function call (`#image("a.png")`). Inside code you don't (`image("a.png")`). Inside math, `#` drops back into code (`$ #x $`).

## Three rule-like directives (most-wrong area)

```typ
#let name = value           // binding — value or function
#set heading(numbering: "1.") // "from here on, use these defaults"
#show heading.where(level: 1): it => [== #it.body]  // "rewrite matching content"
```

- `#show target: replacement` — replacement is either a function `it => ...` (receives the element) or direct content.
- `it` alone preserves default rendering; destructuring to `it.body` **drops numbering, outline entries, counters**. Use `it.numbering`, `it.body`, `it.level` explicitly, or just return `it` when you only want a side-effect styling like color.
- Selectors: `heading.where(level: 1)`, `figure.where(kind: image)`, `regex("\d+")`, `"literal string"`.
- Set rules inside `[...]` don't leak out of that block.

## `context` is mandatory for introspection (0.11+)

```typ
#context counter(heading).get()      // reading counter → needs context
#context here().page()               // location queries → needs context
#context document.title               // document metadata → needs context
```

`locate(loc => ...)` is **deprecated** — always use `#context` blocks. See [version-drift](references/version-drift.md).

## Top 8 gotchas → where to look

1. Show rule destructuring drops defaults → [styling-and-state](references/styling-and-state.md)
2. `locate()`, `style(styles => ...)` removed → [version-drift](references/version-drift.md)
3. `image(path: ...)` renamed to `image(source: ...)` in 0.13 → [version-drift](references/version-drift.md)
4. `#set par(spacing:)` replaced the old `#show par: set block(spacing:)` hack → [version-drift](references/version-drift.md)
5. Top-level `#columns(n)[...]` is discouraged; use `#set page(columns: n)` → [version-drift](references/version-drift.md)
6. Template = function that takes `body` + named args, applied via `#show: tmpl.with(...)` → [templates](references/templates.md)
7. `@preview/pkg:x.y.z` imports are version-pinned per-import; hallucinated versions fail → [packages](references/packages.md)
8. Math: multi-letter identifiers are treated as words unless `#`-escaped; alignment uses `&` → [styling-and-state](references/styling-and-state.md)

## Content vs str vs symbol

| Type | Literal | Convert | Notes |
|---|---|---|---|
| `content` | `[hello #name]` | `[#str_var]` | The universal display type |
| `str` | `"hello"` | `str(42)` | Plain string; **not** `str(content)` — use `.text` or `repr()` |
| `symbol` | `sym.arrow.r` | — | Unicode symbols; valid in markup & math |

## Compile

```bash
typst compile main.typ           # → main.pdf
typst compile main.typ out.svg   # also supports --format svg|png
typst watch main.typ             # live rebuild
typst compile --root . --font-path ./fonts main.typ
```

See [toolchain](references/toolchain.md) for tinymist LSP, `@local` packages, CI.

## When the user says "coming from LaTeX"

Strong signal — jump straight to [latex-migration](references/latex-migration.md). The direct command-mapping table (`\newcommand` → `#let`, `\usepackage` → `#import "@preview/..."`, align env → `$ ... & ... \ $`) is the fastest path.

## References

- [version-drift](references/version-drift.md) — **read this first for any non-trivial task.** Do-not-emit list for deprecated pre-0.12 idioms.
- [styling-and-state](references/styling-and-state.md) — set/show/let semantics, `context`, counters, state, math mode rules.
- [templates](references/templates.md) — the `#show: tmpl.with(...)` pattern, packaging, author/title conventions.
- [latex-migration](references/latex-migration.md) — translation tables for common LaTeX idioms.
- [packages](references/packages.md) — task → canonical `@preview` package picker with pinned versions.
- [toolchain](references/toolchain.md) — CLI, tinymist, fonts, `@local` dev namespace, CI rendering, package publishing.
