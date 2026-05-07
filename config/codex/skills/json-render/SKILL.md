---
name: json-render
description: "Use when working with json-render packages or generated JSON UI specs: @json-render/core catalogs, React rendering, shadcn registries, React Email rendering, code generation, AI-generated UI, streaming JSONL UI patches, or Bun/TanStack Start generative UI routes. Prefer Bun commands and load only the package-specific reference needed."
---

# json-render

Use this skill to add or modify json-render integrations. json-render is a catalog-first generative UI framework: the model emits constrained JSON specs, while the app owns the component catalog, registry, action handlers, state, and rendering.

## Local Defaults

- Prefer Bun package commands. Do not translate upstream `npm install` examples unless the project is not a Bun project.
- In TanStack Start projects, also use the `bun-tanstack-start` skill. Keep json-render output inside route content; do not regenerate `src/routes/__root.tsx` or the global app shell.
- Zod is allowed for json-render catalog definitions because `defineCatalog` component and action schemas use Zod. Keep Effect Schema for TanStack server function inputs, route loader inputs, environment config, domain validation, and business logic.
- Use runtime rendering for interactive generated UIs. Use codegen only when the user explicitly wants exported source files or a custom exporter.
- Treat specs as data. Never ask the model to generate arbitrary React code for runtime execution.

## Reference Map

- `references/json-render-core.md`: `defineCatalog`, prompts, specs, streaming patches, prop expressions, state, validation.
- `references/json-render-react.md`: React renderer, providers, registries, events, bindings, TanStack Start route layout.
- `references/json-render-shadcn.md`: prebuilt shadcn component definitions and implementations for Tailwind apps.
- `references/json-render-react-email.md`: render JSON specs to HTML or plain-text email with React Email.
- `references/json-render-codegen.md`: traverse specs and generate source files from json-render trees.

## Bun Install Recipes

React web runtime:

```sh
bun add @json-render/core @json-render/react zod
```

React web with shadcn components:

```sh
bun add @json-render/core @json-render/react @json-render/shadcn zod
```

AI streaming:

```sh
bun add ai
```

React Email:

```sh
bun add @json-render/core @json-render/react-email @react-email/components @react-email/render
```

Codegen:

```sh
bun add @json-render/codegen
```

## TanStack Start Shape

For generated React UI in a Bun + TanStack Start app, prefer this file layout:

```text
src/lib/json-render/catalog.ts    # server-safe catalog and prompt generation
src/lib/json-render/registry.tsx  # React component registry
src/routes/api/generate.tsx       # streaming server route returning Response
src/routes/generative-ui.tsx      # route component using useUIStream + Renderer
```

Use a TanStack server route for streaming APIs because json-render and the AI SDK return a `Response` stream. Use Effect for surrounding app-domain work such as auth, persistence, audits, database reads, and policy checks, but do not buffer a streaming AI response just to wrap it.

## Workflow

1. Inspect `package.json`, lockfiles, route structure, and existing UI/component conventions.
2. Load only the relevant reference files from the map above.
3. Install packages with `bun add`.
4. Define a minimal catalog first. Add components deliberately; do not expose a whole design system unless the user needs it.
5. Put server-safe catalog imports in server/shared files and React component implementations in `*.tsx` registry files.
6. Wire action handlers explicitly. Built-in React actions such as state updates can remain built-in; app-domain actions need handlers.
7. Verify with the project checks. For TanStack Start, default to `bun run build` plus the app's typecheck/lint/test scripts when present.

## Sources

- https://json-render.dev/docs
- https://json-render.dev/docs/installation
- https://json-render.dev/docs/quick-start
- https://json-render.dev/docs/skills
- https://github.com/vercel-labs/json-render/tree/main/skills
