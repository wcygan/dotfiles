---
name: connectrpc-rust
description: ConnectRPC Rust expert for the `connectrpc` crate (anthropics/connect-rust). Use when building Tower-based ConnectRPC servers/clients in Rust, generating code via `connectrpc-build` or `protoc-gen-connect-rust`, working with `OwnedView`/`ServiceStream`/`ConnectError`/`RequestContext`/`Encodable`, or porting from tonic. Prefers Axum integration. Auto-loads on `connectrpc` crate imports, `connectrpc-build` in build.rs, or ConnectRPC mentions in Rust contexts. Keywords connectrpc, connect-rust, connectrpc-build, protoc-gen-connect-rust, OwnedView, ServiceStream, ConnectError, Encodable, buffa, axum, tower, rustls, tonic migration.
---

# ConnectRPC for Rust

Tower-based Rust implementation of the ConnectRPC protocol. One server speaks
**Connect**, **gRPC**, and **gRPC-Web** over HTTP/1.1 and HTTP/2 with binary or
JSON protobuf. Zero-copy decoding via `buffa` borrowed views.

- Crate: `connectrpc` v0.3.x — Apache-2.0, **MSRV 1.88** (2024 edition)
- Repo: <https://github.com/anthropics/connect-rust>
- API docs: <https://docs.rs/connectrpc/latest/connectrpc/>
- Guide: <https://github.com/anthropics/connect-rust/blob/main/docs/guide.md>
- Status: pre-1.0, passes all 6,558 Connect conformance tests
- Reported perf vs tonic 0.14: 1.35×–1.95× lower single-request latency

## Preferences (codified)

1. **Axum-first.** Mount on `axum::Router` via
   `service.register(Router::new()).into_axum_router()`. Use the standalone
   `connectrpc::Server` only when there is no existing HTTP stack. Rationale:
   composes with `tower-http`, `axum::middleware::from_fn`, and the rest of
   the Tower ecosystem.
2. **Codegen via `connectrpc-build` from `build.rs`** by default. Switch to
   `buf generate` only when checked-in code or multi-language repos demand it.
3. **Return owned messages from handlers** unless a benchmark proves the view
   path matters. View returns break JSON clients — see `gotchas.md`.
4. **TLS via rustls** (`client-tls` / `server-tls` features). No native-tls.

## Where to look — always

The two upstream sources below are authoritative. Skim them before answering
shape-of-API questions from memory:

| Question | Source |
|----------|--------|
| Exact type / trait / method signature, feature gates, sealed traits | <https://docs.rs/connectrpc/latest/connectrpc/> |
| End-to-end "how do I build this" with full snippets, design rationale | <https://github.com/anthropics/connect-rust/blob/main/docs/guide.md> |
| Working code | <https://github.com/anthropics/connect-rust/tree/main/examples> |

`docs.rs` is canonical for *what exists*. The guide is canonical for *how to use it*.
When they disagree, trust `docs.rs` for signatures and the guide for rationale.
See `references/upstream-docs.md` for a navigation index of both.

## Cargo snippet

```toml
[dependencies]
connectrpc = { version = "0.3", features = ["axum", "client", "tls"] }
tokio = { version = "1", features = ["full"] }
axum = "0.7"

[build-dependencies]
connectrpc-build = "0.3"
```

Feature flags: `gzip` / `zstd` / `streaming` (default), `client`, `client-tls`,
`server`, `server-tls`, `tls`, `axum`. Generated proto types come from `buffa`,
not `prost` — no separate `prost` dependency is required.

## Architecture at a glance

```
Browser / mobile / CLI
        │   Connect | gRPC | gRPC-Web
        ▼
  axum::Router  ◀─ tower-http, auth, tracing layers
        │
        │  service.register(Router::new()).into_axum_router()
        ▼
  ConnectRpcService  ◀─ codecs, compression, dispatcher
        │
        ▼
  Generated trait impl  ◀─ async fn handler(ctx, req: OwnedView<…View<'static>>)
```

The dispatcher auto-selects the protocol from request headers — one handler
serves all three. `RequestContext` carries headers, deadline, and
`http::Extensions` so middleware-set state flows into handlers.

## References

| File | Read when |
|------|-----------|
| [`upstream-docs.md`](references/upstream-docs.md) | Looking something up — canonical URLs, module map for docs.rs, examples directory index |
| [`quickstart-axum.md`](references/quickstart-axum.md) | Bootstrapping a new project end-to-end with Axum |
| [`server.md`](references/server.md) | Handlers, `RequestContext`, `OwnedView`, response builder, registration, streaming |
| [`client.md`](references/client.md) | `HttpClient`, `ClientConfig`, `CallOptions`, response access patterns |
| [`errors.md`](references/errors.md) | `ConnectError`, codes, `ErrorDetail`, HTTP status mapping |
| [`protocols.md`](references/protocols.md) | Connect / gRPC / gRPC-Web matrix and conformance |
| [`compression-tls.md`](references/compression-tls.md) | gzip/zstd negotiation, custom `CompressionProvider`, rustls server/client |
| [`codegen.md`](references/codegen.md) | `connectrpc-build` vs `buf generate` vs `protoc-gen-connect-rust` |
| [`gotchas.md`](references/gotchas.md) | JSON+view incompatibility, `extern_path` orphan rule, `refining_impl_trait` lint, no built-in health, pre-1.0 caveats, tonic-migration deltas |

## Quick triage

- "Add a new RPC service" → `quickstart-axum.md` then `server.md`
- "Hook this into our auth middleware" → `server.md` (Extensions) + Axum middleware
- "Why does the JSON client get `unimplemented`?" → `gotchas.md`
- "What error code should I return?" → `errors.md`
- "Migrating from tonic" → `gotchas.md` (deltas) + `server.md` + `client.md`
- "How do I generate code without `build.rs`?" → `codegen.md`
- "TLS / mTLS setup" → `compression-tls.md`
