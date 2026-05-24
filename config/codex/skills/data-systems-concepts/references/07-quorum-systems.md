# Quorum Systems

Use this when reasoning about quorum reads, quorum writes, read repair, hinted handoff, and tunable consistency.

## Mental Model

A quorum system accepts work after enough replicas respond. The intersection between read and write quorums determines whether a read can observe the latest write without extra coordination. Quorums improve availability under partial failure, but they do not remove the need for versioning and repair.

## Key Invariants

- Write acknowledgment means at least W replicas stored the version.
- Read success means at least R replicas responded.
- Fresh reads require quorum intersection and a way to compare versions.

## Implementation Exercise

Build an in-memory three-replica key-value store with configurable R and W, vector or logical versions, and read repair.

## Tests And Failure Cases

Partition one replica, write with W=2, then read with R=1 and R=2. Compare staleness behavior.

## Online References

- [Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Cassandra Consistency Documentation](https://cassandra.apache.org/doc/stable/cassandra/architecture/dynamo.html)
- [Jepsen: Consistency Models](https://jepsen.io/consistency/models)

