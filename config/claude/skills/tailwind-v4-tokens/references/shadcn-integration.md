# shadcn/ui Integration

shadcn/ui is the default component library for this stack's opinion. Its design-token vocabulary (`background`, `foreground`, `primary`, `muted`, `accent`, `destructive`, `border`, `input`, `ring`, `card`, `popover`) matches this skill's token set exactly — by design.

## Install in a TanStack Start project

```sh
bunx shadcn@latest init
```

When prompted, choose:
- **Style**: `new-york` (more opinionated borders and spacing) or `default`
- **Base color**: aligns with the token set — pick one and let the CLI write tokens into your CSS entry
- **CSS variables**: **yes** (this enables the token pattern)

This creates:
- `components.json` — config
- Updates your CSS entry with semantic token variables
- Installs `tailwind-merge`, `clsx`, `class-variance-authority`

## Adding components

```sh
bunx shadcn@latest add button card dialog input
```

Components land in `src/components/ui/`. Treat them as *yours* — edit freely. Do not wrap them in higher-order components just to "skin" them; edit in place.

## Composition rules (the shadcn way)

- **Forms**: use `Form`, `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormMessage` together. Don't hand-roll with `<label>` + `<input>`.
- **Option groups**: prefer `ToggleGroup` / `RadioGroup` over custom button rows.
- **Field groups**: prefer `FieldGroup` (when available) for labelled clusters.
- **Icons**: use `lucide-react`, imported per-icon. Never inline SVG in a component.

## `data-slot` attributes

shadcn components expose `data-slot` attributes (`data-slot="label"`, `data-slot="description"`). Use them for:
- Structural verification in tests
- Style overrides via `[data-slot="label"]` selectors — avoid deep child selectors

## Composition: `cn` helper

Always compose classes with `cn`:

```tsx
import { cn } from '@/lib/utils'

<button className={cn(
  'bg-primary text-primary-foreground',
  'hover:bg-primary/90',
  disabled && 'opacity-50',
  className,
)}/>
```

`cn` is `clsx + tailwind-merge` — it deduplicates conflicting utilities so the last one wins predictably.

## What not to do

- Do not install a second component library (MUI, Chakra, Mantine) alongside shadcn — tokens will collide.
- Do not override shadcn primitives by wrapping — edit the component file directly.
- Do not skip the CLI and hand-write shadcn-style components; the CLI keeps versions in sync.

## Canonical source

- https://ui.shadcn.com/docs/installation
- https://ui.shadcn.com/docs/theming
- https://ui.shadcn.com/docs/skills
