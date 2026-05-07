# json-render React

Use this reference for `@json-render/react`: rendering generated specs as React component trees, defining registries, wiring providers, handling actions, and streaming UI in a TanStack Start app.

## Install

```sh
bun add @json-render/core @json-render/react zod
```

For AI-generated streaming UIs:

```sh
bun add ai
```

## Catalog and Registry

The catalog is server-safe and tells the model what it can generate. The registry maps those component names to React implementations.

```ts
// src/lib/json-render/catalog.ts
import { defineCatalog } from "@json-render/core"
import { schema } from "@json-render/react/schema"
import { z } from "zod"

export const catalog = defineCatalog(schema, {
  components: {
    Card: {
      props: z.object({ title: z.string() }),
      slots: ["default"],
      description: "Card container with a heading",
    },
    Button: {
      props: z.object({
        label: z.string(),
        variant: z.enum(["primary", "secondary"]).nullable(),
      }),
      description: "Clickable button",
    },
  },
  actions: {
    submit_form: {
      params: z.object({ formId: z.string() }),
      description: "Submit a form by id",
    },
  },
})
```

```tsx
// src/lib/json-render/registry.tsx
import { defineRegistry } from "@json-render/react"
import { catalog } from "./catalog"

export const { registry, handlers } = defineRegistry(catalog, {
  components: {
    Card: ({ props, children }) => (
      <section className="rounded-md border p-4">
        <h2 className="text-lg font-semibold">{props.title}</h2>
        <div className="mt-3">{children}</div>
      </section>
    ),
    Button: ({ props, emit }) => (
      <button
        className="rounded-md border px-3 py-2"
        data-variant={props.variant ?? "primary"}
        onClick={() => emit("press")}
      >
        {props.label}
      </button>
    ),
  },
})
```

## Providers

Wrap the rendered tree with the providers for the features you use:

```tsx
import {
  ActionProvider,
  Renderer,
  StateProvider,
  ValidationProvider,
  VisibilityProvider,
} from "@json-render/react"
import { registry } from "~/lib/json-render/registry"

export function GeneratedUI({ spec }: { spec: unknown }) {
  return (
    <StateProvider initialState={{}}>
      <VisibilityProvider>
        <ActionProvider
          handlers={{
            submit_form: async (params) => {
              console.log("submit", params)
            },
          }}
        >
          <ValidationProvider customFunctions={{}}>
            <Renderer spec={spec} registry={registry} />
          </ValidationProvider>
        </ActionProvider>
      </VisibilityProvider>
    </StateProvider>
  )
}
```

If using an external state adapter, pass a store to `StateProvider` instead of `initialState`.

## Events and Actions

Components emit events. Specs map events to action bindings.

```tsx
Button: ({ props, emit }) => (
  <button onClick={() => emit("press")}>{props.label}</button>
)
```

```json
{
  "type": "Button",
  "props": { "label": "Save" },
  "on": { "press": { "action": "submit_form", "params": { "formId": "profile" } } }
}
```

Use `on("eventName")` instead of `emit` when a component needs metadata such as whether the default browser action should be prevented.

## Bound Props

Components receive resolved props. For two-way bound form props, use `useBoundProp` with the renderer's binding metadata.

```tsx
import { useBoundProp } from "@json-render/react"

Input: ({ element, bindings }) => {
  const [value, setValue] = useBoundProp<string>(
    element.props.value,
    bindings?.value,
  )

  return <input value={value ?? ""} onChange={(event) => setValue(event.target.value)} />
}
```

Generated specs should bind natural value props:

```json
{
  "type": "Input",
  "props": {
    "value": { "$bindState": "/form/email" },
    "placeholder": "Email"
  }
}
```

## TanStack Start Streaming Route

Use a server route for streaming generation. Keep the catalog import server-safe.

```tsx
// src/routes/api/generate.tsx
import { createFileRoute } from "@tanstack/react-router"
import { streamText } from "ai"
import { catalog } from "~/lib/json-render/catalog"
import { yourModel } from "~/server/ai"

export const Route = createFileRoute("/api/generate")({})

export const server = {
  POST: async ({ request }: { request: Request }) => {
    const { prompt, currentSpec } = await request.json()
    const context = currentSpec
      ? `\n\nCurrent UI spec:\n${JSON.stringify(currentSpec, null, 2)}`
      : ""

    const result = streamText({
      model: yourModel,
      system: catalog.prompt() + context,
      prompt,
    })

    return result.toTextStreamResponse()
  },
}
```

If this route also performs auth, policy checks, database reads, or persistence, use the repo's Effect boundary pattern for that domain work before returning the stream. Do not buffer the stream unless the user explicitly wants a non-streaming response.

## TanStack Start Client Route

```tsx
// src/routes/generative-ui.tsx
import { createFileRoute } from "@tanstack/react-router"
import {
  ActionProvider,
  Renderer,
  StateProvider,
  ValidationProvider,
  VisibilityProvider,
  useUIStream,
} from "@json-render/react"
import { registry } from "~/lib/json-render/registry"

export const Route = createFileRoute("/generative-ui")({
  component: GenerativeUIRoute,
})

function GenerativeUIRoute() {
  const { spec, isStreaming, error, send } = useUIStream({
    api: "/api/generate",
  })

  return (
    <StateProvider initialState={{}}>
      <VisibilityProvider>
        <ActionProvider handlers={{}}>
          <ValidationProvider customFunctions={{}}>
            <form
              onSubmit={(event) => {
                event.preventDefault()
                const formData = new FormData(event.currentTarget)
                send(String(formData.get("prompt") ?? ""))
              }}
            >
              <input name="prompt" />
              <button type="submit" disabled={isStreaming}>
                Generate
              </button>
            </form>
            {error ? <p>{error.message}</p> : null}
            <Renderer spec={spec} registry={registry} loading={isStreaming} />
          </ValidationProvider>
        </ActionProvider>
      </VisibilityProvider>
    </StateProvider>
  )
}
```

Adapt styling to the project. Do not introduce marketing-page layout or global-shell rewrites just to host generated UI.

## Source

Adapted from:

- https://github.com/vercel-labs/json-render/blob/main/skills/react/SKILL.md
- https://json-render.dev/docs/quick-start
- https://json-render.dev/docs/ai-sdk
- https://json-render.dev/docs/registry
