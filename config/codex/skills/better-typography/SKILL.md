---
name: better-typography
description: "Web typography from choosing fonts to spacing, wrapping and accessibility. Use when picking or pairing typefaces, configuring variable fonts or OpenType features, setting up a type scale, checking heading hierarchy, styling text in components, truncating text, styling underlines, selection, placeholders or carets, or reviewing frontend code for typography. Triggers on typography, fonts, font formats, woff2, variable fonts, font-weight, opentype, font-feature-settings, letter-spacing, line-height, type scale, heading hierarchy, heading levels, tabular numbers, text-wrap, truncation, line clamp, underlines, text-decoration, text selection, iOS input zoom, font smoothing, text contrast, measure, line length, text-box, smart punctuation, drop cap."
---

# Great typography

Good typography is mostly restraint. A sensible scale, comfortable spacing and enough contrast beat any clever effect. A label, a table cell, a marketing headline and an article paragraph should not share one set of rules. Apply these principles when building or reviewing anything with text in it.

**Match the project's styling system.** Before suggesting or writing any fix, check how the codebase styles things and express every change in that system: Tailwind utilities in a Tailwind project, plain declarations in CSS, CSS Modules, styled-components or StyleX. The [cheat sheet](css-cheat-sheet.md) maps each declaration to its Tailwind equivalent. Never introduce a second styling approach just to apply a typography fix.

## Quick Reference

| Category | When to use | Reference |
| --- | --- | --- |
| Choosing fonts | Font categories, pairing, formats, typeface anatomy | [choosing-fonts.md](choosing-fonts.md) |
| Variable fonts & OpenType | Axes, weights, tabular numbers, stylistic sets | [variable-fonts-and-opentype.md](variable-fonts-and-opentype.md) |
| Spacing & sizing | Type scale, heading hierarchy, line-height, letter-spacing, text trimming | [spacing-and-sizing.md](spacing-and-sizing.md) |
| Wrapping & punctuation | Measure, wrapping, truncation, smart punctuation, RTL | [wrapping-and-punctuation.md](wrapping-and-punctuation.md) |
| Details & accessibility | Underlines, selection, forms, decorative text, contrast | [details-and-accessibility.md](details-and-accessibility.md) |
| CSS cheat sheet | Quick lookup of every property covered, with Tailwind equivalents | [css-cheat-sheet.md](css-cheat-sheet.md) |

## Core Principles

### 1. Serve the Right Format

Use `.woff2` (Brotli compression, broadly supported) on the web. `.woff` is a fallback only for very old browsers; `.ttf` and `.otf` are raw desktop formats with no web compression. How the files are loaded is the project's own concern, this skill does not prescribe it.

### 2. Properties Over Raw Tags

When a CSS property exists, use it. `font-weight: 650` instead of `font-variation-settings: "wght" 650`, `font-optical-sizing: auto` instead of `"opsz"`, `font-variant-numeric: tabular-nums` instead of `font-feature-settings: "tnum" 1`. Properties keep working when a non-variable fallback renders. Reserve the raw-tag properties for custom axes (`"GRAD" 80`) and niche features (`"ss01" 1`) that have no property of their own.

### 3. No Fake Weights

When a weight or style is not loaded, the browser synthesizes it. That is a safety mechanism, not a feature. Set `font-synthesis: none` so missing files fail visibly instead of rendering a faked bold or italic.

### 4. Fewer Fonts, Sizes and Weights

Rarely use more than three fonts. Weight and size define hierarchy, but overusing them hurts readability quickly. Pair for contrast, not similarity: a serif headline with a sans body reads as deliberate, two near-identical sans-serifs read as a mistake.

### 5. Use a Type Scale with Semantic Names

Define a small set of sizes and deviate from it as little as possible. Hard-coded sizes without a system break down at scale. For solo projects, default names like `text-sm` work fine as long as the usage rules are clear. On a team, name sizes by use (`text-body-sm`), not by size, so the rules stay consistent.

### 6. Heading Sizes Descend with Level

