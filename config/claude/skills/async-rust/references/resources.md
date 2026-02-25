# Async Rust Resources

## Official Documentation

| Resource | URL | Level |
|----------|-----|:-----:|
| Tokio Tutorial | <https://tokio.rs/tokio/tutorial> | Beginner |
| Tokio API Docs | <https://docs.rs/tokio/latest/tokio/> | Reference |
| The Async Book | <https://rust-lang.github.io/async-book/> | Beginner/Inter |
| Rust Book Ch17: Async | <https://doc.rust-lang.org/book/ch17-00-async-await.html> | Beginner |
| std::pin docs | <https://doc.rust-lang.org/std/pin/index.html> | Advanced |
| futures crate | <https://docs.rs/futures/latest/futures/> | Reference |
| bytes crate | <https://docs.rs/bytes/latest/bytes/> | Reference |
| tracing crate | <https://docs.rs/tracing/latest/tracing/> | Reference |
| tonic crate | <https://docs.rs/tonic/latest/tonic/> | Reference |
| hyper crate | <https://docs.rs/hyper/latest/hyper/> | Reference |
| tower crate | <https://docs.rs/tower/latest/tower/> | Reference |
| axum crate | <https://docs.rs/axum/latest/axum/> | Reference |

## Must-Read Blog Posts

### Alice Ryhl (Tokio maintainer)
- [Async: What is blocking?](https://ryhl.io/blog/async-what-is-blocking/) — Why async code should never spend long without reaching `.await`. **Beginner/Inter.**
- [Actors with Tokio](https://ryhl.io/blog/actors-with-tokio/) — Building actor patterns with channels + spawned tasks. **Intermediate.**

### Jon Gjengset
- [Decrusting the tokio crate](https://www.youtube.com/watch?v=o2ob8zkeq2s) (video) — Deep runtime walkthrough. **Inter/Advanced.**
- [Decrusting the tracing crate](https://www.youtube.com/watch?v=21rtHinFA40) (video) — Spans, events, subscribers. **Intermediate.**
- [Rust for Rustaceans](https://rust-for-rustaceans.com/) (book) — Concurrency and async chapters. **Advanced.**

### Tyler Mandry (Async Working Group lead)
- [How Rust optimizes async/await I](https://tmandry.gitlab.io/blog/posts/optimizing-await-1/) — Compiler-level state machine generation. **Advanced.**
- [Making Async Rust Reliable](https://tmandry.gitlab.io/blog/posts/making-async-reliable/) — Async foundations vision. **Intermediate.**

### without.boats (Language designer)
- [Why async Rust?](https://without.boats/blog/why-async-rust/) — Design rationale. **Intermediate.**
- [All async posts](https://without.boats/tags/async/) — Full index.

### Yoshua Wuyts
- [Futures Concurrency series](https://blog.yoshuawuyts.com/futures-concurrency/) (3 parts) — All modes of async concurrency. **Inter/Advanced.**
- [Async Cancellation I](https://blog.yoshuawuyts.com/async-cancellation-1/) — Cancellation mechanics. **Advanced.**

### Other Essential Posts
- [Oxide RFD 400: Cancel Safety](https://rfd.shared.oxide.computer/rfd/400) — Production cancel-safety patterns. **Advanced.**
- [Luca Palmieri: Error Handling in Rust](https://lpalmieri.com/posts/error-handling-rust/) — Definitive error handling guide. **Intermediate.**
- [corrode: The State of Async Rust](https://corrode.dev/blog/async/) — Runtime comparison. **Intermediate.**
- [ScyllaDB: Async Rust in Practice](https://www.scylladb.com/2022/01/12/async-rust-in-practice-performance-pitfalls-profiling/) — Performance lessons. **Inter/Advanced.**

## Books

| Book | Author | Focus |
|------|--------|-------|
| [Zero to Production in Rust](https://www.zero2prod.com/) | Luca Palmieri | Building a production API (500 pages, hands-on) |
| [Rust for Rustaceans](https://rust-for-rustaceans.com/) | Jon Gjengset | Advanced Rust including async internals |

## Codebases Worth Studying

| Project | URL | Why |
|---------|-----|-----|
| mini-redis | <https://github.com/tokio-rs/mini-redis> | Official Tokio learning codebase |
| axum examples | <https://github.com/tokio-rs/axum/tree/main/examples> | 40+ idiomatic HTTP patterns |
| linkerd2-proxy | <https://github.com/linkerd/linkerd2-proxy> | Production Tower/Tokio reference |
| Vector (Datadog) | <https://github.com/vectordotdev/vector> | Large-scale async data pipeline |
| SurrealDB | <https://github.com/surrealdb/surrealdb> | Multi-model database, WASM support |
| reqwest | <https://github.com/seanmonstar/reqwest> | Async/blocking dual API, connection pooling |

## Tools

| Tool | URL | Purpose |
|------|-----|---------|
| tokio-console | <https://github.com/tokio-rs/console> | Real-time async runtime debugger |
| tracing + tracing-subscriber | <https://docs.rs/tracing-subscriber> | Structured async-aware logging |
| tracing-opentelemetry | <https://docs.rs/tracing-opentelemetry> | Bridge to OpenTelemetry |
| loom | <https://github.com/tokio-rs/loom> | Concurrency permutation testing |
| wiremock-rs | <https://github.com/LukeMathWalker/wiremock-rs> | Async HTTP mock servers |
| cargo-flamegraph | <https://github.com/flamegraph-rs/flamegraph> | Performance flamegraphs |
| miri | <https://github.com/rust-lang/miri> | Undefined behavior detection |

## Tokio-Specific Documentation

| Topic | URL |
|-------|-----|
| Graceful Shutdown | <https://tokio.rs/tokio/topics/shutdown> |
| Shared State (Mutex guidance) | <https://tokio.rs/tokio/tutorial/shared-state> |
| Channels | <https://tokio.rs/tokio/tutorial/channels> |
| select! cancel safety | <https://docs.rs/tokio/latest/tokio/macro.select.html> |
| Cooperative scheduling | <https://tokio.rs/blog/2020-04-preemption> |
| Inventing the Service trait | <https://tokio.rs/blog/2021-05-14-inventing-the-service-trait> |
| JoinSet | <https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html> |
| TaskTracker | <https://docs.rs/tokio-util/latest/tokio_util/task/task_tracker/struct.TaskTracker.html> |
| CancellationToken | <https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html> |

## Emerging / Watch

- **Async traits**: Stable since Rust 1.75 for static dispatch; `dyn Trait` support still WIP
- **`gen` blocks / async generators**: Nightly, expected to stabilize soon
- **io_uring runtimes** (glommio, monoio): 2-3x throughput but [cancellation soundness concerns](https://tonbo.io/blog/async-rust-is-not-safe-with-io-uring)
- **TokioConf 2026**: First ever, April 20-22 in Portland — <https://www.tokioconf.com>
- [JetBrains: Evolution of Async Rust (Feb 2026)](https://blog.jetbrains.com/rust/2026/02/17/the-evolution-of-async-rust-from-tokio-to-high-level-applications/)
