# Go Headers & Trailers

## Reading Request Headers (Server)

```go
func (s *Server) GetUser(
    ctx context.Context,
    req *connect.Request[apiv1.GetUserRequest],
) (*connect.Response[apiv1.GetUserResponse], error) {
    // Standard HTTP headers
    authHeader := req.Header().Get("Authorization")
    contentType := req.Header().Get("Content-Type")

    // Custom headers
    requestID := req.Header().Get("X-Request-ID")
    traceID := req.Header().Get("X-Trace-ID")

    // Binary headers (base64-encoded, suffix must be -Bin)
    encodedData := req.Header().Get("X-Custom-Data-Bin")  // automatically decoded
    _ = encodedData  // already decoded bytes
}
```

## Writing Response Headers (Server)

```go
func (s *Server) GetUser(
    ctx context.Context,
    req *connect.Request[apiv1.GetUserRequest],
) (*connect.Response[apiv1.GetUserResponse], error) {
    user, _ := s.db.GetUser(ctx, req.Msg.Id)

    resp := connect.NewResponse(&apiv1.GetUserResponse{User: userToProto(user)})

    // Set response headers before returning
    resp.Header().Set("X-Request-ID", generateRequestID())
    resp.Header().Set("X-Version", "v1.2.3")

    return resp, nil
}
```

## Headers on Error Responses

```go
connectErr := connect.NewError(connect.CodeUnauthenticated, fmt.Errorf("expired token"))

// Headers travel on the error, not a response object
connectErr.Meta().Set("WWW-Authenticate", `Bearer realm="api", error="token_expired"`)
return nil, connectErr
```

## Binary Headers

Headers with names ending in `-Bin` are automatically base64-encoded/decoded:

```go
// Server: reading binary header
rawBytes := req.Header().Get("X-Session-Token-Bin")
// rawBytes contains decoded binary data

// Server: writing binary header
resp.Header().Set("X-Signature-Bin", string(signatureBytes))

// Node client: sending binary header
headers: { 'X-Session-Token-Bin': Buffer.from(tokenBytes).toString('base64') }
```

## Reserved Header Prefixes

Do not use these prefixes in custom headers:
- `Connect-` — reserved for Connect protocol
- `Grpc-` — reserved for gRPC protocol
- `Trailer-` — HTTP/1.1 trailer mechanism

## Trailers (Streaming)

Trailers are metadata sent after the response body — mainly useful for streaming:

```go
// Server streaming: set trailers on the stream
func (s *Server) ListUsers(
    ctx context.Context,
    req *connect.Request[apiv1.ListUsersRequest],
    stream *connect.ServerStream[apiv1.User],
) error {
    count := 0
    for _, user := range s.db.AllUsers(ctx) {
        if err := stream.Send(userToProto(user)); err != nil {
            return err
        }
        count++
    }
    // Trailers sent after all messages
    stream.ResponseTrailer().Set("X-Total-Count", strconv.Itoa(count))
    return nil
}
```

## Accessing Headers in Interceptors

```go
connect.UnaryInterceptorFunc(
    func(next connect.UnaryFunc) connect.UnaryFunc {
        return func(ctx context.Context, req connect.AnyRequest) (connect.AnyResponse, error) {
            // Read any header on the request
            traceID := req.Header().Get("X-Trace-ID")
            if traceID == "" {
                traceID = uuid.New().String()
                req.Header().Set("X-Trace-ID", traceID)
            }
            ctx = withTraceID(ctx, traceID)

            resp, err := next(ctx, req)

            // Set response header (resp is nil on error)
            if resp != nil {
                resp.Header().Set("X-Trace-ID", traceID)
            }
            return resp, err
        }
    },
)
```

## Setting Headers on the Go Client (outgoing requests)

```go
// Per-request headers
req := connect.NewRequest(&apiv1.GetUserRequest{Id: "123"})
req.Header().Set("Authorization", "Bearer "+token)
req.Header().Set("X-Request-ID", uuid.New().String())

resp, err := client.GetUser(ctx, req)
```

## Reading Response Headers from Go Client

```go
resp, err := client.GetUser(ctx, connect.NewRequest(&apiv1.GetUserRequest{Id: "123"}))
if err != nil {
    return err
}
// Response headers
serverVersion := resp.Header().Get("X-Version")
requestID := resp.Header().Get("X-Request-ID")
```

## Per-Call Metadata Pattern

Use context to pass metadata through a call stack without threading headers manually:

```go
// Store in context (set in middleware/interceptor)
type mdKey struct{}
ctx = context.WithValue(ctx, mdKey{}, map[string]string{
    "user_id": "u123",
    "org_id":  "org456",
})

// Retrieve in handler
md, _ := ctx.Value(mdKey{}).(map[string]string)
userID := md["user_id"]
```

## Docs

- https://connectrpc.com/docs/go/headers/ — Go request/response headers reference
- https://connectrpc.com/docs/go/trailers/ — Go trailers reference
- https://pkg.go.dev/connectrpc.com/connect#CallInfoForHandlerContext — CallInfoForHandlerContext
- https://pkg.go.dev/connectrpc.com/connect#EncodeBinaryHeader — Binary header utilities
