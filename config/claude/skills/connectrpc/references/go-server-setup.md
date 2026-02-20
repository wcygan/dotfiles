# Go Server Setup

## Dependencies

```bash
go get connectrpc.com/connect@latest
go get google.golang.org/protobuf@latest
go get golang.org/x/net/http2
go get golang.org/x/net/http2/h2c
```

Optionally for compression:
```bash
go get connectrpc.com/connect/compress  # not needed; built-in gzip available
```

## Minimal Server (main.go)

```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"

    "connectrpc.com/connect"
    "golang.org/x/net/http2"
    "golang.org/x/net/http2/h2c"

    apiv1 "github.com/myorg/myproject/gen/go/api/v1"
    "github.com/myorg/myproject/gen/go/api/v1/apiv1connect"
    "github.com/myorg/myproject/internal/handler"
)

func main() {
    mux := http.NewServeMux()

    // Register services
    path, userHandler := apiv1connect.NewUserServiceHandler(
        &handler.UserServiceServer{},
        connect.WithInterceptors(
            authInterceptor(),
            loggingInterceptor(),
        ),
    )
    mux.Handle(path, userHandler)

    // h2c wraps the mux to support HTTP/2 without TLS (for internal services)
    server := &http.Server{
        Addr:    ":8080",
        Handler: h2c.NewHandler(mux, &http2.Server{}),
    }

    fmt.Println("Starting server on :8080")
    log.Fatal(server.ListenAndServe())
}
```

## HTTP/2 Configuration

**h2c** (HTTP/2 Cleartext) — for internal services without TLS:
```go
h2c.NewHandler(mux, &http2.Server{})
```

**TLS** — for external or production services:
```go
server := &http.Server{
    Addr:    ":443",
    Handler: mux,  // standard mux, no h2c wrapper
    TLSConfig: &tls.Config{
        MinVersion: tls.VersionTLS12,
    },
}
log.Fatal(server.ListenAndServeTLS("cert.pem", "key.pem"))
```

Node clients connecting to h2c need the gRPC transport or Connect transport with HTTP/2 forced:
```typescript
createGrpcTransport({ baseUrl: 'http://localhost:8080' })
// or
createConnectTransport({ baseUrl: 'http://localhost:8080', httpVersion: '2' })
```

## Handler Options (connect.HandlerOption)

```go
// Use JSON encoding instead of binary protobuf
connect.WithProtoJSON()

// Compress responses larger than 1KB
connect.WithCompressMinBytes(1024)

// Custom codec (e.g., for msgpack)
connect.WithCodec(myCodec)

// Apply interceptors
connect.WithInterceptors(interceptor1, interceptor2)

// Recovery from panics
connect.WithRecover(func(ctx context.Context, spec connect.Spec, h http.Header, r any) error {
    log.Printf("panic: %v", r)
    return connect.NewError(connect.CodeInternal, fmt.Errorf("internal error"))
})
```

## Registering Multiple Services

```go
mux := http.NewServeMux()

// Each service gets its own path prefix: /api.v1.UserService/
userPath, userHandler := apiv1connect.NewUserServiceHandler(&handler.UserServer{})
orderPath, orderHandler := apiv1connect.NewOrderServiceHandler(&handler.OrderServer{})

mux.Handle(userPath, userHandler)
mux.Handle(orderPath, orderHandler)
```

## Path Prefixing

If your services live under a sub-path (e.g., behind a proxy at `/rpc/`):

```go
// Option 1: StripPrefix in mux
mux.Handle("/rpc/"+userPath, http.StripPrefix("/rpc", userHandler))

// Option 2: Use a subrouter with net/http
rpcMux := http.NewServeMux()
rpcMux.Handle(userPath, userHandler)
mux.Handle("/rpc/", http.StripPrefix("/rpc", rpcMux))
```

## Serialization Options

| Option | Wire format | Use when |
|--------|-------------|----------|
| Default (none) | Binary protobuf | Production, maximum efficiency |
| `WithProtoJSON()` | JSON | Debugging, human-readable logs |
| Custom codec | Any | Special encoding requirements |

## CORS (for browser clients)

```go
import "github.com/rs/cors"

corsHandler := cors.New(cors.Options{
    AllowedOrigins: []string{"https://myapp.com"},
    AllowedMethods: []string{"POST"},  // Connect uses POST
    AllowedHeaders: []string{
        "Content-Type",
        "Connect-Protocol-Version",
        "Connect-Timeout-Ms",
        "Grpc-Timeout",
        "X-Grpc-Web",
    },
    ExposedHeaders: []string{
        "Grpc-Status",
        "Grpc-Message",
        "Connect-Status",
    },
})

handler := corsHandler.Handler(h2c.NewHandler(mux, &http2.Server{}))
```

## Graceful Shutdown

```go
srv := &http.Server{Addr: ":8080", Handler: h2c.NewHandler(mux, &http2.Server{})}

go func() {
    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
    <-sig

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    srv.Shutdown(ctx)
}()

log.Fatal(srv.ListenAndServe())
```

## Docs

- https://connectrpc.com/docs/go/getting-started/ — Go getting started guide
- https://pkg.go.dev/connectrpc.com/connect — connectrpc.com/connect Go package reference
- https://pkg.go.dev/golang.org/x/net/http2/h2c — h2c package for HTTP/2 cleartext
