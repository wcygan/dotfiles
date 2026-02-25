# Tower Middleware

## The Service Trait

Tower's core abstraction for request/response services:

```rust
pub trait Service<Request> {
    type Response;
    type Error;
    type Future: Future<Output = Result<Self::Response, Self::Error>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>>;
    fn call(&mut self, req: Request) -> Self::Future;
}
```

- `poll_ready`: backpressure signal — "can I accept a request?"
- `call`: process the request, return a future

## Using Built-in Layers

```rust
use tower::ServiceBuilder;
use tower_http::{
    trace::TraceLayer,
    timeout::TimeoutLayer,
    compression::CompressionLayer,
    cors::CorsLayer,
};

// Layers wrap bottom-to-top:
// Request → Trace → Timeout → Compression → Handler
// Response ← Trace ← Timeout ← Compression ← Handler
let app = Router::new()
    .route("/api/items", get(list_items))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())       // outermost
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(CorsLayer::permissive())
            .layer(CompressionLayer::new()),          // innermost
    );
```

## Writing Custom Middleware

### Simple: Function-Based (axum)

```rust
use axum::middleware::{self, Next};
use axum::extract::Request;

async fn auth_middleware(
    req: Request,
    next: Next,
) -> Result<impl IntoResponse, StatusCode> {
    let token = req.headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok())
        .ok_or(StatusCode::UNAUTHORIZED)?;

    validate_token(token).map_err(|_| StatusCode::UNAUTHORIZED)?;
    Ok(next.run(req).await)
}

let app = Router::new()
    .route("/protected", get(handler))
    .layer(middleware::from_fn(auth_middleware));
```

### Full: Tower Service + Layer

```rust
use std::task::{Context, Poll};
use tower::{Layer, Service};

// Layer: factory that wraps a service
#[derive(Clone)]
struct RateLimitLayer {
    semaphore: Arc<Semaphore>,
}

impl<S> Layer<S> for RateLimitLayer {
    type Service = RateLimitService<S>;

    fn layer(&self, inner: S) -> Self::Service {
        RateLimitService {
            inner,
            semaphore: self.semaphore.clone(),
        }
    }
}

// Service: the actual middleware logic
#[derive(Clone)]
struct RateLimitService<S> {
    inner: S,
    semaphore: Arc<Semaphore>,
}

impl<S, Req> Service<Req> for RateLimitService<S>
where
    S: Service<Req> + Clone + Send + 'static,
    S::Future: Send,
    Req: Send + 'static,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = Pin<Box<dyn Future<Output = Result<S::Response, S::Error>> + Send>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Req) -> Self::Future {
        let sem = self.semaphore.clone();
        let mut inner = self.inner.clone();
        Box::pin(async move {
            let _permit = sem.acquire().await.unwrap();
            inner.call(req).await
        })
    }
}
```

## When to Use Tower vs a Simple Function

| Situation | Use |
|-----------|-----|
| One-off middleware for a single app | axum `middleware::from_fn` |
| Reusable middleware across services | Tower `Layer` + `Service` |
| Need backpressure (`poll_ready`) | Tower `Service` |
| gRPC + HTTP sharing same middleware | Tower `Layer` (applies to both axum and tonic) |

## Common Tower Layers

| Layer | Crate | Purpose |
|-------|-------|---------|
| `TraceLayer` | `tower-http` | Request/response tracing with spans |
| `TimeoutLayer` | `tower-http` | Request timeout |
| `CompressionLayer` | `tower-http` | Response compression (gzip, brotli, zstd) |
| `CorsLayer` | `tower-http` | CORS headers |
| `ConcurrencyLimitLayer` | `tower` | Max concurrent requests |
| `RateLimitLayer` | `tower` | Requests per time window |
| `RetryLayer` | `tower` | Automatic retries with backoff |
| `LoadShedLayer` | `tower` | Reject requests when overloaded |

## Key Documentation

- [Inventing the Service Trait (Tokio blog)](https://tokio.rs/blog/2021-05-14-inventing-the-service-trait)
- [Tower Service trait](https://docs.rs/tower/latest/tower/trait.Service.html)
- [Tower middleware guide](https://github.com/tower-rs/tower/blob/master/guides/building-a-middleware-from-scratch.md)
- [tower-http crate](https://docs.rs/tower-http/latest/tower_http/)
- [axum middleware docs](https://docs.rs/axum/latest/axum/middleware/index.html)
