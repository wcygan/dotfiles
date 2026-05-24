# Event Time And Watermarks

Use this when questions involve windows, late data, processing time, event time, triggers, or when a result should be considered complete.

## Mental Model

Event time is when data claims something happened. Processing time is when the system observes it. Watermarks are progress estimates that let a stream processor close windows while still modeling late arrivals. The hard problem is choosing how much lateness the system accepts.

## Key Invariants

- Window assignment uses event timestamps.
- Watermarks describe progress, not truth.
- Late data has a defined policy: drop, correct, retract, or update.

## Implementation Exercise

Write a tumbling-window aggregator that accepts events out of order and closes windows when a watermark passes the window end.

## Tests And Failure Cases

Feed events in shuffled order. Verify normal output, late correction behavior, and the boundary case at exactly the watermark.

## Online References

- [The Dataflow Model](https://research.google/pubs/pub43864/)
- [Apache Flink: Timely Stream Processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/)
- [Apache Beam: Windowing](https://beam.apache.org/documentation/programming-guide/#windowing)
