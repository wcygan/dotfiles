# Partitioning And Rebalancing

Use this when studying sharding, range partitions, hash partitions, hot keys, split points, placement, and rebalancing.

## Mental Model

Partitioning maps data to ownership scopes. Rebalancing changes that mapping while serving traffic. The central tradeoff is stable routing versus adaptive load movement. Every design needs a way to find the owner, move state, and handle requests during movement.

## Key Invariants

- Every key maps to an owner or an explicit migration state.
- Movement preserves durability before the old owner stops serving.
- Clients and routers converge on the new mapping.

## Implementation Exercise

Build a consistent-hashing ring and simulate adding and removing nodes while measuring key movement.

## Tests And Failure Cases

Move a shard while reads and writes continue. Verify whether writes are forwarded, rejected, or dual-written.

## Online References

- [Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [CockroachDB Distribution Layer](https://www.cockroachlabs.com/docs/stable/architecture/distribution-layer)
- [TiKV Region Guide](https://tikv.github.io/tikv-dev-guide/understanding-tikv/scalability/region.html)
