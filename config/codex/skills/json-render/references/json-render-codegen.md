# json-render Codegen

Use this reference for `@json-render/codegen`: traversing specs, collecting dependencies, serializing props, and building custom source-code exporters.

## Install

```sh
bun add @json-render/codegen
```

Install renderer packages separately when generated code imports them:

```sh
bun add @json-render/core @json-render/react @json-render/shadcn zod
```

## When To Use

Use codegen when the user wants one of these outcomes:

- Export a generated UI into source files.
- Build a custom exporter for TanStack Start, Next.js, email templates, or design-system components.
- Inspect a spec to list used components, state paths, or actions.
- Convert a runtime spec into a reviewable artifact.

Do not use codegen for normal interactive generated UI. Runtime rendering with `Renderer` is simpler and preserves dynamic state/actions.

## Tree Traversal

```ts
import {
  collectActions,
  collectStatePaths,
  collectUsedComponents,
  traverseSpec,
} from "@json-render/codegen"

traverseSpec(spec, (element, key, depth, parent) => {
  console.log({ key, type: element.type, depth, parentType: parent?.type })
})

const components = collectUsedComponents(spec)
const statePaths = collectStatePaths(spec)
const actions = collectActions(spec)
```

Use these collectors before generating files so the exporter only imports what the spec uses.

## Prop Serialization

```ts
import {
  escapeString,
  serializePropValue,
  serializeProps,
} from "@json-render/codegen"

serializePropValue("hello")
serializePropValue({ $state: "/user/name" })
serializeProps({ title: "Dashboard", columns: 3, disabled: true })
escapeString('hello "world"')
```

Prefer library serialization helpers over ad hoc string concatenation. Generated code should format cleanly and preserve dynamic expression objects deliberately.

## Custom Exporter Shape

```ts
import type { CodeGenerator, GeneratedFile } from "@json-render/codegen"
import { collectUsedComponents, traverseSpec } from "@json-render/codegen"

export const tanStackStartPageGenerator: CodeGenerator = {
  generate(spec): GeneratedFile[] {
    const usedComponents = collectUsedComponents(spec)
    const files: GeneratedFile[] = []

    files.push({
      path: "src/routes/generated.tsx",
      content: renderRouteFile(spec, usedComponents),
    })

    return files
  },
}

function renderRouteFile(spec: unknown, usedComponents: Set<string>) {
  // Build imports, component JSX, and route declaration from the spec.
  return ""
}
```

## TanStack Start Export Guidance

- Generate route files under `src/routes/`; do not rewrite `src/routes/__root.tsx`.
- Import existing app components or json-render registries according to the user's requested output.
- Keep generated files deterministic. Stable order imports, elements, and object keys before writing.
- Use codegen for source export, not for executing untrusted model code.
- Run the app formatter and typecheck after writing generated files.

## Source

Adapted from:

- https://github.com/vercel-labs/json-render/blob/main/skills/codegen/SKILL.md
- https://json-render.dev/docs/code-export
