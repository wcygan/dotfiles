# Leases And Fencing

Use this when studying distributed locks, leader leases, stale owners, fencing tokens, or cache consistency.

## Mental Model

A lease grants temporary authority. A fencing token makes authority comparable after delays and pauses. The hard case is an old owner that resumes after its lease expired and still reaches a shared resource. Fencing gives the resource a way to reject stale work.

## Key Invariants

- Lease validity depends on a time or quorum assumption.
- Fencing tokens increase monotonically for each authority grant.
- Shared resources compare tokens before accepting guarded writes.

## Implementation Exercise

Build a lease service that returns increasing fencing tokens and a storage object that rejects stale tokens.

## Tests And Failure Cases

Pause a lease holder past expiration, elect a new holder, then deliver the old holder's delayed write.

## Online References

- [Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency](https://web.stanford.edu/class/cs240/readings/leases.pdf)
- [How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
- [ZooKeeper Recipes: Locks](https://zookeeper.apache.org/doc/current/recipes.html#sc_recipes_Locks)
