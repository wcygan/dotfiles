# OKLCH Palette from a Single Brand Hue

OKLCH is `oklch(L C H)` — lightness 0–100%, chroma (saturation) 0–~0.4, hue 0–360°. Unlike HSL/RGB, equal lightness values look equally bright across hues, which is why this works for deriving a consistent scale.

## The pattern

Hold chroma and hue nearly constant, vary lightness to generate the scale:

```css
@theme {
  --brand-hue: 265;

  --color-primary-50:  oklch(97% 0.02 var(--brand-hue));
  --color-primary-100: oklch(93% 0.04 var(--brand-hue));
  --color-primary-200: oklch(86% 0.07 var(--brand-hue));
  --color-primary-300: oklch(78% 0.10 var(--brand-hue));
  --color-primary-400: oklch(70% 0.14 var(--brand-hue));
  --color-primary-500: oklch(62% 0.18 var(--brand-hue));   /* base */
  --color-primary-600: oklch(54% 0.17 var(--brand-hue));
  --color-primary-700: oklch(46% 0.15 var(--brand-hue));
  --color-primary-800: oklch(36% 0.12 var(--brand-hue));
  --color-primary-900: oklch(26% 0.08 var(--brand-hue));
  --color-primary-950: oklch(18% 0.05 var(--brand-hue));
}
```

Changing `--brand-hue` (e.g., from `265` to `150`) shifts the entire palette coherently. This is the whole point.

## Contrast-safe foregrounds

For each accent color, define its paired foreground:

```css
--color-primary:            oklch(62% 0.18 var(--brand-hue));
--color-primary-foreground: oklch(98% 0.02 var(--brand-hue));
```

Rule: foreground lightness should differ from base by at least 45 percentage points for WCAG AA on normal text.

## Extending to secondary / destructive / accent

Give each role its own hue offset:

```css
--brand-hue: 265;

--color-primary:     oklch(62% 0.18 var(--brand-hue));
--color-secondary:   oklch(62% 0.18 calc(var(--brand-hue) + 60));
--color-accent:      oklch(62% 0.18 calc(var(--brand-hue) - 30));
--color-destructive: oklch(58% 0.22 25);   /* red, fixed — not relative */
```

Destructive is usually fixed red; it reads as "error" across every brand and shouldn't drift with hue.

## Tooling

- https://oklch.com/ — pick a color, copy values
- Chrome DevTools supports OKLCH in the color picker natively.
