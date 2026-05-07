# json-render Core

Use this reference for `@json-render/core`: schemas, catalogs, prompt generation, specs, streaming patches, prop expressions, validation, and framework-agnostic state.

## Install

```sh
bun add @json-render/core zod
```

Renderer packages usually bring their own schema. For React, import the schema from `@json-render/react/schema`; for React Email, use the React Email schema exports.

## Catalog Pattern

The catalog is the guardrail. It declares the component and action names that generated specs may use.

```ts
import { defineCatalog } from "@json-render/core"
import { schema } from "@json-render/react/schema"
import { z } from "zod"

export const catalog = defineCatalog(schema, {
  components: {
    Card: {
      props: z.object({
        title: z.string(),
        description: z.string().nullable(),
      }),
      slots: ["default"],
      description: "Container for a related UI section",
    },
    Metric: {
      props: z.object({
        label: z.string(),
        value: z.union([z.string(), z.number()]),
        format: z.enum(["currency", "percent", "number"]).nullable(),
      }),
      description: "Single KPI or statistic",
    },
  },
  actions: {
    export_data: {
      params: z.object({ format: z.enum(["csv", "json"]) }),
      description: "Export the currently displayed data",
    },
  },
})
```

Generate the model system prompt from the catalog:

```ts
const system = catalog.prompt({
  customRules: [
    "Use Stack for vertical grouping.",
    "Prefer concise labels over long paragraphs.",
  ],
})
```

## Spec Shape

Specs are data. The model should produce JSON that conforms to the selected schema and catalog. The common React-style shape is a root element plus an element tree or element map, depending on the renderer/schema version used by the installed package. Follow the installed package types and existing app examples when resolving the exact shape.

When editing an existing spec, prefer json-render's prompt helpers and edit modes rather than asking the model for arbitrary prose:

```ts
import { buildUserPrompt } from "@json-render/core"

const prompt = buildUserPrompt({
  prompt: "Add a filters section above the table.",
  currentSpec,
  state,
  editModes: ["patch", "merge"],
})
```

## Streaming

json-render streams UI as JSONL patch operations. Each line is a JSON Patch operation that incrementally builds or edits the spec.

```ts
import { createSpecStreamCompiler } from "@json-render/core"

const compiler = createSpecStreamCompiler()

for await (const chunk of stream) {
  const { result, newPatches } = compiler.push(chunk)
  // result is the current spec; newPatches are the applied changes.
}

const finalSpec = compiler.getResult()
```

In web apps, prefer renderer-specific hooks such as `useUIStream` from `@json-render/react` unless you need lower-level stream control.

## Dynamic Prop Expressions

Generated props may be static values or expressions resolved at render time:

- `{ "$state": "/path" }`: read a value from state.
- `{ "$bindState": "/path" }`: two-way bind a natural component prop such as `value`, `checked`, or `pressed`.
- `{ "$bindItem": "field" }`: bind to the current repeated item.
- `{ "$cond": condition, "$then": value, "$else": value }`: choose between values.
- `{ "$template": "Hello, ${/user/name}" }`: interpolate state paths into strings.
- `{ "$computed": "functionName", "args": { ... } }`: call a registered computed function.

Do not invent a generic `statePath` prop for two-way binding. Put `$bindState` on the component's natural value prop.

## Visibility

Visibility conditions are state-based:

```json
{ "$state": "/form/enabled" }
{ "$state": "/activeTab", "eq": "billing" }
{ "$state": "/showAdvanced", "not": true }
{ "$and": [{ "$state": "/signedIn" }, { "$state": "/role", "eq": "admin" }] }
```

Use helpers from `@json-render/core` when hand-authoring specs:

```ts
import { visibility } from "@json-render/core"

visibility.when("/signedIn")
visibility.eq("/activeTab", "billing")
visibility.and(visibility.when("/signedIn"), visibility.eq("/role", "admin"))
```

## Validation

json-render has validation check helpers for generated forms. These are UI validation checks, not a replacement for server-side validation.

```ts
import { check } from "@json-render/core"

check.required("Email is required")
check.email("Enter a valid email")
check.matches("/form/confirmPassword", "Passwords must match")
```

For TanStack Start server functions and loaders in this repo's preferred stack, still use Effect Schema at the server boundary.

## State Store

Use `createStateStore` for framework-agnostic state or to bridge to renderer providers:

```ts
import { createStateStore } from "@json-render/core"

const store = createStateStore({ count: 0 })
store.set("/count", 1)
store.subscribe(() => console.log(store.getSnapshot()))
```

## Source

Adapted from:

- https://github.com/vercel-labs/json-render/blob/main/skills/core/SKILL.md
- https://json-render.dev/docs/catalog
- https://json-render.dev/docs/streaming
- https://json-render.dev/docs/data-binding
