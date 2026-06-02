# Issue #59427: comments style optimizer hints can't work for point get plan sometimes

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59427
- Status: closed
- Type: type/bug
- Created At: 2025-02-11T15:44:12Z
- Closed At: 2025-04-15T11:20:24Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- One of the hints is ineffective.

## Linked PRs
- Fix PR #60516: planner: add comments style hints check for the fast path
  URL: https://github.com/pingcap/tidb/pull/60516
  State: closed
  Merged At: 2025-04-15T11:20:23Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/point_get_plan.go
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: What problem does this PR solve? Problem Summary: The comment style optimizer hint is not checked in the fast path. It should not cause any actual performance problems, but the user just can't enforce another index. Previously, we added a check for the  syntax hint in #23666. But checks for the comment style hint are missing. What changed and how does it work?
- Fix PR #60585: planner: add comments style hints check for the fast path (#60516)
  URL: https://github.com/pingcap/tidb/pull/60585
  State: closed
  Merged At: 2025-04-15T19:50:32Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/point_get_plan.go
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: This is an automated cherry-pick of #60516 What problem does this PR solve? Problem Summary: The comment style optimizer hint is not checked in the fast path. It should not cause any actual performance problems, but the user just can't enforce another index. Previously, we added a check for the  syntax hint in #23666. But checks for the comment style hint are missing.
- Related PR #63230: parse: cp distribution table feat to release-8.5 
  URL: https://github.com/pingcap/tidb/pull/63230
  State: closed
  Merged At: 2025-09-05T22:21:15Z
  Changed Files Count: 9
  Main Modules: pkg/parser, pkg/planner/core
  Sample Changed Files:
  - pkg/parser/ast/dml.go
  - pkg/parser/ast/misc.go
  - pkg/parser/keywords.go
  - pkg/parser/keywords_test.go
  - pkg/parser/misc.go
  - pkg/parser/parser.go
  - pkg/parser/parser.y
  - pkg/parser/parser_test.go
  - pkg/planner/core/planbuilder.go
  PR Summary: What problem does this PR solve? related commit: 1. 2. 3.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
