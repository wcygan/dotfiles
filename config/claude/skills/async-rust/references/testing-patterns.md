# Testing Async Rust

## Test Runtime Setup

### Basic: `#[tokio::test]`

```rust
#[tokio::test]
async fn test_fetch_user() {
    let db = setup_test_db().await;
    let user = fetch_user(&db, 1).await.unwrap();
    assert_eq!(user.name, "Alice");
}
```

Default: single-threaded runtime. Use `flavor = "multi_thread"` to expose race conditions:

```rust
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_concurrent_access() {
    // This test exercises real multi-threaded behavior
}
```

### Time Control

```rust
#[tokio::test]
async fn test_timeout_behavior() {
    tokio::time::pause(); // freezes time

    let start = tokio::time::Instant::now();
    tokio::time::sleep(Duration::from_secs(3600)).await; // instant

    assert!(start.elapsed() >= Duration::from_secs(3600));
    // Only ~milliseconds of real wall time elapsed
}
```

Use `tokio::time::advance(Duration)` to manually advance the clock.

## Mocking Async Dependencies

### Trait-Based Mocking

```rust
#[async_trait]
trait UserRepository {
    async fn find_by_id(&self, id: u64) -> Result<User>;
    async fn save(&self, user: &User) -> Result<()>;
}

// Production implementation
struct PgUserRepository { pool: PgPool }

#[async_trait]
impl UserRepository for PgUserRepository {
    async fn find_by_id(&self, id: u64) -> Result<User> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(id as i64)
            .fetch_one(&self.pool)
            .await
            .map_err(Into::into)
    }
    // ...
}

// Test mock
struct MockUserRepository {
    users: HashMap<u64, User>,
}

#[async_trait]
impl UserRepository for MockUserRepository {
    async fn find_by_id(&self, id: u64) -> Result<User> {
        self.users.get(&id)
            .cloned()
            .ok_or_else(|| anyhow::anyhow!("not found"))
    }
    // ...
}
```

### HTTP Mocking with wiremock

```rust
use wiremock::{MockServer, Mock, ResponseTemplate};
use wiremock::matchers::{method, path};

#[tokio::test]
async fn test_api_client() {
    let mock_server = MockServer::start().await;

    Mock::given(method("GET"))
        .and(path("/users/1"))
        .respond_with(
            ResponseTemplate::new(200)
                .set_body_json(json!({"id": 1, "name": "Alice"}))
        )
        .mount(&mock_server)
        .await;

    let client = ApiClient::new(&mock_server.uri());
    let user = client.get_user(1).await.unwrap();
    assert_eq!(user.name, "Alice");
}
```

Each `MockServer` binds to an ephemeral port — tests run in parallel safely.

## Testing Channels and Tasks

```rust
#[tokio::test]
async fn test_worker_processes_jobs() {
    let (tx, rx) = mpsc::channel(10);
    let (result_tx, mut result_rx) = mpsc::channel(10);

    // Spawn the worker under test
    tokio::spawn(async move {
        worker(rx, result_tx).await;
    });

    // Send test data
    tx.send(Job::new("test")).await.unwrap();
    drop(tx); // close channel to signal worker to stop

    // Verify output
    let result = result_rx.recv().await.unwrap();
    assert_eq!(result.status, "completed");
}
```

## Testing Cancellation

```rust
#[tokio::test]
async fn test_worker_handles_cancellation() {
    let token = CancellationToken::new();
    let t = token.clone();

    let handle = tokio::spawn(async move {
        worker(t).await
    });

    // Let worker start
    tokio::time::sleep(Duration::from_millis(10)).await;

    // Cancel and verify clean shutdown
    token.cancel();
    handle.await.unwrap(); // should not panic
}
```

## Testing Graceful Shutdown

```rust
#[tokio::test]
async fn test_graceful_shutdown_drains() {
    tokio::time::pause();

    let token = CancellationToken::new();
    let tracker = TaskTracker::new();

    // Spawn a slow task
    let t = token.clone();
    tracker.spawn(async move {
        tokio::select! {
            _ = tokio::time::sleep(Duration::from_secs(5)) => {},
            _ = t.cancelled() => {},
        }
    });

    token.cancel();
    tracker.close();

    // Should complete quickly after cancellation
    tokio::time::timeout(Duration::from_secs(1), tracker.wait())
        .await
        .expect("shutdown should complete within timeout");
}
```

## Testing with Ephemeral Ports

```rust
async fn start_test_server() -> (SocketAddr, CancellationToken) {
    let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
    let addr = listener.local_addr().unwrap();
    let token = CancellationToken::new();
    let t = token.clone();

    tokio::spawn(async move {
        axum::serve(listener, app)
            .with_graceful_shutdown(async move { t.cancelled().await })
            .await
            .unwrap();
    });

    (addr, token)
}

#[tokio::test]
async fn test_integration() {
    let (addr, token) = start_test_server().await;
    let client = reqwest::Client::new();

    let resp = client.get(format!("http://{addr}/health"))
        .send().await.unwrap();
    assert_eq!(resp.status(), 200);

    token.cancel(); // clean shutdown
}
```

## Key Crates for Testing

| Crate | Purpose |
|-------|---------|
| `tokio::test` | Async test runtime with time control |
| `wiremock` | HTTP mock servers (parallel-safe) |
| `mockall` | Generate mock implementations from traits |
| `tokio-test` | `io::Builder` for mocking `AsyncRead`/`AsyncWrite` |
| `assert_matches` | Pattern matching assertions |

## Key Documentation

- [tokio::test macro](https://docs.rs/tokio/latest/tokio/attr.test.html)
- [wiremock-rs](https://github.com/LukeMathWalker/wiremock-rs)
- [Luca Palmieri: Zero to Production (testing chapters)](https://www.zero2prod.com/)
