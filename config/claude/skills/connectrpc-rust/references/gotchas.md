# Gotchas, limitations, and tonic-migration deltas

Read before debugging anything that "should just work."

## Table of contents

- [JSON requests + view bodies](#json-requests--view-bodies)
- [extern_path orphan rule](#extern_path-orphan-rule)
- [refining_impl_trait lint](#refining_impl_trait-lint)
- [No built-in health or reflection endpoints](#no-built-in-health-or-reflection-endpoints)
- [MSRV 1.88 and pre-1.0 status](#msrv-188-and-pre-10-status)
- [Migrating from tonic — what differs](#migrating-from-tonic--what-differs)

## JSON requests + view bodies

A handler can return a borrowed view via the `Encodable<M>` trait to skip
allocation on the proto path. **JSON clients hitting that handler will
receive an `unimplemented` error** — JSON serialization is only wired for
owned proto structs, not views.

Default rule: return owned messages from handlers. Only return views when:

1. You have measured the allocation as a real bottleneck.
2. The RPC will never be called with `content-type: application/json` (e.g.
   internal-only gRPC traffic, no browser/JS clients).

If you do return views, document it on the handler so future maintainers
don't accidentally enable JSON for that endpoint.

## extern_path orphan rule

`connectrpc_build::Config::extern_path(".my.pkg", "::other_crate::my::pkg")`
remaps types to a foreign crate. Because of Rust's orphan rule,
`connectrpc-build` cannot emit `impl Encodable<...>` for types it doesn't own.

Effect: any handler whose request or response type lives behind an
`extern_path` mapping must use owned messages (the view fast-path is
unavailable). This is rarely a concern — it just means you can't squeeze the
view-path optimization out of cross-crate types.

## refining_impl_trait lint

Returning a view from a handler tightens `impl Encodable<M>` further than the
trait declares. Rust's `refining_impl_trait` lint flags this. The crate-level
fix:

```rust
// in lib.rs / main.rs
#![allow(refining_impl_trait)]
```

Or per-impl:

```rust
#[allow(refining_impl_trait)]
impl GreetService for MyGreet { /* … */ }
```

This is documented in the guide. It's a deliberate trade — the refinement
buys the zero-copy return.

## No built-in health or reflection endpoints

There is no `connectrpc::health` or `connectrpc::reflection` module the way
`tonic` has `tonic-health` and `tonic-reflection`. Options:

1. **Define an explicit health RPC in your `.proto`** and implement it. This
   is the simplest path and works for any client.
2. **Add a plain Axum route**: `app.route("/healthz", get(|| async { "ok" }))`.
   Reverse proxies and Kubernetes probes don't need ConnectRPC for liveness.

For gRPC reflection specifically, a Rust server intended to interop with
`grpcurl` users will need to roll a reflection RPC by hand or expose the
service descriptors via a separate endpoint.

## MSRV 1.88 and pre-1.0 status

- **MSRV 1.88, edition 2024.** This is recent — older toolchains and Linux
  distro packages will not work. Pin a `rust-toolchain.toml`.
- **Pre-1.0.** APIs may shift across 0.3.x. The 6,558-test conformance suite
  is a strong stability signal for *protocol* behavior, not Rust API
  stability. When upgrading, expect minor type-level churn.
- **Crate published 2025-10-14, repo open-sourced 2026-03-04.** Look at recent
  release notes (`gh release list -R anthropics/connect-rust`) before
  trusting older third-party tutorials.

## Migrating from tonic — what differs

For someone fluent in tonic, the deltas are:

| Concept | tonic | connectrpc |
|---------|-------|------------|
| Service trait | `#[tonic::async_trait]` decorated | Plain `async fn` (Rust 2024 edition) |
| Request type | `tonic::Request<T>` | `(RequestContext, OwnedView<TView<'static>>)` |
| Response type | `tonic::Response<T>` | `Response<T>` (different module) |
| Server entrypoint | `Server::builder().add_service(...).serve(addr)` | `service.register(Router::new()).into_axum_router()` + `axum::serve` |
| Interceptors | `tonic::Interceptor` trait | Axum / Tower middleware via `http::Extensions` |
| Error type | `tonic::Status` | `ConnectError` (same code set, different name) |
| Codegen | `tonic-build` / `prost-build` | `connectrpc-build` / `buffa` |
| Streaming type | `tonic::Streaming<T>` | `ServiceStream<T>` |
| Feature flag for transport | `transport` (default) | `axum` + `client` etc. (more granular) |

Behavioral wins on the connectrpc side:

- **One server speaks all three protocols.** No separate setup for gRPC vs
  gRPC-Web vs Connect.
- **JSON encoding is built in.** No tonic-equivalent of `application/json`.
- **Tower composition is first-class.** No special interceptor abstraction —
  you use the same middleware everywhere else in your Axum app uses.
- **Zero-copy decode** for handlers that opt into the view path.

Behavioral *losses*:

- **No `tonic-health`, `tonic-reflection`, `tonic-web` story.** Roll-your-own
  for health; reflection requires manual work.
- **Pre-1.0 churn risk.** tonic is 0.x but mature; connectrpc is 0.x and young.
- **`prost` ecosystem doesn't apply directly.** `buffa`-typed messages work
  differently (views vs owned). Code that hand-builds `prost::Message` impls
  needs reworking.
