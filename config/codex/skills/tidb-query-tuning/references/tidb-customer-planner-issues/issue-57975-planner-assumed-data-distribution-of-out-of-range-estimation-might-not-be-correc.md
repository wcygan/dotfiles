# Issue #57975: planner: assumed data distribution of out-of-range estimation might not be correct in some cases

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/57975
- Status: open
- Type: type/enhancement
- Created At: 2024-12-04T08:57:34Z
- Labels: affects-7.5, epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Below is a real bad case from one customer: ![Image]()

## Linked PRs
- Fix PR #59561: planner: add risk for out of range
  URL: https://github.com/pingcap/tidb/pull/59561
  State: closed
  Merged At: not merged
  Changed Files Count: 14
  Main Modules: pkg/planner, pkg/statistics, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/cardinality/cross_estimation.go
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/row_count_test.go
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/stats.go
  - pkg/planner/util/path.go
  - pkg/statistics/handle/ddl/ddl_test.go
  - pkg/statistics/handle/handletest/handle_test.go
  - pkg/statistics/handle/storage/read_test.go
  - pkg/statistics/handle/updatetest/update_test.go
  - pkg/statistics/statistics_test.go
  - pkg/statistics/table.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
