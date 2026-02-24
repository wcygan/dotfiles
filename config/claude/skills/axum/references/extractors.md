---
title: Extractors
description: All axum extractors, FromRequest and FromRequestParts traits, ordering rules, optional extractors, custom extractors, and rejection handling
tags: [axum, extractor, FromRequest, FromRequestParts, Path, Query, Json, State, Form]
---

# Extractors

## Overview

Extractors are types implementing `FromRequest` or `FromRequestParts` that automatically parse incoming request data. They are the primary way to access request information in handlers.

## Built-in Extractors

### FromRequestParts (don't consume body, any position)

| Extractor | Purpose | Example |
|-----------|---------|---------|
| `Path<T>` | Deserialize URL path params | `Path(id): Path<u32>` |
| `Query<T>` | Deserialize query string | `Query(params): Query<Pagination>` |
| `State<T>` | Access shared app state | `State(db): State<Pool>` |
| `HeaderMap` | All request headers | `headers: HeaderMap` |
| `Method` | HTTP method | `method: Method` |
| `Uri` | Request URI | `uri: Uri` |
| `Version` | HTTP version | `version: Version` |
| `Extension<T>` | Request extensions | `Extension(val): Extension<MyType>` |
| `ConnectInfo<T>` | Client connection info | `ConnectInfo(addr): ConnectInfo<SocketAddr>` |
| `MatchedPath` | Matched route pattern | `path: MatchedPath` |
| `OriginalUri` | Original URI (before nesting) | `OriginalUri(uri): OriginalUri` |
| `Host` | Request host | `Host(host): Host` |
| `NestedPath` | Path prefix stripped by nesting | `NestedPath(prefix): NestedPath` |
| `RawQuery` | Unparsed query string | `RawQuery(q): RawQuery` |
| `RawPathParams` | Unparsed path params | `params: RawPathParams` |

### FromRequest (consume body, must be LAST)

| Extractor | Purpose | Example |
|-----------|---------|---------|
| `Json<T>` | Deserialize JSON body | `Json(data): Json<CreateUser>` |
| `Form<T>` | Deserialize form body | `Form(data): Form<Login>` |
| `String` | Body as UTF-8 string | `body: String` |
| `Bytes` | Raw body bytes | `body: Bytes` |
| `Request` | Full request access | `req: Request` |
| `Multipart` | Multipart form data | `multipart: Multipart` |
| `RawForm` | Unparsed form body | `RawForm(bytes): RawForm` |

## Ordering Rules

**Critical**: The request body is an async stream consumed once.

- `FromRequestParts` extractors: **any position**, multiple allowed
- `FromRequest` extractors: **must be last**, only ONE allowed

```rust
async fn handler(
    method: Method,                   // FromRequestParts — OK anywhere
    Path(id): Path<u32>,              // FromRequestParts — OK anywhere
    State(db): State<Pool>,           // FromRequestParts — OK anywhere
    Query(params): Query<Params>,     // FromRequestParts — OK anywhere
    Json(body): Json<CreateItem>,     // FromRequest — MUST be last
) -> impl IntoResponse { ... }
```

## Path Extractor Details

```rust
// Single param
async fn get_user(Path(id): Path<u32>) -> String { ... }

// Multiple params — tuple
async fn get_comment(Path((post_id, comment_id)): Path<(u32, u32)>) -> String { ... }

// Named params — struct (requires serde::Deserialize)
#[derive(Deserialize)]
struct Params { user_id: u32, post_id: u32 }
async fn handler(Path(p): Path<Params>) -> String { ... }
```

## Query Extractor Details

```rust
#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    per_page: Option<u32>,
}

// GET /items?page=2&per_page=10
async fn list(Query(pagination): Query<Pagination>) -> impl IntoResponse { ... }
```

## Json Extractor Details

```rust
#[derive(Deserialize)]
struct CreateUser {
    username: String,
    email: String,
}

async fn create_user(Json(payload): Json<CreateUser>) -> impl IntoResponse {
    // payload is deserialized CreateUser
}
```

Default body limit: **2MB**. Override with `DefaultBodyLimit`:

```rust
use axum::extract::DefaultBodyLimit;

let app = Router::new()
    .route("/upload", post(upload))
    .layer(DefaultBodyLimit::max(10 * 1024 * 1024)); // 10MB
```

## Optional Extractors

Wrap in `Option<T>` to make extraction optional:

```rust
async fn handler(
    user_agent: Option<TypedHeader<UserAgent>>,
) -> impl IntoResponse {
    match user_agent {
        Some(TypedHeader(ua)) => format!("Agent: {ua}"),
        None => "No user agent".to_string(),
    }
}
```

`Option<T>` returns `None` if the value isn't present. It still rejects if the value is present but invalid.

## Handling Rejections with Result

```rust
use axum::extract::rejection::JsonRejection;

async fn handler(
    payload: Result<Json<Value>, JsonRejection>,
) -> impl IntoResponse {
    match payload {
        Ok(Json(data)) => (StatusCode::OK, Json(data)).into_response(),
        Err(JsonRejection::MissingJsonContentType(_)) => {
            (StatusCode::BAD_REQUEST, "Missing Content-Type: application/json").into_response()
        }
        Err(err) => {
            (StatusCode::BAD_REQUEST, err.to_string()).into_response()
        }
    }
}
```

## Custom Extractors

### Implementing FromRequestParts (no body access)

```rust
use axum::extract::FromRequestParts;
use http::request::Parts;

struct AuthUser { id: u32, name: String }

impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, &'static str);

    async fn from_request_parts(
        parts: &mut Parts,
        _state: &S,
    ) -> Result<Self, Self::Rejection> {
        let auth_header = parts.headers
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .ok_or((StatusCode::UNAUTHORIZED, "Missing auth"))?;

        // Validate token, look up user...
        Ok(AuthUser { id: 1, name: "alice".into() })
    }
}

// Use like any other extractor
async fn handler(user: AuthUser) -> String {
    format!("Hello, {}", user.name)
}
```

### Implementing FromRequest (body access)

```rust
use axum::extract::FromRequest;

struct CsvBody(Vec<Vec<String>>);

impl<S> FromRequest<S> for CsvBody
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, String);

    async fn from_request(
        req: Request,
        state: &S,
    ) -> Result<Self, Self::Rejection> {
        let body = String::from_request(req, state)
            .await
            .map_err(|e| (StatusCode::BAD_REQUEST, e.to_string()))?;

        let rows: Vec<Vec<String>> = body.lines()
            .map(|line| line.split(',').map(String::from).collect())
            .collect();

        Ok(CsvBody(rows))
    }
}
```

### Using Other Extractors in Custom Implementations

```rust
use axum::RequestPartsExt;

impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = Response;

    async fn from_request_parts(
        parts: &mut Parts,
        _state: &S,
    ) -> Result<Self, Self::Rejection> {
        // Use another extractor inside your implementation
        let Extension(db) = parts
            .extract::<Extension<DatabasePool>>()
            .await
            .map_err(IntoResponse::into_response)?;

        // Look up user from DB...
        Ok(AuthUser { ... })
    }
}
```

## Debugging Extractors

Enable rejection tracing:

```bash
RUST_LOG=info,axum::rejection=trace cargo run
```

This logs detailed information about why extractors fail.
