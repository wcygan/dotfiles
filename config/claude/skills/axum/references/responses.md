---
title: Responses
description: Axum IntoResponse trait, built-in response types, tuple responses, IntoResponseParts, custom response types
tags: [axum, response, IntoResponse, Json, Html, Redirect, StatusCode]
---

# Responses

## IntoResponse Trait

Any type implementing `IntoResponse` can be returned from a handler. Axum provides implementations for many common types.

## Built-in IntoResponse Implementations

| Type | Status | Content-Type | Body |
|------|--------|-------------|------|
| `()` | 200 | none | empty |
| `&'static str` | 200 | `text/plain` | the string |
| `String` | 200 | `text/plain` | the string |
| `Vec<u8>` / `Bytes` | 200 | `application/octet-stream` | raw bytes |
| `Json<T>` | 200 | `application/json` | serialized JSON |
| `Html<T>` | 200 | `text/html` | HTML content |
| `StatusCode` | code | none | empty |
| `Redirect` | 3xx | `Location` header | empty |
| `Response` | as built | as built | as built |

## Tuple Responses

Combine status codes, headers, and bodies with tuples:

```rust
use axum::http::{StatusCode, HeaderMap, header};

// (StatusCode, body)
async fn not_found() -> (StatusCode, &'static str) {
    (StatusCode::NOT_FOUND, "Not found")
}

// (StatusCode, headers, body)
async fn with_headers() -> (StatusCode, [(header::HeaderName, &'static str); 1], String) {
    (
        StatusCode::OK,
        [(header::CONTENT_TYPE, "text/plain")],
        "Hello".to_string(),
    )
}

// (HeaderMap, body)
async fn custom_headers() -> (HeaderMap, Json<Data>) {
    let mut headers = HeaderMap::new();
    headers.insert("X-Custom", "value".parse().unwrap());
    (headers, Json(data))
}
```

Tuple element ordering:
1. `StatusCode` (optional, overrides default)
2. Headers — `HeaderMap`, `[(HeaderName, &str); N]`, or `IntoResponseParts` types
3. Body — the `IntoResponse` type (last position)

## Json Response

```rust
use axum::Json;
use serde::Serialize;

#[derive(Serialize)]
struct User { id: u32, name: String }

async fn get_user() -> Json<User> {
    Json(User { id: 1, name: "Alice".into() })
}

// With status code
async fn created() -> (StatusCode, Json<User>) {
    (StatusCode::CREATED, Json(User { id: 1, name: "Alice".into() }))
}
```

## Html Response

```rust
use axum::response::Html;

async fn index() -> Html<&'static str> {
    Html("<h1>Hello, World!</h1>")
}

async fn dynamic_html() -> Html<String> {
    Html(format!("<h1>Count: {}</h1>", 42))
}
```

## Redirect

```rust
use axum::response::Redirect;

async fn redirect() -> Redirect {
    Redirect::to("/new-location")
}

async fn permanent_redirect() -> Redirect {
    Redirect::permanent("/new-location")
}

// Redirect::to        — 303 See Other
// Redirect::temporary — 307 Temporary Redirect
// Redirect::permanent — 308 Permanent Redirect
```

## NoContent

```rust
use axum::response::NoContent;

async fn delete_item() -> NoContent {
    // ... delete logic
    NoContent
}
// Returns 204 No Content with empty body
```

## AppendHeaders

Add headers without overriding existing ones:

```rust
use axum::response::AppendHeaders;

async fn handler() -> (AppendHeaders<[(header::HeaderName, &'static str); 2]>, &'static str) {
    (
        AppendHeaders([
            (header::SET_COOKIE, "a=1"),
            (header::SET_COOKIE, "b=2"),
        ]),
        "body",
    )
}
```

## Custom Response Types

Implement `IntoResponse` for your own types:

```rust
use axum::response::{IntoResponse, Response};

struct ApiResponse<T: Serialize> {
    status: StatusCode,
    data: T,
}

impl<T: Serialize> IntoResponse for ApiResponse<T> {
    fn into_response(self) -> Response {
        (self.status, Json(self.data)).into_response()
    }
}

async fn handler() -> ApiResponse<User> {
    ApiResponse {
        status: StatusCode::OK,
        data: User { id: 1, name: "Alice".into() },
    }
}
```

## IntoResponseParts

For types that add headers/extensions without providing a body:

```rust
use axum::response::IntoResponseParts;

struct RequestId(String);

impl IntoResponseParts for RequestId {
    type Error = Infallible;

    fn into_response_parts(
        self,
        mut res: ResponseParts,
    ) -> Result<ResponseParts, Self::Error> {
        res.headers_mut().insert(
            "x-request-id",
            self.0.parse().unwrap(),
        );
        Ok(res)
    }
}

// Use in tuples alongside a body
async fn handler() -> (RequestId, Json<Data>) {
    (RequestId("abc-123".into()), Json(data))
}
```

## Result as Response

`Result<T, E>` implements `IntoResponse` when both `T` and `E` implement `IntoResponse`:

```rust
async fn handler() -> Result<Json<Data>, StatusCode> {
    let data = fetch().map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    Ok(Json(data))
}

// More expressive errors
async fn handler() -> Result<Json<Data>, (StatusCode, String)> {
    let data = fetch().map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;
    Ok(Json(data))
}
```

## Response Builder (low-level)

```rust
use axum::response::Response;
use axum::body::Body;

async fn handler() -> Response {
    Response::builder()
        .status(StatusCode::OK)
        .header("X-Custom", "value")
        .body(Body::from("Hello"))
        .unwrap()
}
```

## Server-Sent Events (SSE)

```rust
use axum::response::sse::{Event, Sse};
use tokio_stream::StreamExt;

async fn sse_handler() -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let stream = tokio_stream::iter(vec![
        Ok(Event::default().data("hello")),
        Ok(Event::default().data("world")),
    ]);
    Sse::new(stream)
}
```
