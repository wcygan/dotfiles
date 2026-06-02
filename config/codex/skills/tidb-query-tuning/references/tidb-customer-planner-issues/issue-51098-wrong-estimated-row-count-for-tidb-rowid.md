# Issue #51098: Wrong estimated row count for _tidb_rowid

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/51098
- Status: open
- Type: type/enhancement
- Created At: 2024-02-13T10:10:51Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, component/statistics, epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The  is close to the total row count of the table. Thus, the cost of  is equal to  and the optimizer sometimes chooses , which is very slow and even causes TiKV OOM.

## Linked PRs
- Fix PR #51111: *: fix wrong estimated row count for _tidb_rowid
  URL: https://github.com/pingcap/tidb/pull/51111
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/internal/base/plan.go
  - pkg/planner/core/planbuilder.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
