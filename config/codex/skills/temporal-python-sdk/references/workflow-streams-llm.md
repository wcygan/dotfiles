# Workflow Streams For LLM Output

Checked: 2026-06-05
Source: https://docs.temporal.io/develop/python/workflows/workflow-streams
Relevant section: "Application: Stream LLM output"

Use this reference when designing or reviewing Python Temporal Workflows that stream model output to a terminal, desktop UI, browser, SSE endpoint, or other live consumer.

## Why Workflow Streams Fit LLM Integrations

Workflow Streams gives a Workflow a durable, offset-addressed event channel built on Temporal Signals, Updates, and Queries. For LLM integrations, that means a subscriber can watch partial output while the Temporal Workflow still owns orchestration, retries, timeout policy, and the final durable result.

The useful split is:

- The Workflow hosts the stream and orchestrates the Activity.
- The Activity calls the LLM provider and publishes deltas as they arrive.
- The consumer subscribes to the Workflow ID, renders deltas, handles retry markers, and acknowledges the close marker.
- The Workflow returns the final Activity result after the consumer either acknowledges the terminator or a timeout expires.

Use this for modest fan-out progress streams: one chat session, one agent run, one UI with a few subscribers, or an SSE backend forwarding events to a browser. Do not use it for ultra-low-latency real-time voice or thousands of subscribers per Workflow.

## Stream LLM Output Pattern

1. Enable streaming in the Workflow `@workflow.init` method with `WorkflowStream()`.
2. Run the LLM call in an Activity, not in Workflow code.
3. In the Activity, construct `WorkflowStreamClient.from_within_activity(batch_interval=timedelta(milliseconds=200))`.
4. Publish typed `delta` events for text chunks.
5. Publish a `retry` event with `force_flush=True` when `activity.info().attempt > 1`.
6. Publish a `close` event at the end of a successful stream.
7. In the consumer, subscribe to `["delta", "retry", "close"]` with `result_type=RawValue` when topics carry different types.
8. Clear accumulated UI state on `retry`, append/render on `delta`, and signal the Workflow after receiving `close`.
9. In the Workflow, wait for the subscriber acknowledgment with a timeout fallback before returning.

## Design Rules

- Keep the Activity as publisher because the LLM call is non-deterministic external I/O.
- Disable provider-side retries when possible and let Temporal own retry policy at the Activity layer.
- Keep Workflow state independent of streamed output. The Workflow sees only the Activity's successful return value; subscribers may see partial failed attempts.
- Use `force_flush=True` for the first delta so the UI feels live, and for `retry` or other sentinel events. Do not force-flush every token unless the extra Signal volume is acceptable.
- Start around `batch_interval=200ms` for chat UI streaming. Lower latency means more Signals, more history, and higher server/workload cost.
- Add an application-level terminator such as a `close` topic. A subscriber's loop does not inherently know when the publisher is done.
- Use an acknowledgment handshake when the Workflow should not sleep after the terminator. Keep a timeout fallback for cases where no subscriber is attached.
- If the stream can run for hours or accumulate thousands of events, plan Continue-As-New and carry `WorkflowStreamState | None` through the input.

## Retry Semantics To Explain In Reviews

Workflow Streams deduplicates publish batches at the execution layer, but Activity retries are visible to subscribers. If an Activity emits three text deltas, fails, then retries and emits a complete answer, the subscriber can receive the first attempt's partial deltas and then the retry attempt's output.

That is why the LLM pattern publishes a `retry` sentinel on attempts greater than one. Consumers should clear or annotate displayed state on `retry` before rendering new deltas.

## Tuning And Limits

- `batch_interval`: maximum time between automatic flushes. Use about 200 ms as a starting point for LLM chat UI streaming.
- `force_flush=True`: use selectively for first output and important sentinel events.
- `max_batch_size`: set when item count or item size could make a publish batch too large.
- `poll_cooldown`: subscriber-side delay between polls; usually leave at default unless UI responsiveness or poll load requires tuning.
- `max_retry_duration` and `publisher_ttl`: tune together and keep `max_retry_duration < publisher_ttl`.
- For large payloads, publish references to external storage rather than large data blobs.

## Review Checklist

- Is the LLM provider call inside an Activity or external client, never Workflow code?
- Does the Activity heartbeat or otherwise surface liveness during long provider calls?
- Does the consumer handle `retry` by clearing or marking stale partial output?
- Does the stream publish a close marker?
- Does the Workflow wait briefly or use an acknowledgment Signal before returning?
- Are topics typed consistently, or are heterogeneous topics decoded through `RawValue`?
- Is the batching strategy appropriate for the UI latency target and Workflow history growth?
- If the Workflow is long-running, is Continue-As-New planned with `WorkflowStreamState | None`?
