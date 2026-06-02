# Issue #52036: `tidb_opt_ordering_index_selectivity_threshold` should also be valid for clustered index

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52036
- Status: open
- Type: type/enhancement
- Created At: 2024-03-22T10:50:09Z
- Labels: affects-7.1, affects-7.5, affects-8.1, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- If a table has a clustered index as an option of order index, the choice between the clustered index and another index using selection condition is not controlled by the variable . It'd be better to support this case, to avoid choosing bad plan for the same case (but for clustered index) as described in

## Linked PRs
- Related PR #61506: planner: apply ordering ratio to tablerangescan | tidb-test=pr/2527
  URL: https://github.com/pingcap/tidb/pull/61506
  State: closed
  Merged At: 2025-07-26T16:49:45Z
  Changed Files Count: 22
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/cross_estimation.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/pushdown/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_xut.json
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/plan_cost_ver2.go
  - tests/integrationtest/r/access_path_selection.result
  - tests/integrationtest/r/executor/issues.result
  - tests/integrationtest/r/explain_easy.result
  - tests/integrationtest/r/explain_easy_stats.result
  - tests/integrationtest/r/planner/cascades/integration.result
  - tests/integrationtest/r/planner/core/casetest/hint/hint.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/partition/integration_partition.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_result_reorder.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Similar to other PRs that have utilized tidb_opt_ordering_index_selectivity_ratio - this PR will allow this variable to adjust the estimated rows for an ordering plan estimate for the following: table range scan - where the table range scan provides order,

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
