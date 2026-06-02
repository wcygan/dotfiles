# Issue #57991: planner: the estimation results of same predicate on different index statistics are not consistent

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/57991
- Status: open
- Type: type/enhancement
- Created At: 2024-12-04T11:44:21Z
- Labels: epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Enhancement See the result below, the estimation result of the second query should be less than the first's, since predicates of the first is a sub-set of the second's. But since we estimate them on different index statistics (IDX1 and IDX2), and statistics has a certain level of randomness, then finally their estimation results are not consistent: ![Image]()

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
