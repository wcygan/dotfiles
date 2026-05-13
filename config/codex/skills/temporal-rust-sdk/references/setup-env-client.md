# Setup, Environment, and Client

Use this for project setup, Temporal CLI local development, `temporal.toml`, environment variables, client creation, workflow starts, results, and workflow interactions.

Official docs:
- Quickstart: https://docs.temporal.io/develop/rust/quickstart
- Client: https://docs.temporal.io/develop/rust/client/temporal-client
- Environment configuration: https://docs.temporal.io/develop/environment-configuration

Local anchors:
- Hello world worker: `crates/sdk/examples/hello_world/worker.rs:13`
- Hello world starter: `crates/sdk/examples/hello_world/starter.rs:11`
- Client README: `crates/client/README.md:15`
- Env var and TOML docs: `crates/common/src/envconfig.rs:7`
- Config conversion to client options: `crates/client/src/envconfig.rs:19`
- Workflow start options: `crates/client/src/options_structs.rs:198`

## Setup Shape

The official quickstart expects:
- Rust and Cargo installed.
- Dependencies including `temporalio-sdk`, `temporalio-client`, `temporalio-common`, `temporalio-macros`, `temporalio-sdk-core`, `tokio`, `serde`, and `serde_json`.
- A local Temporal dev server from Temporal CLI:
  - `temporal server start-dev`
  - service on `localhost:7233`
  - Web UI on `http://localhost:8233` unless `--ui-port` changes it.

When editing this workspace, do not blindly copy dependency versions from docs. Prefer the workspace `Cargo.toml` and local examples because this checkout may be ahead of released crates.

## Client Creation

The Rust client model is:

1. Build or load `ConnectionOptions`.
2. `Connection::connect(conn_opts).await?`.
3. `Client::new(connection, client_opts)?`.

The canonical envconfig pattern in this repo is:

```rust
let (conn_opts, client_opts) =
    ClientOptions::load_from_config(LoadClientConfigProfileOptions::default())?;
let connection = Connection::connect(conn_opts).await?;
let client = Client::new(connection, client_opts)?;
```

See `crates/sdk/examples/hello_world/worker.rs:18` and `crates/sdk/examples/hello_world/starter.rs:11`.

Important rule from the official client docs: do not create or use a Temporal Client inside Workflow code. Using a client inside an Activity is acceptable when the activity needs to communicate with Temporal.

## Environment Configuration

Local source lists the Rust-supported environment variables at `crates/common/src/envconfig.rs:7`:
- `TEMPORAL_CONFIG_FILE`
- `TEMPORAL_PROFILE`
- `TEMPORAL_ADDRESS`
- `TEMPORAL_NAMESPACE`
- `TEMPORAL_API_KEY`
- `TEMPORAL_TLS`
- `TEMPORAL_TLS_CLIENT_CERT_PATH` or `TEMPORAL_TLS_CLIENT_CERT_DATA`
- `TEMPORAL_TLS_CLIENT_KEY_PATH` or `TEMPORAL_TLS_CLIENT_KEY_DATA`
- `TEMPORAL_TLS_SERVER_CA_CERT_PATH` or `TEMPORAL_TLS_SERVER_CA_CERT_DATA`
- `TEMPORAL_TLS_SERVER_NAME`
- `TEMPORAL_TLS_DISABLE_HOST_VERIFICATION`
- `TEMPORAL_CODEC_ENDPOINT`
- `TEMPORAL_CODEC_AUTH`
- `TEMPORAL_GRPC_META_*`

The TOML shape is anchored in `crates/common/src/envconfig.rs:31`:

```toml
[profile.default]
address = "localhost:7233"
namespace = "default"

[profile.default.grpc_meta]
custom_header = "value"

[profile.prod]
address = "your-namespace.account.tmprl.cloud:7233"
namespace = "your-namespace"
api_key = "..."
```

Local behavior to remember:
- `crates/client/src/envconfig.rs:16` defaults to `http://localhost:7233` and namespace `default`.
- `crates/client/src/envconfig.rs:43` adds a URL scheme when the address is bare `host:port`.
- `crates/client/src/envconfig.rs:95` enables TLS when a TLS section is not disabled or when an API key is set.

Never commit real API keys, certificate data, or local machine-specific secrets into examples or tests.

## Starting Workflows and Getting Results

The docs and local starter agree on this shape:

```rust
let handle = client
    .start_workflow(
        HelloWorldWorkflow::run,
        "Temporal".to_string(),
        WorkflowStartOptions::new("hello-world", "hello-world-workflow-id").build(),
    )
    .await?;

let result = handle
    .get_result(WorkflowGetResultOptions::default())
    .await?;
```

Use `WorkflowStartOptions::new(task_queue, workflow_id)` and choose a workflow id that maps to a stable business entity or process where possible. The official client docs call out that a task queue is usually required and a worker must poll the same queue for progress.

## Signals, Queries, Updates

Use `crates/client/README.md:87` and `crates/sdk/examples/message_passing/workflows.rs:19` together:
- signals are fire-and-forget mutations
- queries are read-only
- updates mutate state and return a result
- validators can reject invalid updates before state mutation

For typed interactions, prefer generated function references such as `MyWorkflow::method`. For cross-language or dynamic cases, use the untyped APIs and the payload converter deliberately.
