# Testing Data Systems

Use this when validating a storage engine, distributed protocol, transaction system, stream processor, or consistency claim.

## Mental Model

Data-system testing works best when it checks invariants over histories and persisted state. Unit tests exercise local rules. Crash tests exercise durability. Fault-injection and history checking exercise distributed guarantees. The test should name the guarantee before generating workloads.

## Key Invariants

- Each test records enough history to explain a failure.
- Faults target boundaries where guarantees can break.
- The checker encodes the advertised contract, not the implementation strategy.

## Implementation Exercise

Write a harness that performs random key-value operations, injects crashes, restarts, and checks a model of expected state.

## Tests And Failure Cases

Inject process crashes, dropped messages, clock jumps, partial writes, and duplicated requests.

## Online References

- [Jepsen Analyses](https://jepsen.io/analyses)
- [Jepsen: Consistency Models](https://jepsen.io/consistency/models)
- [FoundationDB Paper](https://www.foundationdb.org/files/fdb-paper.pdf)

