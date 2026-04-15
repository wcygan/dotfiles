# Templates

A Typst template is **a function that takes `body` (and named args) and returns content**, applied to the rest of the document via `#show: tmpl.with(...)`. That's the whole idea.

## Contents

- [The pattern](#the-pattern)
- [Why `#show: f` works](#why-show-f-works)
- [Canonical template skeleton](#canonical-template-skeleton)
- [Authors as list of dicts](#authors-as-list-of-dicts)
- [Using the template](#using-the-template)
- [Packaging as a local module](#packaging-as-a-local-module)
- [Publishing to @preview](#publishing-to-preview)

## The pattern

```typ
// conf.typ
#let conf(
  title: none,
  authors: (),
  abstract: [],
  body,
) = {
  set document(title: title, author: authors.map(a => a.name))
  set page(paper: "us-letter", margin: 1in, numbering: "1")
  set text(font: "New Computer Modern", size: 11pt)
  set par(justify: true, leading: 0.65em)

  // Title block
  align(center)[
    #text(size: 20pt, weight: "bold", title) \
    #v(1em)
    #authors.map(a => [#a.name \ #text(size: 9pt, a.affiliation)]).join(h(2em))
  ]

  v(1em)

  // Abstract
  if abstract != [] {
    align(center, text(weight: "bold", [Abstract]))
    pad(x: 1in, abstract)
    v(1em)
  }

  // Main body
  body
}
```

## Why `#show: f` works

```typ
#show: conf.with(title: [My Paper], authors: (...))

= Introduction
Text...
```

`#show: f` with no selector means "wrap the entire remaining document content and pass it as the argument to `f`." `conf.with(...)` partially applies the named args, leaving `body` to be filled in by the show-transform. The rest of the file becomes `body`.

Equivalent, more explicit:

```typ
#conf(
  title: [My Paper],
  authors: (...),
)[
  = Introduction
  Text...
]
```

`#show: tmpl.with(...)` is preferred because it keeps document content at the top level (not nested in content brackets), which matters for outline extraction and editor folding.

## Canonical template skeleton

```typ
#let template(
  // Required
  title: none,
  body,

  // Optional with defaults
  subtitle: none,
  authors: (),
  date: none,
  abstract: [],

  // Appearance
  paper: "us-letter",
  font: "New Computer Modern",
  font-size: 11pt,
) = {
  // 1. Document metadata (for PDF properties)
  set document(
    title: title,
    author: authors.map(a => a.at("name", default: a)),
  )

  // 2. Page setup
  set page(paper: paper, margin: 1in, numbering: "1 / 1")

  // 3. Text defaults
  set text(font: font, size: font-size, lang: "en")

  // 4. Paragraph defaults
  set par(justify: true, leading: 0.65em, first-line-indent: 0pt)

  // 5. Heading style
  set heading(numbering: "1.1")
  show heading.where(level: 1): set block(above: 2em, below: 1em)
  show heading.where(level: 1): set text(size: 16pt)

  // 6. Link & reference colors
  show link: set text(fill: rgb("#0066cc"))
  show ref: set text(fill: rgb("#0066cc"))

  // 7. Title block
  align(center)[
    #text(size: 20pt, weight: "bold", title)
    #if subtitle != none [ \ #text(size: 14pt, subtitle) ]
    #if authors.len() > 0 [
      \ #v(0.5em)
      #authors.map(a => a.at("name", default: a)).join(", ", last: ", and ")
    ]
    #if date != none [ \ #text(size: 10pt, date) ]
  ]

  v(2em)

  // 8. Abstract
  if abstract != [] {
    pad(x: 0.5in)[
      #align(center, text(weight: "bold", [Abstract]))
      #abstract
    ]
    v(1em)
  }

  // 9. Body
  body
}
```

## Authors as list of dicts

Preferred convention for structured author data:

```typ
#show: template.with(
  title: [Spectral Analysis of ...],
  authors: (
    (
      name: "Ada Lovelace",
      affiliation: "University of X",
      email: "ada@example.edu",
      orcid: "0000-0000-0000-0001",
    ),
    (
      name: "Alan Turing",
      affiliation: "University of Y",
    ),
  ),
  abstract: [We show that...],
)
```

Inside the template, use `authors.map(a => a.name)` and `a.at("email", default: none)` to access fields safely.

## Using the template

```typ
// paper.typ
#import "conf.typ": conf
#show: conf.with(title: [My Paper], authors: ((name: "Me"),))

= Introduction
...

= Methods
...

#bibliography("refs.bib")
```

## Packaging as a local module

For personal reuse across documents without publishing:

```
~/.local/share/typst/packages/local/mypkg/0.1.0/
  typst.toml
  lib.typ
```

`typst.toml`:

```toml
[package]
name = "mypkg"
version = "0.1.0"
entrypoint = "lib.typ"
authors = ["You"]
license = "MIT"
description = "Personal template"
```

`lib.typ` exports your `#let conf(...)` function. Then in any document:

```typ
#import "@local/mypkg:0.1.0": conf
#show: conf.with(title: [...])
```

## Publishing to @preview

See [toolchain](toolchain.md#publishing-a-package). Short version: fork `typst/packages`, add `packages/preview/<name>/<version>/` with `typst.toml`, `README.md`, entrypoint, and an example thumbnail. PR. Versions are immutable once merged.
