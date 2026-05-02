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
connectrpc = { version = "0.3", default-features = false, features = ["axum"] }
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

Enable the `server-tls` feature, build a `rustls::ServerConfig`, and either
hand it to the standalone server or wrap an `axum::serve` listener:

```rust
use std::sync::Arc;
use rustls::ServerConfig;

let tls: Arc<ServerConfig> = build_server_config()?;

// Standalone:
connectrpc::Server::new(router)
    .with_tls(tls)
    .serve("0.0.0.0:8443".parse()?)
    .await?;

// Axum + tokio-rustls (more flexible):
let acceptor = tokio_rustls::TlsAcceptor::from(tls);
let listener = tokio::net::TcpListener::bind("0.0.0.0:8443").await?;
loop {
    let (stream, _) = listener.accept().await?;
    let acceptor = acceptor.clone();
    let app = app.clone();
    tokio::spawn(async move {
        let stream = acceptor.accept(stream).await?;
        axum::serve::serve(stream, app).await
    });
}
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

The `eliza` example covers the full client-CA pattern: generate a CA,
issue server and client certs, and pin them on both sides:

```rust
let client_cfg = rustls::ClientConfig::builder()
    .with_root_certificates(server_ca_roots)
    .with_client_auth_cert(my_chain, my_key)?;

let server_cfg = rustls::ServerConfig::builder()
    .with_client_cert_verifier(WebPkiClientVerifier::builder(client_ca_roots).build()?)
    .with_single_cert(server_chain, server_key)?;
```

Pull authenticated identity off the connection via `RequestContext::extensions`
once your TLS layer inserts it (`tokio_rustls::server::TlsStream` exposes the
peer cert chain).
