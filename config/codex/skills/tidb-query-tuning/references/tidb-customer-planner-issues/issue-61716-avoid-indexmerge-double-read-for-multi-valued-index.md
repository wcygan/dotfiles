# Issue #61716: Avoid IndexMerge double-read for multi-valued index

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61716
- Status: open
- Type: type/enhancement
- Created At: 2025-06-13T03:00:51Z
- Labels: affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The multi-valued index uses operator to fetch data. However, if a composite index can cover needed columns, the operator should avoid reading data(TableRowIDScan) that introduces unnecessary overhead.

## Linked PRs
- Fix PR #66952: executor,planner: add index-only index-merge path for MVIndex queries
  URL: https://github.com/pingcap/tidb/pull/66952
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/builder.go
  - pkg/executor/index_merge_reader.go
  - pkg/executor/test/indexmergereadtest/BUILD.bazel
  - pkg/executor/test/indexmergereadtest/index_merge_reader_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/flat_plan.go
  - pkg/planner/core/operator/physicalop/physical_indexmerge_reader.go
  - pkg/planner/core/operator/physicalop/task_base.go
  PR Summary: What problem does this PR solve? Problem Summary: executor,planner: add index-only index-merge path for MVIndex queries What changed and how does it work? Summary Add an index-only fast path for  when accessing MVIndex in eligible queries.
- Fix PR #66996: planner: enable index-only MV IndexMerge only for single covered partial path (optimizer part)
  URL: https://github.com/pingcap/tidb/pull/66996
  State: closed
  Merged At: 2026-03-18T11:28:33Z
  Changed Files Count: 7
  Main Modules: pkg/planner/core, pkg/executor
  Sample Changed Files:
  - pkg/executor/builder.go
  - pkg/executor/test/indexmergereadtest/BUILD.bazel
  - pkg/executor/test/indexmergereadtest/index_merge_reader_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/flat_plan.go
  - pkg/planner/core/operator/physicalop/physical_indexmerge_reader.go
  - pkg/planner/core/optimizer.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: enable index-only MV IndexMerge only for single covered partial path (optimizer part) What changed and how does it work? This PR improves optimizer behavior for MV IndexMerge by allowing index-only plans only when both conditions are met: 1. IndexMerge has exactly one partial MV index path.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
