# Cancellation Safety in Async Rust

## What Is Cancellation?

In async Rust, a future can be **dropped at any `.await` point** without completing. This happens when:

- `tokio::select!` drops the losing branch
- `tokio::time::timeout` exceeds its deadline
- A `JoinHandle` is aborted or dropped
- A parent future is dropped (cascades to children)

When a future is dropped, its `Drop` impl runs **synchronously**. You cannot do async cleanup in a destructor.

## Cancel-Safety Reference Table

| Operation | Cancel-Safe? | Notes |
|-----------|:------------:|-------|
| `mpsc::Receiver::recv` | Yes | No data lost on cancellation |
| `oneshot::Receiver` | Yes | Value stays in channel if not received |
| `TcpListener::accept` | Yes | Connection returned to queue |
| `AsyncReadExt::read` | Yes | Partial read lost, but retryable |
| `AsyncReadExt::read_exact` | **No** | Partial read lost; track offset externally |
| `AsyncWriteExt::write_all` | **No** | Partial write; track bytes written |
| `Mutex::lock` | **No** | Lose queue position |
| `Semaphore::acquire` | **No** | Lose queue position |
| `tokio_stream::StreamExt::next` | Yes | Safe to retry |
| `broadcast::Receiver::recv` | Yes | Lagged messages may be lost (by design) |
| `watch::Receiver::changed` | Yes | Only latest value matters |

## Patterns for Cancel-Safe Code

### Pattern 1: Use `CancellationToken` for Cooperative Cancellation

```rust
use tokio_util::sync::CancellationToken;

async fn worker(token: CancellationToken, mut rx: mpsc::Receiver<Job>) {
    loop {
        tokio::select! {
            Some(job) = rx.recv() => {
                // Check between units of work
                if token.is_cancelled() {
                    tracing::info!("draining: skipping new job");
                    continue;
                }
                process_job(job).await;
            }
            _ = token.cancelled() => {
                tracing::info!("shutdown signal received");
                flush_state().await;
                break;
            }
        }
    }
}

// Hierarchical: child tokens cancel when parent does
let parent = CancellationToken::new();
let child = parent.child_token();
parent.cancel(); // cascades to child
```

### Pattern 2: Protect Critical Sections with `spawn`

Spawned tasks are independent — they continue even if the parent is cancelled.

```rust
// Critical section that MUST complete atomically
async fn transfer(from: &Account, to: &Account, amount: u64) {
    // Spawn to protect from parent cancellation
    let result = tokio::spawn(async move {
        let tx = db.begin_transaction().await?;
        tx.debit(from, amount).await?;
        tx.credit(to, amount).await?;
        tx.commit().await
    }).await??;
}
```

### Pattern 3: Track Progress Externally for Non-Cancel-Safe Operations

```rust
// read_exact is not cancel-safe — track progress ourselves
async fn read_frame(stream: &mut TcpStream, buf: &mut [u8]) -> io::Result<()> {
    let mut offset = 0;
    while offset < buf.len() {
        // If cancelled here, offset is preserved for retry
        let n = stream.read(&mut buf[offset..]).await?;
        if n == 0 {
            return Err(io::Error::new(io::ErrorKind::UnexpectedEof, "EOF"));
        }
        offset += n;
    }
    Ok(())
}
```

### Pattern 4: Idempotent Operations

Design async functions so re-execution after cancellation produces the same result.

```rust
// Idempotent: safe to retry if cancelled
async fn upsert_user(db: &Database, user: &User) -> Result<()> {
    db.execute(
        "INSERT INTO users (id, name) VALUES ($1, $2)
         ON CONFLICT (id) DO UPDATE SET name = $2",
        &[&user.id, &user.name],
    ).await?;
    Ok(())
}
```

## The Async Drop Problem

```rust
struct DbConnection { /* ... */ }

impl Drop for DbConnection {
    fn drop(&mut self) {
        // CANNOT do: self.send_disconnect().await
        // Drop is synchronous. The connection leaks.
    }
}
```

**Workarounds:**
- Use connection pools (`sqlx::Pool`) that handle cleanup internally
- Explicit `async fn close(self)` method that users must call
- Background task that monitors dropped connections

## Key Documentation

- [Oxide RFD 400: Cancel Safety](https://rfd.shared.oxide.computer/rfd/400)
- [sunshowers: Cancelling async Rust](https://sunshowers.io/posts/cancelling-async-rust/)
- [Tokio select! cancel safety](https://docs.rs/tokio/latest/tokio/macro.select.html)
- [CancellationToken API](https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html)
- [Cybernetist: Tokio Task Cancellation Patterns](https://cybernetist.com/2024/04/19/rust-tokio-task-cancellation-patterns/)
- [Yoshua Wuyts: Async Cancellation I](https://blog.yoshuawuyts.com/async-cancellation-1/)
