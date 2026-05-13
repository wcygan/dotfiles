# Testing handlers and clients

Two layers of test, two patterns. Unit tests call the handler directly with a
synthetic `RequestContext` and `OwnedView`; integration tests spin up an
ephemeral `axum::serve` and hit it with the generated `*Client`.

## Table of contents

- [Unit test: handler in isolation](#unit-test-handler-in-isolation)
- [Constructing OwnedView from owned messages](#constructing-ownedview-from-owned-messages)
- [Asserting on the Response](#asserting-on-the-response)
- [Integration test: ephemeral server + generated client](#integration-test-ephemeral-server--generated-client)
- [Asserting on response views and trailers](#asserting-on-response-views-and-trailers)
- [Asserting on error codes](#asserting-on-error-codes)
- [Testing middleware-set extensions](#testing-middleware-set-extensions)

## Unit test: handler in isolation

The service trait is just `async fn`s on your struct. Construct the handler,
pass a context and an owned view, await:

```rust
#[tokio::test]
async fn square_doubles_the_input() {
    let svc = NumberServiceImpl;
    let ctx = RequestContext::default();
    let req = OwnedView::<SquareRequestView<'static>>::from_owned(
        &SquareRequest { value: Some(7), ..Default::default() },
    );
    let resp = svc.square(ctx, req).await.unwrap();
    assert_eq!(resp.body.squared, Some(49));
}
```

`RequestContext` derives `Default` — empty headers, no deadline, empty
extensions. Use `RequestContext::new(headers)` /
`.with_deadline(Some(instant))` / `.with_extensions(ext)` when the handler
reads them.

## Constructing OwnedView from owned messages

`OwnedView<TView<'static>>` is normally produced by the wire decoder. For
tests, build an owned message (`buffa`-generated, `#[derive(Default)]`) and
hand it to the helper:

```rust
use buffa::view::OwnedView;

let owned = GreetRequest { name: Some("alice".into()), ..Default::default() };
let view = OwnedView::<GreetRequestView<'static>>::from_owned(&owned);
```

The view borrows from `owned`, so keep `owned` alive for the call. In a
typical test that's automatic — the binding stays in scope.

## Asserting on the Response

`Response<M>` is `pub struct`, so its fields are directly inspectable:

```rust
let resp = svc.greet(ctx, view).await.unwrap();
assert_eq!(resp.body.greeting.as_deref(), Some("hello, alice"));
assert_eq!(resp.headers.get("x-version").unwrap(), "v2");
assert_eq!(resp.trailers.get("x-server-id").unwrap(), "node-7");
```

For the error path, match on `ConnectError::code`:

```rust
let err = svc.greet(ctx, bad_view).await.unwrap_err();
assert_eq!(err.code, ErrorCode::InvalidArgument);
assert!(err.message.contains("name must not be empty"));
```

Unit tests are the right home for argument validation, ACL enforcement,
formatting, and any branch that doesn't depend on the wire format or
middleware.

## Integration test: ephemeral server + generated client

For anything that exercises the wire path (codecs, headers, trailers,
middleware, TLS), bind a TcpListener on port 0 and spawn the server:

```rust
async fn start_server() -> std::net::SocketAddr {
    let service = Arc::new(NumberServiceImpl);
    let connect_router = service.register(Router::new());
    let app = connect_router.into_axum_router();

    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let addr = listener.local_addr().unwrap();
    tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });
    addr
}

fn make_client(addr: std::net::SocketAddr) -> NumberServiceClient<HttpClient> {
    let config = ClientConfig::new(format!("http://{addr}").parse().unwrap());
    NumberServiceClient::new(HttpClient::plaintext(), config)
}

#[tokio::test]
async fn square_over_the_wire() {
    let addr = start_server().await;
    let client = make_client(addr);
    let resp = client.square(SquareRequest {
        value: Some(7),
        ..Default::default()
    }).await.unwrap();
    assert_eq!(resp.view().squared, Some(49));
}
```

Port `0` lets the OS pick a free port — parallel tests don't collide. The
spawned server stays alive until the runtime shuts down at end-of-test; there
is no explicit cleanup to write.

For tests that need the *full* middleware stack (auth, tracing, timeouts),
build the same `axum::Router` your production `main.rs` builds — extracting it
into a helper is the standard refactor:

```rust
// In src/lib.rs of the example crate
pub fn build_app(service: Arc<MyService>, deps: Deps) -> axum::Router { /* ... */ }

// In tests
let app = build_app(Arc::new(MyService::new()), test_deps());
let listener = ...;
tokio::spawn(async move { axum::serve(listener, app).await.unwrap() });
```

This mirrors the pattern in `examples/middleware/tests/e2e.rs` (the canonical
reference for middleware-bearing integration tests).

## Asserting on response views and trailers

The client response exposes the body as a view and the trailers as a
`HeaderMap`:

```rust
let resp = client.get_secret(req).await.unwrap();
assert_eq!(resp.view().value, Some("the value of teamwork"));
assert_eq!(
    resp.trailers().get("x-served-by").unwrap().to_str().unwrap(),
    "alice",
);
```

`resp.view()` is the zero-copy path — fields are `&str` borrowed from the
internal buffer. Use `resp.into_owned()` when you need to outlive the
response (storing in test fixtures, returning across an `await` boundary
that drops `resp`).

## Asserting on error codes

Errors propagate as `ConnectError` regardless of which protocol was used:

```rust
let err = client.get_secret(bad_req).await.expect_err("should be denied");
assert_eq!(err.code, ErrorCode::PermissionDenied);
assert!(err.message.contains("alice-only"));
```

For structured error payloads (`ErrorDetail` entries), see `errors.md`.

## Testing middleware-set extensions

When a handler reads `ctx.extensions.get::<UserId>()`, the unit-test version
inserts directly into the context:

```rust
let mut ext = http::Extensions::new();
ext.insert(UserId("alice".into()));
let ctx = RequestContext::default().with_extensions(ext);
let resp = svc.get_secret(ctx, view).await.unwrap();
```

The integration-test version goes through the real middleware chain — build
the app with the auth layer wired in, send the right `Authorization` header
on the client, and the layer inserts the extension on the way through.
Asymmetry between the two layers usually indicates a misconfigured
middleware stack in production, so it pays to have at least one
integration test that covers the auth path end-to-end.
