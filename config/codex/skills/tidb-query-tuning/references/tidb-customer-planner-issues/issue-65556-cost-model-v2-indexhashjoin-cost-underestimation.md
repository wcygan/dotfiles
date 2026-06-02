# Issue #65556: Cost Model v2: `IndexHashJoin` cost underestimation

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65556
- Status: open
- Type: type/bug
- Created At: 2026-01-13T09:20:03Z
- Labels: epic/cost-model, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- IndexHashJoin cost formula misses hashprobe(...) and shows hashkey(...*0*...) in .

## Linked PRs
- Related PR #65557: planner: fix indexHashJoin cost formula
  URL: https://github.com/pingcap/tidb/pull/65557
  State: open
  Merged At: not merged
  Changed Files Count: 13
  Main Modules: tests/integrationtest, pkg/bindinfo, pkg/planner/core
  Sample Changed Files:
  - pkg/bindinfo/binding_auto_test.go
  - pkg/bindinfo/testdata/binding_auto_suite_out.json
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/globalindex/index_join.result
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  - tests/integrationtest/r/planner/core/physical_plan.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  - tests/integrationtest/r/planner/core/rule_join_reorder.result
  - tests/integrationtest/r/tpch.result
  PR Summary: What problem does this PR solve? Problem Summary: Cost Model v2 underestimates : the cost formula missed probe-side hash cost and could use incorrect join key count, leading to wrong plan preference. What changed and how does it work? Fix cost model v2 for index-join family in :
- Fix PR #66786: planner: Adjust cost for semijoin and apply | tidb-test=pr/2703
  URL: https://github.com/pingcap/tidb/pull/66786
  State: closed
  Merged At: 2026-03-18T00:50:47Z
  Changed Files Count: 16
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/cascades/testdata/cascades_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/correlated/testdata/correlated_subquery_suite_out.json
  - pkg/planner/core/casetest/correlated/testdata/correlated_subquery_suite_xut.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_out.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_xut.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_out.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/operator/logicalop/logical_apply.go
  - pkg/planner/core/plan_cost_ver2.go
  - tests/integrationtest/r/planner/core/grouped_ranges_order_by.result
  - tests/integrationtest/r/topn_push_down.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Changes This PR improves planner cost modeling for semi-join operators (EXISTS/NOT EXISTS subqueries) across IndexJoin and Apply plans, particularly when ordering is involved.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
