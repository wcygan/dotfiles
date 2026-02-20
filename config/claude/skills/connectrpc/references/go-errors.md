# Go Errors

## Error Code Reference

| Code | connect constant | HTTP (Connect) | HTTP (gRPC) | When to use |
|------|-----------------|----------------|-------------|-------------|
| `canceled` | `connect.CodeCanceled` | 408 | 499 | Client canceled the request |
| `unknown` | `connect.CodeUnknown` | 500 | 2 | Unknown error (default) |
| `invalid_argument` | `connect.CodeInvalidArgument` | 400 | 3 | Bad input; don't retry |
| `deadline_exceeded` | `connect.CodeDeadlineExceeded` | 408 | 4 | Timeout |
| `not_found` | `connect.CodeNotFound` | 404 | 5 | Resource not found |
| `already_exists` | `connect.CodeAlreadyExists` | 409 | 6 | Resource already exists |
| `permission_denied` | `connect.CodePermissionDenied` | 403 | 7 | Authenticated but no access |
| `resource_exhausted` | `connect.CodeResourceExhausted` | 429 | 8 | Rate limited, quota exceeded |
| `failed_precondition` | `connect.CodeFailedPrecondition` | 412 | 9 | System state prevents operation |
| `aborted` | `connect.CodeAborted` | 409 | 10 | Concurrency conflict |
| `out_of_range` | `connect.CodeOutOfRange` | 400 | 11 | Invalid range (e.g., offset past end) |
| `unimplemented` | `connect.CodeUnimplemented` | 404 | 12 | Method not implemented |
| `internal` | `connect.CodeInternal` | 500 | 13 | Internal server error |
| `unavailable` | `connect.CodeUnavailable` | 503 | 14 | Service temporarily down; safe to retry |
| `data_loss` | `connect.CodeDataLoss` | 500 | 15 | Unrecoverable data corruption |
| `unauthenticated` | `connect.CodeUnauthenticated` | 401 | 16 | No valid credentials |

## Creating Errors

```go
// Simple error
return nil, connect.NewError(connect.CodeNotFound, fmt.Errorf("user %q not found", id))

// With formatted message
return nil, connect.NewError(connect.CodeInvalidArgument,
    fmt.Errorf("invalid email address: %q", email))

// Wrapping an existing error
if err := db.Query(ctx); err != nil {
    return nil, connect.NewError(connect.CodeInternal, fmt.Errorf("database error: %w", err))
}
```

## Error Details

Attach structured proto messages to errors for rich client-side handling:

```go
import (
    "connectrpc.com/connect"
    "google.golang.org/genproto/googleapis/rpc/errdetails"
)

func invalidFieldError(field, description string) error {
    connectErr := connect.NewError(connect.CodeInvalidArgument,
        fmt.Errorf("validation failed"))

    // Attach a BadRequest detail
    detail, err := connect.NewErrorDetail(&errdetails.BadRequest{
        FieldViolations: []*errdetails.BadRequest_FieldViolation{
            {Field: field, Description: description},
        },
    })
    if err == nil {
        connectErr.AddDetail(detail)
    }
    return connectErr
}
```

Common detail types from `google.golang.org/genproto/googleapis/rpc/errdetails`:
- `BadRequest` — field validation errors
- `QuotaFailure` — quota/rate limit details
- `RetryInfo` — when to retry
- `ResourceInfo` — which resource was not found
- `PreconditionFailure` — what precondition failed

## Extracting Error Details (Go client)

```go
resp, err := client.GetUser(ctx, connect.NewRequest(&apiv1.GetUserRequest{Id: id}))
if err != nil {
    var connectErr *connect.Error
    if errors.As(err, &connectErr) {
        for _, detail := range connectErr.Details() {
            msg, valueErr := detail.Value()
            if valueErr != nil {
                continue
            }
            switch v := msg.(type) {
            case *errdetails.BadRequest:
                for _, violation := range v.FieldViolations {
                    log.Printf("field %s: %s", violation.Field, violation.Description)
                }
            case *errdetails.RetryInfo:
                delay := v.RetryDelay.AsDuration()
                time.Sleep(delay)
            }
        }
    }
    return err
}
```

## Context Error Mapping

ConnectRPC automatically maps `context` errors to appropriate RPC codes:

```go
// context.DeadlineExceeded → connect.CodeDeadlineExceeded
// context.Canceled         → connect.CodeCanceled

func (s *Server) GetUser(ctx context.Context, req *connect.Request[...]) (..., error) {
    // If ctx is already canceled when handler runs:
    if err := ctx.Err(); err != nil {
        return nil, err  // ConnectRPC maps this for you
    }

    // Or let it bubble:
    result, err := s.db.Query(ctx, query)
    if err != nil {
        return nil, err  // context.DeadlineExceeded → CodeDeadlineExceeded
    }
}
```

## Checking Error Code (Go client)

```go
resp, err := client.GetUser(ctx, req)
if err != nil {
    if connect.CodeOf(err) == connect.CodeNotFound {
        // handle not found
    }
    // or
    var connectErr *connect.Error
    if errors.As(err, &connectErr) {
        switch connectErr.Code() {
        case connect.CodeUnauthenticated:
            return refreshTokenAndRetry(ctx)
        case connect.CodeUnavailable:
            return retryWithBackoff(ctx)
        default:
            return fmt.Errorf("rpc error: %w", err)
        }
    }
}
```

## Setting Headers on Error Responses

```go
connectErr := connect.NewError(connect.CodeUnauthenticated,
    fmt.Errorf("token expired"))

// Metadata on errors goes through err.Meta()
connectErr.Meta().Set("WWW-Authenticate", `Bearer realm="example"`)
return nil, connectErr
```

## Docs

- https://connectrpc.com/docs/go/errors/ — Go error handling reference
- https://connectrpc.com/docs/go/status-codes/ — Status codes and HTTP mapping
- https://pkg.go.dev/connectrpc.com/connect#Error — connect.Error Go type
- https://pkg.go.dev/connectrpc.com/connect#Code — connect.Code Go type
