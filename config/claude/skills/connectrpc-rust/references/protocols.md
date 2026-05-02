# Protocols: Connect, gRPC, gRPC-Web

One server, three wire protocols. Clients pick by sending different headers;
the dispatcher routes accordingly.

## Table of contents

- [Protocol matrix](#protocol-matrix)
- [How the dispatcher chooses](#how-the-dispatcher-chooses)
- [When each protocol is appropriate](#when-each-protocol-is-appropriate)
- [Conformance](#conformance)
- [Known constraints](#known-constraints)

## Protocol matrix

| Protocol | HTTP version | Encoding | Streaming | Browser native | curl-friendly |
|----------|--------------|----------|-----------|----------------|---------------|
| Connect | HTTP/1.1 + HTTP/2 | binary proto **or** JSON | yes (H/2) | yes (unary) | yes |
| gRPC | HTTP/2 only | binary proto | yes | no | no (length-prefix + trailers) |
| gRPC-Web | HTTP/1.1 | binary proto | server only | yes (via grpc-web client) | partially |

All three speak to the same generated handler. There is no separate "gRPC
server" or "gRPC-Web server" mode.

## How the dispatcher chooses

| Header / signal | Routes to |
|-----------------|-----------|
| `content-type: application/grpc` (or `+proto`) | gRPC |
| `content-type: application/grpc-web` (or `+proto`) | gRPC-Web |
| `content-type: application/proto` | Connect (binary) |
| `content-type: application/json` | Connect (JSON) |
| `content-type: application/connect+proto` (streaming) | Connect streaming |

The dispatcher also handles the `connect-protocol-version` and
`connect-content-encoding` request headers transparently.

## When each protocol is appropriate

**Connect (binary or JSON)** — default. JSON encoding is invaluable for
debugging and for browser clients that don't want to ship a protobuf runtime.
Choose this for any new internal API.

**gRPC** — interop with existing gRPC infrastructure (Envoy, gRPC clients in
other languages, gRPC reflection tooling). Picks up HTTP/2 multiplexing.

**gRPC-Web** — browser clients that need streaming and use a `grpc-web` client
library. For unary calls from a browser, plain Connect over HTTP/1.1 is
simpler.

## Conformance

The README states the runtime passes all **6,558 Connect conformance tests**.
This covers cross-protocol behavior: a gRPC client hitting a Connect server,
trailers, error mapping, encoding negotiation, and edge cases like
zero-message streams. If something seems off, check whether your test is one
of the conformance scenarios first — the suite is comprehensive.

## Known constraints

- **JSON request bodies cannot use view-bodied responses.** When a handler
  returns a borrowed view and the request was JSON, the codec falls back to
  `unimplemented`. Return owned messages for any RPC that may serve JSON.
  See `gotchas.md`.
- **gRPC requires HTTP/2.** Behind a reverse proxy, terminate H/2 to the
  service or use h2c if cleartext.
- **Compression negotiation is automatic.** If the client advertises `gzip` or
  `zstd`, the server may compress responses. To disable, drop the feature
  flag. See `compression-tls.md`.
