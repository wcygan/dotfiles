# Issue #66644: planner: common handle doesn't recognize order

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66644
- Status: closed
- Type: type/bug
- Created At: 2026-03-03T00:40:40Z
- Closed At: 2026-03-05T20:45:28Z
- Labels: affects-8.5, report/customer, severity/minor, sig/planner, type/bug

## Customer-Facing Phenomenon
- Given two simple table examples - first with an int PK, and the 2nd with a column handle PK. The int PK (t1) can recognize the ordering of the PK, but the common handle (t2) does not).

## Linked PRs
- Fix PR #66645: planner: recognize order on common handle PK
  URL: https://github.com/pingcap/tidb/pull/66645
  State: closed
  Merged At: 2026-03-05T20:45:27Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_common_handle_ordering_test.go
  - pkg/planner/core/find_best_task.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? As exposed by the issue - common handle PKs were not recognized as providing order after the index columns. Integer PKs did recognize order. This PR adds that support. Previously it was 7 lines missing coverage, and now it is 8. But when it was 7 - here is claude code's response:
- Fix PR #67107: planner: recognize order on common handle PK (#66645)
  URL: https://github.com/pingcap/tidb/pull/67107
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_common_handle_ordering_test.go
  - pkg/planner/core/find_best_task.go
  PR Summary: This is an automated cherry-pick of #66645 What problem does this PR solve? Problem Summary: What changed and how does it work? As exposed by the issue - common handle PKs were not recognized as providing order after the index columns. Integer PKs did recognize order. This PR adds that support.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
