# Compression and TLS

## Table of contents

- [Compression negotiation](#compression-negotiation)
- [Per-RPC overrides](#per-rpc-overrides)
- [Custom CompressionProvider](#custom-compressionprovider)
- [Server TLS](#server-tls)
- [Client TLS](#client-tls)
- [mTLS](#mtls)

## Compression negotiation

The default features pull in `gzip` and `zstd`. The runtime advertises
`accept-encoding: gzip, zstd` on responses. Clients sending
`connect-content-encoding: gzip` (or `zstd`) get decompressed automatically;
responses are compressed if the client advertises `accept-encoding`.

To strip a compressor entirely:

```toml
connectrpc = { version = "0.4", default-features = false, features = ["axum"] }
```

(`streaming` is also default — keep it on for streaming RPCs.)

## Per-RPC overrides

```rust
let mut resp = Response::ok(big_payload);
if response_is_huge() {
    resp = resp.compress(true);
}
```

Useful when a handler knows its payload is small and the codec-level threshold
would compress unnecessarily, or vice versa.

## Custom CompressionProvider

```rust
use connectrpc::compression::{CompressionProvider, CompressionRegistry};
use std::io::Read;

struct MyZip;

impl CompressionProvider for MyZip {
    fn name(&self) -> &'static str { "my-zip" }
    fn compress(&self, data: &[u8]) -> Result<bytes::Bytes, ConnectError> {
        /* … */
    }
    fn decompressor<'a>(&self, data: &'a [u8]) -> Result<Box<dyn Read + 'a>, ConnectError> {
        /* … */
    }
}

let registry = CompressionRegistry::default().register(MyZip);
let svc = ConnectRpcService::new(router).with_compression(registry);
```

You only need this for proprietary algorithms. gzip and zstd are already
covered.

## Server TLS

Enable the `server-tls` feature, build a `rustls::ServerConfig`, and hand it
to `connectrpc::axum::serve_tls` (added in 0.4.2). It is the companion to
`axum::serve` for the TLS path:

```rust
use std::sync::Arc;
use rustls::ServerConfig;

let tls: Arc<ServerConfig> = build_server_config()?;

let app = service.register(axum::Router::new()).into_axum_router();
let listener = tokio::net::TcpListener::bind("0.0.0.0:8443").await?;

connectrpc::axum::serve_tls(listener, app, tls)
    .with_graceful_shutdown(async {
        tokio::signal::ctrl_c().await.ok();
    })
    .await?;
```

Why use the helper rather than wrapping `axum::serve` with
`tokio_rustls::TlsAcceptor` yourself: the naive wrapper hangs on h2 ALPN
negotiation. `serve_tls` owns the accept loop and TLS handshake correctly.

If you have no axum stack and just want a TLS server, use the standalone:

```rust
connectrpc::Server::new(router)
    .with_tls(tls)
    .serve("0.0.0.0:8443".parse()?)
    .await?;
```

In production, terminate TLS at a reverse proxy (Envoy, ALB, ngrok) unless
your threat model requires end-to-end encryption to the process.

## Client TLS

```rust
use connectrpc::client::HttpClient;
use std::sync::Arc;

let mut roots = rustls::RootCertStore::empty();
roots.extend(webpki_roots::TLS_SERVER_ROOTS.iter().cloned());

let cfg = rustls::ClientConfig::builder()
    .with_root_certificates(roots)
    .with_no_client_auth();

let http = HttpClient::with_tls(Arc::new(cfg));
```

Always use the OS root store or a vendored `webpki-roots` set. Never disable
verification.

## mTLS

The `examples/mtls-identity/` example is the canonical reference. It:

- Generates an in-memory PKI (CA, server cert, two workload client certs)
  with `rcgen` — no PEM files on disk.
- Hosts on axum behind `connectrpc::axum::serve_tls`.
- The TLS layer stamps `PeerCerts` and `PeerAddr` into request extensions
  (same convention `connectrpc::Server::with_tls` uses).
- A handler parses the leaf cert's DNS SAN to derive a workload identity
  and enforces an ACL against it.

The configs themselves:

```rust
let client_cfg = rustls::ClientConfig::builder()
    .with_root_certificates(server_ca_roots)
    .with_client_auth_cert(my_chain, my_key)?;

let server_cfg = rustls::ServerConfig::builder()
    .with_client_cert_verifier(WebPkiClientVerifier::builder(client_ca_roots).build()?)
    .with_single_cert(server_chain, server_key)?;
```

In your handler, pull peer identity off the extensions:

```rust
let peer_certs = ctx.extensions.get::<PeerCerts>()
    .ok_or_else(|| ConnectError::new(ErrorCode::Unauthenticated, "no client cert"))?;
```

`PeerCerts` is the same shape whether you use `serve_tls` or
`Server::with_tls`, so handler code is portable between the two.
