# Styling, Rules, and State

The Typst mental model most unlike Markdown/LaTeX. This is where most bugs live.

## Contents

- [`#let`, `#set`, `#show` — what each does](#let-set-show--what-each-does)
- [Show rule patterns](#show-rule-patterns)
- [Selectors](#selectors)
- [Scope and leakage](#scope-and-leakage)
- [Counters](#counters)
- [State](#state)
- [`context` blocks](#context-blocks)
- [Math mode rules](#math-mode-rules)
- [Figures, labels, references](#figures-labels-references)

## `#let`, `#set`, `#show` — what each does

```typ
// Binding: introduce a name (value or function)
#let pi = 3.14159
#let warn(msg) = text(fill: red, weight: "bold")[⚠ #msg]
#let warn(msg) = { text(fill: red)[⚠ #msg] }   // code-block body
#let warn(msg) = [⚠ #text(red)[#msg]]           // content body — same effect, different syntax

// Set: change default args of a function (elements are functions)
#set text(font: "New Computer Modern", size: 11pt)
#set page(paper: "us-letter", margin: 1in)
#set heading(numbering: "1.1")

// Show: rewrite matching content through a replacement
#show heading: set block(above: 1.5em, below: 1em)     // show + set: restyle
#show heading.where(level: 1): it => align(center, it) // transform
#show "TODO": it => text(fill: orange, it)             // string selector
#show regex("\d+"): it => text(fill: blue, it)         // regex selector
```

### The distinction

| | `#set` | `#show` |
|---|---|---|
| Target | A function (element type) | A selector (element or string/regex) |
| Effect | Changes defaults | Wraps/replaces matched content |
| Scope | Block-scoped | Block-scoped |
| Composable | Additive | First match wins per element |

## Show rule patterns

```typ
// Pattern 1 — cosmetic wrap, preserves everything
#show heading.where(level: 1): it => align(center, it)

// Pattern 2 — restyle but need to re-emit structure
#show heading.where(level: 1): it => [
  #set text(size: 24pt, weight: "bold")
  #it.body       // ⚠ drops numbering, outline entry
]

// Pattern 3 — correct restyle preserving numbering
#show heading.where(level: 1): it => {
  set text(size: 24pt, weight: "bold")
  if it.numbering != none [
    #counter(heading).display(it.numbering) #h(0.5em)
  ]
  it.body
}

// Pattern 4 — show + set shorthand for pure defaults change
#show heading.where(level: 1): set text(24pt)   // cleanest

// Pattern 5 — transform based on properties
#show link: it => if type(it.dest) == str [
  #text(fill: blue, underline(it))
] else [#it]
```

### The destructuring trap

`it.body` is **only the prose content**, not the element. Emitting `it.body` drops numbering, references, outline visibility, and counters. Prefer returning `it` whole, or use `show: set` when you only need to change defaults.

## Selectors

```typ
heading                          // any heading
heading.where(level: 2)          // only level-2 headings
figure.where(kind: image)        // only image figures (not table/raw)
figure.where(kind: table)
raw.where(block: true)           // block code vs inline raw
"TODO"                            // literal string in text
regex("\d+(\.\d+)?")             // regex in text
math.equation.where(block: true)  // only display math
link                              // any link
ref                               // any @label reference
```

Selector functions: `.where(...)`, `.or(other)`, `.and(other)`, `selector.before(other)`, `.after(other)`.

## Scope and leakage

```typ
Before [
  #set text(fill: red)      // scoped to [...] block
  Inside is red
] after is not.
```

- `#set`/`#show` applied at top level of a file lasts to end of file (or `#import`'s scope).
- Inside a `[...]` content block, they reset at block end.
- Inside a `{...}` code block, they reset at block end **and** the block evaluates to the content produced by expressions.
- Template functions rely on this: a template is typically a `{ set ...; show ...; body }` block.

## Counters

```typ
// Built-in counters: page, heading, figure, footnote, math.equation

#context counter(page).get()           // [current, ...] — must be in context
#context counter(page).final()         // [last value]

// Custom counter
#let mycount = counter("mycount")
#mycount.step()                         // increment by 1
#mycount.update(0)                      // reset
#mycount.update(n => n + 5)             // apply function
#context mycount.display()              // show current
#context mycount.display("I")           // show as Roman numeral

// Display format strings: "1", "1.1", "1.1.1", "I", "A", "a", "①"
#set heading(numbering: "1.1")
```

## State

```typ
#let todo-count = state("todo-count", 0)
#todo-count.update(n => n + 1)
#context todo-count.get()            // current value at this point

// State is document-position-aware
#context todo-count.final()          // value at end of document
#context todo-count.at(<label>)      // value at a specific label location
```

State vs counter: counters are for sequential numbering; state is for arbitrary values tracked across document positions.

## `context` blocks

`#context` creates a scope that can read values whose truth depends on layout (page numbers, counter values, query results). **Required** for:

- `here()`, `locate(<label>)` (the function `here` replaced the old `locate(loc=>)` idiom)
- `counter(...).get/final/at`
- `state(...).get/final/at`
- `query(selector)`
- `document.*` (title, author, keywords)
- `measure(content)`

```typ
#context [
  Page #counter(page).get().first() of #counter(page).final().first()
]

// Works inline too
= Introduction <intro>
Later: see page #context counter(page).at(<intro>).first().
```

## Math mode rules

```typ
$ x + y = z $                          // inline
$ sum_(i=0)^n i = n(n+1)/2 $           // display-ish via display style
$ integral_(-oo)^oo e^(-x^2) dif x = sqrt(pi) $

// Greek: just spell them
$ alpha beta gamma Delta Omega $

// Operators: built-ins are upright automatically
$ sin cos tan log exp lim inf sup det $

// Multi-char identifiers are "words" (upright), single letters are variables (italic)
$ ab $          // a·b (two vars)
$ "ab" $        // "ab" upright word

// Alignment
$
  a + b &= c \
  d     &= e + f
$

// Fractions, roots, vectors, matrices
$ 1/2, sqrt(x), arrow(v), vec(1, 2, 3), mat(1, 2; 3, 4) $

// Custom operators
$ op("argmax")_x f(x) $
#let argmax = math.op("argmax")
$ #argmax _x f(x) $
```

## Figures, labels, references

```typ
#figure(
  image("diagram.svg", width: 60%),
  caption: [A diagram.],
) <fig:diagram>

See @fig:diagram on page #context counter(page).at(<fig:diagram>).first().

// Tables
#figure(
  table(
    columns: 3,
    [*A*], [*B*], [*C*],
    [1],   [2],   [3],
  ),
  caption: [Results.],
) <tab:results>

// Reference styles
#set ref(supplement: it => {
  if it.func() == figure and it.kind == image [Fig.]
  else if it.func() == figure and it.kind == table [Tab.]
  else [Sec.]
})
```

Labels must come **immediately after** the element (no intervening text). Reference with `@label` or `#ref(<label>)`.
