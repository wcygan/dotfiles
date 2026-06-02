# Issue #54812: planner: NDV scaling estimation formula is too naive

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54812
- Status: closed
- Type: type/enhancement
- Created At: 2024-07-22T10:39:12Z
- Closed At: 2025-08-27T14:03:35Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Below is a concrete case:

## Linked PRs
- Fix PR #63068: planner: update the fundamental NDV scaling estimation formula 
  URL: https://github.com/pingcap/tidb/pull/63068
  State: closed
  Merged At: 2025-08-27T14:03:34Z
  Changed Files Count: 25
  Main Modules: pkg/planner/core, pkg/planner, pkg/session
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/ndv.go
  - pkg/planner/cardinality/ndv_test.go
  - pkg/planner/cascades/old/implementation_rules.go
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/indexmerge_path.go
  - pkg/planner/core/operator/logicalop/logical_selection.go
  - pkg/planner/core/operator/physicalop/physical_index_scan.go
  - pkg/planner/core/operator/physicalop/physical_indexmerge_reader.go
  - pkg/planner/core/operator/physicalop/physical_merge_join.go
  - pkg/planner/core/operator/physicalop/physical_table_scan.go
  - pkg/planner/core/operator/physicalop/tiflash_predicate_push_down.go
  - pkg/planner/core/rule_inject_extra_projection.go
  - pkg/planner/core/stats.go
  - pkg/planner/core/task.go
  - pkg/planner/core/task_base.go
  - pkg/planner/property/BUILD.bazel
  PR Summary: What problem does this PR solve? Problem Summary: planner: update the fundamental NDV scaling estimation formula What changed and how does it work? The prior formula is too aggressive and biased, we'll use this new formula based on uniform assumption. Please see more details on the comments of  function.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
