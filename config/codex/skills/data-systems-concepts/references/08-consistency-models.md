# Consistency Models

Use this when distinguishing linearizability, sequential consistency, causal consistency, read-your-writes, monotonic reads, eventual consistency, or serializability.

## Mental Model

A consistency model defines which histories are legal. It is a contract between the system and its clients. Stronger models constrain more histories and usually require more coordination. Weaker models allow more availability and lower latency but move more reasoning into application logic.

## Key Invariants

- The model names what clients may observe.
- The history checker knows the operation start, operation end, input, and output.
- The model's scope is clear: object, key, transaction, session, or database.

## Implementation Exercise

Record histories for a register and write a small checker for read-your-writes and monotonic-read violations.

## Tests And Failure Cases

Generate concurrent reads and writes. Compare histories that pass eventual consistency but fail linearizability.

## Online References

- [Jepsen Consistency Models](https://jepsen.io/consistency/models)
- [Linearizability: A Correctness Condition for Concurrent Objects](https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf)
- [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf)

