---
name: data-systems-concepts
description: Use when studying, explaining, designing, reviewing, or implementing data systems concepts including stream processing, replication, partitioning, transactions, isolation, consistency, consensus, failure detection, gossip, CRDTs, storage engines, pages, slotted pages, B-Trees, WAL, ARIES, MVCC, LSM trees, SSTables, compaction, Bloom filters, Merkle trees, checksums, compression, columnar storage, and database testing.
---

# Data Systems Concepts

Goal: Help Codex turn data-systems questions into clear mental models, implementation exercises, and validation ideas.

Success means:
- The answer names the relevant system boundary, invariants, tradeoffs, and failure modes.
- The answer loads only the reference files needed for the current task.
- The answer points to credible online references when the user wants deeper study.

Stop when: The response gives a practical next step, implementation sketch, or review conclusion grounded in the relevant concepts.

## Workflow

1. Identify the user's topic: dataflow, distributed coordination, storage engine internals, indexing, recovery, or testing.
2. Read `references/00-topic-map.md` when the best topic file is unclear.
3. Load one to three focused reference files for the task.
4. Return the smallest useful structure: mental model, key invariants, tradeoffs, implementation exercise, and tests or failure cases.
5. When writing code, choose a narrow artifact that demonstrates one concept and name the omissions explicitly.

## Reference Groups

- High-level dataflow: topic map, architecture, logs, stream processing, watermarks, derived data.
- Distributed systems: replication, quorums, consistency, transactions, consensus, election, failure detection, partitioning, time, leases, snapshots, repair, CRDTs.
- Validation: data-system testing, model checking, deterministic simulation.
- Storage engines: pages, slotted pages, buffer pools, B-Trees, locking, secondary indexes, WAL, ARIES, MVCC, checkpoints, LSMs, SSTables, compaction, Bloom filters, Merkle trees, compression, checksums, columnar storage, blob separation.

## Response Shape

Use this shape when it fits:

```text
Mental model:
Key invariants:
Tradeoffs:
Implementation exercise:
Tests and failure cases:
References:
```

