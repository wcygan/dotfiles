# Pi extensions

Extensions are TypeScript modules that can register tools, commands, flags,
shortcuts, UI, renderers, providers, and lifecycle hooks.

Because the API evolves, read the version-matched
`packages/coding-agent/docs/extensions.md`, its examples directory, and the
extension type definitions before implementing an extension.

## When to use an extension

Use an extension when behavior requires executable integration:

- a model-callable tool;
- a slash command or keyboard shortcut;
- a CLI flag;
- lifecycle interception;
- UI status, prompts, or widgets;
- a custom provider or OAuth flow; or
- communication between extensions.

Use a Pi skill instead when reusable instructions plus scripts or references are
enough.

## Discovery and loading

Common locations are global and project-level extension directories under the
Pi config roots. Extensions can also be selected through settings, a package, or
an explicit CLI flag. Confirm current paths and flags with the installed docs.

Use explicit loading and disabled discovery for isolated testing. Run `/reload`
only after verifying that the installed version supports it.

## Module shape

An extension commonly default-exports a factory that receives the extension API:

```typescript
import type { ExtensionAPI } from "<installed-pi-package>";
import { Type } from "typebox";

export default function register(extension: ExtensionAPI) {
  extension.registerTool({
    name: "greet",
    label: "Greet",
    description: "Greet someone by name",
    parameters: Type.Object({
      name: Type.String({ description: "Name" }),
    }),
    async execute(_callId, parameters) {
      return {
        content: [
          {
            type: "text",
            text: `Hello, ${parameters.name}!`,
          },
        ],
      };
    },
  });
}
```

Replace the package placeholder with the scope used by the installed Pi package
or matching source checkout.

## API map

Version-dependent registration methods typically cover:

- tools;
- commands;
- shortcuts;
- flags;
- providers; and
- message renderers.

Lifecycle hooks commonly cover session, agent, turn, message, tool, model,
provider-request, and resource-discovery events. Some hooks can block or modify
behavior, so treat them as security-sensitive code.

## Implementation workflow

1. Identify the installed/source version.
2. Find the closest official example.
3. Read the relevant type definition rather than guessing a signature.
4. Keep the extension's authority narrow.
5. Load it explicitly in an isolated Pi config and disposable checkout.
6. Exercise success, failure, cancellation, and reload paths.
7. Run the source package's focused tests when modifying Pi itself.

Do not install an extension globally or add it to settings merely to test it.
