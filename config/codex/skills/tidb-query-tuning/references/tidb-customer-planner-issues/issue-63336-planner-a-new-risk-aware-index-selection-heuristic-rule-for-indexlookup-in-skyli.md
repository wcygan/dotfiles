# Issue #63336: planner: a new risk-aware index selection heuristic rule for IndexLookup in skyline pruning

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63336
- Status: open
- Type: type/enhancement
- Created At: 2025-09-02T10:44:08Z
- Labels: affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- In the case above, the optimizer is prone to select since its estimated rows is slightly smaller than . But from the perspective of risk, especially avoiding large number of cop-tasks, the plan using seems lower-risky, since it contains all columns of , which means at least after index accessing / filtering, has less rows to trigger cop-tasks.

## Linked PRs
- Fix PR #63349: planner: refactor compareCandidates logic | tidb-test=pr/2594
  URL: https://github.com/pingcap/tidb/pull/63349
  State: closed
  Merged At: 2025-09-04T15:49:12Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_xut.json
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? The following changes to the compareCandidates logic: 1. Factor out pseudo index comparison logic to simplify compareCandidates.
- Fix PR #63591: planner: refactor compareCandidates logic (#63349) | tidb-test=pr/2610
  URL: https://github.com/pingcap/tidb/pull/63591
  State: closed
  Merged At: 2025-09-23T21:09:46Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_xut.json
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/logical_plans_test.go
  - tests/integrationtest/r/imdbload.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #63349 What problem does this PR solve? Problem Summary: What changed and how does it work? The following changes to the compareCandidates logic:

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
