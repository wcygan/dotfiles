# DDL Owner Memory Leak From the Internal Session Pool

## User Symptom
- One TiDB node, usually the owner node, has much higher memory than its peers.

## Investigation Signals
- The memory skew is concentrated on the owner node.
- TTL framework, distributed framework, and auto analyze are all active around the same time.
- The public issue attributes the leak to the internal session pool and session bookkeeping.

## Workaround
- The handbook does not record a clean runtime workaround.
- If operationally possible, reduce background framework pressure until the node can be upgraded.

## Fixed Version
- `v8.4.0`

## Public References
- https://github.com/pingcap/tidb/issues/56934
- https://github.com/pingcap/tidb/pull/56935
