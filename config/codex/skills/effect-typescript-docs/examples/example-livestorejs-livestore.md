# livestorejs/livestore Effect Examples

Snapshot: `cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52` on the `main` branch, inspected 2026-06-04.

Use these examples for Effect in local-first sync/state systems: public Effect integration APIs, central Effect facades, RPC, browser channels, scoped resources, queues, streams, and reconnection loops.

## High-Level Read

LiveStore uses Effect to make local-first sync infrastructure tractable. The interesting parts are not basic `Effect.gen` usage; they are connection lifecycles, RPC protocols, browser messaging, schema-encoded payloads, queue-backed streams, and retry/reconnect loops. Effect gives these workflows a common model for scope, shutdown, typed decode/encode, and concurrent background fibers.

This repo is also a good example of project-level Effect ergonomics. LiveStore centralizes Effect, platform, RPC, and internal helpers behind a local facade, then exposes Effect-native integration points such as context tags and layers. Study it when designing reusable libraries that need to support browser, worker, node, and sync-engine boundaries.

## Permalinks

- [Central Effect facade](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/utils/src/effect/mod.ts#L3-L155) - project-owned re-export surface for `effect`, `@effect/platform`, `@effect/rpc`, observability, AI, and internal helpers.
- [RPC protocol socket layer](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/utils/src/effect/RpcClient.ts#L1-L43) - `Layer.scoped`, `Protocol.make`, socket serialization, connection state, and ping/retry options.
- [RPC socket read loop and timeout race](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/utils/src/effect/RpcClient.ts#L41-L103) - parser decode, `Effect.whileLoop`, connection state updates, and `Effect.raceFirst` with ping timeout failure.
- [BroadcastChannel WebChannel](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/utils/src/browser/WebChannelBrowser.ts#L14-L55) - `Effect.scopeWithCloseable`, finalizers, schema encode/decode, event streams, and shutdown handles.
- [window.postMessage WebChannel](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/utils/src/browser/WebChannelBrowser.ts#L60-L130) - schema-tagged browser messages, transferable encoding, filtered event streams, and closeable scopes.
- [WebSocket edge connection](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/webmesh/src/websocket-edge.ts#L43-L67) - scoped websocket edge setup, `Effect.acquireRelease`, `Effect.forever`, interruption, and platform layer provisioning.
- [WebSocket edge stream retry](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/webmesh/src/websocket-edge.ts#L90-L140) - queue shutdown finalizers, deferred close signaling, exponential/spaced retry schedule, socket stream decoding, and stream drain.
- [Direct channel reconnect loop](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/webmesh/src/channel/direct-channel.ts#L46-L130) - closeable scopes, pubsub stream fibers, `Effect.raceFirst`, scoped retries, and explicit reconnection semantics.
- [Proxy channel send retry](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40livestore/webmesh/src/channel/proxy-channel.ts#L411-L453) - schema encoding, deferred acknowledgements, fiber handles, timeout, and exponential retry.
- [Effect-powered file watch pipeline](https://github.com/livestorejs/livestore/blob/cd0e60d4a96e05c5ef16664e5f0a915ebccd5c52/packages/%40local/astro-tldraw/src/cli.ts#L274-L350) - platform filesystem watch stream, debounce, sequential `Stream.mapEffect`, and long-running drain.

## Code Samples

These are distilled pattern sketches from the linked code, not verbatim excerpts.

### Scoped Protocol Layer

```ts
import { Effect, Layer, Schedule } from "effect"

const protocolLayer = (options: {
  readonly url: string
  readonly retryTransientErrors?: Schedule.Schedule<unknown>
}) =>
  Layer.scoped(
    Protocol,
    Protocol.make(
      Effect.fnUntraced(function* (writeResponse) {
        const socket = yield* Socket.Socket
        const serialization = yield* RpcSerialization.RpcSerialization
        const parser = serialization.unsafeMake()

        yield* socket.runRaw((message) =>
          Effect.forEach(parser.decode(message), writeResponse, {
            discard: true,
          })
        )
      })
    )
  )
```

### Browser Channel With Schema And Finalizer

```ts
const broadcastChannel = <Listen, Send>(input: ChannelInput<Listen, Send>) =>
  Effect.scopeWithCloseable((scope) =>
    Effect.gen(function* () {
      const schema = mapSchema(input.schema)
      const channel = new BroadcastChannel(input.channelName)

      yield* Effect.addFinalizer(() =>
        Effect.try(() => channel.close()).pipe(Effect.ignoreLogged)
      )

      const send = (message: Send) =>
        Effect.gen(function* () {
          channel.postMessage(yield* Schema.encode(schema.send)(message))
        })

      const listen = Stream.fromEventListener<MessageEvent>(channel, "message").pipe(
        Stream.map((event) => Schema.decodeEither(schema.listen)(event.data))
      )

      return { send, listen, shutdown: Scope.close(scope, Exit.void) }
    })
  )
```

### Reconnect Race With Scoped Cleanup

```ts
const reconnectLoop = Effect.gen(function* () {
  while (true) {
    const attemptScope = yield* Scope.make()
    yield* Effect.addFinalizer((exit) => Scope.close(attemptScope, exit))

    const waitForNewEdge = Stream.fromPubSub(newEdgeAvailable).pipe(
      Stream.take(1),
      Stream.runDrain,
      Effect.as("new-edge" as const),
      Effect.fork
    )

    const openChannel = makeChannel.pipe(Scope.extend(attemptScope), Effect.forkIn(attemptScope))
    const result = yield* Effect.raceFirst(openChannel, waitForNewEdge.pipe(Effect.disconnect))

    if (result === "new-edge") {
      yield* Scope.close(attemptScope, Exit.fail("retry"))
    } else {
      return result
    }
  }
})
```

### Debounced File Watch Stream

```ts
const watchDiagrams = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  yield* fs.watch(diagramsRoot).pipe(
    Stream.map(toWatchSummary),
    Stream.filter((summary): summary is WatchSummary => summary !== null),
    Stream.debounce("200 millis"),
    Stream.mapEffect((event) => rebuild("watch", event), { concurrency: 1 }),
    Stream.runDrain
  )
})
```
