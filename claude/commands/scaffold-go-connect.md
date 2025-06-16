# /scaffold-go-connect

Creates a new Go RPC server project for $ARGUMENT using ConnectRPC with Protocol Buffers, Buf schema management, and type-safe service definitions.

## What it does

1. Creates a new directory with the specified project name
2. Sets up Protocol Buffer schema with buf.yaml configuration
3. Creates a simple Greet service with request/response messages
4. Generates Go code using buf generate
5. Implements a ConnectRPC server with proper handlers
6. Runs `go mod tidy` to ensure dependencies are resolved

## Example

```
/scaffold-go-connect greet-api
```

This creates a production-ready ConnectRPC server with:

- Protocol Buffer schema in `proto/greet/v1/greet.proto`
- Buf configuration for schema management and code generation
- Go server implementation with ConnectRPC handlers
- HTTP/2 support with h2c for development
- Type-safe client/server communication
- Server listening on localhost:8080

## ConnectRPC Features (TLDR)

### Core Benefits

- **Simple HTTP**: Works with any HTTP client, curl, browsers
- **Three protocols**: gRPC, gRPC-Web, and Connect's own protocol
- **Streaming**: Bidirectional, client, and server streaming support
- **Interceptors**: Middleware for auth, logging, metrics, retries
- **Error handling**: Rich error details with connect.Error type
- **Production ready**: Load balancers, proxies, CDNs work out of the box

### Key Capabilities

- **Routing**: Standard HTTP mux compatibility, custom routing
- **Streaming**: `stream` keyword in proto for real-time communication
- **Interceptors**: Chain-able middleware with `connect.UnaryInterceptorFunc`
- **Errors**: Structured errors with codes, messages, and details
- **Deployment**: Works behind any HTTP proxy, no gRPC infrastructure needed

### Development Workflow

1. Define services in `.proto` files
2. Generate code with `buf generate`
3. Implement service handlers
4. Add interceptors for cross-cutting concerns
5. Deploy as standard HTTP service
