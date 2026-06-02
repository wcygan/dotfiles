# Issue #49986: ERROR 1105 (HY000): runtime error: index out of range [0] with length 0

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/49986
- Status: closed
- Type: type/bug
- Created At: 2024-01-02T12:51:20Z
- Closed At: 2024-01-03T07:03:34Z
- Labels: affects-6.5, affects-7.1, affects-7.5, found/gs, report/community, report/customer, severity/moderate, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Related PR #50002: planner: fix agg push down rule mistake order by item inside agg function
  URL: https://github.com/pingcap/tidb/pull/50002
  State: closed
  Merged At: 2024-01-03T07:03:32Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_aggregation_push_down.go
  - tests/integrationtest/r/expression/issues.result
  - tests/integrationtest/t/expression/issues.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #50016: planner: fix agg push down rule mistake order by item inside agg function (#50002)
  URL: https://github.com/pingcap/tidb/pull/50016
  State: closed
  Merged At: 2024-01-25T10:34:51Z
  Changed Files Count: 2
  Main Modules: planner/core, statistics/integration_test.go
  Sample Changed Files:
  - planner/core/rule_aggregation_push_down.go
  - statistics/integration_test.go
  PR Summary: This is an automated cherry-pick of #50002 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #50017: planner: fix agg push down rule mistake order by item inside agg function (#50002)
  URL: https://github.com/pingcap/tidb/pull/50017
  State: closed
  Merged At: 2024-01-25T09:25:52Z
  Changed Files Count: 2
  Main Modules: planner/core, statistics/integration_test.go
  Sample Changed Files:
  - planner/core/rule_aggregation_push_down.go
  - statistics/integration_test.go
  PR Summary: This is an automated cherry-pick of #50002 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #50018: planner: fix agg push down rule mistake order by item inside agg function (#50002)
  URL: https://github.com/pingcap/tidb/pull/50018
  State: closed
  Merged At: 2024-01-26T05:24:21Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/rule_aggregation_push_down.go
  - tests/integrationtest/r/statistics/integration.result
  - tests/integrationtest/t/statistics/integration.test
  PR Summary: This is an automated cherry-pick of #50002 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
