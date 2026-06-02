# Issue #53652: a new table with FK will not create stats_meta by ddl event

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/53652
- Status: closed
- Type: type/bug
- Created At: 2024-05-29T09:02:05Z
- Closed At: 2024-05-29T11:27:04Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, report/customer, severity/critical, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #53654: statstics,ddl: fix FK table forgets to send CreateTable event
  URL: https://github.com/pingcap/tidb/pull/53654
  State: closed
  Merged At: 2024-05-29T11:27:03Z
  Changed Files Count: 2
  Main Modules: pkg/ddl, pkg/statistics
  Sample Changed Files:
  - pkg/ddl/table.go
  - pkg/statistics/handle/ddl/ddl_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? FK table forgets to send CreateTable event
- Fix PR #53661: statstics,ddl: fix FK table forgets to send CreateTable event (#53654)
  URL: https://github.com/pingcap/tidb/pull/53661
  State: closed
  Merged At: 2024-05-29T15:02:52Z
  Changed Files Count: 2
  Main Modules: pkg/ddl, pkg/statistics
  Sample Changed Files:
  - pkg/ddl/table.go
  - pkg/statistics/handle/ddl_test.go
  PR Summary: This is an automated cherry-pick of #53654 What problem does this PR solve? Problem Summary: What changed and how does it work? FK table forgets to send CreateTable event
- Fix PR #53662: statstics,ddl: fix FK table forgets to send CreateTable event (#53654)
  URL: https://github.com/pingcap/tidb/pull/53662
  State: closed
  Merged At: 2024-05-30T07:38:52Z
  Changed Files Count: 2
  Main Modules: pkg/ddl, pkg/statistics
  Sample Changed Files:
  - pkg/ddl/table.go
  - pkg/statistics/handle/ddl/ddl_test.go
  PR Summary: This is an automated cherry-pick of #53654 What problem does this PR solve? Problem Summary: What changed and how does it work? FK table forgets to send CreateTable event
- Fix PR #53663: statstics,ddl: fix FK table forgets to send CreateTable event (#53654)
  URL: https://github.com/pingcap/tidb/pull/53663
  State: closed
  Merged At: 2024-08-28T09:12:17Z
  Changed Files Count: 2
  Main Modules: ddl/table.go, statistics/handle
  Sample Changed Files:
  - ddl/table.go
  - statistics/handle/ddl_test.go
  PR Summary: This is an automated cherry-pick of #53654 What problem does this PR solve? Problem Summary: What changed and how does it work? FK table forgets to send CreateTable event
- Fix PR #53674: statstics,ddl: fix FK table forgets to send CreateTable event (#53654)
  URL: https://github.com/pingcap/tidb/pull/53674
  State: closed
  Merged At: 2024-05-31T08:37:23Z
  Changed Files Count: 2
  Main Modules: ddl/table.go, statistics/handle
  Sample Changed Files:
  - ddl/table.go
  - statistics/handle/ddl_test.go
  PR Summary: This is an automated cherry-pick of #53654 What problem does this PR solve? Problem Summary: What changed and how does it work? FK table forgets to send CreateTable event

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
