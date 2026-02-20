# Go Interceptors

## Interceptor Function Pattern

```go
import "connectrpc.com/connect"

// UnaryInterceptorFunc: func(ctx, req, next) (resp, error)
// It implements connect.Interceptor; streaming RPCs pass through unaffected.
func loggingInterceptor() connect.Interceptor {
    return connect.UnaryInterceptorFunc(
        func(ctx context.Context, req connect.AnyRequest, next connect.UnaryFunc) (connect.AnyResponse, error) {
            start := time.Now()
            resp, err := next(ctx, req)
            duration := time.Since(start)
            if err != nil {
                log.Printf("RPC %s failed in %v: %v", req.Spec().Procedure, duration, err)
            } else {
                log.Printf("RPC %s succeeded in %v", req.Spec().Procedure, duration)
            }
            return resp, err
        },
    )
}
```

## Auth Interceptor (Server-Side)

```go
func authInterceptor(secret string) connect.Interceptor {
    return connect.UnaryInterceptorFunc(
        func(ctx context.Context, req connect.AnyRequest, next connect.UnaryFunc) (connect.AnyResponse, error) {
            // Skip auth check for public methods
            if req.Spec().Procedure == "/api.v1.AuthService/Login" {
                return next(ctx, req)
            }

            token := req.Header().Get("Authorization")
            if token == "" {
                return nil, connect.NewError(connect.CodeUnauthenticated,
                    fmt.Errorf("missing authorization header"))
            }

            userID, err := validateToken(token, secret)
            if err != nil {
                return nil, connect.NewError(connect.CodeUnauthenticated,
                    fmt.Errorf("invalid token"))
            }

            // Attach user ID to context for handlers
            ctx = context.WithValue(ctx, userIDKey{}, userID)
            return next(ctx, req)
        },
    )
}

type userIDKey struct{}

func UserIDFromContext(ctx context.Context) (string, bool) {
    id, ok := ctx.Value(userIDKey{}).(string)
    return id, ok
}
```

## Auth Interceptor (Client-Side)

```go
func clientAuthInterceptor(tokenFn func() string) connect.Interceptor {
    return connect.UnaryInterceptorFunc(
        func(ctx context.Context, req connect.AnyRequest, next connect.UnaryFunc) (connect.AnyResponse, error) {
            // req.Spec().IsClient is true on client side
            if req.Spec().IsClient {
                req.Header().Set("Authorization", "Bearer "+tokenFn())
            }
            return next(ctx, req)
        },
    )
}
```

## Applying Interceptors

```go
// To a handler (server-side)
path, handler := apiv1connect.NewUserServiceHandler(
    &handler.UserServer{},
    connect.WithInterceptors(
        authInterceptor(secret),   // runs first
        loggingInterceptor(),      // runs second
    ),
)

// To a client (client-side)
client := apiv1connect.NewUserServiceClient(
    http.DefaultClient,
    baseURL,
    connect.WithInterceptors(
        clientAuthInterceptor(getToken),
        loggingInterceptor(),
    ),
)
```

## Interceptor Chaining Order

Interceptors wrap the handler like onion layers. With `WithInterceptors(A, B, C)`:

```
Request:  A.before → B.before → C.before → handler
Response: C.after  → B.after  → A.after  → caller
```

First interceptor in the list is outermost (first to run on request, last on response).

## Streaming Interceptors

For streaming RPCs, implement the full `Interceptor` interface:

```go
type myInterceptor struct{}

func (m *myInterceptor) WrapUnary(next connect.UnaryFunc) connect.UnaryFunc {
    return func(ctx context.Context, req connect.AnyRequest) (connect.AnyResponse, error) {
        log.Printf("unary: %s", req.Spec().Procedure)
        return next(ctx, req)
    }
}

func (m *myInterceptor) WrapStreamingClient(next connect.StreamingClientFunc) connect.StreamingClientFunc {
    return func(ctx context.Context, spec connect.Spec) connect.StreamingClientConn {
        log.Printf("stream client: %s", spec.Procedure)
        return next(ctx, spec)
    }
}

func (m *myInterceptor) WrapStreamingHandler(next connect.StreamingHandlerFunc) connect.StreamingHandlerFunc {
    return func(ctx context.Context, conn connect.StreamingHandlerConn) error {
        log.Printf("stream server: %s", conn.Spec().Procedure)
        return next(ctx, conn)
    }
}
```

## Recovery Interceptor (Panic Handler)

```go
func recoveryInterceptor() connect.Interceptor {
    return connect.UnaryInterceptorFunc(
        func(ctx context.Context, req connect.AnyRequest, next connect.UnaryFunc) (resp connect.AnyResponse, err error) {
            defer func() {
                if r := recover(); r != nil {
                    log.Printf("panic in %s: %v\n%s", req.Spec().Procedure, r, debug.Stack())
                    err = connect.NewError(connect.CodeInternal, fmt.Errorf("internal error"))
                }
            }()
            return next(ctx, req)
        },
    )
}
```

## Docs

- https://connectrpc.com/docs/go/interceptors/ — Go interceptors reference
- https://pkg.go.dev/connectrpc.com/connect#Interceptor — connect.Interceptor interface
- https://pkg.go.dev/connectrpc.com/connect#UnaryInterceptorFunc — UnaryInterceptorFunc type
