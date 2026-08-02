# Pi SDK patterns

This is a routing reference, not a substitute for the version-matched `sdk.md`.
Read the relevant section of that file before implementing.

## Minimal session

The current package documents this shape:

```typescript
import {
  createAgentSession,
  ModelRuntime,
  SessionManager,
} from "@earendil-works/pi-coding-agent";

const modelRuntime = await ModelRuntime.create();
const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  modelRuntime,
});

const unsubscribe = session.subscribe((event) => {
  if (
    event.type === "message_update" &&
    event.assistantMessageEvent.type === "text_delta"
  ) {
    process.stdout.write(event.assistantMessageEvent.delta);
  }
});

try {
  await session.prompt("What files are in the current directory?");
} finally {
  unsubscribe();
  session.dispose();
}
```

Keep `SessionManager.inMemory()` for ephemeral integrations unless persistence
is a deliberate requirement. If a project uses a different package scope, read
its installed package exports rather than copying this import unchanged.

## Session versus runtime

Use `AgentSession` for prompting, steering, follow-ups, event subscriptions,
model/thinking changes, compaction, abort, and disposal. Use
`createAgentSessionRuntime()` and `AgentSessionRuntime` when the active session
must be replaced or its cwd-bound services rebuilt. After replacement,
`runtime.session` is a new object: unsubscribe from the old session and attach
listeners again. Re-bind extensions when the API requires it.

## Events and queueing

Subscribe to events rather than scraping terminal output. At minimum, handle
`message_update` text deltas and `agent_end`; tolerate event types added by
newer releases. During streaming, choose deliberately:

- `steer()` interrupts the current direction after the current tool-call phase;
- `followUp()` waits until the current agent run stops.

Do not call `prompt()` during streaming without the version-documented
`streamingBehavior` option.

## Tools and resources

Use `tools: ["read", "grep", "find", "ls"]` for read-only sessions. The
documented built-ins also include `bash`, `edit`, and `write`; do not enable
those by default for review or documentation tasks.

Use `defineTool()` with a TypeBox schema for standalone custom tools and pass
them through `customTools`. If an extension must register tools, commands,
events, or UI, load it through a `ResourceLoader` instead. A default resource
loader discovers project resources from `cwd` and global resources from
`agentDir`; read the current SDK docs for the exact discovery paths.

## Models and credentials

`ModelRuntime` resolves models and credentials. These are separate questions:
model lookup can succeed even when authentication is unavailable. Prefer
`getAvailable()` when the integration needs models with valid authentication.
Runtime API-key overrides should be treated as transient and must never be
logged. For tests, inject in-memory credentials or a fake runtime where the
project’s API allows it.

## Choosing SDK, RPC, or CLI

| Need | Preferred surface |
| --- | --- |
| Embed agent behavior in a TypeScript process | SDK |
| Isolate the agent or control it from another language | RPC |
| Run one shell automation prompt | `pi -p` |
| Consume structured one-shot events | JSON mode |
| Use Pi's interactive terminal UI | Interactive CLI |

When process isolation, cancellation, or untrusted tool execution is a primary
requirement, do not choose the SDK just because it has a convenient API.
