# Async Rust Pattern Catalog

## Spawning vs Joining vs Select

### `tokio::join!` — Concurrent, Same Task

Runs futures concurrently on the **same task** (no cross-thread parallelism). Borrows freely, no `Arc` needed.

```rust
let (users, orders) = tokio::try_join!(
    db.fetch_users(),
    db.fetch_orders(),
)?;
// All complete before this line. If any fails, others are cancelled.
```

| Correctness | Performance | Ergonomics | Debuggability |
|:-----------:|:-----------:|:----------:|:-------------:|
| 5 | 3 | 5 | 4 |

### `tokio::spawn` — Parallel, Detached

Creates a new task scheduled independently. Requires `'static + Send`. True parallelism across threads.

```rust
let handle = tokio::spawn(async move {
    fetch_remote(url).await
});
match handle.await {
    Ok(Ok(data)) => use_data(data),
    Ok(Err(e)) => handle_error(e),
    Err(join_err) => {
        if join_err.is_panic() {
            tracing::error!("task panicked");
        }
    }
}
```

| Correctness | Performance | Ergonomics | Debuggability |
|:-----------:|:-----------:|:----------:|:-------------:|
| 3 | 5 | 4 | 2 |

### `tokio::select!` — First to Complete

Polls all branches; first to complete wins, **losers are dropped (cancelled)**.

```rust
loop {
    tokio::select! {
        Some(msg) = rx.recv() => handle(msg).await,
        _ = token.cancelled() => break,
        _ = tokio::time::sleep(Duration::from_secs(30)) => {
            warn!("idle timeout");
            break;
        }
    }
}
```

| Correctness | Performance | Ergonomics | Debuggability |
|:-----------:|:-----------:|:----------:|:-------------:|
| 2 | 4 | 3 | 3 |

### `JoinSet` — Dynamic Task Collection

Collects results from a dynamic set of spawned tasks. **Abort-on-drop**: dropping the `JoinSet` aborts all remaining tasks.

```rust
let mut set = JoinSet::new();
for url in urls {
    set.spawn(fetch_url(url));
}
while let Some(res) = set.join_next().await {
    match res {
        Ok(Ok(data)) => results.push(data),
        Ok(Err(e)) => tracing::warn!(?e, "fetch failed"),
        Err(je) => tracing::error!("task panicked: {je}"),
    }
}
```

### `TaskTracker` — Graceful Drain

Fire-and-forget tasks with graceful shutdown. **Drop does NOT abort** — tasks continue to completion.

```rust
let tracker = TaskTracker::new();
for url in urls {
    tracker.spawn(async move { fetch_and_store(url).await });
}
tracker.close();
tracker.wait().await; // waits for all, doesn't abort
```

## Channel Patterns

| Channel | Topology | Buffer | Use Case |
|---------|----------|--------|----------|
| `mpsc` | N:1 | Bounded or unbounded | Work queues, command dispatch |
| `oneshot` | 1:1 | Single value | Request/response, completion signal |
| `broadcast` | N:M | Ring buffer | Event fan-out, pub/sub |
| `watch` | N:M | Latest only | Config reload, state snapshot |

### Actor Pattern (mpsc + oneshot)

```rust
enum Command {
    Get { key: String, reply: oneshot::Sender<Option<Vec<u8>>> },
    Set { key: String, value: Vec<u8>, reply: oneshot::Sender<()> },
}

async fn db_actor(mut rx: mpsc::Receiver<Command>, db: Database) {
    while let Some(cmd) = rx.recv().await {
        match cmd {
            Command::Get { key, reply } => {
                let _ = reply.send(db.get(&key).await);
            }
            Command::Set { key, value, reply } => {
                db.set(&key, &value).await;
                let _ = reply.send(());
            }
        }
    }
}

// Client side
async fn get(tx: &mpsc::Sender<Command>, key: String) -> Option<Vec<u8>> {
    let (reply_tx, reply_rx) = oneshot::channel();
    tx.send(Command::Get { key, reply: reply_tx }).await.ok()?;
    reply_rx.await.ok()?
}
```

### Config Hot-Reload (watch)

```rust
let (config_tx, config_rx) = watch::channel(load_config()?);

// Watcher task
tokio::spawn(async move {
    let mut interval = tokio::time::interval(Duration::from_secs(30));
    loop {
        interval.tick().await;
        if let Ok(cfg) = load_config() {
            let _ = config_tx.send(cfg);
        }
    }
});

// Worker reacts to changes
let mut rx = config_rx.clone();
loop {
    rx.changed().await?;
    let cfg = rx.borrow().clone();
    reconfigure(&cfg);
}
```

## Shared State

### Decision Tree

```
Lock held across .await?
  ├─ Yes → tokio::sync::Mutex (last resort) or actor pattern
  └─ No  → std::sync::Mutex (faster)
```

```rust
// PREFERRED: std Mutex, lock never crosses .await
struct AppState {
    inner: std::sync::Mutex<StateInner>,
}

impl AppState {
    fn increment(&self) -> u64 {
        let mut guard = self.inner.lock().unwrap();
        guard.counter += 1;
        guard.counter
        // guard dropped here, before any .await
    }
}
```

## Stream Processing

```rust
use tokio_stream::{StreamExt, wrappers::ReceiverStream};

let stream = ReceiverStream::new(rx);

let processed = stream
    .filter(|e| e.is_valid())
    .map(|e| transform(e))
    .chunks_timeout(100, Duration::from_millis(500)) // micro-batch
    .map(|batch| async move { write_batch(&batch).await })
    .buffer_unordered(4); // 4 concurrent writes

tokio::pin!(processed);
while let Some(result) = processed.next().await {
    result?;
}
```

## Backpressure

```rust
// Semaphore-based concurrency limiting
let semaphore = Arc::new(Semaphore::new(50));

loop {
    let (socket, _) = listener.accept().await?;
    let sem = semaphore.clone();
    tokio::spawn(async move {
        let _permit = sem.acquire().await.unwrap();
        handle_connection(socket).await;
        // permit dropped, freeing a slot
    });
}
```

## Key Documentation

- [Tokio Tutorial: Spawning](https://tokio.rs/tokio/tutorial/spawning)
- [Tokio Tutorial: Channels](https://tokio.rs/tokio/tutorial/channels)
- [Tokio Tutorial: Shared State](https://tokio.rs/tokio/tutorial/shared-state)
- [tokio::select! docs](https://docs.rs/tokio/latest/tokio/macro.select.html)
- [JoinSet API](https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html)
- [TaskTracker API](https://docs.rs/tokio-util/latest/tokio_util/task/task_tracker/struct.TaskTracker.html)
- [Alice Ryhl: Actors with Tokio](https://ryhl.io/blog/actors-with-tokio/)
