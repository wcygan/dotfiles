---
title: Commands & Events
description: Calling Rust from frontend, calling frontend from Rust, commands, events, channels, streaming
tags: [commands, events, invoke, channels, streaming, ipc, calling-rust, calling-frontend]
---

# Commands & Events

## Calling Rust from Frontend (Commands)

### Define a Command

```rust
#[tauri::command]
fn my_custom_command() {
    println!("I was invoked from JavaScript!");
}
```

### Register with Builder

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![my_custom_command])
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

### Invoke from JavaScript

```javascript
import { invoke } from '@tauri-apps/api/core';
invoke('my_custom_command');
```

Command names must be unique. Commands in `lib.rs` cannot be `pub`; commands in separate modules must be `pub`.

### Passing Arguments

```rust
#[tauri::command]
fn my_custom_command(invoke_message: String) {
    println!("Message: {}", invoke_message);
}
```

```javascript
invoke('my_custom_command', { invokeMessage: 'Hello!' });
```

JavaScript uses **camelCase**; Rust uses **snake_case**. Force snake_case on JS side:

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_custom_command(invoke_message: String) {}
```

### Returning Data

Return types must implement `serde::Serialize`:

```rust
#[tauri::command]
fn my_custom_command() -> String {
    "Hello from Rust!".into()
}
```

```javascript
const message = await invoke('my_custom_command');
```

### Error Handling

```rust
#[tauri::command]
fn login(user: String, password: String) -> Result<String, String> {
    if user == "tauri" && password == "tauri" {
        Ok("logged_in".to_string())
    } else {
        Err("invalid credentials".to_string())
    }
}
```

```javascript
invoke('login', { user: 'tauri', password: 'pass' })
    .then((msg) => console.log(msg))
    .catch((err) => console.error(err));
```

**Custom error type (with `thiserror`):**

```rust
#[derive(Debug, thiserror::Error)]
enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

impl serde::Serialize for Error {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer,
    {
        serializer.serialize_str(self.to_string().as_ref())
    }
}
```

### Async Commands

```rust
#[tauri::command]
async fn my_custom_command(value: String) -> String {
    some_async_function().await;
    value
}
```

**Caveat**: borrowed types (`&str`, `State<'_, T>`) don't work in async commands. Workaround — wrap return in `Result`:

```rust
#[tauri::command]
async fn my_custom_command(value: &str) -> Result<String, ()> {
    some_async_function().await;
    Ok(format!(value))
}
```

### Optimized Array Buffer Returns

For large data (files, downloads):

```rust
use tauri::ipc::Response;

#[tauri::command]
fn read_file() -> Response {
    let data = std::fs::read("/path/to/file").unwrap();
    tauri::ipc::Response::new(data)
}
```

### Channels for Streaming Data

```rust
use tokio::io::AsyncReadExt;

#[tauri::command]
async fn load_image(
    path: std::path::PathBuf,
    reader: tauri::ipc::Channel<&[u8]>
) {
    let mut file = tokio::fs::File::open(path).await.unwrap();
    let mut chunk = vec![0; 4096];
    loop {
        let len = file.read(&mut chunk).await.unwrap();
        if len == 0 { break; }
        reader.send(&chunk).unwrap();
    }
}
```

### Accessing Special Types in Commands

```rust
// WebviewWindow
#[tauri::command]
async fn my_command(webview_window: tauri::WebviewWindow) {
    println!("Window: {}", webview_window.label());
}

// AppHandle
#[tauri::command]
async fn my_command(app_handle: tauri::AppHandle) {
    let app_dir = app_handle.path().app_dir();
}

// Managed State
#[tauri::command]
fn my_command(state: tauri::State<MyState>) {
    println!("{}", state.0);
}

// Raw Request Body & Headers
#[tauri::command]
fn upload(request: tauri::ipc::Request) -> Result<(), Error> {
    let tauri::ipc::InvokeBody::Raw(data) = request.body() else {
        return Err(Error::RequestBodyMustBeRaw);
    };
    let auth = request.headers().get("Authorization");
    Ok(())
}
```

### Modular Commands

```rust
// src-tauri/src/commands.rs
#[tauri::command]
pub fn my_custom_command() {
    println!("I was invoked from JavaScript!");
}

// src-tauri/src/lib.rs
mod commands;

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![commands::my_custom_command])
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

## Calling Frontend from Rust

### Global Events

```rust
use tauri::{AppHandle, Emitter};

