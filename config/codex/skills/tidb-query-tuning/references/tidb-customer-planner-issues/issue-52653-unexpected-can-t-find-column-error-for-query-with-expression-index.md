# Issue #52653: Unexpected `Can't find column` error for query with expression index

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52653
- Status: closed
- Type: type/bug
- Created At: 2024-04-17T01:18:52Z
- Closed At: 2025-09-25T04:48:02Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Sometimes(related to the query plan I believe) we can see the error:

## Linked PRs
- Fix PR #63683: planner: fix cannot find column error for expression index | pr=tidb-test/2613
  URL: https://github.com/pingcap/tidb/pull/63683
  State: closed
  Merged At: 2025-09-25T04:48:01Z
  Changed Files Count: 12
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_eliminate_projection_test.go
  - pkg/planner/core/operator/logicalop/logical_aggregation.go
  - pkg/planner/core/operator/logicalop/logical_cte.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/operator/logicalop/logical_projection.go
  - pkg/planner/core/operator/logicalop/logical_selection.go
  - pkg/planner/core/operator/logicalop/logical_sort.go
  - pkg/planner/core/operator/logicalop/logical_top_n.go
  - pkg/planner/core/operator/logicalop/logical_window.go
  - pkg/planner/core/rule/util/misc.go
  - pkg/planner/core/rule_eliminate_projection.go
  PR Summary: What problem does this PR solve? Problem Summary: Investigation: Why got "cannot find column error": proj_2 need , but HashJoin didn't output this column. Why this happens:
- Fix PR #64778: planner: fix cannot find column error for expression index (#63683) | tidb-test=release-8.5
  URL: https://github.com/pingcap/tidb/pull/64778
  State: closed
  Merged At: 2025-12-12T10:05:32Z
  Changed Files Count: 12
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_eliminate_projection_test.go
  - pkg/planner/core/operator/logicalop/logical_aggregation.go
  - pkg/planner/core/operator/logicalop/logical_cte.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/operator/logicalop/logical_projection.go
  - pkg/planner/core/operator/logicalop/logical_selection.go
  - pkg/planner/core/operator/logicalop/logical_sort.go
  - pkg/planner/core/operator/logicalop/logical_top_n.go
  - pkg/planner/core/operator/logicalop/logical_window.go
  - pkg/planner/core/rule/util/misc.go
  - pkg/planner/core/rule_eliminate_projection.go
  PR Summary: This is an automated cherry-pick of #63683 What problem does this PR solve? Problem Summary: Investigation: Why got "cannot find column error": proj_2 need , but HashJoin didn't output this column.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
