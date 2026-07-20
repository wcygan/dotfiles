# Details and accessibility

Underlines, selection, forms, decorative text and the floors that keep everything readable.

## Underlines

Default underline position is browser-determined: sometimes too close, cutting through descenders or too thin. Pull position and thickness from the font's own metrics:

```css
a {
  text-underline-position: from-font;
  text-decoration-thickness: from-font;
}
```
The line does not have to be solid. `text-decoration-style` can draw it dotted, dashed or wavy. A dotted underline is a common hint that a word carries extra information, like an abbreviation or a defined term:

```css
abbr {
  text-decoration: underline dotted;
}
```

Or tune manually:

```css
a {
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
  text-decoration-skip-ink: auto;
  text-decoration-color: var(--color-gray-1000);
  transition: text-decoration-color 200ms ease-out;
}

a:hover {
  text-decoration-color: var(--color-gray-1200);
}
```

Unless the only thing animating is a color change, build the underline as a custom element instead of using `text-decoration`: color is the only part of a real underline that animates reliably. Animate the custom element however the effect requires.

## Selection

- `::selection` changes the background and color of selected text; a subtle way to embed brand. Keep the combination legible.
- `user-select: none` on button labels: copying a label is unlikely and selection there feels distracting. Also make sure `cmd+A` only grabs text the user expects to copy.
- In cross-platform apps that feel closer to native, disable text selection for the interface and keep it enabled only for content the user may actually want to copy.
- `::target-text` styles the phrase a shared link scrolls to.
- The Custom Highlight API styles ranges you pick yourself, like search matches, without extra markup.

## Forms and editable text

- `::placeholder` styles the hint in an empty field.
- `caret-color` colors the blinking insertion bar. Color is about as far as caret styling goes: a fully custom caret is very difficult to build and usually not worth it unless a very specific effect calls for it.

### iOS input zoom

Focusing an input with text smaller than `16px` zooms the whole page (an accessibility feature: `16px` is the web default and Safari treats smaller as too hard to read while typing).

```tsx
// Good: 16px on mobile, smaller from the sm breakpoint up
<input className="text-base sm:text-sm" type="email" />
```

Avoid the `maximum-scale=1` viewport meta as a fix: Safari ignores the cap for pinch zoom, but every other browser honors it and restricts pinch zoom, which fails WCAG 1.4.4. The responsive input size solves the zoom with no accessibility cost.

## Decorative text

| Property | Effect |
| --- | --- |
| `::first-letter` | Drop cap, widely supported |
| `::first-line` | Styles only the first line |
| `initial-letter` | Sizes the drop cap; limited support, no Firefox yet |
| `background-clip: text` | Clips a background or gradient to the letter shapes |
| `-webkit-text-stroke` | Outlines the letters; works across modern browsers despite the prefix |
| `text-shadow` | Like `box-shadow` but follows the character shapes |

If a text stroke draws lines inside the letters, that is the font: the stroke traces every contour and variable fonts usually keep overlapping shapes unmerged. Static fonts do not have this issue.

## Sizes and contrast

Typography must survive the reader changing it: zoom, a larger browser font size, overridden line height or letter spacing.

| Text | Size |
| --- | --- |
| Body | `16px` (the web default, the right reading size) |
| Inputs and menus | `14px` |
| Captions | `13px` |
| Floor | Rarely below `12px` |

WCAG AA contrast:

| Text | Minimum |
| --- | --- |
| Regular text | `4.5:1` |
| Large text (~`24px`+) | `3:1` |

Bigger, heavier letters stay legible at lower contrast.

## Font smoothing

On macOS text renders heavier than intended. Apply font smoothing once on the root layout so it covers all text. Tailwind's `antialiased` sets both properties:

```css
html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

```tsx
<html lang="en">
  <body class="font-sans antialiased">
    <main>{children}</main>
  </body>
</html>
```
