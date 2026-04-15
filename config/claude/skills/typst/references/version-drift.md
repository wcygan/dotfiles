# Version Drift — Do Not Emit

Typst is pre-1.0 and has shipped breaking renames in 0.11, 0.12, and 0.13. LLM training data tends to be 0.10–0.11 era. This file is a do-not-emit list. **Always prefer the new form.**

## Contents

- [Introspection: `locate()` → `context`](#introspection-locate--context)
- [Image: `path:` → `source:` (0.13)](#image-path--source-013)
- [Bibliography: `path:` → `sources:` (0.13)](#bibliography-path--sources-013)
- [Plugin: type → function (0.13)](#plugin-type--function-013)
- [Paragraph spacing (0.12)](#paragraph-spacing-012)
- [Columns (0.12)](#columns-012)
- [`style(styles => ...)` removed](#stylestyles---removed)
- [Math: `$"x"$` quoting (0.13)](#math-x-quoting-013)
- [Quick audit checklist](#quick-audit-checklist)

## Introspection: `locate()` → `context`

**Deprecated (do not emit):**

```typ
#locate(loc => [Page #counter(page).at(loc).first()])
```

**Current:**

```typ
#context [Page #counter(page).get().first()]
```

Any value that depends on layout position (`here()`, `counter(...).get()`, `counter(...).at(loc)`, `state(...).get()`, `document.title`, `query(...)`) must be read from inside a `#context` block. `locate` is gone.

## Image: `path:` → `source:` (0.13)

```typ
// ❌ old
#image(path: "logo.png", width: 3cm)

// ✅ 0.13+
#image("logo.png", width: 3cm)            // positional still works
#image(source: "logo.png", width: 3cm)    // named arg renamed
```

The first positional arg is the source. The named parameter is `source`, not `path`.

## Bibliography: `path:` → `sources:` (0.13)

```typ
// ❌ old
#bibliography("refs.bib")                 // still works positionally
#bibliography(path: "refs.bib")           // named form changed

// ✅ 0.13+
#bibliography("refs.bib")
#bibliography(sources: ("refs.bib", "extra.yml"))
```

`sources:` can also take a single path or an array. Typst supports BibLaTeX `.bib` and Hayagriva `.yml` natively.

## Plugin: type → function (0.13)

```typ
// ❌ old
#let p = plugin("my.wasm")

// ✅ 0.13+
#let p = plugin("my.wasm")     // same call site, but `plugin` is now a function, not a type
// type-checking `type(x) == plugin` no longer valid; use `type(x)` comparison to a constructed plugin
```

If code introspects types of plugin values, it likely needs updating. Most user code is unaffected.

## Paragraph spacing (0.12)

**Deprecated hack:**

```typ
#show par: set block(spacing: 1.2em)
```

**Current:**

```typ
#set par(spacing: 1.2em)
#set par(leading: 0.65em)        // line-within-paragraph spacing is `leading`
```

`par` now has a real `spacing` parameter. Do not emit the old `show par: set block` workaround.

## Columns (0.12)

**Discouraged:**

```typ
#columns(2)[
  Lots of text...
]
```

**Preferred:**

```typ
#set page(columns: 2)
Lots of text...
```

Only the page-level columns properly integrate with floats, footnotes, and line numbers. Inline `#columns()` exists but is a last resort.

## `style(styles => ...)` removed

```typ
// ❌ removed
#style(styles => measure([Hello], styles))

// ✅ current
#context measure([Hello])
```

`measure` no longer needs a styles argument — call it directly inside `#context`.

## Math: `$"x"$` quoting (0.13)

In 0.13 the behavior of quoted strings in math normalized:

- `$x$` — single letter, italic variable.
- `$"text"$` — upright word/operator (same as before).
- `$ab$` — **two italic variables multiplied** (`a·b`), not "ab".
- `$"ab"$` — upright word "ab".
- `$#"ab"$` — insert the string value; usually you want `$"ab"$` instead.

Claude often writes `$sin(x)$` — this produces `s·i·n·(x)`. Correct forms:

```typ
$ sin(x) $            // `sin` is a built-in operator constant
$ op("sin")(x) $      // define a new operator
$ "myop"(x) $         // upright word, less ideal
```

Use `$ alpha beta $` for Greek (built-ins), `$ upright(x) $` to force upright, `$ italic("text") $` for italic words.

## Quick audit checklist

Before considering Typst code ready, grep for:

```
locate(              → replace with #context
path:                → on image/bibliography, switch to source:/sources: or positional
show par: set block  → use set par(spacing:)
#columns(            → at top level, switch to set page(columns:)
style(styles =>      → drop, use #context
```

If any match, update to the current idiom.
