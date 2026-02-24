---
title: Middleware
description: Axum middleware patterns including from_fn, from_extractor, Tower layers, execution order, and common middleware setups
tags: [axum, middleware, tower, layer, from_fn, from_extractor, Next]
---

# Middleware

Axum uses Tower middleware — no proprietary middleware system. This means middleware is reusable across Hyper, Tonic, and any Tower-based framework.

## from_fn — Simple Async Middleware

The most common pattern for custom middleware:

```rust
use axum::middleware::{self, Next};
use axum::http::Request;
use axum::response::Response;

async fn my_middleware(
    req: Request,
    next: Next,
) -> Response {
    // Do something before the handler
    println!("Request: {} {}", req.method(), req.uri());

    let response = next.run(req).await;

    // Do something after the handler
    println!("Response: {}", response.status());

    response
}

let app = Router::new()
    .route("/", get(handler))
    .layer(middleware::from_fn(my_middleware));
```

## from_fn_with_state — Middleware with State

```rust
async fn auth_middleware(
    State(state): State<AppState>,
    req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req.headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok());

    match auth_header {
        Some(token) if validate_token(token, &state.jwt_secret) => {
            Ok(next.run(req).await)
        }
        _ => Err(StatusCode::UNAUTHORIZED),
    }
}

let app = Router::new()
    .route("/protected", get(handler))
    .route_layer(middleware::from_fn_with_state(state.clone(), auth_middleware))
    .with_state(state);
```

## Using Extractors in Middleware

`from_fn` middleware can use extractors just like handlers:

```rust
async fn log_middleware(
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
    method: Method,
    uri: Uri,
    req: Request,
    next: Next,
) -> Response {
    println!("{addr} - {method} {uri}");
    next.run(req).await
}
```

**Important**: extractors in middleware follow the same rules — `FromRequestParts` extractors before the `Request` argument.

## from_extractor — Extractor as Middleware

Run an extractor and reject the request if it fails:

```rust
use axum::middleware::from_extractor;

// This extractor rejects if auth fails
struct RequireAuth(User);

impl<S> FromRequestParts<S> for RequireAuth { ... }

let app = Router::new()
    .route("/protected", get(handler))
    .route_layer(from_extractor::<RequireAuth>());
```

With state:

```rust
let app = Router::new()
    .route("/protected", get(handler))
    .route_layer(from_extractor_with_state::<RequireAuth, _>(state.clone()))
    .with_state(state);
```

## map_request / map_response

Tower combinators for simple transformations:

```rust
use tower::ServiceBuilder;
use axum::middleware::{map_request, map_response};

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(map_request(|mut req: Request| async move {
                req.headers_mut().insert("x-custom", "value".parse().unwrap());
                req
            }))
            .layer(map_response(|mut res: Response| async move {
                res.headers_mut().insert("x-powered-by", "axum".parse().unwrap());
                res
            }))
    );
```

## Execution Order

Layers wrap like an onion. When stacking with `.layer()`:

```rust
Router::new()
    .route("/", get(handler))
    .layer(layer_a)  // innermost — runs first on request, last on response
    .layer(layer_b)  // middle
    .layer(layer_c)  // outermost — runs last on request, first on response
```

**Request flow**: layer_c -> layer_b -> layer_a -> handler
**Response flow**: handler -> layer_a -> layer_b -> layer_c

### ServiceBuilder (intuitive order)

`ServiceBuilder` reverses the order — top-to-bottom execution:

```rust
use tower::ServiceBuilder;

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(layer_a)  // runs FIRST on request
            .layer(layer_b)  // runs second
            .layer(layer_c)  // runs third
    );
```

**Recommendation**: Use `ServiceBuilder` for multiple layers to avoid confusion.

## layer vs route_layer

```rust
let app = Router::new()
    .route("/api/data", get(handler))
    .route_layer(require_auth)     // only applied to matched routes
    .fallback(handler_404)
    .layer(TraceLayer::new_for_http());  // applied to everything, including fallback
```

- **`layer(L)`**: applies to all requests (matched routes AND fallback)
- **`route_layer(L)`**: applies only to matched routes, NOT fallback

Use `route_layer` for auth middleware — you don't want 404s to require auth.

## Passing Data from Middleware to Handlers

Use request extensions:

```rust
#[derive(Clone)]
struct CurrentUser(User);

async fn auth_middleware(mut req: Request, next: Next) -> Result<Response, StatusCode> {
    let user = authenticate(&req).ok_or(StatusCode::UNAUTHORIZED)?;
    req.extensions_mut().insert(CurrentUser(user));
    Ok(next.run(req).await)
}

async fn handler(Extension(user): Extension<CurrentUser>) -> impl IntoResponse {
    format!("Hello, {}", user.0.name)
}
```

## Common Middleware Stack

```rust
use tower::ServiceBuilder;
use tower_http::{
    cors::CorsLayer,
    trace::TraceLayer,
    compression::CompressionLayer,
    timeout::TimeoutLayer,
};
use std::time::Duration;

let app = Router::new()
    .route("/api/data", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(CorsLayer::permissive())
            .layer(CompressionLayer::new())
    );
```

## Custom Tower Service (Advanced)

For publishable, configurable middleware:

```rust
use tower::{Layer, Service};
use std::task::{Context, Poll};

#[derive(Clone)]
struct MyLayer;

impl<S> Layer<S> for MyLayer {
    type Service = MyMiddleware<S>;

    fn layer(&self, inner: S) -> Self::Service {
        MyMiddleware { inner }
    }
}

#[derive(Clone)]
struct MyMiddleware<S> {
    inner: S,
}

impl<S> Service<Request> for MyMiddleware<S>
where
    S: Service<Request, Response = Response> + Send + 'static,
    S::Future: Send + 'static,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = Pin<Box<dyn Future<Output = Result<Self::Response, Self::Error>> + Send>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Request) -> Self::Future {
        let future = self.inner.call(req);
        Box::pin(async move {
            let response = future.await?;
            Ok(response)
        })
    }
}
```
