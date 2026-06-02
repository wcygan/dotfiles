# Issue #63370: Limit doesn't pushdown to tikv automatically

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63370
- Status: closed
- Type: type/bug
- Created At: 2025-09-04T07:04:04Z
- Closed At: 2025-09-10T16:29:20Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- limit didn't pushdown to tikv:

## Linked PRs
- Fix PR #63399: planner: limit pushdown shouldn't be affected by tidb_opt_limit_push_down_threshold | tidb-test=pr/2601
  URL: https://github.com/pingcap/tidb/pull/63399
  State: closed
  Merged At: 2025-09-10T16:29:19Z
  Changed Files Count: 12
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/physicalplantest/BUILD.bazel
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_in.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  PR Summary: What problem does this PR solve? Problem Summary: Limit pushdown shouldn’t be affected by , so at first glance this description looks a bit strange. In practice, limit pushdown should always happen since it has no side effects. Therefore,  only impacts TopN pushdown, not limit pushdown.
- Fix PR #63760: planner: limit pushdown shouldn't be affected by tidb_opt_limit_push_down_threshold | tidb-test=pr/2601 (#63399)
  URL: https://github.com/pingcap/tidb/pull/63760
  State: closed
  Merged At: not merged
  Changed Files Count: 0
  PR Summary: This is an automated cherry-pick of #63399 What problem does this PR solve? Problem Summary: Limit pushdown shouldn’t be affected by , so at first glance this description looks a bit strange. In practice, limit pushdown should always happen since it has no side effects.
- Fix PR #63761: planner: limit pushdown shouldn't be affected by tidb_opt_limit_push_down_threshold | tidb-test=pr/2601 (#63399)
  URL: https://github.com/pingcap/tidb/pull/63761
  State: open
  Merged At: not merged
  Changed Files Count: 12
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/physicalplantest/BUILD.bazel
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_in.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  PR Summary: This is an automated cherry-pick of #63399 What problem does this PR solve? Problem Summary: Limit pushdown shouldn’t be affected by , so at first glance this description looks a bit strange. In practice, limit pushdown should always happen since it has no side effects.
- Fix PR #63762: planner: limit pushdown shouldn't be affected by tidb_opt_limit_push_down_threshold | tidb-test=pr/2601 (#63399)
  URL: https://github.com/pingcap/tidb/pull/63762
  State: closed
  Merged At: 2025-09-29T08:32:16Z
  Changed Files Count: 9
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/exhaust_physical_plans.go
  - tests/integrationtest/r/executor/issues.result
  - tests/integrationtest/r/planner/core/rule_result_reorder.result
  PR Summary: This is an automated cherry-pick of #63399 What problem does this PR solve? Problem Summary: Limit pushdown shouldn’t be affected by , so at first glance this description looks a bit strange. In practice, limit pushdown should always happen since it has no side effects.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
