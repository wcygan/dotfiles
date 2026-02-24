# Worker Setup

## Full Worker Example

```rust
use std::str::FromStr;
use std::sync::Arc;
use temporalio_client::{Client, ClientOptions, Connection, ConnectionOptions};
use temporalio_common::worker::{WorkerDeploymentOptions, WorkerDeploymentVersion, WorkerTaskTypes};
use temporalio_sdk::{Worker, WorkerOptions};
use temporalio_sdk_core::{CoreRuntime, RuntimeOptions, Url};
use temporalio_sdk_core::telemetry::TelemetryOptions;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. Create runtime
    let runtime_options = RuntimeOptions::builder()
        .telemetry_options(TelemetryOptions::builder().build())
        .build()?;
    let runtime = CoreRuntime::new_assume_tokio(runtime_options)?;

    // 2. Connect to Temporal
    let url = Url::from_str("http://localhost:7233")?;
    let conn_opts = ConnectionOptions::new(url).build();
    let connection = Connection::connect(conn_opts).await?;

    // 3. Create client
    let client_opts = ClientOptions::new("default").build();
    let client = Client::new(connection, client_opts)?;

    // 4. Build worker options
    let worker_opts = WorkerOptions::new("my-task-queue")
        .task_types(WorkerTaskTypes::all())
        .max_cached_workflows(1000)
        .build();

    // 5. Create and run worker
    let mut worker = Worker::new(&runtime, client, worker_opts)?;
    worker.register_workflow::<MyWorkflow>();
    worker.register_activities(Arc::new(MyActivities::new()));
    worker.run().await?;

    Ok(())
}
```

## Runtime Options

```rust
let runtime_options = RuntimeOptions::builder()
    .telemetry_options(
        TelemetryOptions::builder()
            // Configure logging, metrics, tracing here
            .build()
    )
    .build()?;

// Use existing tokio runtime
let runtime = CoreRuntime::new_assume_tokio(runtime_options)?;
```

## Connection Options

### Local Development

```rust
let conn = ConnectionOptions::new(
    Url::from_str("http://localhost:7233")?
).build();
```

### Temporal Cloud (mTLS)

```rust
let conn = ConnectionOptions::new(
    Url::from_str("https://my-namespace.tmprl.cloud:7233")?
)
    .tls(TlsConfig {
        client_cert: std::fs::read("client.pem")?,
        client_private_key: std::fs::read("client.key")?,
        ..Default::default()
    })
    .build();
```

### Temporal Cloud (API Key)

```rust
let conn = ConnectionOptions::new(
    Url::from_str("https://my-namespace.tmprl.cloud:7233")?
)
    .api_key("my-api-key".to_string())
    .build();
```

## Client Options

```rust
let client_opts = ClientOptions::new("my-namespace")
    // Additional client configuration
    .build();
let client = Client::new(connection, client_opts)?;
```

## WorkerOptions

```rust
let opts = WorkerOptions::new("my-task-queue")
    // What this worker handles
    .task_types(WorkerTaskTypes::all())         // workflows + activities
    // .task_types(WorkerTaskTypes::activity_only())
    // .task_types(WorkerTaskTypes::workflow_only())

    // Workflow caching
    .max_cached_workflows(1000)

    // Poller tuning
    .workflow_task_poller_behavior(PollerBehavior::SimpleMaximum(5))
    .activity_task_poller_behavior(PollerBehavior::SimpleMaximum(5))

    // Sticky queue (workflow task routing optimization)
    .sticky_queue_schedule_to_start_timeout(Duration::from_secs(10))

    // Activity rate limiting
    .max_task_queue_activities_per_second(Some(100.0))
    .max_worker_activities_per_second(Some(50.0))

    // Heartbeat throttling
    .max_heartbeat_throttle_interval(Duration::from_secs(60))
    .default_heartbeat_throttle_interval(Duration::from_secs(30))

    // Worker versioning / deployment
    .deployment_options(WorkerDeploymentOptions {
        version: WorkerDeploymentVersion {
            deployment_name: "my-service".to_owned(),
            build_id: env!("CARGO_PKG_VERSION").to_owned(),
        },
        use_worker_versioning: true,
        default_versioning_behavior: None,
    })

    .build();
```

## Registration

```rust
let mut worker = Worker::new(&runtime, client, worker_opts)?;

// Register workflow types
worker.register_workflow::<OrderWorkflow>();
worker.register_workflow::<PaymentWorkflow>();

// Register activities (with shared state)
let activities = Arc::new(MyActivities::new(pool.clone()));
worker.register_activities(activities);

// Register activities (stateless)
worker.register_activities(Arc::new(StatelessActivities));

// Optional: add interceptor
worker.set_worker_interceptor(MyInterceptor {});
```

## Graceful Shutdown

```rust
let shutdown = worker.shutdown_handle();

// Spawn shutdown trigger
tokio::spawn(async move {
    tokio::signal::ctrl_c().await.unwrap();
    shutdown(); // Signal worker to stop
});

// worker.run() will complete gracefully
worker.run().await?;
```

## Multiple Workers

Run multiple workers in the same process for different task queues:

```rust
let worker1 = Worker::new(&runtime, client.clone(), opts_queue_a)?;
let worker2 = Worker::new(&runtime, client.clone(), opts_queue_b)?;

tokio::try_join!(
    worker1.run(),
    worker2.run(),
)?;
```
