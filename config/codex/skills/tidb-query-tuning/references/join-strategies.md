# Join Strategies

TiDB supports multiple join algorithms. The optimizer picks one based on cost estimation, but stale stats or cardinality misestimation can lead to a wrong choice.

## Available join algorithms

### Hash Join (`HASH_JOIN`)

- **How it works:** Builds a hash table on the smaller (build) side, probes with the larger (probe) side.
- **Best for:** Large equi-joins where neither side has a useful index on the join key.
- **Cost profile:** O(build + probe) in time, O(build side) in memory.
- **Watch out for:** Memory pressure when the build side is large. Check `MEMORY_QUOTA` or `tidb_mem_quota_query`.

### Index Nested Loop Join (`INL_JOIN`)

- **How it works:** For each row on the outer side, probes the inner side using an index lookup.
- **Best for:** Inner table has a good index on the join key; outer side is small to moderate.
- **Cost profile:** O(outer rows × index lookup cost). Very fast when outer side is small.
- **Watch out for:** Outer side cardinality misestimation. If outer side is actually large, this becomes expensive.
- **Also watch out for:** The join type can be right while the chosen inner probe index is wrong. Always inspect the probe-side `access object` and pushed predicates.

### Index Hash Join (`INL_HASH_JOIN`)

- **How it works:** Like INL_JOIN but uses hash matching on the inner side instead of pure index order.
- **Best for:** Similar to INL_JOIN but when inner side needs hash-based matching.
- **Watch out for:** Like `INL_JOIN`, `INL_HASH_JOIN` can still be slow if the optimizer picks the wrong probe index on the inner side.

### Merge Join (`MERGE_JOIN`)

- **How it works:** Both sides sorted on join key, then merged in a single pass.
- **Best for:** Both sides already sorted (e.g., from index scans on the join key) or when data is naturally ordered.
- **Cost profile:** O(N + M) after sorting. Sorting cost matters if data isn't pre-sorted.

### Shuffle Hash Join (`SHUFFLE_JOIN`) — MPP only

- **How it works:** Redistributes (shuffles) both sides by join key across TiFlash nodes, then hash joins locally.
- **Best for:** Large-to-large joins in TiFlash where neither side is small enough to broadcast.

### Broadcast Join (`BROADCAST_JOIN`) — MPP only

- **How it works:** Broadcasts the smaller side to all TiFlash nodes, then joins locally.
- **Best for:** One side is small, the other is large. Avoids shuffling the large side.

## Decision guide

```
Both tables small (< 10K rows)?
├── Doesn't matter much. Any strategy works.
│
Is there a good index on the join key of one side?
├── YES → Is the other side small?
│         ├── YES → INL_JOIN (indexed side as inner)
│         └── NO  → Still consider INL_JOIN if indexed side is large but
│                   outer side is moderate. Otherwise HASH_JOIN.
└── NO  → HASH_JOIN (smaller side as build).
          └── Are both sides pre-sorted on join key?
              └── YES → Consider MERGE_JOIN.

Using TiFlash?
├── One side small → BROADCAST_JOIN
└── Both sides large → SHUFFLE_JOIN
```

## Forcing join strategy

```sql
-- Force hash join between orders and customers
SELECT /*+ HASH_JOIN(o, c) */ *
FROM orders o JOIN customers c ON o.cust_id = c.id;

-- Force index join with customers as inner (probed) side
SELECT /*+ INL_JOIN(c) */ *
FROM orders o JOIN customers c ON o.cust_id = c.id;

-- Force index hash join with customers as inner (probed) side
SELECT /*+ INL_HASH_JOIN(c) */ *
FROM orders o JOIN customers c ON o.cust_id = c.id;

-- Force join order: join orders and items first, then customers
SELECT /*+ LEADING(o, i, c) */ *
FROM orders o
JOIN items i ON i.order_id = o.id
JOIN customers c ON c.id = o.cust_id;
```

Join hints only control the join algorithm and inner table choice. They do not guarantee that the chosen probe-side index is the best one. For `IndexJoin` and `IndexHashJoin`, always inspect the inner `access object` and compare candidate indexes when latency remains high.

## Common misoptimization patterns

### Pattern: Hash join with huge build side

**Symptom:** `EXPLAIN ANALYZE` shows `HashJoin` with a large `Build` side consuming excessive memory or spilling to disk.

**Fix:** If the inner table has an index on the join key, try `INL_JOIN`:

```sql
SELECT /*+ INL_JOIN(big_table) */ ...
FROM small_table s JOIN big_table b ON s.id = b.ref_id;
```

### Pattern: Index join on a non-selective outer side

**Symptom:** `EXPLAIN ANALYZE` shows `IndexJoin` with a large `actRows` on the outer (driving) side, causing millions of index probes.

**Fix:** Switch to `HASH_JOIN`:

```sql
SELECT /*+ HASH_JOIN(t1, t2) */ ...
FROM t1 JOIN t2 ON t1.id = t2.ref_id
WHERE t1.status = 'active';
```

### Pattern: Right index-based join, wrong probe index

**Symptom:** `EXPLAIN ANALYZE` shows `IndexJoin` or `IndexHashJoin`, and that join type looks reasonable, but the probe child uses the wrong index. Common signs are:

- The probe-side `access object` does not align with the full join key.
- Residual filters remain on the probe side even though another existing index could push more predicates down.
- The plan uses `IndexLookUp` plus heavy table lookup even though a more covering inner index already exists.

**Fix:** Keep the join algorithm if it is otherwise correct, but compare candidate inner indexes with `USE_INDEX` or `IGNORE_INDEX`:

```sql
SELECT /*+ INL_JOIN(t2) USE_INDEX(t2, idx_join_cols) */ ...
FROM t1 JOIN t2 ON ...;
```

If the better probe index wins consistently, stabilize it with a SQL binding or query hint.

### Pattern: Wrong join order in multi-way join

**Symptom:** Intermediate join produces a huge result that is then joined with a small table.

**Fix:** Use `LEADING` to force the small table earlier:

```sql
SELECT /*+ LEADING(small, medium, large) */ ...
FROM large l JOIN medium m ON ... JOIN small s ON ...;
```
