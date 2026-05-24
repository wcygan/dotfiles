# Stream Processing

Use this when a system continuously consumes events, updates state, emits derived records, or coordinates processors over partitions.

## Mental Model

Stream processing turns an unbounded log into continuously maintained state. The core boundary is between input ordering, state management, output guarantees, and failure recovery. A stream processor is easiest to reason about when each operator has explicit inputs, state, timers, and outputs.

## Key Invariants

- Input position and operator state advance together.
- Outputs match the chosen delivery contract: at-most-once, at-least-once, or exactly-once effect.
- Reprocessing produces acceptable duplicates or idempotent results.

## Implementation Exercise

Implement a partitioned word-count consumer that checkpoints offsets and local state after each batch.

## Tests And Failure Cases

Crash after processing and before checkpointing. Restart and verify whether duplicates are expected, suppressed, or repaired.

## Online References

- [The Dataflow Model](https://research.google/pubs/pub43864/)
- [Apache Flink: Stateful Stream Processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/)
- [Kafka Streams Architecture](https://kafka.apache.org/documentation/streams/architecture)
