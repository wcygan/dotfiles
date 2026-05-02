# Upstream documentation index

Always prefer these two sources over reciting from memory. The crate is pre-1.0
and APIs shift across 0.3.x point releases.

## Table of contents

- [Primary references](#primary-references)
- [docs.rs module map](#docsrs-module-map)
- [Guide table of contents](#guide-table-of-contents)
- [Examples directory](#examples-directory)
- [How to fetch](#how-to-fetch)

## Primary references

| Source | URL | Use for |
|--------|-----|---------|
| API docs (canonical) | <https://docs.rs/connectrpc/latest/connectrpc/> | Exact type / trait / method signatures, feature gates, sealed-trait warnings |
| Guide (canonical) | <https://github.com/anthropics/connect-rust/blob/main/docs/guide.md> | End-to-end snippets, design rationale, streaming patterns, middleware composition |
| Repo root | <https://github.com/anthropics/connect-rust> | README, release notes, issue tracker |
| Examples | <https://github.com/anthropics/connect-rust/tree/main/examples> | Compilable working code |
| crates.io | <https://crates.io/crates/connectrpc> | Latest version, feature flags, downloads |
| Conformance | Mentioned in README — runtime passes 6,558 tests | Confidence signal for protocol behavior |

When the user asks "does X work?" and you are unsure of the current shape,
fetch `docs.rs` first, the guide second.

## docs.rs module map

Pinned URL: <https://docs.rs/connectrpc/latest/connectrpc/>

Top-level modules to know:

| Module | What lives there |
|--------|------------------|
| `connectrpc` (root) | `ConnectError`, `ErrorCode`, `ErrorDetail`, `ServiceResult`, `Response`, `RequestContext`, `OwnedView` |
| `connectrpc::client` | `HttpClient`, `ClientConfig`, `CallOptions`, generated client traits |
| `connectrpc::server` | `Server`, `ConnectRpcService`, registration helpers |
| `connectrpc::stream` | `ServiceStream`, stream adapters |
| `connectrpc::codec` | Wire codecs (proto / JSON), `Encodable<M>` |
| `connectrpc::compression` | `CompressionProvider`, `CompressionRegistry` |
| `connectrpc::axum` | `into_axum_router`, `into_axum_service` (gated on `axum` feature) |

Feature-gated re-exports may be hidden if the corresponding feature is off in
the docs build. If a symbol is missing from `docs.rs`, check whether the
feature flag is enabled in the docs.rs build (`Cargo.toml` `[package.metadata.docs.rs]`).

## Guide table of contents

Pinned URL: <https://github.com/anthropics/connect-rust/blob/main/docs/guide.md>

Sections (paraphrased — fetch the live document for exact headings):

1. **Three-crate ecosystem** — `connectrpc`, `connectrpc-build`, `protoc-gen-connect-rust`
2. **Code generation** — `build.rs` and `buf generate` paths
3. **Server setup** — handler trait, `RequestContext`, `OwnedView`
4. **Hosting** — Axum integration, standalone `Server`
5. **Zero-copy message handling** — view types, `Encodable<M>`
6. **Streaming** — server / client / bidi via `ServiceStream`
7. **Client setup** — `HttpClient::plaintext` / `with_tls`, `ClientConfig`, `CallOptions`
8. **Protocol support** — Connect, gRPC, gRPC-Web
9. **Error handling** — `ConnectError`, canonical codes, `ErrorDetail`
10. **Tower middleware** — `ServiceBuilder`, `tower-http`, axum `from_fn`
11. **Compression** — gzip / zstd negotiation, custom `CompressionProvider`
12. **TLS** — server `with_tls`, client `with_tls`, mTLS notes
13. **Examples directory walk-through**
14. **Limitations** — JSON+view, `extern_path`, `refining_impl_trait`, no built-in health

## Examples directory

<https://github.com/anthropics/connect-rust/tree/main/examples>

| Example | Coverage |
|---------|----------|
| `streaming-tour` | All four RPC kinds, handler signatures, client patterns |
| `middleware` | Tower auth, trailers, header / timeout `CallOptions` |
| `eliza` | Production-shaped app: TLS / mTLS, CORS, IPv6, streaming |
| `multiservice` | Multiple proto packages, `buf generate`, well-known types |
| `wasm-client` | Browser fetch transport, custom `ClientTransport` |
| `bazel` | Bazel build integration |

When in doubt, point at `streaming-tour` for handler shapes and `eliza` for a
realistic end-to-end deployment. Both are kept in sync with the runtime.

## How to fetch

From inside Claude Code:

```bash
# docs.rs — feature-gated; load with the feature you care about
gh api repos/anthropics/connect-rust/contents/docs/guide.md \
    --jq .content | base64 -d | head -200

# Latest release notes
gh release list -R anthropics/connect-rust -L 5

# Conformance run output (CI workflow names may shift)
gh run list -R anthropics/connect-rust --workflow conformance.yml -L 1
```

For `docs.rs`, the `WebFetch` tool works well — pass the module path, e.g.
<https://docs.rs/connectrpc/latest/connectrpc/client/struct.HttpClient.html>.
