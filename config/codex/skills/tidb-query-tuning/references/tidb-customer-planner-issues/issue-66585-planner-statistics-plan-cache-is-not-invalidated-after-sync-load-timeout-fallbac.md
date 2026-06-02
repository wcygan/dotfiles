# Issue #66585: planner, statistics: plan cache is not invalidated after sync-load timeout fallback when stats become fully loaded

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66585
- Status: closed
- Type: type/bug
- Created At: 2026-02-27T16:08:36Z
- Closed At: 2026-04-02T10:51:14Z
- Labels: affects-8.5, component/statistics, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The cached plan keeps being reused () after stats become fully loaded in memory, until an operation that bumps stats version (e.g. ) or manual cache flush happens.

## Linked PRs
- Fix PR #67411: planner, statistics: skip plan cache for sync-load fallback plans
  URL: https://github.com/pingcap/tidb/pull/67411
  State: closed
  Merged At: 2026-04-02T10:51:12Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/planstats/BUILD.bazel
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/rule/rule_collect_plan_stats.go
  PR Summary: What problem does this PR solve? Problem Summary: When sync-load times out and the optimizer falls back to pseudo/partial stats, TiDB can cache the plan built under that temporary degraded state. Later executions may then keep reusing the fallback-built plan even after the missing stats have been loaded. What changed and how does it work? This PR simplifies the fix by treating sync-load timeout fallback as a non-cacheable planning path.
- Fix PR #67695: planner, statistics: skip plan cache for sync-load fallback plans (#67411)
  URL: https://github.com/pingcap/tidb/pull/67695
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/planstats/BUILD.bazel
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/rule_collect_plan_stats.go
  PR Summary: This is an automated cherry-pick of #67411 What problem does this PR solve? Problem Summary: When sync-load times out and the optimizer falls back to pseudo/partial stats, TiDB can cache the plan built under that temporary degraded state. Later executions may then keep reusing the fallback-built plan even after the missing stats have been loaded. What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
