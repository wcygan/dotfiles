# Issue #59972: planner: selection splits the join group to two parts, forbidding join reorder to get best order

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59972
- Status: closed
- Type: type/enhancement
- Created At: 2025-03-10T03:10:02Z
- Closed At: 2026-01-22T04:18:57Z
- Labels: affects-6.5, affects-8.5, planner/cascades, planner/join-order, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- See the case below, the best join order is joining and first, but both our join-order and can't support it:

## Linked PRs
- Related PR #63522: planner: Allow leading ordered table to survive (WIP)
  URL: https://github.com/pingcap/tidb/pull/63522
  State: open
  Merged At: not merged
  Changed Files Count: 11
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/operator/physicalop/physical_index_join.go
  - pkg/planner/core/operator/physicalop/physical_topn.go
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/rule_join_reorder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #64535: planner: handle the selection between the join group
  URL: https://github.com/pingcap/tidb/pull/64535
  State: closed
  Merged At: 2026-01-22T04:18:56Z
  Changed Files Count: 6
  Main Modules: pkg/session, tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_join_reorder.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - tests/integrationtest/r/planner/core/join_reorder2.result
  - tests/integrationtest/t/planner/core/join_reorder2.test
  PR Summary: What problem does this PR solve? Problem Summary: Handle the selection between the join group. Let more join group to participate the join order phase. What changed and how does it work? The  plan node prevent the function  to get more join groups.
- Related PR #65742: planner: handle the selection between the join group (#64535)
  URL: https://github.com/pingcap/tidb/pull/65742
  State: closed
  Merged At: 2026-01-23T16:11:02Z
  Changed Files Count: 6
  Main Modules: pkg/session, tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_join_reorder.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  - tests/integrationtest/r/planner/core/join_reorder2.result
  - tests/integrationtest/t/planner/core/join_reorder2.test
  PR Summary: This is an automated cherry-pick of #64535 What problem does this PR solve? Problem Summary: Handle the selection between the join group. Let more join group to participate the join order phase. What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
