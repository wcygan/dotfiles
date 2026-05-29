# pi extensions

Extensions are TypeScript modules that hook pi's lifecycle and register tools, slash commands, CLI flags, keyboard shortcuts, UI, message renderers, and LLM providers. This is pi's main extension point — features pi omits on purpose (MCP, sub-agents, plan mode, permission gates, background bash) are meant to be built here. Doc: `packages/coding-agent/docs/extensions.md` (2600 lines — read it for the full surface). Examples live in `packages/coding-agent/examples/extensions/`.

## Discovery & loading

- Global: `~/.pi/agent/extensions/*.ts` or `~/.pi/agent/extensions/*/index.ts`
- Project: `.pi/extensions/*.ts` or `.pi/extensions/*/index.ts`
- Settings: `extensions: ["/path/to/ext.ts"]`
- CLI: `pi -e ./ext.ts` (repeatable); `--no-extensions` disables discovery but explicit `-e` still loads.
- Hot reload: `/reload`.

A directory extension with a `package.json` may declare npm deps and an entry point. Packages bundle extensions + skills + prompts + themes (`pi install <source>`).

## Shape

The module's **default export** is a factory `(pi: ExtensionAPI) => void | Promise<void>`. It may be `async` for one-time init (e.g. fetch a model list before startup — pi awaits the factory, so dynamic providers are ready for `pi --list-models`).

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "greet",
    label: "Greet",
    description: "Greet someone by name",
    parameters: Type.Object({ name: Type.String({ description: "Name" }) }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      return { content: [{ type: "text", text: `Hello, ${params.name}!` }] };
    },
  });

  pi.registerCommand("hello", {
    description: "Say hello",
    handler: async (args, ctx) => ctx.ui.notify(`Hello ${args || "world"}!`, "info"),
  });
}
```

## Registration API (on `pi`)

| Method | Registers |
|--------|-----------|
| `pi.registerTool(def)` | LLM-callable tool: `name,label,description,parameters` (Typebox), `async execute(id,params,signal,onUpdate,ctx)` → `{content:[{type:"text",text}], details?, terminate?}`; optional `renderCall/renderResult/promptSnippet/promptGuidelines` |
| `pi.registerCommand(name, opts)` | `/command`: `handler(args, ctx)`, optional `description`, `getArgumentCompletions(prefix)` |
| `pi.registerShortcut(combo, opts)` | keybinding: `handler(ctx)`, `description` |
| `pi.registerFlag(name, opts)` | CLI flag (`type`, `default`), read via `pi.getFlag(name)` |
| `pi.registerProvider(name, cfg)` | LLM provider/override (see local-models.md & custom-provider.md) |
| `pi.registerMessageRenderer(customType, renderer)` | custom rendering of persisted entries |

Also: `pi.sendMessage`/`pi.sendUserMessage` (inject messages, `deliverAs:"steer"|"followUp"|"nextTurn"`), `pi.appendEntry` (persist session-local state, not in LLM context), `pi.setSessionName`, `pi.setLabel` (bookmark for `/tree`), tool management (`getActiveTools/getAllTools/setActiveTools`), model/thinking control, `pi.exec`, `pi.events` (inter-extension bus), `pi.unregisterProvider`.

## Lifecycle events (`pi.on(name, handler)`)

Handlers receive `(event, ctx)` and can return an object to **block, modify, or inject** depending on the event.

- Session: `session_start`, `session_before_switch/fork/compact`, `session_shutdown`
- Agent/turn: `before_agent_start` (inject message / modify system prompt), `agent_start/end`, `turn_start/end`
- Messages: `message_start/update/end` (can replace the message — e.g. normalize provider overflow errors so pi auto-compacts; see custom-provider.md)
- Tools: `tool_call` (block / mutate input — this is where you build a permission gate), `tool_result` (modify), `tool_execution_start/update/end`
- Model/input: `model_select`, `thinking_level_select`, `input` (transform/handle/continue)
- Provider: `before_provider_request` (inspect/replace payload), `after_provider_response`
- Resources: `resources_discover` (contribute skill/prompt/theme paths)

`ctx` (`ExtensionContext`): `ui` (`select/confirm/input/editor`, `notify`, status, widgets, themes), `sessionManager`, `cwd`, `signal`, `getSystemPrompt()`, `compact()`, `getContextUsage()`, `isIdle()/abort()/shutdown()`. Command handlers get `ExtensionCommandContext` extras: `waitForIdle()`, `newSession()`, `fork()`, `switchSession()`, `navigateTree()`, `reload()`.

## Imports available to extensions

- `@earendil-works/pi-coding-agent` — `ExtensionAPI`, `ExtensionContext`, event/tool types, truncation helpers
- `typebox` — tool parameter schemas
- `@earendil-works/pi-ai` — provider/stream types (`StringEnum`, `createAssistantMessageEventStream`, `calculateCost`, …)
- `@earendil-works/pi-tui` — TUI components
- `node:*`

## Custom providers via extension (vs models.json)

Use `pi.registerProvider` when you need OAuth/SSO (`oauth: { login, refreshToken, getApiKey, modifyModels? }`, integrates with `/login`) or a non-standard streaming API (implement `streamSimple` following the `start → text/thinking/toolcall events → done/error` pattern). For plain OpenAI/Anthropic/Google-compatible endpoints, prefer `models.json` — it needs no code. Full provider config and stream contract: `packages/coding-agent/docs/custom-provider.md`.
