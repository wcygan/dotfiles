---
name: async-rust
description: >
  Async Rust and Tokio ecosystem expert. Provides idiomatic patterns, architectural guidance,
  and code review for async Rust code using tokio, futures, bytes, tracing, tonic, hyper, tower,
  axum, tokio-stream, and pin-project. Covers runtime internals, cancellation safety, graceful
  shutdown, channel selection, shared state, backpressure, structured concurrency, error handling,
  Tower middleware, stream processing, and performance tuning. Also identifies async footguns
  (blocking the runtime, holding locks across .await, silent task panics, accidental cancellation)
  and suggests fixes. Use when writing async Rust, debugging async issues, reviewing async code,
  choosing between spawn/join/select, designing channel topologies, implementing graceful shutdown,
  or learning how futures, Pin, and the Tokio runtime work under the hood.
  Keywords: async, await, tokio, futures, spawn, select, join, channels, streams, pin, tower,
  tonic, hyper, axum, tracing, bytes, cancellation, runtime, backpressure, graceful shutdown.
---

# Async Rust & Tokio Ecosystem

Async Rust is a **scaling technique for concurrent I/O**, not a default programming mode. Use it when you have hundreds+ of concurrent connections where thread-per-connection becomes impractical.

## The Mental Model

```
async fn → compiler → state machine (enum with one variant per .await point)
         → runtime polls it → Pending? park. I/O ready? waker.wake() → re-poll
         → 1000s of tasks on a handful of OS threads (~few hundred bytes/task vs 2MB/thread)
```

**Core trait:**
```rust
pub trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Futures are **lazy** — they do nothing until polled. `Pin` prevents the state machine from being moved in memory (protecting self-referential internal pointers). The runtime (Tokio) manages polling, parking, and waking.

## The Tokio Stack

```
┌─────────────────────────────────────────┐
│  Application (async/await)              │
├──────────────┬──────────────────────────┤
│ axum (HTTP)  │  tonic (gRPC)            │
├──────────────┴──────────────────────────┤
│ tower (Service trait, middleware layers) │
├─────────────────────────────────────────┤
│ hyper (HTTP/1.1, HTTP/2)                │
├─────────────────────────────────────────┤
│ tokio (runtime, I/O, sync, timers)      │
├────────────┬───────────┬────────────────┤
│ bytes      │ futures   │ tracing        │
│ (zero-copy)│(combinat.)│(observability) │
└────────────┴───────────┴────────────────┘
```

## Quick Decision Trees

**Concurrency primitive:**
- Need all results, no orphans? → `tokio::join!` / `try_join!`
- Need true parallelism across threads? → `tokio::spawn`
- Need first-to-complete or shutdown signal? → `tokio::select!`
- Dynamic set of tasks with abort-on-drop? → `JoinSet`
- Graceful drain without collecting results? → `TaskTracker`

**Shared state:**
- Lock NOT held across `.await`, low contention? → `std::sync::Mutex`
- Lock held across `.await` (last resort)? → `tokio::sync::Mutex`
- Complex state needing async operations? → Actor pattern (mpsc + dedicated task)

**Channel type:**
- Work distribution (N:1)? → `mpsc`
- Request/response (1:1)? → `oneshot`
- Event fan-out (N:M)? → `broadcast`
- Config/state snapshot (latest value)? → `watch`

## Before Going Async, Ask:

1. Do I actually have concurrent I/O? (If not → blocking I/O)
2. CPU-bound or I/O-bound? (CPU → threads/rayon)
3. Will I exceed ~500-1000 concurrent connections? (If not → threads are simpler)
4. Can the team afford the complexity tax? (Worse errors, harder debugging, Pin/Send/Sync)
5. What happens when a future is cancelled at each `.await`? (If unsure → you have bugs)

## Reference Files

Detailed guidance organized by topic:

References: [mental-model](references/mental-model.md)
References: [pattern-catalog](references/pattern-catalog.md)
References: [crate-composition](references/crate-composition.md)
References: [footguns-and-pitfalls](references/footguns-and-pitfalls.md)
References: [cancellation-safety](references/cancellation-safety.md)
References: [performance](references/performance.md)
References: [error-handling](references/error-handling.md)
References: [graceful-shutdown](references/graceful-shutdown.md)
References: [testing-patterns](references/testing-patterns.md)
References: [tower-middleware](references/tower-middleware.md)
References: [resources](references/resources.md)
