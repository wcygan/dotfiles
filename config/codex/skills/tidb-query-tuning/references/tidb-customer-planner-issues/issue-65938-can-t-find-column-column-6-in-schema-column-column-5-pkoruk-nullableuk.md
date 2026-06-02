# Issue #65938: Can't find column Column#6 in schema Column: [Column#5] PKOrUK: [] NullableUK:

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65938
- Status: closed
- Type: type/bug
- Created At: 2026-01-31T09:46:53Z
- Closed At: 2026-03-27T11:44:19Z
- Labels: contribution, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Related PR #67359: planner: fix projection pushdown for double-read index lookup
  URL: https://github.com/pingcap/tidb/pull/67359
  State: closed
  Merged At: 2026-03-27T11:44:18Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/task.go
  PR Summary: What problem does this PR solve? Problem Summary: A query can fail during planning with  when an unfinished double-read path pushes a projection to the index side even though the projection expression still needs table columns. What changed and how does it work? Check whether projection expressions are fully covered by the unfinished index plan before pushing the projection into a cop task.
- Fix PR #67405: planner: fix projection pushdown for double-read index lookup (#67359)
  URL: https://github.com/pingcap/tidb/pull/67405
  State: closed
  Merged At: 2026-03-30T04:01:18Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/task.go
  PR Summary: What problem does this PR solve? Problem Summary: For double-read index lookup plans, projection pushdown could be attached to the unfinished index side even when the projected expressions still needed table columns. That could leave required table columns unavailable for the projection. What changed and how does it work? In , when attaching a physical projection to a , finish the index plan first if the unfinished index side cannot provide all projected columns, then push the projection to the table side.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
