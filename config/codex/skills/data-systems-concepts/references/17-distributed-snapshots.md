# Distributed Snapshots

Use this when studying global state, checkpoint barriers, consistent cuts, stream checkpoints, or recovery across operators.

## Mental Model

A distributed snapshot records a consistent cut: local states plus messages in transit that could have existed together. Snapshotting becomes practical when markers or barriers flow through channels and each participant records state at a compatible boundary.

## Key Invariants

- A snapshot includes no effect without its causal prerequisites.
- Channels are recorded consistently with local state.
- Recovery restarts from state and inputs that match the snapshot boundary.

## Implementation Exercise

Simulate three processes with channels and implement the Chandy-Lamport marker protocol.

## Tests And Failure Cases

Inject messages during snapshot capture and verify that in-transit messages are recorded exactly when required.

## Online References

- [Distributed Snapshots: Determining Global States of Distributed Systems](https://lamport.azurewebsites.net/pubs/chandy.pdf)
- [Apache Flink Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/)
- [Lightweight Asynchronous Snapshots for Distributed Dataflows](https://arxiv.org/abs/1506.08603)
