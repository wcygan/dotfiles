# Issue #63369: TiFlash query result materialization can't take effect after setting sql_mode by set_var

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63369
- Status: closed
- Type: type/bug
- Created At: 2025-09-04T06:39:18Z
- Closed At: 2025-09-16T07:54:35Z
- Labels: affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The [sql_mode check]() for result materialization occurs before [set_var action](), it cannot take effect.

## Linked PRs
- Fix PR #63380: planner: fix `set_var` not working for write statements to read on TiFlash
  URL: https://github.com/pingcap/tidb/pull/63380
  State: closed
  Merged At: 2025-09-15T15:34:31Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/integration_test.go
  - pkg/planner/optimize.go
  PR Summary: What problem does this PR solve? Problem Summary: See has fixed this issue, but it also made other changes, making it unsuitable for cherry-picking to other release branches. This PR fixes the bug on release-8.5 and will be cherry-picked to older release branches.
- Related PR #63531: planner: fix `set_var` not working for write statements to read on TiFlash (#63380)
  URL: https://github.com/pingcap/tidb/pull/63531
  State: open
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/integration_test.go
  - pkg/planner/optimize.go
  PR Summary: This is an automated cherry-pick of #63380 What problem does this PR solve? Problem Summary: See has fixed this issue, but it also made other changes, making it unsuitable for cherry-picking to other release branches.
- Related PR #63532: planner: fix `set_var` not working for write statements to read on TiFlash (#63380)
  URL: https://github.com/pingcap/tidb/pull/63532
  State: open
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/integration_test.go
  - pkg/planner/optimize.go
  PR Summary: This is an automated cherry-pick of #63380 What problem does this PR solve? Problem Summary: See has fixed this issue, but it also made other changes, making it unsuitable for cherry-picking to other release branches.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
