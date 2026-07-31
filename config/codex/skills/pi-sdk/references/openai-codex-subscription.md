# Pi SDK with an OpenAI Codex subscription

Use this reference when a Pi SDK application should authenticate through a
ChatGPT Plus/Pro Codex subscription rather than an OpenAI API key.

The observed implementation baseline used:

- Pi `@earendil-works/pi-coding-agent` `0.82.1`;
- Effect `4.0.0-beta.102`;
- Bun `1.3.13`;
- default provider `openai-codex`;
- default model `gpt-5.6-luna`; and
- low thinking effort for the latency-sensitive default path.

Treat those versions as the observed implementation baseline, not universal
requirements. Recheck the installed Pi package, provider catalog, and current
model guidance before changing them.

## Subscription versus API-key authentication

The adapter should use Pi's public in-process login seam:

1. Create one `ModelRuntime` for the application layer.
2. Call `ModelRuntime.login("openai-codex", "oauth", interaction)` when the
   required OAuth credential is missing.
3. Let the application-owned interaction render Pi's prompts and notifications.
4. Let `ModelRuntime.create()` and Pi's credential store handle later reuse and
   refresh.

Pi stores and refreshes this credential in its own machine-local
`~/.pi/agent/auth.json`. The application must not read, print, copy, commit, or
link that file.

This is distinct from the Codex CLI login surface. OpenAI's Codex documentation
describes `codex login` and the CLI's `~/.codex/auth.json`; that is not the
credential store consumed by Pi's `ModelRuntime`. Pi's `/login` flow remains a
compatible manual setup path, but a Pi SDK application can use the direct
`ModelRuntime.login` flow documented below instead.

