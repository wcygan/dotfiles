# Issue #61093: index merge alternative picking should consider the countAfterAccess more than the allSingleIndex limitation

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61093
- Status: closed
- Type: type/enhancement
- Created At: 2025-05-13T10:25:57Z
- Closed At: 2025-06-05T10:19:42Z
- Labels: affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- phenomenon: The plan cost from the explain format verbose with index merge hint is much lower than the plan without, and while the index merge plan wasn't be picked.

## Linked PRs
- Related PR #61372: planner: fix index merge skyline pruning may be prior to choose distinct partial index rather than the low count one.
  URL: https://github.com/pingcap/tidb/pull/61372
  State: closed
  Merged At: 2025-06-05T10:19:41Z
  Changed Files Count: 12
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  - pkg/planner/core/testdata/index_merge_suite_out.json
  - tests/integrationtest/r/explain_indexmerge_stats.result
  - tests/integrationtest/r/index_merge.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexmerge_path.result
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/s.zip
  - tests/integrationtest/t/explain_indexmerge_stats.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #61562: planner: fix index merge skyline pruning may be prior to choose distinct partial index rather than the low count one. (#61372)
  URL: https://github.com/pingcap/tidb/pull/61562
  State: closed
  Merged At: 2025-06-25T09:41:21Z
  Changed Files Count: 12
  Main Modules: tests/integrationtest, pkg/planner/core, tests/realtikvtest, pkg/disttask
  Sample Changed Files:
  - pkg/disttask/framework/scheduler/scheduler_manager.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  - pkg/planner/core/testdata/index_merge_suite_out.json
  - tests/integrationtest/r/explain_indexmerge_stats.result
  - tests/integrationtest/r/index_merge.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/s.zip
  - tests/integrationtest/t/explain_indexmerge_stats.test
  - tests/realtikvtest/addindextest1/BUILD.bazel
  - tests/realtikvtest/addindextest1/disttask_test.go
  PR Summary: This is an automated cherry-pick of #61372 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
