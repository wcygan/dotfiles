---
title: Error Handling
description: Axum error handling model, Result pattern, custom error types, rejections, HandleError, and best practices
tags: [axum, error, IntoResponse, Result, rejection, HandleError, anyhow]
---

# Error Handling

## Core Philosophy

Axum ensures all handlers always produce a response. The type system enforces this — handler error types must implement `IntoResponse`, converting errors into HTTP responses rather than propagating them.

```rust
// This handler ALWAYS returns a response
// Even Err(StatusCode) becomes a valid HTTP response
async fn handler() -> Result<Json<Data>, StatusCode> {
    let data = fetch().map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    Ok(Json(data))
}
```

## The Result Pattern

### Simple: StatusCode errors

```rust
async fn get_user(Path(id): Path<u32>) -> Result<Json<User>, StatusCode> {
    let user = db.find(id).ok_or(StatusCode::NOT_FOUND)?;
    Ok(Json(user))
}
```

### Better: Tuple errors with messages

```rust
async fn get_user(Path(id): Path<u32>) -> Result<Json<User>, (StatusCode, String)> {
    let user = db.find(id)
        .ok_or((StatusCode::NOT_FOUND, format!("User {id} not found")))?;
    Ok(Json(user))
}
```

### Best: Custom error type

```rust
use axum::response::{IntoResponse, Response};

enum AppError {
    NotFound(String),
    BadRequest(String),
    Internal(anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Internal(err) => {
                // Log the actual error
                tracing::error!("Internal error: {err:?}");
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".to_string())
            }
        };

        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}

// Enable ? with anyhow errors
impl From<anyhow::Error> for AppError {
    fn from(err: anyhow::Error) -> Self {
        AppError::Internal(err)
    }
}

// Now handlers are clean
async fn handler() -> Result<Json<Data>, AppError> {
    let data = fetch().await?;  // anyhow::Error -> AppError::Internal
    Ok(Json(data))
}
```

## Structured Error Responses

For API servers, return consistent JSON errors:

```rust
#[derive(Serialize)]
struct ErrorResponse {
    error: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    details: Option<Value>,
}

impl AppError {
    fn json_response(status: StatusCode, error: impl Into<String>) -> Response {
        (status, Json(ErrorResponse {
            error: error.into(),
            details: None,
        })).into_response()
    }
}
```

## Extractor Rejections

When an extractor fails (e.g., invalid JSON, missing path param), axum returns a rejection response without calling your handler.

### Default rejection behavior

Each extractor has specific rejection types:
- `JsonRejection` — invalid JSON, wrong content type, body too large
- `PathRejection` — missing or invalid path parameters
- `QueryRejection` — invalid query string

### Customizing rejection responses

```rust
use axum::extract::rejection::JsonRejection;

async fn create_user(
    payload: Result<Json<CreateUser>, JsonRejection>,
) -> Result<Json<User>, AppError> {
    let Json(data) = payload.map_err(|rejection| {
        AppError::BadRequest(rejection.body_text())
    })?;
    // ...
}
```

### Global rejection handling with a custom extractor

```rust
struct AppJson<T>(pub T);

impl<S, T> FromRequest<S> for AppJson<T>
where
    T: DeserializeOwned,
    S: Send + Sync,
{
    type Rejection = AppError;

    async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        match Json::<T>::from_request(req, state).await {
            Ok(Json(value)) => Ok(AppJson(value)),
            Err(rejection) => Err(AppError::BadRequest(rejection.body_text())),
        }
    }
}

// Use AppJson instead of Json for consistent error formatting
async fn handler(AppJson(data): AppJson<CreateUser>) -> Result<Json<User>, AppError> {
    // ...
}
```

## HandleError — For Fallible Middleware

Tower middleware can produce errors (e.g., timeouts). Use `HandleErrorLayer` to convert them to responses:

```rust
use axum::error_handling::HandleErrorLayer;
use tower::timeout::TimeoutLayer;
use std::time::Duration;

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(HandleErrorLayer::new(|err: BoxError| async move {
                if err.is::<tower::timeout::error::Elapsed>() {
                    (StatusCode::REQUEST_TIMEOUT, "Request timed out")
                } else {
                    (StatusCode::INTERNAL_SERVER_ERROR, "Internal error")
                }
            }))
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
    );
```

### HandleError with Extractors

Access request data when handling errors:

```rust
.layer(HandleErrorLayer::new(|method: Method, uri: Uri, err: BoxError| async move {
    tracing::error!("{method} {uri} failed: {err}");
    (StatusCode::INTERNAL_SERVER_ERROR, "Something went wrong")
}))
```

## Anyhow Integration Pattern

```rust
// In your error module
struct AppError(anyhow::Error);

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        tracing::error!("Application error: {:#}", self.0);
        (StatusCode::INTERNAL_SERVER_ERROR, "Something went wrong").into_response()
    }
}

impl<E> From<E> for AppError
where
    E: Into<anyhow::Error>,
{
    fn from(err: E) -> Self {
        Self(err.into())
    }
}

// Handlers can use ? freely
async fn handler() -> Result<Json<Data>, AppError> {
    let data = sqlx::query_as("SELECT ...").fetch_one(&pool).await?;
    let processed = process(data)?;
    Ok(Json(processed))
}
```

## Best Practices

1. **Define one `AppError` type** per application with `IntoResponse`
2. **Implement `From<T>` for common error types** to enable `?` operator
3. **Log internal errors** in `IntoResponse`, return sanitized messages to clients
4. **Use `#[debug_handler]`** to catch error type mismatches early
5. **Return structured JSON errors** for API services
6. **Use `Result<T, E>` everywhere** — not `unwrap()` or `expect()` in handlers
