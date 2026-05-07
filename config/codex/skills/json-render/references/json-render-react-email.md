# json-render React Email

Use this reference for `@json-render/react-email`: rendering JSON specs to HTML or plain-text email using React Email components.

## Install

```sh
bun add @json-render/core @json-render/react-email @react-email/components @react-email/render
```

Add `zod` if the project does not already have it and you are defining custom catalog components:

```sh
bun add zod
```

When sending email through Resend, also use the `resend`, `resend-cli`, `react-email`, and `email-best-practices` skills if they are available.

## Server-Safe Imports

For schema and catalog definitions without pulling in React component implementations, use server-safe entry points.

```ts
import { defineCatalog } from "@json-render/core"
import {
  schema,
  standardComponentDefinitions,
} from "@json-render/react-email/server"

export const emailCatalog = defineCatalog(schema, {
  components: standardComponentDefinitions,
  actions: {},
})
```

If you need custom component definitions, import definitions from the catalog entry point and use Zod for custom props.

## Render HTML

```ts
import { renderToHtml, renderToPlainText } from "@json-render/react-email"

const html = await renderToHtml(spec, {
  state: {
    user: { firstName: "Ada" },
  },
})

const text = await renderToPlainText(spec)
```

Use `state` in render options when the spec contains `$state`, `$template`, `$cond`, or repeat expressions.

## Email Spec Rules

- The root element should be `Html`.
- `Html` should contain `Head` and `Body`.
- Put layout content inside `Container` within `Body`.
- Keep the main container width constrained, usually around `600px`.
- Use inline styles or React Email style props. Do not rely on external CSS.
- Keep generated email actions conservative. Emails render to static HTML; interactivity should be links to app routes, not client-side handlers.

Example shape:

```json
{
  "root": "html",
  "elements": {
    "html": {
      "type": "Html",
      "props": { "lang": "en" },
      "children": ["head", "body"]
    },
    "head": { "type": "Head", "props": {}, "children": [] },
    "body": {
      "type": "Body",
      "props": { "style": { "backgroundColor": "#f6f9fc" } },
      "children": ["container"]
    },
    "container": {
      "type": "Container",
      "props": { "style": { "maxWidth": "600px", "margin": "0 auto" } },
      "children": ["heading", "message"]
    },
    "heading": {
      "type": "Heading",
      "props": { "text": "Welcome" },
      "children": []
    },
    "message": {
      "type": "Text",
      "props": { "text": { "$template": "Hi ${/user/firstName}, thanks for signing up." } },
      "children": []
    }
  }
}
```

## Custom Registry

Use a custom registry when the standard email components are not enough.

```tsx
import { defineCatalog } from "@json-render/core"
import { defineRegistry, renderToHtml, schema } from "@json-render/react-email"
import { standardComponentDefinitions } from "@json-render/react-email/catalog"
import { Text } from "@react-email/components"
import { z } from "zod"

const catalog = defineCatalog(schema, {
  components: {
    ...standardComponentDefinitions,
    Alert: {
      props: z.object({
        message: z.string(),
        variant: z.enum(["info", "success", "warning"]).nullable(),
      }),
      description: "Highlighted email-safe alert text",
    },
  },
  actions: {},
})

const { registry } = defineRegistry(catalog, {
  components: {
    Alert: ({ props }) => (
      <Text style={{ padding: "12px", backgroundColor: "#f2f4f8" }}>
        {props.message}
      </Text>
    ),
  },
})

const html = await renderToHtml(spec, { registry })
```

Only spread all standard email definitions when building a general email generator. For product-specific transactional emails, select a smaller component set.

## Source

Adapted from:

- https://github.com/vercel-labs/json-render/blob/main/skills/react-email/SKILL.md
- https://json-render.dev/docs/installation
- https://json-render.dev/docs/api/react-email