#[tauri::command]
fn download(app: AppHandle, url: String) {
    app.emit("download-started", &url).unwrap();
    for progress in [1, 15, 50, 80, 100] {
        app.emit("download-progress", progress).unwrap();
    }
    app.emit("download-finished", &url).unwrap();
}
```

### Window-Specific Events

```rust
use tauri::{AppHandle, Emitter};

app.emit_to("login", "login-result", result).unwrap();
```

### Filtered Events

```rust
use tauri::{AppHandle, Emitter, EventTarget};

app.emit_filter("open-file", path, |target| match target {
    EventTarget::WebviewWindow { label } => label == "main" || label == "file-viewer",
    _ => false,
}).unwrap();
```

### Structured Event Payloads

Payloads must implement `Clone` and `Serialize`:

```rust
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct DownloadStarted<'a> {
    url: &'a str,
    download_id: usize,
    content_length: usize,
}

app.emit("download-started", DownloadStarted {
    url: &url,
    download_id: 1,
    content_length: 1000,
}).unwrap();
```

### Channels (High-Throughput Streaming)

Optimized for streaming ordered data and large payloads.

**Rust:**

```rust
use tauri::ipc::Channel;
use serde::Serialize;

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase", rename_all_fields = "camelCase", tag = "event", content = "data")]
enum DownloadEvent<'a> {
    Started { url: &'a str, download_id: usize, content_length: usize },
    Progress { download_id: usize, chunk_length: usize },
    Finished { download_id: usize },
}

#[tauri::command]
fn download(app: AppHandle, url: String, on_event: Channel<DownloadEvent>) {
    on_event.send(DownloadEvent::Started {
        url: &url, download_id: 1, content_length: 1000,
    }).unwrap();

    for chunk_length in [15, 150, 35, 500, 300] {
        on_event.send(DownloadEvent::Progress {
            download_id: 1, chunk_length,
        }).unwrap();
    }

    on_event.send(DownloadEvent::Finished { download_id: 1 }).unwrap();
}
```

**JavaScript:**

```typescript
import { invoke, Channel } from '@tauri-apps/api/core';

type DownloadEvent =
    | { event: 'started'; data: { url: string; downloadId: number; contentLength: number } }
    | { event: 'progress'; data: { downloadId: number; chunkLength: number } }
    | { event: 'finished'; data: { downloadId: number } };

const onEvent = new Channel<DownloadEvent>();
onEvent.onmessage = (message) => {
    console.log(`got download event ${message.event}`);
};

await invoke('download', { url: 'https://example.com/file', onEvent });
```

### JavaScript eval()

```rust
use tauri::Manager;

let webview = app.get_webview_window("main").unwrap();
webview.eval("console.log('hello from Rust')")?;
```

### Frontend Event Listening

```typescript
import { listen, once, emit, emitTo } from '@tauri-apps/api/event';

// Listen
const unlisten = await listen<DownloadStarted>('download-started', (event) => {
    console.log(event.payload.url);
});
unlisten(); // cleanup

// Listen once
await once('ready', (event) => {});

// Emit to backend
await emit('file-selected', '/path/to/file');

// Emit to specific window
await emitTo('settings', 'settings-update-requested', { key: 'notification', value: 'all' });
```

### Rust Event Listening

```rust
use tauri::Listener;

let event_id = app.listen("download-started", |event| {
    if let Ok(payload) = serde_json::from_str::<DownloadStarted>(&event.payload()) {
        println!("downloading {}", payload.url);
    }
});
app.unlisten(event_id);

// Listen once
app.once("ready", |event| {
    println!("app is ready");
});
```

## When to Use What

| Mechanism | Direction | Type Safety | Streaming | Use Case |
|-----------|-----------|-------------|-----------|----------|
| Commands (`invoke`) | Frontend → Rust | Yes | No | Request-response |
| Events | Both directions | No (JSON strings) | No | Notifications, broadcasts |
| Channels | Rust → Frontend | Yes | Yes | High-throughput, large payloads |
| `eval()` | Rust → Frontend | No | No | One-off JS execution |

## Further Reading

- https://v2.tauri.app/develop/calling-rust/
- https://v2.tauri.app/develop/calling-frontend/
