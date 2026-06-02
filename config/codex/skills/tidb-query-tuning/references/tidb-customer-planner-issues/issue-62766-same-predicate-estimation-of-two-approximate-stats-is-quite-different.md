# Issue #62766: same predicate estimation of two approximate stats is quite different

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62766
- Status: open
- Type: type/enhancement
- Created At: 2025-08-01T07:22:37Z
- Labels: affects-7.5, component/statistics, epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- we can tell from the pic above, it's 3M vs 0.3M actually, ref TCOC-3945 to get the replayer detail

## Linked PRs
- Related PR #62695: planner: handle histogram last bucket end value underrepresented
  URL: https://github.com/pingcap/tidb/pull/62695
  State: closed
  Merged At: 2025-08-02T19:33:51Z
  Changed Files Count: 6
  Main Modules: pkg/planner, pkg/statistics
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/statistics/histogram.go
  PR Summary: What problem does this PR solve? Problem Summary: Like what the linked issue describes, the end value in the last histogram bucket could be underrepresented due to stale stats. This PR tries to detect such case precisely by looking at two conditions: 1.  The value should be in last histogram bucket and it should be the upper bound 2. The last bucket end count is much less than the average count of other NDV, indicating this might be a tail write traffic

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