ChatGPT Plus includes Codex in the CLI and the GPT-5.6 family, including Luna;
Pro provides higher Codex limits. See the [official Codex pricing documentation](https://learn.chatgpt.com/docs/pricing) and [Codex CLI login documentation](https://learn.chatgpt.com/docs/developer-commands#codex-login) for the separate OpenAI-owned surfaces.

Do not add an `OPENAI_API_KEY` fallback when the application is intended to
consume subscription access. API-key authentication is a different billing and
entitlement path. The reference implementation explicitly checks that the
selected provider is configured and using OAuth before creating a session.

### Raw SDK login

`ModelRuntime.login` is the supported direct path. It invokes Pi's built-in
browser PKCE or device-code flow, persists the resulting credential through Pi's
credential store, and does not require a `pi` CLI subprocess.

```ts
import {
  createAgentSession,
  ModelRuntime,
  SessionManager,
} from "@earendil-works/pi-coding-agent";
import type {
  AuthEvent,
  AuthInteraction,
  AuthPrompt,
} from "@earendil-works/pi-ai";

const runtime = await ModelRuntime.create();

const interaction: AuthInteraction = {
  prompt: async (request: AuthPrompt) => {
    if (request.type === "select") {
      // Render request.options and return "browser" or "device_code".
      return "browser";
    }

    // Render text, secret, or manual_code input in application-owned UI.
    return readValueFromYourUi(request);
  },
  notify: (event: AuthEvent) => {
    // Show auth_url, device_code, info, and progress in application-owned UI.
    showInYourUi(event);
  },
};

if (!runtime.hasConfiguredAuth("openai-codex") ||
    !runtime.isUsingOAuth("openai-codex")) {
  await runtime.login("openai-codex", "oauth", interaction);
}

const model = runtime.getModel("openai-codex", "gpt-5.6-luna");
if (model === undefined) throw new Error("Codex model is unavailable");

const { session } = await createAgentSession({
  model,
  modelRuntime: runtime,
  noTools: "all",
  sessionManager: SessionManager.inMemory(),
  thinkingLevel: "low",
});
```

The interaction must honor `AbortSignal`. Browser login emits an `auth_url`
and uses Pi's loopback callback server; device-code login emits a verification
URL and user code. Use device-code login for headless environments. The OAuth
implementation is Node/Bun-oriented and should remain behind a server-side
boundary rather than being bundled into a browser page.

## Provider and model preflight

Use a stable application configuration:

```ts
export const CODEX_PROVIDER = "openai-codex";
export const CODEX_MODEL = "gpt-5.6-luna";

export const DefaultPiAgentConfig = {
  provider: CODEX_PROVIDER,
  model: CODEX_MODEL,
  thinkingLevel: "low" as const,
};
```

Create one `ModelRuntime` per application layer, then validate the requested
provider/model before session creation:

```ts
const modelRuntime = await ModelRuntime.create();
const resolvedModel = modelRuntime.getModel(CODEX_PROVIDER, CODEX_MODEL);

if (!modelRuntime.hasConfiguredAuth(CODEX_PROVIDER) ||
    !modelRuntime.isUsingOAuth(CODEX_PROVIDER)) {
  throw new MissingCodexLogin({ provider: CODEX_PROVIDER });
}

if (resolvedModel === undefined) {
  throw new CodexModelUnavailable({
    provider: CODEX_PROVIDER,
    model: CODEX_MODEL,
  });
}
```

Keep these checks separate. A model can be present in the catalog while the
subscription credential is missing, expired, or being overridden by a different
auth path. `ModelRuntime.getAvailable()` is useful when selecting from several
authenticated models; an explicit default should still validate the exact
provider/model pair.

The official OpenAI model guidance describes Luna as the efficient,
high-volume GPT-5.6 option. For Pi, the provider catalog remains authoritative:
only use `gpt-5.6-luna` after `getModel("openai-codex", "gpt-5.6-luna")` succeeds.
See the [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model#update-api-and-model-parameters).

## Session construction

For a focused subscription-backed helper, create an in-memory, tool-free
session:

```ts
const { session } = await createAgentSession({
  model: resolvedModel,
  modelRuntime,
  noTools: "all",
  sessionManager: SessionManager.inMemory(),
  thinkingLevel: "low",
});
```

This is appropriate when the application only needs streamed text and should
not read or mutate the repository. If the product needs tools, make that an
explicit capability decision and constrain the allowlist; do not inherit Pi's
default `bash`, `edit`, and `write` tools accidentally.

The implementation creates a fresh session per prompt while reusing the single
runtime. This keeps mutable conversation state isolated between requests and
still avoids rebuilding provider/auth resolution for every prompt. If an
application intentionally retains conversation state, give that session one
clear owner and serialize access to it.

## Effect service and stream adapter

Expose an application-shaped Effect service, not raw Pi objects:

```ts
export class PiAgent extends Context.Service<PiAgent, {
  readonly authenticate: (
    interaction: AuthInteraction,
  ) => Effect.Effect<void, PiAuthenticationError>;
  readonly metadata: () => Effect.Effect<PiAgentConfig, PiAgentError>;
  readonly streamPrompt: (prompt: string) => Stream.Stream<string, PiAgentError>;
}>()("app/PiAgent") {}
```

Keep authentication explicit and separate from metadata/inference. A missing
credential may trigger an application-level login flow, but model preflight
should not silently open a browser.

```ts
const authenticate = Effect.fn("PiAgent.authenticate")(function* (
  interaction: AuthInteraction,
) {
  yield* Effect.tryPromise({
    try: (signal) =>
      runtime.login("openai-codex", "oauth", {
        ...interaction,
        signal: interaction.signal === undefined
          ? signal
          : AbortSignal.any([signal, interaction.signal]),
      }),
    catch: (cause) =>
      new PiAuthenticationError({
        provider: "openai-codex",
        cause,
      }),
  });
});
```

Provide that operation through the live `Layer`. On interruption, cancel the
signal passed to Pi so device-code polling stops and the browser callback
server closes. Use `Effect.acquireRelease` for terminal/UI resources owned by
the application. Cleanup must be best-effort without hiding the primary login
failure.

Adapt Pi's `session.subscribe` callback to an Effect `Stream`:

1. Subscribe only after provider/model preflight succeeds.
2. Forward `message_update` + `text_delta` payloads to a queue-backed stream.
3. End the stream after `session.prompt()` resolves.
4. Fail the stream with the typed adapter error if prompting fails.
5. Keep event callbacks small and non-blocking.

The implementation uses `Stream.callback`, `Queue.offerUnsafe`,
`Queue.failCauseUnsafe`, and `Queue.endUnsafe` for this bridge. Use the current
Effect declarations and the existing project conventions before copying those
low-level operations into a new adapter.

## Scoped cleanup and interruption

Treat the session and subscription as scoped resources:

```ts
const acquireSession = Effect.acquireRelease(
  Effect.tryPromise({
    try: () => runtime.createSession(config),
    catch: (cause) => new PiSessionCreationError({ cause }),
  }),
  (session) => Effect.try({
    try: session.dispose,
    catch: () => undefined,
  }).pipe(Effect.ignore),
);
```

Register the unsubscribe finalizer in the same scope. Wrap the prompt with an
interrupt handler:

```ts
const runPrompt = Effect.tryPromise({
  try: () => session.prompt(prompt),
  catch: (cause) => new PiInferenceError({ cause }),
}).pipe(
  Effect.onInterrupt(() =>
    Effect.tryPromise({ try: session.abort, catch: () => undefined }).pipe(
      Effect.ignore,
    ),
  ),
);
```

The finalizer should be best-effort: cleanup failure must not hide the primary
model or provider failure. On normal completion and failure, unsubscribe before
disposing the session. On interruption, abort first and then let scope cleanup
finish the subscription/session lifecycle.

## Error taxonomy

Keep failures actionable and typed:

- `MissingCodexLogin`: no configured OAuth credential, or the provider is using
  API-key auth instead of the required subscription auth;
- `CodexModelUnavailable`: the requested provider/model is not in Pi's catalog;
- `PiRuntimeCreationError`: `ModelRuntime.create()` failed;
- `PiAuthenticationError`: direct Pi OAuth login failed or was cancelled;
- `PiSessionCreationError`: model/session or event subscription setup failed;
- `PiInferenceError`: an accepted prompt failed during inference.

Do not retry `session.prompt()` by default. A failed prompt may have already
executed work or consumed subscription usage. Retry only a separately proven
idempotent setup/read boundary, with an explicit bounded policy. Preserve
partial streamed output as partial output; do not report a successful final
answer after a stream failure.

## Output and diagnostics

Keep diagnostics separate from the answer stream:

```ts
writeDiagnostic(
  `[pi] provider=${config.provider} model=${config.model} auth=oauth thinking=${config.thinkingLevel}\n`,
);
writeResponse(delta);
```

Write metadata to stderr and assistant text to stdout so callers can pipe the
answer without parsing logs. Never include credential sources, token values,
raw auth errors, or full provider configuration in diagnostics.

## Test contract

Do not require a live subscription for ordinary unit tests. Inject a fake
`PiSdk`/`PiRuntime` and provide the `PiAgent` layer with `@effect/vitest`.
The implementation's useful cases are:

- streamed deltas preserve order;
- success unsubscribes and disposes;
- missing auth fails before session creation;
- direct OAuth login delegates to Pi with the `openai-codex` provider;
- login failures are typed and cancellation reaches Pi's interaction signal;
- successful login precedes model/session creation;
- API-key auth is rejected;
- unavailable model fails before session creation;
- runtime, session, subscription, and inference failures are typed;
- subscription setup failure still disposes the session;
- an interrupted prompt aborts, unsubscribes, and disposes without sleeps;
- one runtime is reused while each prompt receives a fresh session; and
- the CLI writes metadata before deltas and does not append a newline after a
  failed stream.

Reserve a small explicit integration smoke test for the real provider/model and
credential store. Keep it separate from deterministic CI tests and never log
the credential contents.

## Checklist

- [ ] Direct Pi SDK login uses `ModelRuntime.login("openai-codex", "oauth", ...)`.
- [ ] The interaction renders browser/device-code prompts and auth events.
- [ ] The adapter uses Pi's `openai-codex` OAuth provider, not `OPENAI_API_KEY`.
- [ ] `gpt-5.6-luna` resolves in the installed Pi catalog, or the chosen model is explicitly configured.
- [ ] `ModelRuntime` is reused at the application layer.
- [ ] Sessions are in-memory/tool-free unless persistence/tools are intentional.
- [ ] Auth/model preflight occurs before session creation.
- [ ] Stream subscription and session disposal are scoped.
- [ ] Interrupts abort the active prompt.
- [ ] Prompt inference is not blindly retried.
- [ ] Unit tests use fakes; live subscription checks are explicit and isolated.
