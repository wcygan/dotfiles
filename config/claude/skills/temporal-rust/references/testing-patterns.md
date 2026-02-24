# Testing Patterns

## Testing Activities

Activities are regular async functions — test them directly:

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use temporalio_sdk::activities::ActivityContext;

    #[tokio::test]
    async fn test_send_email() {
        // Activities can be tested by calling the function directly
        // ActivityContext is needed but can be created for testing
        let result = MyActivities::send_email(
            test_activity_context(),
            "user@example.com".to_string(),
            "Hello".to_string(),
        ).await;

        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_activity_error_types() {
        let result = MyActivities::validate_input(
            test_activity_context(),
            "".to_string(), // invalid input
        ).await;

        match result {
            Err(ActivityError::NonRetryable(_)) => {} // expected
            other => panic!("Expected NonRetryable, got {:?}", other),
        }
    }
}
```

## Testing Activities with Shared State

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;

    #[tokio::test]
    async fn test_db_activity() {
        let pool = setup_test_db().await;
        let activities = Arc::new(DbActivities { pool });

        let result = DbActivities::fetch_user(
            activities.clone(),
            test_activity_context(),
            1,
        ).await;

        assert!(result.is_ok());
        assert_eq!(result.unwrap().name, "Test User");
    }
}
```

## Interceptors for Testing

### FailOnNondeterminismInterceptor

Catches determinism violations during replay:

```rust
use temporalio_sdk::interceptors::FailOnNondeterminismInterceptor;

// In test worker setup
worker.set_worker_interceptor(FailOnNondeterminismInterceptor {});
// Worker will panic if nondeterminism detected during replay
```

### ReturnWorkflowExitValueInterceptor

Captures workflow return values for assertion:

```rust
use temporalio_sdk::interceptors::ReturnWorkflowExitValueInterceptor;

let interceptor = ReturnWorkflowExitValueInterceptor::new();
let exit_rx = interceptor.exit_receiver();

worker.set_worker_interceptor(interceptor);

// After workflow completes:
let exit_value = exit_rx.recv().await.unwrap();
match exit_value {
    WorkflowTermination::Completed(payload) => {
        // Assert on the result
    }
    WorkflowTermination::Failed(failure) => {
        panic!("Workflow failed: {:?}", failure);
    }
    _ => panic!("Unexpected termination"),
}
```

### Custom Test Interceptor

```rust
use temporalio_sdk::interceptors::WorkerInterceptor;

struct TestInterceptor {
    activation_count: Arc<AtomicU32>,
}

#[async_trait::async_trait(?Send)]
impl WorkerInterceptor for TestInterceptor {
    async fn on_workflow_activation(
        &self,
        activation: &WorkflowActivation,
    ) -> Result<(), anyhow::Error> {
        self.activation_count.fetch_add(1, Ordering::SeqCst);
        Ok(())
    }

    async fn on_workflow_activation_completion(
        &self,
        completion: &WorkflowActivationCompletion,
    ) {
        // Inspect commands sent back to server
    }

    fn on_shutdown(&self, _worker: &Worker) {
        // Cleanup
    }
}
```

## Integration Testing with Local Server

For full integration tests, run against a local Temporal server:

```rust
#[tokio::test]
async fn test_workflow_end_to_end() {
    // Start local Temporal server (or use docker)
    // Connect client
    let client = create_test_client().await;

    // Start worker in background
    let worker_handle = tokio::spawn(async move {
        let mut worker = create_test_worker(&runtime, client.clone()).await;
        worker.register_workflow::<OrderWorkflow>();
        worker.register_activities(Arc::new(TestActivities));
        worker.run().await.unwrap();
    });

    // Start workflow
    let run = client.execute_workflow(
        StartWorkflowOptions {
            workflow_id: "test-order-1".to_string(),
            task_queue: "test-queue".to_string(),
            workflow_type: "OrderWorkflow".to_string(),
            ..Default::default()
        },
        vec![/* input */],
    ).await.unwrap();

    // Wait for result
    let result = run.get_result().await.unwrap();
    assert_eq!(result, expected_output);

    // Shutdown
    shutdown();
    worker_handle.await.unwrap();
}
```

## Testing Signals and Queries

```rust
#[tokio::test]
async fn test_signal_and_query() {
    let client = create_test_client().await;
    // ... start worker and workflow ...

    // Send signal
    client.signal_workflow(
        "test-workflow-id",
        "",
        "add_item",
        vec![/* signal payload */],
    ).await.unwrap();

    // Query state
    let result = client.query_workflow(
        "test-workflow-id",
        "",
        "get_items",
        vec![],
    ).await.unwrap();

    assert_eq!(result.len(), 1);
}
```

## Testing Cancellation

```rust
#[tokio::test]
async fn test_workflow_cancellation() {
    let client = create_test_client().await;
    // ... start worker and workflow ...

    // Cancel workflow
    client.cancel_workflow("test-workflow-id", "").await.unwrap();

    // Verify graceful cleanup occurred
    let result = run.get_result().await;
    // Assert workflow handled cancellation properly
}
```

## Test Utilities

### Helper for Test Worker Creation

```rust
async fn create_test_worker(
    runtime: &CoreRuntime,
    client: Client,
) -> Worker {
    let opts = WorkerOptions::new("test-queue")
        .task_types(WorkerTaskTypes::all())
        .max_cached_workflows(10)
        .build();

    Worker::new(runtime, client, opts).unwrap()
}
```

### Test Activity Context

```rust
fn test_activity_context() -> ActivityContext {
    // Create a minimal ActivityContext for unit testing
    // Implementation depends on SDK version and test utilities
    ActivityContext::for_testing()
}
```

## Property-Based Testing Ideas

- Verify workflow determinism by running the same input twice and comparing command sequences
- Test that all `ActivityError` variants are handled in workflow logic
- Fuzz workflow inputs to ensure no panics in workflow code
- Verify `state()` and `state_mut()` consistency under random signal orderings
