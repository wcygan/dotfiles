# Tailwind CSS — Colors

## Color Palette

Tailwind v4 includes 24 color families, each with 11 shades (50–950). All use OKLCH color space.

**Chromatic colors:**
`red` `orange` `amber` `yellow` `lime` `green` `emerald` `teal` `cyan` `sky` `blue` `indigo` `violet` `purple` `fuchsia` `pink` `rose`

**Neutral colors:**
`slate` `gray` `zinc` `neutral` `stone`

**Special:** `black` `white`

### Shade Scale

| Shade | Lightness | Usage |
|-------|-----------|-------|
| 50 | Very light | Tinted backgrounds |
| 100 | Light | Subtle backgrounds |
| 200 | | Light borders |
| 300 | | Disabled text |
| 400 | Medium-light | Placeholder text |
| 500 | Medium | Brand colors, icons |
| 600 | Medium-dark | Primary buttons |
| 700 | Dark | Hover states |
| 800 | Very dark | Dark text |
| 900 | Near-black | Headings |
| 950 | Darkest | High-contrast text |

## Color Utilities

```html
<!-- Background -->
<div class="bg-white bg-gray-50 bg-blue-500 bg-transparent">

<!-- Text -->
<p class="text-gray-900 text-gray-500 text-blue-600">

<!-- Border -->
<div class="border border-gray-200 border-red-500">

<!-- Ring (focus outline) -->
<button class="ring-2 ring-blue-500 ring-offset-2">

<!-- Shadow with color -->
<div class="shadow-lg shadow-blue-500/30">

<!-- Inset ring -->
<input class="inset-ring inset-ring-gray-300 focus:inset-ring-blue-500">

<!-- SVG fill / stroke -->
<svg class="fill-blue-500 stroke-blue-700">

<!-- Outline -->
<div class="outline outline-black/5">

<!-- Decoration (underline color) -->
<a class="underline decoration-blue-500">

<!-- Accent (checkbox/radio) -->
<input type="checkbox" class="accent-blue-500">

<!-- Caret -->
<input class="caret-pink-500">
```

## Opacity Modifier

Append `/[opacity]` to any color utility:

```html
<!-- Percentage values -->
<div class="bg-sky-500/10">    <!-- 10% opacity -->
<div class="bg-sky-500/25">    <!-- 25% -->
<div class="bg-sky-500/50">    <!-- 50% -->
<div class="bg-sky-500/75">    <!-- 75% -->

<!-- Arbitrary opacity -->
<div class="bg-pink-500/[71.37%]">
<div class="text-blue-500/(--my-alpha)">   <!-- CSS variable -->

<!-- Works with all color utilities -->
<div class="border-red-500/20 shadow-black/5 ring-blue-500/30">
```

## Dark Mode Colors

```html
<div class="bg-white dark:bg-gray-900">
<p class="text-gray-900 dark:text-white">
<p class="text-gray-600 dark:text-gray-300">
<button class="bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-500">

<!-- Borders and rings -->
<div class="border-gray-200 dark:border-gray-700">
<input class="ring-gray-300 dark:ring-gray-600">

<!-- Common dark mode palette -->
<!-- Light: gray-50/100 bg, gray-900 text, gray-200 borders -->
<!-- Dark:  gray-900/950 bg, gray-50 text, gray-700/800 borders -->
```

## Custom Colors

```css
@import "tailwindcss";

@theme {
  /* Add to existing palette */
  --color-brand-50: oklch(0.97 0.02 240);
  --color-brand-100: oklch(0.94 0.04 240);
  --color-brand-500: oklch(0.65 0.20 240);
  --color-brand-600: oklch(0.55 0.22 240);
  --color-brand-900: oklch(0.25 0.10 240);

  /* Simple named color */
  --color-mint: oklch(0.85 0.12 168);

  /* Semantic alias */
  --color-success: oklch(0.72 0.16 142);
  --color-warning: oklch(0.80 0.15 70);
  --color-error: oklch(0.65 0.22 25);
}
```

```html
<button class="bg-brand-500 hover:bg-brand-600 text-white">
<span class="text-success">Saved!</span>
<p class="text-error">Something went wrong</p>
```

## OKLCH Color Format

All v4 colors use OKLCH (Oklab-based cylindrical LCH):

```css
/* oklch(lightness chroma hue) */
oklch(0.637 0.237 25.33)   /* red-500 */
oklch(0.546 0.245 262.88)  /* blue-600 */
oklch(0.130 0.028 261.69)  /* gray-950 */

/* With alpha */
oklch(0.65 0.20 240 / 50%)
```

**Benefits over hex/hsl:**
- Perceptually uniform (equal chroma feels equal across hues)
- Wider color gamut (P3 displays)
- Better lightness scaling across shades

## Semantic Color System (shadcn pattern)

```css
:root {
  --background: oklch(1 0 0);        /* white */
  --foreground: oklch(0.145 0 0);    /* near-black */
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --border: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --border: oklch(0.269 0 0);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-border: var(--border);
  --color-ring: var(--ring);
}
```

```html
<div class="bg-background text-foreground">
<button class="bg-primary text-primary-foreground hover:bg-primary/90">
<p class="text-muted-foreground">
<div class="border-border ring-ring">
```

## --alpha() Function

Adjust opacity of a CSS variable color in custom CSS:

```css
.element {
  background: --alpha(var(--color-blue-500) / 10%);
  /* compiles to: color-mix(in oklab, var(--color-blue-500) 10%, transparent) */
}
```

## light-dark() Function

```html
<div class="bg-[light-dark(var(--color-white),var(--color-gray-950))]">
  <!-- white in light mode, gray-950 in dark mode -->
</div>
```
