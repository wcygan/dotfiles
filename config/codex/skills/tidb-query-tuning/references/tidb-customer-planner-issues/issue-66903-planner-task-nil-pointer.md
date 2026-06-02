# Issue #66903: planner:task nil pointer

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66903
- Status: closed
- Type: type/bug
- Created At: 2026-03-11T04:11:15Z
- Closed At: 2026-03-28T02:44:11Z
- Labels: affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #67105:  planner: fix TopN heavy-function panic when heavy item is not first
  URL: https://github.com/pingcap/tidb/pull/67105
  State: closed
  Merged At: 2026-03-28T02:44:09Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/task.go
  - pkg/planner/core/task_heavy_function_optimize_test.go
  - tests/integrationtest/r/planner/core/topn_heavy_function_optimize.result
  - tests/integrationtest/t/planner/core/topn_heavy_function_optimize.test
  PR Summary: What problem does this PR solve? Issue #67104  was closed by mistake. I have left a comment there requesting a reopen. This PR directly addresses the reported problem. The old  implementation assumes that the first item is the rewritten heavy-function distance column.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
