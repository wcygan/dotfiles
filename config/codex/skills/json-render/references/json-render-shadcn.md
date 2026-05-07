# json-render shadcn

Use this reference for `@json-render/shadcn`: prebuilt Tailwind/Radix-style component definitions and implementations for generated React UIs.

## Install

```sh
bun add @json-render/core @json-render/react @json-render/shadcn zod
```

The app must already have Tailwind configured. In this repo's Bun + TanStack Start stack, use the Tailwind v4 Vite setup from `bun-tanstack-start`.

## Entry Points

- `@json-render/shadcn/catalog`: catalog definitions. This is safe for server-side prompt generation.
- `@json-render/shadcn`: React implementations. Use from client/React registry files.

## Usage Pattern

Select components explicitly. Do not spread the whole component set into a catalog unless the user explicitly wants a broad playground.

```ts
// src/lib/json-render/catalog.ts
import { defineCatalog } from "@json-render/core"
import { schema } from "@json-render/react/schema"
import { shadcnComponentDefinitions } from "@json-render/shadcn/catalog"

export const catalog = defineCatalog(schema, {
  components: {
    Card: shadcnComponentDefinitions.Card,
    Stack: shadcnComponentDefinitions.Stack,
    Heading: shadcnComponentDefinitions.Heading,
    Text: shadcnComponentDefinitions.Text,
    Button: shadcnComponentDefinitions.Button,
    Input: shadcnComponentDefinitions.Input,
  },
  actions: {},
})
```

```tsx
// src/lib/json-render/registry.tsx
import { defineRegistry } from "@json-render/react"
import { shadcnComponents } from "@json-render/shadcn"
import { catalog } from "./catalog"

export const { registry } = defineRegistry(catalog, {
  components: {
    Card: shadcnComponents.Card,
    Stack: shadcnComponents.Stack,
    Heading: shadcnComponents.Heading,
    Text: shadcnComponents.Text,
    Button: shadcnComponents.Button,
    Input: shadcnComponents.Input,
  },
})
```

## Extending With App Components

Add local components only when the generated UI needs domain-specific surface area.

```tsx
import { z } from "zod"

const MetricProps = z.object({
  label: z.string(),
  value: z.string(),
  change: z.string().nullable(),
  changeType: z.enum(["positive", "negative", "neutral"]).nullable(),
})

const MetricDefinition = {
  props: MetricProps,
  description: "Dashboard metric with optional trend text",
}

const Metric = ({ props }: { props: z.infer<typeof MetricProps> }) => (
  <div className="rounded-md border p-4">
    <div className="text-sm text-muted-foreground">{props.label}</div>
    <div className="text-2xl font-semibold">{props.value}</div>
    {props.change ? <div data-change={props.changeType}>{props.change}</div> : null}
  </div>
)
```

Keep custom components small, typed, and hard to misuse. The catalog description should explain when the model should choose the component.

## Component Families

Common built-in component categories:

- Layout: `Card`, `Stack`, `Grid`, `Separator`.
- Navigation: `Tabs`, `Accordion`, `Collapsible`, `Pagination`.
- Overlay: `Dialog`, `Drawer`, `Tooltip`, `Popover`, `DropdownMenu`.
- Content: `Heading`, `Text`, `Image`, `Avatar`, `Badge`, `Alert`, `Carousel`, `Table`.
- Feedback: `Progress`, `Skeleton`, `Spinner`.
- Input: `Button`, `Link`, `Input`, `Textarea`, `Select`, `Checkbox`, `Radio`, `Switch`, `Slider`, `Toggle`, `ToggleGroup`, `ButtonGroup`.

## Built-In React Actions

The React schema handles state-oriented actions through `ActionProvider`. Do not redeclare these in catalog actions:

- `setState`
- `pushState`
- `removeState`
- `validateForm`

App-domain actions such as `save_report`, `submit_order`, or `export_data` should be declared in the catalog and implemented in handlers.

## Notes

- The shadcn implementations are bundled json-render components, not the app's local `components/ui` directory.
- All form inputs can use checks for UI validation and `validateOn` timing.
- Favor the smallest component vocabulary that solves the use case. A smaller catalog produces more predictable generated specs.

## Source

Adapted from:

- https://github.com/vercel-labs/json-render/blob/main/skills/shadcn/SKILL.md
- https://json-render.dev/docs/quick-start
- https://json-render.dev/docs/api/shadcn
