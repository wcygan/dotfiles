---
title: Concurrency
description: Idiomatic Rust concurrency patterns — threads, async, Arc/Mutex, channels, Send/Sync
tags: [concurrency, async, threads, mutex, arc, channels, send, sync, tokio]
---

# Concurrency

## Thread Safety Traits

| Trait | Meaning | Auto-Derived |
|---|---|---|
| `Send` | Safe to transfer ownership across threads | Yes (if all fields are `Send`) |
| `Sync` | Safe to share `&T` across threads | Yes (if all fields are `Sync`) |

The compiler enforces these at compile time — data races are prevented statically.

## Shared State Pattern

```rust
use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));

let handles: Vec<_> = (0..10)
    .map(|_| {
        let counter = Arc::clone(&counter);
        std::thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        })
    })
    .collect();

for handle in handles {
    handle.join().unwrap();
}
```

### When to Use What

| Type | Use Case |
|---|---|
| `Mutex<T>` | Exclusive access, short critical sections |
| `RwLock<T>` | Read-heavy workloads (many readers, few writers) |
| `Arc<T>` | Shared ownership across threads (wrap `Mutex`/`RwLock`) |
| `Atomic*` | Simple counters/flags without locking overhead |

## Message Passing

Prefer message passing over shared state when possible:

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

let sender = std::thread::spawn(move || {
    tx.send("hello".to_string()).unwrap();
});

let received = rx.recv().unwrap();
```

## Async/Await Conventions

### Function Signatures

```rust
// Async function
async fn fetch_data(url: &str) -> Result<Response, Error> {
    let resp = client.get(url).send().await?;
    Ok(resp)
}

// Async trait method (use `async-trait` crate or Rust 1.75+ RPITIT)
pub trait Repository {
    async fn find(&self, id: &str) -> Result<Item, Error>;
}
```

### Tokio Patterns

```rust
// Main entry point
#[tokio::main]
async fn main() -> Result<()> {
    // ...
}

// Spawn concurrent tasks
let (a, b) = tokio::join!(
    fetch_users(),
    fetch_orders(),
);

// Spawn background task
tokio::spawn(async move {
    process_in_background().await;
});

// Select first completed future
tokio::select! {
    result = operation_a() => handle_a(result),
    result = operation_b() => handle_b(result),
    _ = tokio::time::sleep(Duration::from_secs(5)) => timeout(),
}
```

### Async Mutex vs Std Mutex

```rust
// Use std::sync::Mutex when lock is held briefly and not across .await
let data = std::sync::Mutex::new(vec![]);

// Use tokio::sync::Mutex when lock must be held across .await points
let data = tokio::sync::Mutex::new(vec![]);
```

Rule: If you don't hold the lock across an `.await`, prefer `std::sync::Mutex` (faster).

## Interior Mutability (Single-Threaded)

| Type | Use Case |
|---|---|
| `Cell<T>` | For `Copy` types; get/set without borrowing |
| `RefCell<T>` | Runtime borrow checking; `borrow()` / `borrow_mut()` |
| `OnceCell<T>` | Write-once lazy initialization |

**Never use `RefCell` across threads** — it is not `Sync`. Use `Mutex` instead.

## Common Patterns

### Scoped Threads (std)

```rust
std::thread::scope(|s| {
    s.spawn(|| {
        // Can borrow from outer scope without Arc
        process(&shared_data);
    });
});
```

### Parallel Processing with Rayon

```rust
use rayon::prelude::*;

let results: Vec<_> = items
    .par_iter()
    .map(|item| expensive_computation(item))
    .collect();
```

### Graceful Shutdown

```rust
use tokio::sync::watch;

let (shutdown_tx, mut shutdown_rx) = watch::channel(false);

// In worker
tokio::select! {
    _ = do_work() => {},
    _ = shutdown_rx.changed() => {
        // Clean up and exit
    }
}

// To signal shutdown
shutdown_tx.send(true).unwrap();
```

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `Arc<Mutex<T>>` for everything | Only when shared mutable state is genuinely needed |
| Holding `Mutex` lock across `.await` | Use `tokio::sync::Mutex` or restructure to release before await |
| `unwrap()` on `Mutex::lock()` | Consider `lock().expect("mutex poisoned")` or handle poisoning |
| Spawning unbounded tasks | Use semaphores or bounded channels to limit concurrency |
| Blocking in async context | Use `tokio::task::spawn_blocking` for CPU-heavy or blocking I/O |
