# shadcn/ui — Installation & Tailwind v4

shadcn/ui is a collection of copy-paste components built with Radix UI primitives and Tailwind CSS. Components live in your codebase (not a package) so you own and customize them.

## Quick Start (New Project)

```bash
# Create new project with Tailwind + shadcn pre-configured
pnpm create @tanstack/start@latest --tailwind --add-ons shadcn

# Or with Next.js
pnpm create next-app@latest my-app --tailwind
```

## Manual Installation (Existing Project)

### 1. Install dependencies

```bash
# Core
pnpm add tailwindcss @tailwindcss/vite
pnpm add class-variance-authority clsx tailwind-merge
pnpm add tw-animate-css

# Radix UI (installed per-component, but lucide for icons)
pnpm add lucide-react
```

### 2. Initialize shadcn

```bash
pnpm dlx shadcn@latest init
```

This creates:
- `components.json` — shadcn config
- Updates `globals.css` with CSS variables
- Creates `src/lib/utils.ts` with `cn()` helper
- Creates `src/components/ui/` directory

### 3. globals.css (Tailwind v4 format)

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:where(.dark, .dark *));

@theme inline {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.205 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.556 0 0);
}

@layer base {
  * { @apply border-border outline-ring/50; }
  body { @apply bg-background text-foreground; }
}
```

### 4. components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "tailwind": {
    "config": "",
    "css": "src/styles/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

### 5. cn() utility

```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Adding Components

```bash
# Add individual components
pnpm dlx shadcn@latest add button
pnpm dlx shadcn@latest add card dialog input form
pnpm dlx shadcn@latest add dropdown-menu select toast

# Add all at once
pnpm dlx shadcn@latest add --all
```

## Using Components

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

function LoginForm() {
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Sign in</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="you@example.com" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" />
        </div>
        <Button className="w-full">Sign in</Button>
      </CardContent>
    </Card>
  )
}
```

## Theming with CSS Variables

Customize the theme by editing the CSS variables in `globals.css`:

```css
:root {
  /* Change primary color */
  --primary: oklch(0.65 0.2 240);           /* blue */
  --primary-foreground: oklch(0.98 0 0);

  /* Change border radius */
  --radius: 0.25rem;                         /* sharp corners */
  /* or */
  --radius: 1rem;                            /* very rounded */
}
```

Use the [shadcn/ui themes page](https://ui.shadcn.com/themes) to generate custom color palettes.

## Tailwind v4 Migration Notes

### What changed from v3

- HSL colors → OKLCH: `hsl(210 40% 98%)` → `oklch(0.97 0.01 210)`
- `@layer base` → variables now at `:root` / `.dark` level
- `tailwindcss-animate` → `tw-animate-css` (different import)
- `forwardRef` removed from components (React 19)
- `data-slot` attributes added to all Radix primitives
- `size-*` replaces `w-* h-*` for square elements

### Migrating existing v3 setup

```css
/* Old v3 globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;      /* HSL without hsl() */
    --primary: 222.2 47.4% 11.2%;
  }
}

/* New v4 globals.css */
@import "tailwindcss";
@import "tw-animate-css";

:root {
  --background: oklch(1 0 0);    /* OKLCH */
  --primary: oklch(0.18 0.04 240);
}

@theme inline {
  --color-background: var(--background);
  --color-primary: var(--primary);
}
```

## Component Customization

Since components are in your codebase, edit them directly:

```tsx
// src/components/ui/button.tsx
// Add a new variant
const buttonVariants = cva(
  "inline-flex items-center justify-center ...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        // Add your own:
        brand: "bg-brand-500 text-white hover:bg-brand-600",
      },
    },
  }
)
```

```html
<Button variant="brand">Custom button</Button>
```

## Available Components

**Layout**: Aspect Ratio, Separator, Scroll Area
**Forms**: Button, Checkbox, Form, Input, Label, Radio Group, Select, Slider, Switch, Textarea, Toggle, Toggle Group
**Overlays**: Alert Dialog, Dialog, Drawer, Popover, Sheet, Tooltip
**Navigation**: Breadcrumb, Command, Dropdown Menu, Menubar, Navigation Menu, Pagination, Tabs
**Data**: Accordion, Avatar, Badge, Calendar, Card, Carousel, Chart, Collapsible, Data Table, Date Picker, Table
**Feedback**: Alert, Progress, Skeleton, Sonner (toast), Toast (deprecated)
**Other**: Hover Card, Input OTP, Resizable, Sidebar
