# Graceful Shutdown Patterns

## The Standard Three-Phase Pattern

```rust
use tokio::signal;
use tokio_util::sync::CancellationToken;
use tokio_util::task::TaskTracker;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let token = CancellationToken::new();
    let tracker = TaskTracker::new();

    // Spawn workers
    for i in 0..num_workers {
        let t = token.clone();
        tracker.spawn(async move {
            worker(i, t).await;
        });
    }

    // Phase 1: Wait for shutdown signal
    tokio::select! {
        _ = signal::ctrl_c() => {
            tracing::info!("received ctrl-c");
        }
    }

    // Phase 2: Signal all tasks to stop accepting new work
    token.cancel();

    // Phase 3: Wait for in-flight work to drain (with timeout)
    tracker.close();
    if tokio::time::timeout(Duration::from_secs(30), tracker.wait())
        .await
        .is_err()
    {
        tracing::warn!("shutdown timed out, some tasks abandoned");
    }

    tracing::info!("shutdown complete");
    Ok(())
}
```

## Worker Pattern with CancellationToken

```rust
async fn worker(id: usize, token: CancellationToken) {
    loop {
        tokio::select! {
            // Normal work
            Some(job) = job_queue.recv() => {
                if token.is_cancelled() {
                    // Drain mode: skip new work
                    continue;
                }
                process_job(job).await;
            }
            // Shutdown signal
            _ = token.cancelled() => {
                tracing::info!(worker = id, "shutting down");
                flush_pending().await;
                break;
            }
        }
    }
}
```

## HTTP Server Shutdown (axum)

```rust
let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
axum::serve(listener, app)
    .with_graceful_shutdown(shutdown_signal())
    .await?;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("ctrl-c handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("SIGTERM handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
}
```

## gRPC Server Shutdown (tonic)

```rust
let token = CancellationToken::new();
let t = token.clone();

let server = tonic::transport::Server::builder()
    .layer(TraceLayer::new_for_grpc())
    .add_service(my_service)
    .serve_with_shutdown("[::]:50051".parse()?, async move {
        t.cancelled().await;
    });

tokio::select! {
    result = server => result?,
    _ = signal::ctrl_c() => token.cancel(),
}
```

## Hierarchical Cancellation

```rust
let root = CancellationToken::new();

// Each subsystem gets a child token
let http_token = root.child_token();
let grpc_token = root.child_token();
let bg_token = root.child_token();

// Cancelling root cascades to all children
root.cancel();

// Children can also cancel independently
// (does not affect parent or siblings)
http_token.cancel();
```

## Key Points

- **Always set a drain timeout.** Indefinite waiting on in-flight work can prevent process exit.
- **`spawn_blocking` tasks cannot be aborted.** They run to completion regardless of cancellation.
- **Use `TaskTracker` over manual `JoinHandle` collection.** Handles the bookkeeping of tracking spawned tasks.
- **Flush telemetry during shutdown.** Call `opentelemetry::global::shutdown_tracer_provider()` or equivalent.
- **Test shutdown.** Use `#[tokio::test]` with `tokio::time::pause()` to verify timeout behavior.

## Key Documentation

- [Tokio: Graceful Shutdown](https://tokio.rs/tokio/topics/shutdown)
- [CancellationToken API](https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html)
- [TaskTracker API](https://docs.rs/tokio-util/latest/tokio_util/task/task_tracker/struct.TaskTracker.html)
- [tokio-graceful-shutdown crate](https://crates.io/crates/tokio-graceful-shutdown)
