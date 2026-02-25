# Async Rust Footguns & Pitfalls

## The 8 Deadly Footguns

### 1. Holding a Lock Across `.await`

```rust
// BUG: lock held during entire I/O operation
let mut guard = state.lock().await;
guard.value = compute();
do_io().await;  // every other task waiting on this lock is blocked
guard.update();

// FIX: scope the guard tightly
let value = {
    let mut guard = state.lock().await;
    guard.value = compute();
    guard.value.clone()
}; // lock released here
do_io().await;
```

With `std::sync::Mutex`, the compiler often catches this (guard is `!Send`). With `tokio::sync::Mutex`, it compiles but causes contention.

### 2. Blocking the Runtime

```rust
// BUG: blocks a worker thread (default: one per CPU core)
async fn handle(req: Request) -> Response {
    let data = std::fs::read_to_string("config.json").unwrap(); // BLOCKS
    let hash = argon2::hash(password);                           // CPU-BOUND
    // ...
}

// FIX: offload to blocking thread pool
let data = tokio::task::spawn_blocking(|| {
    std::fs::read_to_string("config.json")
}).await??;
```

Works fine in dev with low concurrency. Under load, blocking all worker threads freezes the entire service.

### 3. Accidental Cancellation

```rust
// BUG: timeout can drop future between debit and credit
async fn transfer(from: &Account, to: &Account, amount: u64) {
    from.debit(amount).await;  // completes
    to.credit(amount).await;   // MAY NEVER RUN
}
tokio::time::timeout(Duration::from_secs(5), transfer(&a, &b, 100)).await;

// FIX: make operations atomic or idempotent
// Use database transactions, or spawn the critical section
```

### 4. Silent Task Panics

```rust
// BUG: dropped JoinHandle swallows the panic
tokio::spawn(async { panic!("oops") });
// No log. No error. Task vanishes.

// FIX: always await or use JoinSet
let mut set = JoinSet::new();
set.spawn(async { work().await });
while let Some(result) = set.join_next().await {
    if let Err(je) = result {
        tracing::error!("task failed: {je}");
    }
}
```

### 5. Tracing Spans Across `.await`

```rust
// BUG: span may exit before await completes
{
    let span = tracing::info_span!("work");
    let _guard = span.enter();
    async_work().await;  // span context lost!
}

// FIX: use the Instrument trait
async_work()
    .instrument(tracing::info_span!("work"))
    .await;

// Or use #[instrument] on the function
#[instrument]
async fn do_work() { ... }
```

### 6. Nested `block_on` — Runtime Panic

```rust
// BUG: calling block_on from within an async context
fn sync_helper() {
    // Panics: "Cannot start a runtime from within a runtime"
    tokio::runtime::Runtime::new().unwrap().block_on(async_work());
}

// This is called from an async handler:
async fn handler() {
    sync_helper(); // PANIC
}

// FIX: restructure to keep the async boundary clean
async fn handler() {
    async_work().await; // just await it
}
```

### 7. Unbounded Channel Memory Exhaustion

```rust
// BUG: unbounded channel grows without limit under load
let (tx, rx) = tokio::sync::mpsc::unbounded_channel();
// If producer is faster than consumer, OOM.

// FIX: always use bounded channels with explicit backpressure
let (tx, rx) = tokio::sync::mpsc::channel(1024);
// Producer blocks when buffer is full, naturally throttling
```

### 8. Forgetting `spawn_blocking` Tasks Can't Be Aborted

```rust
// SURPRISE: abort() has no effect on spawn_blocking tasks
let handle = tokio::task::spawn_blocking(|| {
    expensive_computation() // runs to completion regardless
});
handle.abort(); // does nothing!

// Plan for this in shutdown: spawn_blocking tasks WILL complete
```

## Common Misconceptions

| Belief | Reality |
|--------|---------|
| "Async makes code faster" | Async makes code more *concurrent*. Individual requests are slower due to state machine overhead. Helps only with many concurrent I/O operations. |
| "Everything should be async" | Async is a scaling technique, not a default. Keep business logic synchronous. Only add async at I/O boundaries. |
| "`tokio::sync::Mutex` > `std::sync::Mutex`" | `std::sync::Mutex` is faster when the lock isn't held across `.await`. Tokio docs say this explicitly. |
| "`spawn` > `join`" | `join!` borrows freely, no `Arc`, no `JoinError` layer. Use `spawn` only for cross-thread parallelism. |
| "`Pin` is just an annoyance" | Pin is memory safety. Without it, self-referential futures would cause use-after-free. |
| "`select!` is like `switch`" | `select!` is a cancellation operator. Losing branches are **dropped mid-execution**. |
| "I can ignore cancellation" | Every `.await` is a potential cancellation point. Design every async fn assuming it can stop at any `.await`. |
| "Async traits = sync traits" | Dynamic dispatch (`dyn Trait`) requires boxing the returned future. `async fn` in traits works for static dispatch since Rust 1.75, but `dyn Trait` needs extra work. |

## Cognitive Biases

**Complexity bias:** Reaching for async when `std::thread` + blocking I/O would be simpler. You need async when you have 1000+ concurrent connections, not 3 API calls.

**Cargo cult from Go/JS:**
- Go goroutines are preemptively scheduled; Rust tasks are cooperative. A CPU-bound Rust task blocks the worker thread forever.
- Go's GC handles cancellation cleanup; Rust has no GC — dropped futures run destructors synchronously.
- JS is single-threaded — no `Send`/`Sync` concerns.

**Premature optimization:** `Box::pin` allocations are nearly free. Profile before reaching for stack pinning or `unsafe`.

**Tower addiction:** A 3-line function doesn't need a `Service` impl with `poll_ready` + `call` + `Layer` + `BoxError`. Use Tower when you need composable middleware stacks with backpressure.

## Key Documentation

- [Alice Ryhl: Async — What is blocking?](https://ryhl.io/blog/async-what-is-blocking/)
- [Tokio Tutorial: Shared State (Mutex guidance)](https://tokio.rs/tokio/tutorial/shared-state)
- [Qovery: Common Mistakes with Rust Async](https://www.qovery.com/blog/common-mistakes-with-rust-async)
