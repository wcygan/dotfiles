# Pairing Pi SDK with Effect v4

Use this reference when a TypeScript application already uses Effect v4, or
when Pi SDK work needs typed errors, dependency injection, scoped cleanup,
concurrency control, configuration, or deterministic tests.

Read the project-pinned Effect version and the applicable branches of the
[Effect skill](../../effect/SKILL.md) before treating these patterns as exact
API guidance. This reference explains the boundary between the two libraries;
it is not a replacement for Pi's version-matched `sdk.md`.

## Why the pairing is useful

Pi's SDK owns agent-specific concerns: model/runtime resolution, session state,
prompting, tool execution, resource loading, and event streaming. Effect is a
good application boundary around those concerns because it can provide:

- typed domain errors instead of leaking arbitrary promise failures;
- `Context.Service` and `Layer` for replacing Pi in tests or wiring different
  runtimes in different environments;
- scoped acquisition and finalization for `AgentSession.dispose()` and event
  subscriptions;
- `Queue`, `PubSub`, `Deferred`, and fibers for event delivery and cancellation;
- `Config` and redacted values for model/provider configuration;
- `Schedule`, timeouts, and structured retry policies where retrying is safe;
- `it.effect`, test layers, and `TestClock` without sleeping or invoking a live
  model for every unit test.

The useful division is: Pi is the agent adapter; Effect is the application
orchestration and lifecycle boundary.

## Recommended boundary

Keep raw Pi types inside one adapter module. Expose application-shaped methods
through a service rather than passing `AgentSession` through handlers,
repositories, or unrelated domain modules.

```ts
export interface PiAgentInterface {
  readonly prompt: (text: string) => Effect.Effect<string, PiAgentError>
  readonly steer: (text: string) => Effect.Effect<void, PiAgentError>
  readonly followUp: (text: string) => Effect.Effect<void, PiAgentError>
}

export class PiAgent extends Context.Service<PiAgent, PiAgentInterface>()(
  "@app/PiAgent",
) {}
```

The exact service shape should follow the application. Keep Pi-specific details
such as `AgentSessionEvent`, model objects, and `PromptOptions` at the adapter
boundary unless callers genuinely need them.

## Layer the session lifecycle

Create `ModelRuntime` and `AgentSession` in a `Layer.effect` or equivalent
effectful service constructor. Treat a session as mutable state with an explicit
owner; do not casually share one session across concurrent requests.

Use scoped acquisition/finalization for resources:

```ts
const makeSession = Effect.acquireRelease(
  Effect.tryPromise(() => createPiSession()),
  ({ session }) => Effect.sync(() => session.dispose()),
)

export const layer = Layer.effect(
  PiAgent,
  Effect.gen(function* () {
    const runtime = yield* makeModelRuntime
    const session = yield* makeSession(runtime)
    return PiAgent.of(makePiAgentOperations(session))
  }),
)
```

The snippet is an architectural sketch: verify the installed Pi and Effect
declarations before copying helper names or error handling. For short-lived or
test-only integrations, prefer Pi's `SessionManager.inMemory()` and dispose the
session in the scope that owns it.

If the integration subscribes to events, make the subscription part of the
same scope. Unsubscribe during finalization; do not leave callbacks attached to
an old session after `AgentSessionRuntime` replaces `runtime.session`.

## Turn events into Effect values

Pi delivers streaming events through a callback. Effect applications usually
need an explicit bridge:

- use a `Queue` for ordered event delivery to one consumer;
- use a `PubSub` when several consumers need the same stream;
- use a `Deferred` for one-shot readiness, completion, or terminal failure;
- use a scoped fiber for long-lived event consumption;
- keep the Pi callback small and non-blocking; enqueue or signal, then return.

Define the terminal condition explicitly. `message_update` text deltas are not
the same as `agent_end`, and tool execution events may contain errors even when
the process itself remains alive. Preserve enough event data to distinguish a
normal completion, an aborted run, a model/provider failure, and a tool error.

When an application only needs the final answer, keep the event bridge private
and expose a single `Effect` operation. When it needs live progress, expose a
typed domain event stream rather than the entire Pi event union.

## Typed errors and retry boundaries

Map Pi failures at the adapter boundary into errors meaningful to the
application, for example:

- configuration or credential errors during layer acquisition;
- model-resolution errors before a prompt is accepted;
- prompt or agent-run errors for an accepted request;
- tool-execution errors with the tool name and safe diagnostic context;
- interruption or cancellation as a distinct outcome when the caller needs to
  report it differently.

Use the Effect skill's tagged error conventions. Do not turn every failure into
success, and do not retry an accepted prompt blindly: a model may have already
executed tools or produced external side effects. Apply `Schedule` or an
`Effect.fn` transform only around a proven idempotent boundary, such as a
bounded connection/setup attempt or a separately retryable read-only operation.

## Configuration and credentials

Use Effect `Config` to resolve application configuration, and keep provider
secrets redacted. Pass resolved values into the Pi runtime through the supported
SDK options or runtime credential store. Do not read `process.env` directly in
business logic, print `auth.json`, or put API keys in a layer default.

Keep the distinction clear:

1. the requested model can be resolved;
2. credentials may or may not be available;
3. the provider endpoint may or may not be reachable.

Those are separate effects and should remain separately observable in
diagnostics. A test layer should be able to provide a fake runtime or fake
`PiAgent` without requiring live credentials.

## Testing strategy

Use the real Pi SDK only in a small integration suite. Most application tests
should depend on the Effect service and provide a stateful test layer that can:

- record prompts and steering/follow-up messages;
- emit controlled progress and terminal events through a `Queue`;
- fail the next operation with a typed Pi adapter error;
- verify disposal and cancellation behavior.

Prefer `it.effect` and deterministic synchronization with `Deferred`, `Queue`,
`Latch`, `Ref`, or explicit test hooks. Use `TestClock` for timeout/retry logic.
Reserve `it.live` for tests whose purpose is specifically to verify the live
Pi provider, model, tools, or endpoint.

## Choosing the boundary

| Requirement | Pairing guidance |
| --- | --- |
| One prompt from a CLI or script | Use Pi print/JSON mode; Effect may be unnecessary |
| In-process app integration | Wrap SDK session/runtime in an Effect service and layer |
| Live UI progress | Bridge Pi events into a typed Queue/PubSub stream |
| Many concurrent callers | Own and serialize mutable sessions explicitly, or create one per operation |
| Process isolation or another language | Prefer Pi RPC with an Effect adapter around the subprocess |
| Unit tests without provider access | Provide a test layer; do not launch a live model |

The pairing adds value when lifecycle, failure, concurrency, configuration, or
testability matter. It is unnecessary ceremony for a single disposable prompt
whose process and error boundary are already sufficient.

## Review checklist

- [ ] Pi SDK imports and event shapes match the installed package docs/types.
- [ ] Raw Pi session state is isolated behind one Effect service boundary.
- [ ] Session disposal and event unsubscription are scoped.
- [ ] Event streams have explicit ownership, backpressure, and terminal semantics.
- [ ] Typed errors preserve configuration, provider, prompt, tool, and abort distinctions.
- [ ] Retries are bounded and limited to idempotent operations.
- [ ] Secrets stay redacted and runtime state stays machine-local.
- [ ] Unit tests use test layers and deterministic synchronization; live-provider tests are explicit.
