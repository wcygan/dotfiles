# Issue #64375: planner: a more fine-grained track of optimization time

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64375
- Status: closed
- Type: type/enhancement
- Created At: 2025-11-10T03:14:36Z
- Closed At: 2025-12-29T06:13:12Z
- Labels: component/observability, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- We need a more fine-grained track of optimization time which should track all steps that could spend some time: 1. time used in sync_stats_load 2. time used in Plan Cache 3. time used in physical optimization 4. time used to get TiFlash logic core number: 5. derive stats for indexes or columns (if there are a large number of indexes / columns, this could take a long time like 100+ms) 6. ...

## Linked PRs
- Fix PR #65096: planner: track more details about time spent on query optimization
  URL: https://github.com/pingcap/tidb/pull/65096
  State: closed
  Merged At: 2025-12-29T06:13:11Z
  Changed Files Count: 8
  Main Modules: pkg/session, pkg/planner/core, pkg/bindinfo, pkg/executor, pkg/planner
  Sample Changed Files:
  - pkg/bindinfo/binding.go
  - pkg/executor/adapter_test.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule/rule_collect_plan_stats.go
  - pkg/planner/optimize.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/session_test.go
  - pkg/sessionctx/variable/slow_log.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: track more details about time spent on query optimization What changed and how does it work? Track more details about time spent on query optimization: Here is an example:
- Fix PR #65445: bindinfo: collect all the matchSQLBinding's time spent
  URL: https://github.com/pingcap/tidb/pull/65445
  State: closed
  Merged At: 2026-01-06T15:55:53Z
  Changed Files Count: 1
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/binding.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? The core of MatchSQLBinding is matchSQLBinding, but matchSQLBinding itself is used in multiple places, so it's best to add the timing for MatchSQLBinding inside matchSQLBinding.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
