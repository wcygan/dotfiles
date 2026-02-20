---
name: connectrpc
description: ConnectRPC expert for Go servers and Node.js clients. Auto-loads when working with ConnectRPC, connect-go, connect-node, protobuf RPC, buf codegen, gRPC-compatible APIs, streaming RPCs, ConnectError, interceptors, service handlers, transport configuration, or REST-to-RPC proxy patterns. Covers the architecture where Node frontend servers proxy REST+JSON from the UI into ConnectRPC calls to Go backend services.
---

# ConnectRPC

ConnectRPC is a slim RPC framework that speaks three protocols: **Connect** (default, HTTP/1.1 + HTTP/2, browser-compatible), **gRPC** (HTTP/2), and **gRPC-Web** (HTTP/1.1). A single Go server handles all three; clients pick their protocol via transport.

## Core API Quick Reference

### Go Server (`connectrpc.com/connect`)

| API | Purpose |
|-----|---------|
| `connect.NewHandler(svc, opts...)` | Register a service on an HTTP mux |
| `connect.NewClient[C](url, transport, opts...)` | Create a typed RPC client |
| `connect.NewError(code, err)` | Create an RPC error with a status code |
| `connect.NewErrorDetail(msg)` | Attach protobuf detail to an error |
| `connect.WithInterceptors(...)` | Apply interceptors to handler or client |
| `connect.WithProtoJSON()` | Use JSON encoding instead of binary proto |
| `connect.WithCompressMinBytes(n)` | Auto-compress responses above n bytes |
| `req.Msg` | Typed request message pointer |
| `req.Header()` | Incoming request headers (http.Header) |
| `connect.CallMeta(ctx)` | Access procedure + protocol on server |

### Node Client (`@connectrpc/connect-node`)

| API | Purpose |
|-----|---------|
| `createConnectTransport({ baseUrl })` | Connect protocol transport (default) |
| `createGrpcTransport({ baseUrl })` | gRPC protocol transport |
| `createClient(Service, transport)` | Typed client from generated schema |
| `client.method(req, options)` | Unary call (returns Promise<response>) |
| `client.serverStream(req, options)` | Server streaming (returns AsyncIterable) |
| `ConnectError` | Error class with `.code` and `.findDetails()` |
| `Code` | Enum of all 16 RPC error codes |

## Architecture

```
Browser / Mobile
      │  REST+JSON (HTTP)
      ▼
┌─────────────────────┐
│  Node Frontend      │  Express / Fastify / Next.js
│  (REST API layer)   │
└────────┬────────────┘
         │  ConnectRPC (Connect or gRPC protocol)
         ▼
┌─────────────────────┐
│  Go Backend         │  net/http + connect-go handlers
│  (RPC services)     │
└─────────────────────┘
```

The Node server receives REST+JSON from the UI, uses `@connectrpc/connect-node` to call Go services via ConnectRPC, and translates results back to REST responses.

## Protocol Support Matrix

| Protocol | HTTP version | Browser native | Streaming |
|----------|-------------|----------------|-----------|
| Connect  | HTTP/1.1 + HTTP/2 | Yes (unary) | Yes (HTTP/2) |
| gRPC     | HTTP/2 only | No | Yes |
| gRPC-Web | HTTP/1.1 | Yes (via proxy) | Server only |

## References

- [Architecture & Patterns](references/architecture.md) — REST-to-RPC proxy, protocol selection, project layout
- [Protobuf & Buf Codegen](references/protobuf-and-buf.md) — proto schema, buf.yaml, buf.gen.yaml, generated code
- [Go Server Setup](references/go-server-setup.md) — dependencies, main.go, mux, HTTP/2, codec options
- [Go Handlers & Routing](references/go-handlers-and-routing.md) — service impl, route paths, streaming handlers
- [Go Errors](references/go-errors.md) — 16 error codes, error details, context error mapping
- [Go Interceptors](references/go-interceptors.md) — auth, logging, middleware pattern
- [Go Headers & Trailers](references/go-headers-and-trailers.md) — request/response metadata, binary headers
- [Node Client Setup](references/node-client-setup.md) — transports, client instantiation, transport reuse
- [Node Client Usage](references/node-client-usage.md) — unary, streaming, headers, errors, timeouts, interceptors
