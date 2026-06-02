# Issue #67595: Limit make optimizer under estimate the cost of IndexFullScan

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67595
- Status: closed
- Type: type/bug
- Created At: 2026-04-07T12:52:57Z
- Closed At: 2026-04-12T16:56:50Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- should use IndexJoin and use , instead of  and .   was used instead of  because  the  make optimizer under estimate the cost of  on . On master branch,  is default , so we don't have this problem on masster branch. (And if you set  as -1, this issue can reproduce on master branch again).

## Linked PRs
- Fix PR #67588: planner: tidb_opt_ordering_index_selectivity_ratio for merge join
  URL: https://github.com/pingcap/tidb/pull/67588
  State: closed
  Merged At: 2026-04-12T16:56:48Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/planner, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/testdata/binding_auto_suite_out.json
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/operator/physicalop/physical_merge_join.go
  - pkg/planner/core/operator/physicalop/physical_utils.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Extends the tidb_opt_ordering_index_selectivity_ratio (“ordering penalty”) modeling to MergeJoin by reusing a shared child-ExpectedCnt calculation, and adds a planner/cardinality test intended to validate the new cost behavior. Changes:
- Fix PR #67906: planner: tidb_opt_ordering_index_selectivity_ratio for merge join (#67588)
  URL: https://github.com/pingcap/tidb/pull/67906
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/planner, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/testdata/binding_auto_suite_out.json
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/operator/physicalop/physical_merge_join.go
  - pkg/planner/core/operator/physicalop/physical_utils.go
  PR Summary: This is an automated cherry-pick of #67588 What problem does this PR solve? Problem Summary: What changed and how does it work? Extends the tidb_opt_ordering_index_selectivity_ratio (“ordering penalty”) modeling to MergeJoin by reusing a shared child-ExpectedCnt calculation, and adds a planner/cardinality test intended to validate the new cost behavior.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
