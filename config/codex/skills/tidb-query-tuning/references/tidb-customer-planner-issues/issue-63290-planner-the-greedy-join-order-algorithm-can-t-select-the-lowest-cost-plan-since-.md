# Issue #63290: planner: the greedy join order algorithm can't select the lowest-cost plan since it skips cartesian join when comparing join cost

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63290
- Status: closed
- Type: type/enhancement
- Created At: 2025-08-31T09:23:20Z
- Closed At: 2025-09-09T15:44:59Z
- Labels: plan-rewrite, planner/join-order, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- In the case above, the best join order should be , but since our current join order algorithm always use the minimal table as the leading table and skip cartesian joins when comparing join cost, it can't select the lowest cost join in this case. In this case, is the minimal table, and has no join key with , so our optimizer would use as the join order.

## Linked PRs
- Fix PR #63309: planner: allow cartesian joins in greedy join order algo to explore better join orders
  URL: https://github.com/pingcap/tidb/pull/63309
  State: closed
  Merged At: 2025-09-09T15:44:58Z
  Changed Files Count: 10
  Main Modules: pkg/planner/core, pkg/session, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/binding_plan_generation.go
  - pkg/bindinfo/binding_plan_generation_test.go
  - pkg/planner/core/casetest/BUILD.bazel
  - pkg/planner/core/casetest/integration_test.go
  - pkg/planner/core/rule_join_reorder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: allow cartesian joins in greedy join order algo to explore better join orders What changed and how does it work? In the current greedy join order algo implementation, we skip cartesian joins, which means we join tables having join keys with each others first. But this strategy might miss some optimal join orders (see #63290 as an example). This PR allows cartesian joins in the greedy join order algo, and use a  to trade off the risk.
- Related PR #65705: planner: fix join reorder correctness with conflict detection algorithm
  URL: https://github.com/pingcap/tidb/pull/65705
  State: closed
  Merged At: 2026-02-13T04:11:59Z
  Changed Files Count: 13
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/base/BUILD.bazel
  - pkg/planner/core/base/plan_base.go
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_cdc_join_reorder_test.go
  - pkg/planner/core/casetest/rule/testdata/cdc_join_reorder_suite_in.json
  - pkg/planner/core/casetest/rule/testdata/cdc_join_reorder_suite_out.json
  - pkg/planner/core/casetest/rule/testdata/cdc_join_reorder_suite_xut.json
  - pkg/planner/core/joinorder/BUILD.bazel
  - pkg/planner/core/joinorder/bitset_bench_test.go
  - pkg/planner/core/joinorder/conflict_detector.go
  - pkg/planner/core/joinorder/join_order.go
  - pkg/planner/core/rule_join_reorder.go
  PR Summary: What problem does this PR solve? Problem Summary: While TiDB's Join Reorder module has supported both INNER JOIN and OUTER JOIN for a very long time, it continues to suffer from persistent correctness issues. There issues, analyzed over the last three years, basically fall into three categories: 1. Correctness problem: 1. case-1: Lack of effective validation logic for OUTER JOIN reordering: The current detection logic for OUTER JOINs is simple (it prevents reordering the null-producing side). This leads to implementations where the semantics after reordering deviate from the original SQL.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
