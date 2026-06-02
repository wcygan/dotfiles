# Issue #65712: Better plan for `LIMIT n ORDER BY` on `IndexMerge` when not all partial paths satisfy the `ORDER BY`

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65712
- Status: open
- Type: type/enhancement
- Created At: 2026-01-22T01:28:23Z
- Labels: affects-7.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- This is a simplified case from a customer scenario.

## Linked PRs
- Fix PR #66097: planner, executor: support merge sort for IN conditions in IndexMerge…
  URL: https://github.com/pingcap/tidb/pull/66097
  State: open
  Merged At: not merged
  Changed Files Count: 10
  Main Modules: tests/integrationtest, pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/index_merge_reader.go
  - pkg/executor/test/indexmergereadtest/BUILD.bazel
  - pkg/executor/test/indexmergereadtest/index_merge_reader_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/physicalop/physical_index_scan.go
  - pkg/planner/core/operator/physicalop/physical_table_scan.go
  - tests/integrationtest/r/index_merge.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/grouped_ranges_order_by.result
  - tests/integrationtest/t/index_merge.test
  PR Summary: What problem does this PR solve? Problem Summary: For queries like : The  partial path can keep order →  returns The  partial path needs merge sort →  returns
- Fix PR #67771: planner, executor: support merge sort for IN conditions in IndexMerge partial paths
  URL: https://github.com/pingcap/tidb/pull/67771
  State: open
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/executor, tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/index_merge_reader.go
  - pkg/executor/mem_reader.go
  - pkg/executor/test/indexmergereadtest/index_merge_reader_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/physicalop/physical_index_scan.go
  - tests/integrationtest/r/index_merge.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/t/index_merge.test
  PR Summary: What problem does this PR solve? Problem Summary: For queries like , where indexes  and  are available: The  partial path on  can directly satisfy  (). The  partial path on  cannot directly satisfy , because the ranges  and  are individually ordered by  but not globally ordered.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
