# Issue #63353: DP Join reorder on the graph that is not totally connect may fail to execute

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63353
- Status: closed
- Type: type/bug
- Created At: 2025-09-03T07:46:55Z
- Closed At: 2025-09-22T13:40:11Z
- Labels: affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #63648: planner: fix the possble wrong plan for dp join reorder
  URL: https://github.com/pingcap/tidb/pull/63648
  State: closed
  Merged At: 2025-09-22T13:40:10Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_join_reorder_dp.go
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? When the join graph is not totally connected, we may do BFS multiple times to get the connected subgraph. During each bfs, we'll assign the node in the subgraph with an ID that is its BFS order.
- Fix PR #63669: planner: fix the possble wrong plan for dp join reorder (#63648)
  URL: https://github.com/pingcap/tidb/pull/63669
  State: closed
  Merged At: 2025-09-23T05:57:25Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_join_reorder_dp.go
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: This is an automated cherry-pick of #63648 What problem does this PR solve? Problem Summary: What changed and how does it work? When the join graph is not totally connected, we may do BFS multiple times to get the connected subgraph.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
