# Errors: ConnectError, ErrorCode, ErrorDetail

Connect's 16-code error model maps cleanly onto both gRPC status codes and
HTTP status codes. The dispatcher does the mapping — return a `ConnectError`
and trust it.

## Table of contents

- [Returning errors from handlers](#returning-errors-from-handlers)
- [Canonical error codes](#canonical-error-codes)
- [HTTP status mapping](#http-status-mapping)
- [Structured details](#structured-details)
- [Wrapping foreign errors](#wrapping-foreign-errors)

## Returning errors from handlers

```rust
use connectrpc::{ConnectError, ErrorCode, ServiceResult};

if !is_authorized(&user) {
    return Err(ConnectError::new(
        ErrorCode::PermissionDenied,
        "user lacks role admin",
    ));
}
```

`ServiceResult<T>` is `Result<Response<T>, ConnectError>`. Always use
`ConnectError::new(code, message)` rather than panicking — the dispatcher
turns a panic into `Internal` but loses the message.

## Canonical error codes

The 16 codes are inherited from gRPC and carry the same semantics:

| Code | Use for |
|------|---------|
| `Canceled` | Caller canceled (rarely returned by server) |
| `Unknown` | Default for foreign errors with no obvious mapping |
| `InvalidArgument` | Caller-supplied request is malformed regardless of system state |
| `DeadlineExceeded` | Computed deadline passed before the response was ready |
| `NotFound` | Requested entity does not exist |
| `AlreadyExists` | Entity creation conflicted with an existing one |
| `PermissionDenied` | Auth succeeded but caller lacks privilege |
| `ResourceExhausted` | Quota / rate limit / memory exhausted |
| `FailedPrecondition` | System state would have to change for the request to succeed |
| `Aborted` | Concurrency conflict; caller may retry transactionally |
| `OutOfRange` | Argument is outside the valid domain (use over `InvalidArgument` when state-dependent) |
| `Unimplemented` | RPC method not implemented or version mismatch |
| `Internal` | Server invariant violated; should be alerted on |
| `Unavailable` | Transient — retryable with backoff |
| `DataLoss` | Unrecoverable data corruption |
| `Unauthenticated` | Auth missing / invalid (distinct from `PermissionDenied`) |

Picking the right code is the highest-leverage error decision — clients build
retry policies and alerting off these values.

## HTTP status mapping

The dispatcher applies the standard Connect mapping when speaking the Connect
or gRPC-Web protocols. You should not set HTTP status manually.

| Connect code | HTTP |
|--------------|------|
| `InvalidArgument`, `OutOfRange` | 400 |
| `Unauthenticated` | 401 |
| `PermissionDenied` | 403 |
| `NotFound` | 404 |
| `AlreadyExists`, `Aborted` | 409 |
| `ResourceExhausted` | 429 |
| `Canceled` | 499 |
| `DataLoss`, `Unknown`, `Internal` | 500 |
| `Unimplemented` | 501 |
| `Unavailable` | 503 |
| `DeadlineExceeded` | 504 |
| `FailedPrecondition` | 412 |

For gRPC over HTTP/2, status is always 200 with the code carried in the
`grpc-status` trailer — also handled automatically.

## Structured details

Attach typed proto messages to an error for machine-readable handling:

```rust
use connectrpc::{ConnectError, ErrorCode, ErrorDetail};

let detail = ErrorDetail::from_message(&RetryInfo { retry_after_seconds: 30 })?;
return Err(
    ConnectError::new(ErrorCode::ResourceExhausted, "rate limited")
        .with_detail(detail),
);
```

On the client side:

```rust
match client.greet(req).await {
    Err(e) if e.code() == ErrorCode::ResourceExhausted => {
        for d in e.details() {
            if let Some(info) = d.try_decode::<RetryInfo>().ok() {
                tokio::time::sleep(Duration::from_secs(info.retry_after_seconds.into())).await;
            }
        }
    }
    /* … */
}
```

Don't put PII or large blobs in details — they go on the wire and into logs.

## Wrapping foreign errors

Use `From` impls or explicit conversion to avoid sprawling `match` arms:

```rust
impl From<sqlx::Error> for ConnectError {
    fn from(e: sqlx::Error) -> Self {
        let code = match &e {
            sqlx::Error::RowNotFound => ErrorCode::NotFound,
            sqlx::Error::PoolTimedOut => ErrorCode::Unavailable,
            _ => ErrorCode::Internal,
        };
        ConnectError::new(code, e.to_string())
    }
}
```

Then `let row = sqlx::query!(…).fetch_one(pool).await?;` lifts the DB error
into the right Connect code with no boilerplate at the call site.
