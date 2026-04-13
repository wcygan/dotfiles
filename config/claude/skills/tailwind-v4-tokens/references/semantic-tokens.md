# Semantic Tokens: NEVER / INSTEAD Catalog

## Colors

| NEVER | INSTEAD |
|---|---|
| `bg-white` | `bg-background` |
| `bg-black` | `bg-foreground` |
| `bg-gray-100` | `bg-muted` |
| `text-gray-500` | `text-muted-foreground` |
| `bg-blue-500` | `bg-primary` |
| `text-blue-600` | `text-primary` |
| `bg-red-500` | `bg-destructive` |
| `text-red-600` | `text-destructive` |
| `border-gray-200` | `border-border` |
| `ring-blue-500` | `ring-ring` |
| `#3b82f6` | `var(--color-primary)` or `bg-primary` |

## Spacing

| NEVER | INSTEAD |
|---|---|
| `p-[18px]` | Declare `--spacing-card: 1.125rem`; use `p-card` |
| `gap-[7px]` | Use a token from the standard scale |
| Mixed `p-4 m-5 gap-6` without rationale | Pick a small set of spacing tokens and reuse them |

## Radius

| NEVER | INSTEAD |
|---|---|
| `rounded-[6px]` | `rounded` (mapped to `--radius`) |
| `rounded-[14px]` | `rounded-lg` (mapped to `--radius-lg`) |
| Mixing `rounded-md` and `rounded-xl` per-component without a system | Declare the allowed set in `@theme` and stick to it |

## Typography

| NEVER | INSTEAD |
|---|---|
| `font-['Inter']` inline | Add to `@theme` as `--font-sans` or `--font-display` |
| `text-[22px]` | `text-xl` or declare `--text-display-sm` |
| Mixing display and body in the same component unchecked | Deliberate pairing — display for headings, sans for body |

## Why it matters

Every inline hex / arbitrary value is a fork in the design system. Six months later, "update the brand color" turns into a grep-and-replace across the codebase instead of one variable change.

Enforce by grep — see [validation](./validation.md).