Map each heading level used on a page to a descending step of the type scale: a lower level must never render larger than a higher one on the same page. Adjacent levels may share a size toward the small end of the scale as long as weight or spacing keeps them distinct. Pick the tag from the document outline and control the size with CSS; never skip levels or reach for an `h4` because it "looks right".

### 7. Line-Height by Role

Headings tighter, around `1.1`. Body copy `1.5` to `1.6`. Prefer unitless values so line-height scales with the font size; fixed values like `24px` do not.

### 8. Letter-Spacing by Size

Large headings often look better with slightly negative letter-spacing. Small uppercase labels need a little positive letter-spacing so letters do not feel crowded. Body copy at reading sizes needs neither.

### 9. Cap the Measure

Long lines make it hard for the eye to find the next line. Cap long-form text around 60–75 characters per line. Any unit works: `65ch` measures characters directly, and a pixel or rem cap is just as good: at a `16px` body size the range lands roughly between `560px` and `680px` depending on the font, so Tailwind's `max-w-xl` or `max-w-2xl` fit. What matters is that a cap exists and the resulting line length sits in range.

### 10. Wrap Deliberately

`text-wrap: balance` distributes text evenly across lines: use it on headings. `text-wrap: pretty` avoids leaving a single short word on the final line: use it on descriptions. Skip both in long-form text: browsers ignore `balance` past a few lines anyway, and evening out a whole paragraph wastes space and makes it harder to read. `overflow-wrap: break-word` where long words, links or IDs could escape the container. `white-space: nowrap` on labels and badges where a line break looks broken.

### 11. Tabular Numbers on Changing Values

Digits have different widths by default, so timers, counters and prices shift layout as they update. Apply `font-variant-numeric: tabular-nums` to any value that changes.

### 12. Truncate Without Losing Content

Single line: `text-overflow: ellipsis` with `overflow: hidden` and `white-space: nowrap`. Multiple lines: `line-clamp`. Truncation hides content, so if the missing text matters, keep the full value reachable in a tooltip or expanded view.

### 13. Write Copy Naturally, Style with CSS

Store text in natural case and control presentation with `text-transform`, so redesigns never require rewriting copy. Use smart punctuation: curly quotes in prose (straight quotes in code), an en dash for ranges like `2010–2020`, an em dash to set off a thought, the single ellipsis character, `&nbsp;` to keep values like `16 px` together and `&shy;` to control where long words may break.

### 14. Underlines from the Font

Default underlines sit wherever the browser decides. Pull position and thickness from the font's own metrics with `text-underline-position: from-font` and `text-decoration-thickness: from-font`, or tune manually with `text-decoration-thickness`, `text-underline-offset` and `text-decoration-skip-ink`. `text-decoration-style` draws the line dotted, dashed or wavy; a dotted underline is a common hint that a word carries extra information, like an abbreviation or a defined term. Unless the only thing animating is a color change, build the underline as a separate element instead of using `text-decoration`: color is the only part of a real underline that animates reliably.

### 15. Inputs at 16px on Mobile

iOS Safari zooms the whole page when an input's text is smaller than `16px`. Keep input text at `16px` on mobile viewports (`text-base sm:text-sm`). Avoid the `maximum-scale=1` viewport meta: Safari ignores it for pinch zoom, but every other browser honors it and blocks zooming, which fails WCAG.

### 16. Size and Contrast Floors

Body text `16px` (the web default and the right reading size). UI text can go smaller: `14px` for inputs and menus (inputs still need `16px` on mobile, see principle 15), `13px` for captions, rarely below `12px`. WCAG AA: `4.5:1` contrast for regular text, `3:1` for large text (roughly `24px` and up).

### 17. Font Smoothing on the Root

