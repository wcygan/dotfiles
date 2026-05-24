# Model Checking And Simulation

Use this when a protocol has small states, tricky interleavings, or failures that are hard to cover with example-based tests.

## Mental Model

Model checking explores possible states. Simulation controls nondeterminism and makes failures reproducible. Both techniques force the design to expose state transitions, messages, timers, and invariants clearly.

## Key Invariants

- The model has explicit state and transition rules.
- The checker can enumerate or randomize schedules.
- Every failure includes a reproducible trace.

## Implementation Exercise

Model a two-replica primary-backup protocol with message drop, delay, and crash transitions. Check that committed writes are not lost.

## Tests And Failure Cases

Shrink a failing trace to the smallest schedule that violates the invariant.

## Online References

- [TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html)
- [FoundationDB Paper](https://www.foundationdb.org/files/fdb-paper.pdf)
- [TigerBeetle: Safety and Simulation Testing](https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/)

