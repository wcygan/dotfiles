# ConnectRPC Architecture

## The REST-to-RPC Proxy Pattern

Your standard architecture: a Node server sits between browser clients and Go backend services. The Node server translates REST+JSON from the UI into ConnectRPC calls to Go.

```
Browser
  │  GET /api/users/123       (REST)
  ▼
Node Frontend (Express/Fastify)
  │  GetUser({ id: "123" })   (ConnectRPC — Connect protocol)
  ▼
Go Backend (connect-go)
  │  returns User proto
  ▼
Node Frontend
  │  { id: "123", name: "..." }  (JSON response)
  ▼
Browser
```

### Node-side translation example

```typescript
// Express handler that proxies to Go
app.get('/api/users/:id', async (req, res) => {
  try {
    const response = await userClient.getUser({ id: req.params.id });
    res.json({ id: response.id, name: response.name });
  } catch (err) {
    if (err instanceof ConnectError) {
      const statusMap: Record<number, number> = {
        [Code.NotFound]: 404,
        [Code.Unauthenticated]: 401,
        [Code.PermissionDenied]: 403,
        [Code.InvalidArgument]: 400,
      };
      res.status(statusMap[err.code] ?? 500).json({ error: err.message });
    } else {
      res.status(500).json({ error: 'Internal error' });
    }
  }
});
```

## Protocol Selection

| Scenario | Protocol | Why |
|----------|----------|-----|
| Node → Go (server-to-server) | Connect or gRPC | Both work; Connect is simpler to configure |
| Browser → Go directly | Connect | Only browser-native option with streaming |
| Browser → Go via grpc-web proxy | gRPC-Web | If you already have a grpc-web proxy |
| Go → Go | gRPC | Standard in Go-native stacks |

For your architecture (Node → Go), use **Connect protocol** — it supports HTTP/1.1 and HTTP/2, has no streaming restrictions, and the Node client defaults to it.

## Project Structure Recommendation

```
myproject/
  proto/
    buf.yaml              # buf module config
    buf.gen.yaml          # code generation config
    api/v1/
      user.proto          # service definitions
      order.proto
  backend/                # Go service
    cmd/server/main.go
    internal/handler/
      user.go             # UserServiceHandler
      order.go
    go.mod
  frontend/               # Node server
    src/
      clients/
        user.ts           # transport + client setup
        order.ts
      routes/
        users.ts          # REST handlers
    package.json
  gen/
    go/api/v1/            # generated Go code
    ts/api/v1/            # generated TypeScript code
```

## When to Use Each Connect Protocol Feature

- **Unary RPC**: request/response, like REST — use for most operations
- **Server streaming**: server sends multiple messages (e.g., progress updates, feeds)
- **Client streaming**: client sends multiple messages — rare; Go handler reads a stream
- **Bidirectional streaming**: full duplex — requires HTTP/2 on both sides

## Go + Node Version Compatibility

| connect-go | @connectrpc/connect | Notes |
|------------|---------------------|-------|
| v1.x | v1.x | Current stable; use these |
| v0.x | v0.x | Deprecated |

Always use matching major versions for protocol compatibility.

## Docs

- https://connectrpc.com/docs/introduction/ — ConnectRPC overview and protocol comparison
- https://connectrpc.com/docs/protocol/ — Connect protocol wire format specification