On macOS text renders heavier than intended. Apply `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` (both covered by Tailwind's `antialiased`) once on the root layout so they cover all text.

### 18. Logical Properties for Direction

To support right-to-left content, use direction-agnostic properties: `margin-inline-start` instead of `margin-left`, `text-align: start` instead of `left`. Set `lang` so browsers pick the right quotes and hyphenation, and `dir="rtl"` where needed.

### 19. Style the Selection, Disable It Where It Distracts

`::selection` is a subtle way to embed brand in the reading experience; keep the combination legible. Use `user-select: none` on button labels where copying is unlikely and selection feels distracting, and make sure `cmd+A` only grabs text the user expects to copy. In cross-platform apps that feel closer to native, disable selection for the interface and keep it only on content worth copying.

## Review Output Format

Always present changes as a markdown table with **Before** and **After** columns. Include every change you made, not just a subset. Never list findings as separate "Before:" / "After:" lines outside of a table. Group changes by principle using a heading above each table, and keep each row focused on a single diff. Write every **After** snippet in the styling system the project already uses.

### Example

#### Tabular numbers
| Before | After |
| --- | --- |
| `<span>{price}</span>` on live price | `<span className="tabular-nums">{price}</span>` |
| `font-feature-settings: "tnum" 1` | `font-variant-numeric: tabular-nums` |

#### Line-height and measure
| Before | After |
| --- | --- |
| `leading-none` on body paragraph | `leading-normal` (body needs `1.5`–`1.6`) |
| Full-width article column | `max-w-2xl` (~65 characters per line at `16px`) |

Rows should cite the specific file and property when it is not obvious from the snippet. If a principle was reviewed but nothing needed to change, omit that table entirely.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| `.ttf`/`.otf` served on the web | Convert to `.woff2` |
| `font-variation-settings: "wght"` for weight | `font-weight` (works with non-variable fallbacks) |
| `font-feature-settings: "tnum" 1` | `font-variant-numeric: tabular-nums` |
| Browser-faked bold or italic | Load the file, set `font-synthesis: none` |
| Hard-coded one-off font sizes | Use the type scale |
| `h3` rendered larger than `h2` on the same page | Map heading levels to descending scale steps |
| Heading tag picked for its size, skipping levels | Level from the document outline, size via CSS |
| `line-height: 24px` on scalable text | Unitless value (`1.5`) |
| Full-width paragraphs | Cap around 60–75 characters per line |
| Orphan on the last line of a paragraph | `text-wrap: pretty` |
| Lopsided two-line heading | `text-wrap: balance` |
| Numbers cause layout shift | `tabular-nums` |
| Truncated text with no way to read it | Tooltip or expanded view for the full value |
| `UPPERCASE` typed into copy | Natural case + `text-transform` |
| Justified text in an interface | `text-align: start`; reserve justify for specific editorial layouts |
| Underline cuts through descenders | `text-decoration-skip-ink: auto`, `from-font` metrics |
| Inputs below `16px` zoom on iOS | `text-base sm:text-sm` |
| `margin-left` in RTL-capable UI | `margin-inline-start` |
| Selectable button labels in native-feel UI | `user-select: none`, keep selection on real content |
| Extra-info hint with no visual cue | Dotted underline via `text-decoration-style: dotted` |
| Tailwind classes dropped into a CSS-in-JS codebase (or the reverse) | Express the fix in the styling system the project already uses |

## Review Checklist

- [ ] Web fonts are `.woff2`
- [ ] `font-weight` / `font-variant-*` used instead of raw axis and feature tags
- [ ] `font-synthesis: none` set; no faked weights or styles
- [ ] Sizes come from the type scale, no one-off values
- [ ] Heading sizes descend with level (`h1` ≥ `h2` ≥ `h3`…), levels stay visually distinct, none skipped
- [ ] Headings ~`1.1` line-height, body `1.5`–`1.6`, unitless
- [ ] Large headings have slightly negative tracking, small uppercase labels positive
- [ ] Long-form text capped around 60–75 characters per line
- [ ] Headings use `text-wrap: balance`, body uses `text-wrap: pretty`
- [ ] Changing numbers use `tabular-nums`
- [ ] Truncated content is reachable in full somewhere
- [ ] Copy stored in natural case, presentation via `text-transform`
- [ ] Underlines use `from-font` or tuned thickness, offset and skip-ink
- [ ] Inputs are `16px`+ on mobile viewports
- [ ] Text sizes and contrast meet the floors (`16px` body, `4.5:1` / `3:1`)
- [ ] `antialiased` applied once on the root layout
- [ ] Directional properties are logical (`inline-start`, `start`)
- [ ] Any styled `::selection` stays legible
