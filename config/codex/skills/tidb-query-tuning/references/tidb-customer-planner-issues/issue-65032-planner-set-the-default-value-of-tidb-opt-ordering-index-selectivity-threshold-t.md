# Issue #65032: planner: set the default value of `tidb_opt_ordering_index_selectivity_threshold` to 0.01

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65032
- Status: closed
- Type: type/enhancement
- Created At: 2025-12-15T03:30:59Z
- Closed At: 2025-12-15T06:09:00Z
- Labels: duplicate, epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The ordering-index is more risky because its estimation formula contains more assumptions and uncertainty; in contrast, the formula of filtering-index is more stable and natural.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- The issue is closed, but no merged PR was resolved automatically from the timeline. It may have been fixed by an internal branch, a batch PR, or manual closure.
