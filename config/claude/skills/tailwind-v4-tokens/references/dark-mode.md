# Dark Mode via CSS Variable Redefinition

The single biggest consistency failure in Tailwind codebases: `dark:bg-slate-900 dark:text-slate-100` sprinkled across every component. The correct approach is to **redefine the token variables once** and let every `bg-background` / `text-foreground` automatically flip.

## Pattern

```css
@theme {
  --color-background: oklch(98% 0.005 265);
  --color-foreground: oklch(18% 0.02 265);
  --color-muted:      oklch(94% 0.01 265);
  /* ... */
}

/* Either media-query or class-based — pick one */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: oklch(15% 0.02 265);
    --color-foreground: oklch(95% 0.02 265);
    --color-muted:      oklch(22% 0.02 265);
  }
}

/* Or class-based for user-togglable themes */
.dark {
  --color-background: oklch(15% 0.02 265);
  --color-foreground: oklch(95% 0.02 265);
  --color-muted:      oklch(22% 0.02 265);
}
```

Now `<div className="bg-background text-foreground">` works in both modes with zero `dark:` prefixes.

## When `dark:` is still OK

For **opacity** or **intensity** differences that aren't captured by a token flip:

```tsx
<img className="opacity-90 dark:opacity-70" />
```

But for colors: never.

## Toggling

If the app has a theme toggle, apply the `.dark` class to `<html>`. In TanStack Start, do this in `__root.tsx`:

```tsx
export const Route = createRootRoute({
  component: () => {
    const theme = useTheme()  // your hook
    return (
      <html className={theme === 'dark' ? 'dark' : ''}>
        <body><Outlet /></body>
      </html>
    )
  },
})
```

Persist the choice in a cookie so SSR renders with the right class server-side and avoids flash-of-wrong-theme.

## Grep-level enforcement

Catch drift early:

```sh
rg "dark:(bg|text|border)-(slate|gray|zinc|neutral|stone)-" src/
```

Any hit is a smell — it's styling a specific scale instead of letting tokens flip.
