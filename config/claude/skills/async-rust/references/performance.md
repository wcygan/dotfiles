# Async Rust Performance

## When Async Helps vs Hurts

| Scenario | Async Helps? | Why |
|----------|:------------:|-----|
| 10K+ concurrent connections | Yes | ~few hundred bytes/task vs 2-8 MB/thread stack |
| CPU-bound computation | **No** | Overhead of state machine + polling with no I/O to amortize |
| Mixed I/O + CPU | Depends | Offload CPU to `spawn_blocking`; keep I/O on async threads |
| Sequential file processing | **No** | `tokio::fs` is `spawn_blocking` internally anyway |
| Low-concurrency CLI tools | **No** | Runtime overhead exceeds benefit |
| WebSocket chat with 50K users | Yes | Each connection is a lightweight task |

**Rule of thumb:** If your program spends most time waiting for I/O across many concurrent connections, async wins. If it spends most time computing, threads or rayon win.

## `spawn_blocking` — When and Why

Use for any work taking longer than ~10-100 microseconds without an `.await`:

```rust
// File I/O
let contents = tokio::task::spawn_blocking(move || {
    std::fs::read_to_string(path)
}).await??;

// CPU-intensive work
let hash = tokio::task::spawn_blocking(move || {
    argon2::hash_encoded(password.as_bytes(), &salt, &config)
}).await??;

// Synchronous library calls
let thumbnail = tokio::task::spawn_blocking(move || {
    image::open(&path)?.thumbnail(256, 256)
}).await??;
```

**Critical:** `spawn_blocking` tasks **cannot be aborted**. `handle.abort()` has no effect. Plan for this in shutdown.

## Memory Overhead

| | Per-Unit Cost | 10K Units |
|-|:-------------:|:---------:|
| OS thread | 2-8 MB stack | 20-80 GB |
| Tokio task | Size of future's state machine (typically 256 bytes - few KB) | 2.5-50 MB |

Future size = sum of all local variables that live across `.await` points.

```rust
// BAD: 64KB on the future's state machine
async fn bad() {
    let buf = [0u8; 65536]; // stack array lives across .await
    some_io(&buf).await;
}

// GOOD: 24 bytes (Vec metadata) on the state machine
async fn good() {
    let buf = vec![0u8; 65536]; // heap allocated
    some_io(&buf).await;
}
```

## Pinning Costs

| Approach | Allocation | Use When |
|----------|:----------:|----------|
| `tokio::pin!(fut)` / `std::pin::pin!(fut)` | Stack (zero) | Local pinning in `select!` loops, short-lived futures |
| `Box::pin(fut)` | Heap (one) | `dyn Future`, recursive async, trait methods |
| `pin-project` | Zero overhead | Custom `Future`/`Stream` impls with projected fields |

```rust
// Stack pinning — use in select! loops
let sleep = tokio::time::sleep(Duration::from_secs(60));
tokio::pin!(sleep);
loop {
    tokio::select! {
        _ = &mut sleep => break,
        msg = rx.recv() => { /* ... */ }
    }
}

// Recursive async — must heap-allocate
fn traverse(node: &Node) -> Pin<Box<dyn Future<Output = ()> + Send + '_>> {
    Box::pin(async move {
        for child in &node.children {
            traverse(child).await;
        }
    })
}
```

## `async_trait` Allocation Overhead

Every `#[async_trait]` method call heap-allocates a `Pin<Box<dyn Future>>`:

```rust
#[async_trait]
trait MyService {
    async fn process(&self, input: Input) -> Output;
}
// Desugars to:
// fn process(&self, input: Input) -> Pin<Box<dyn Future<Output = Output> + Send + '_>>
```

**Impact:** Measurable in hot paths with millions of calls. Profile before optimizing. Use static dispatch (`impl Trait`) where possible.

**Since Rust 1.75:** Native `async fn` in traits works for static dispatch. `#[async_trait]` is still needed for `dyn Trait` usage.

## Cooperative Scheduling Budget

Tokio allocates 128 operations per task per scheduler tick. Each `.await` on a Tokio resource decrements this. When exhausted, all Tokio resources return `Poll::Pending` to force the task to yield.

**Only works for Tokio resources.** Pure computation bypasses the budget:

```rust
// Starvation risk: no .await in loop
for item in large_dataset {
    compute(item); // blocks the worker thread
}

// Fix: periodic yield
for (i, item) in large_dataset.iter().enumerate() {
    compute(item);
    if i % 256 == 0 {
        tokio::task::yield_now().await;
    }
}
```

## Profiling Async Code

1. **tokio-console**: Real-time task stats, blocking detection, scheduler state
2. **cargo-flamegraph**: SVG flamegraphs — look for wide bars in runtime internals
3. **tracing + tracing-subscriber**: Measure span durations for individual operations
4. **Criterion**: Benchmark async functions with `#[tokio::test]` harness

## Key Documentation

- [Tokio Cooperative Scheduling](https://tokio.rs/blog/2020-04-preemption)
- [tokio::task::spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html)
- [ScyllaDB: Async Rust in Practice](https://www.scylladb.com/2022/01/12/async-rust-in-practice-performance-pitfalls-profiling/)
- [Tyler Mandry: How Rust Optimizes async/await](https://tmandry.gitlab.io/blog/posts/optimizing-await-1/)
