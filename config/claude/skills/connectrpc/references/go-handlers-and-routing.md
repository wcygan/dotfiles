# Go Handlers & Routing

## Implementing a Service Handler

The generated code defines an interface; implement it in a struct:

```go
package handler

import (
    "context"
    "fmt"

    "connectrpc.com/connect"
    apiv1 "github.com/myorg/myproject/gen/go/api/v1"
)

type UserServiceServer struct {
    db *sql.DB
}

// Unary handler: return (*connect.Response[Resp], error)
func (s *UserServiceServer) GetUser(
    ctx context.Context,
    req *connect.Request[apiv1.GetUserRequest],
) (*connect.Response[apiv1.GetUserResponse], error) {
    user, err := s.db.GetUser(ctx, req.Msg.Id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, connect.NewError(connect.CodeNotFound,
                fmt.Errorf("user %q not found", req.Msg.Id))
        }
        return nil, connect.NewError(connect.CodeInternal, err)
    }

    return connect.NewResponse(&apiv1.GetUserResponse{
        User: userToProto(user),
    }), nil
}
```

## Route Path Convention

ConnectRPC maps each RPC to a fixed HTTP path:

```
POST /{package}.{Service}/{Method}
```

Examples from `api.v1.UserService`:
- `POST /api.v1.UserService/GetUser`
- `POST /api.v1.UserService/ListUsers`
- `POST /api.v1.UserService/CreateUser`

The generated `NewUserServiceHandler` registers all these paths on a handler with the service's path prefix as its root. The returned `path` string is `/api.v1.UserService/`.

## Server Streaming Handler

```go
func (s *UserServiceServer) WatchUser(
    ctx context.Context,
    req *connect.Request[apiv1.WatchUserRequest],
    stream *connect.ServerStream[apiv1.UserEvent],
) error {
    // Subscribe to events
    events := s.eventBus.Subscribe(req.Msg.UserId)
    defer s.eventBus.Unsubscribe(events)

    for {
        select {
        case event := <-events:
            if err := stream.Send(&apiv1.UserEvent{
                Type: event.Type,
                User: userToProto(event.User),
            }); err != nil {
                return err  // client disconnected
            }
        case <-ctx.Done():
            return nil  // client canceled or timeout
        }
    }
}
```

## Client Streaming Handler

```go
func (s *UserServiceServer) BatchCreateUsers(
    ctx context.Context,
    stream *connect.ClientStream[apiv1.CreateUserRequest],
) (*connect.Response[apiv1.BatchCreateUsersResponse], error) {
    var created []string
    for stream.Receive() {
        req := stream.Msg()
        id, err := s.db.CreateUser(ctx, req.Name, req.Email)
        if err != nil {
            return nil, connect.NewError(connect.CodeInternal, err)
        }
        created = append(created, id)
    }
    if err := stream.Err(); err != nil {
        return nil, err
    }
    return connect.NewResponse(&apiv1.BatchCreateUsersResponse{
        CreatedIds: created,
    }), nil
}
```

## Bidi Streaming Handler

```go
func (s *UserServiceServer) Chat(
    ctx context.Context,
    stream *connect.BidiStream[apiv1.ChatRequest, apiv1.ChatResponse],
) error {
    for {
        req, err := stream.Receive()
        if err != nil {
            if errors.Is(err, io.EOF) {
                return nil
            }
            return err
        }
        resp := s.processMessage(req.Text)
        if err := stream.Send(&apiv1.ChatResponse{Text: resp}); err != nil {
            return err
        }
    }
}
```

## Using connect.NewResponse

Always wrap your response message:

```go
// Correct
return connect.NewResponse(&apiv1.GetUserResponse{User: user}), nil

// You can also set response headers via the returned response
resp := connect.NewResponse(&apiv1.GetUserResponse{User: user})
resp.Header().Set("X-Request-ID", requestID)
return resp, nil
```

## Reading Request Metadata

```go
func (s *UserServiceServer) GetUser(
    ctx context.Context,
    req *connect.Request[apiv1.GetUserRequest],
) (*connect.Response[apiv1.GetUserResponse], error) {
    // Request headers
    authToken := req.Header().Get("Authorization")
    requestID := req.Header().Get("X-Request-ID")

    // The request message
    userID := req.Msg.Id

    // Procedure info (method name, service, stream type)
    spec := req.Spec()
    _ = spec.Procedure  // "/api.v1.UserService/GetUser"
    _ = spec.IsClient   // false (we are the server)
    _ = spec.StreamType // connect.StreamTypeUnary
    _ = spec.Schema     // *descriptorpb.MethodDescriptorProto (if schema available)
    // ...
}
```

## Docs

- https://connectrpc.com/docs/go/implementing-services/ — Implementing service handlers in Go
- https://connectrpc.com/docs/go/streaming/ — Server, client, and bidi streaming in Go
- https://pkg.go.dev/connectrpc.com/connect — connectrpc.com/connect Go package reference
