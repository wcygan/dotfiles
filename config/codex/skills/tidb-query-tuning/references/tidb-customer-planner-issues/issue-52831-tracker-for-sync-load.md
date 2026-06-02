# Issue #52831: Tracker for sync load 

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52831
- Status: open
- Type: type/enhancement
- Created At: 2024-04-23T04:23:42Z
- Labels: component/statistics, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- sync load has many problems in the old implementation. so we refactor it and make it better.

## Linked PRs
- Related PR #53625: docs: sync load design document
  URL: https://github.com/pingcap/tidb/pull/53625
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: docs/design
  Sample Changed Files:
  - docs/design/2024-05-28-sync-load.md
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #56471: statistics: sync load will be attempted at most 3 times
  URL: https://github.com/pingcap/tidb/pull/56471
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/syncload/stats_syncload.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
