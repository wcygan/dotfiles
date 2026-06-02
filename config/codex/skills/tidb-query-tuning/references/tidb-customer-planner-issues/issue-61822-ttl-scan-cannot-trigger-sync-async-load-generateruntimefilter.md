# Issue #61822: TTL scan cannot trigger sync/async load/generateRuntimeFilter

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61822
- Status: closed
- Type: type/bug
- Created At: 2025-06-19T01:18:13Z
- Closed At: 2025-07-30T17:18:17Z
- Labels: affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- We previously thought that internal SQL was for system tables,and since system tables do not have statistics,we could skip the sync load.However,TTL is different because it generates SQL execution based on user tables.Therefore,we need to align its behavior with regular tables.

## Linked PRs
- Fix PR #62616: planner: TTL scan can trigger sync/async load/generateRuntimeFilter
  URL: https://github.com/pingcap/tidb/pull/62616
  State: closed
  Merged At: 2025-07-30T17:18:16Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/ttl, pkg/session
  Sample Changed Files:
  - pkg/planner/core/collect_column_stats_usage.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule_collect_plan_stats.go
  - pkg/sessionctx/variable/session.go
  - pkg/ttl/ttlworker/session.go
  - pkg/ttl/ttlworker/session_integration_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? The TTL scan is different from our other internal SQL, as it reads user tables. So, our previous approach of determining whether to perform sync load based on whether it is internal SQL has issues.
- Fix PR #62729: planner: TTL scan can trigger sync/async load/generateRuntimeFilter (#62616)
  URL: https://github.com/pingcap/tidb/pull/62729
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/ttl, pkg/session
  Sample Changed Files:
  - pkg/planner/core/collect_column_stats_usage.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/plan_stats.go
  - pkg/sessionctx/variable/session.go
  - pkg/ttl/ttlworker/session.go
  - pkg/ttl/ttlworker/session_integration_test.go
  PR Summary: This is an automated cherry-pick of #62616 What problem does this PR solve? Problem Summary: What changed and how does it work? The TTL scan is different from our other internal SQL, as it reads user tables. So, our previous approach of determining whether to perform sync load based on whether it is internal SQL has issues.
- Fix PR #62730: planner: TTL scan can trigger sync/async load/generateRuntimeFilter (#62616)
  URL: https://github.com/pingcap/tidb/pull/62730
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/ttl, pkg/session
  Sample Changed Files:
  - pkg/planner/core/collect_column_stats_usage.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule_collect_plan_stats.go
  - pkg/sessionctx/variable/session.go
  - pkg/ttl/ttlworker/session.go
  - pkg/ttl/ttlworker/session_integration_test.go
  PR Summary: This is an automated cherry-pick of #62616 What problem does this PR solve? Problem Summary: What changed and how does it work? The TTL scan is different from our other internal SQL, as it reads user tables. So, our previous approach of determining whether to perform sync load based on whether it is internal SQL has issues.
- Fix PR #62731: planner: TTL scan can trigger sync/async load (#62616)
  URL: https://github.com/pingcap/tidb/pull/62731
  State: closed
  Merged At: 2025-09-19T04:59:48Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/session, pkg/ttl
  Sample Changed Files:
  - pkg/planner/core/collect_column_stats_usage.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule_collect_plan_stats.go
  - pkg/sessionctx/variable/session.go
  - pkg/ttl/ttlworker/scan.go
  PR Summary: This is an automated cherry-pick of #62616 What problem does this PR solve? Problem Summary: What changed and how does it work? The TTL scan is different from our other internal SQL, as it reads user tables. So, our previous approach of determining whether to perform sync load based on whether it is internal SQL has issues.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
