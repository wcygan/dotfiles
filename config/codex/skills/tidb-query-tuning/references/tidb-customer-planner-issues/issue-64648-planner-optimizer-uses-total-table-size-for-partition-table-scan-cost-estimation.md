# Issue #64648: planner: Optimizer uses total table size for partition table scan cost estimation even when query can be pruned

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64648
- Status: open
- Type: type/enhancement
- Created At: 2025-11-24T10:44:26Z
- Labels: epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- I encountered an issue regarding the cost estimation logic for partitioned tables. When querying a partitioned table with a specific partition key, the estCost for the IndexFullScan operator is calculated based on the global table statistics (Total Rows) rather than the statistics of the pruned partition(s), resulting in an extremely inflated cost.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
