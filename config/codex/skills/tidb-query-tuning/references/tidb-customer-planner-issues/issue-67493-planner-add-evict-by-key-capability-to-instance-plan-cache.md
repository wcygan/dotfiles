# Issue #67493: planner: add evict-by-key capability to instance plan cache

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67493
- Status: closed
- Type: type/enhancement
- Created At: 2026-04-01T09:21:27Z
- Closed At: 2026-04-01T11:13:15Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The current instance-level plan cache only exposes , , , and in .

## Linked PRs
- Fix PR #67495: pkg/planner, pkg/sessionctx: add delete-by-key support for instance plan cache
  URL: https://github.com/pingcap/tidb/pull/67495
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/plan_cache_instance.go
  - pkg/planner/core/plan_cache_instance_test.go
  - pkg/sessionctx/context.go
  PR Summary: What problem does this PR solve? Problem Summary: The instance plan cache only exposed , , , and , so callers had no exact-key deletion capability. When an old exact cache key was known, stale instance-cache entries could only be left to logical invalidation or background eviction instead of being reclaimed eagerly. What changed and how does it work? add  to

## Notes
- The issue is closed, but no merged PR was resolved automatically from the timeline. It may have been fixed by an internal branch, a batch PR, or manual closure.
