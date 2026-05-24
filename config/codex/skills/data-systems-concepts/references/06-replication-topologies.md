# Replication Topologies

Use this when comparing single-leader, multi-leader, leaderless, log-based, or state-based replication designs.

## Mental Model

Replication copies state or operations across nodes. The topology determines where writes are accepted, how ordering is assigned, how conflicts appear, and how failover works. The strongest question is which node is allowed to say a write is committed.

## Key Invariants

- A committed write has a defined durability quorum or replica set.
- Followers know how to catch up from a stable position.
- Failover preserves the advertised ordering and durability contract.

## Implementation Exercise

Implement primary-backup log shipping with a leader offset and follower acknowledgment offsets.

## Tests And Failure Cases

Kill the leader after local append but before follower acknowledgment. Verify what the client may observe.

## Online References

- [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Kafka Design: Replication](https://kafka.apache.org/documentation/#replication)
- [Spanner: Google's Globally-Distributed Database](https://research.google/pubs/pub39966/)

