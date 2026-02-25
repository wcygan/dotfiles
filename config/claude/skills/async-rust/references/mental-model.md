# Async Rust Mental Model

## How It Works Under the Hood

### 1. Futures Are Lazy State Machines

Every `async fn` compiles into an enum (state machine) with one variant per `.await` point:

```rust
async fn example() {
    let data = fetch().await;   // State 0 → State 1
    let result = process(data); // synchronous, no state transition
    save(result).await;         // State 1 → State 2
}
// Compiles roughly to:
enum ExampleFuture {
    State0 { /* locals for fetch() */ },
    State1 { data: Data, /* locals for save() */ },
    Done,
}
```

### 2. The Polling Mechanism

```
Event Loop (per worker thread):
├─ Poll all ready tasks
├─ If Poll::Pending → park task (suspend, free the thread)
├─ Listen on OS event queue (epoll/kqueue/IOCP)
├─ When event fires → waker.wake() → re-queue task
└─ Repeat
```

Tokio uses a **multi-threaded work-stealing scheduler**. When one thread's queue is empty, it steals from other threads' queues. Default thread count = number of CPU cores.

### 3. Wakers: The Notification System

1. Task registers interest via `Context::waker()`
2. OS event fires (socket becomes readable)
3. Runtime calls `waker.wake()` → puts task back in scheduler queue
4. Next scheduler cycle polls that task again

This is why `Pin<&mut Self>` is needed — the waker holds a stable reference to the task's memory location.

### 4. Pin Explained

Futures can contain self-references (the state machine may reference its own fields across states). `Pin` prevents moving a `Future` in memory after polling begins:

```rust
// Stack pinning — zero allocation
let future = my_async_fn();
tokio::pin!(future); // or std::pin::pin!(future)

// Heap pinning — required for dyn Future, recursive async
let future: Pin<Box<dyn Future<Output = ()> + Send>> = Box::pin(my_async_fn());
```

**Practical rules:**
- Most code never touches `Pin` directly — `async/await` handles it
- Custom `Future`/`Stream` impls need `pin-project` or `pin-project-lite`
- Recursive async functions require `Box::pin` (infinite size otherwise)
- `Unpin` types can be freely moved even when pinned (most concrete types are `Unpin`)

### 5. Send + 'static Requirements

`tokio::spawn` requires `Future: Send + 'static` because the task may run on any worker thread and must outlive the spawning scope. This means:

- All captured data must be `Send` (safe to transfer between threads)
- No borrowed references (must be owned or `Arc`-wrapped)
- `Rc`, `Cell`, `RefCell` cannot cross `.await` in spawned tasks

```rust
// Won't compile — &db is not 'static
let db = &database;
tokio::spawn(async move { db.query().await }); // ERROR

// Fix: clone or Arc-wrap
let db = Arc::new(database);
let db2 = db.clone();
tokio::spawn(async move { db2.query().await }); // OK
```

### 6. Cooperative Scheduling

Tokio allocates **128 operations per task per scheduler tick**. Every `.await` on a Tokio resource (socket read/write, channel send/recv, timer) decrements this budget. When exhausted, Tokio resources return `Poll::Pending` to force the task to yield.

This only works for Tokio's own resources. CPU-bound loops without `.await` bypass the budget entirely → starvation.

```rust
// Manual yield for CPU-intensive async loops
for (i, item) in data.iter().enumerate() {
    compute(item);
    if i % 256 == 0 {
        tokio::task::yield_now().await;
    }
}
```

## Key Documentation

- [Rust Book Ch17: Async/Await](https://doc.rust-lang.org/book/ch17-00-async-await.html)
- [The Async Book](https://rust-lang.github.io/async-book/)
- [std::pin documentation](https://doc.rust-lang.org/std/pin/index.html)
- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [Tyler Mandry: How Rust optimizes async/await](https://tmandry.gitlab.io/blog/posts/optimizing-await-1/)
- [Tokio Cooperative Scheduling](https://tokio.rs/blog/2020-04-preemption)
