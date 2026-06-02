# Issue #67552: Query failed with ERROR 1105 "Unexpected missing column 12"

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67552
- Status: open
- Type: type/bug
- Created At: 2026-04-03T09:54:14Z
- Labels: report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- Intermittent failure:

## Linked PRs
- Fix PR #67692: planner: avoid ambiguous generated column substitution
  URL: https://github.com/pingcap/tidb/pull/67692
  State: open
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/expression, br/pkg, pkg/importsdk, pkg/planner/core
  Sample Changed Files:
  - br/pkg/metautil/BUILD.bazel
  - pkg/expression/column.go
  - pkg/expression/column_test.go
  - pkg/importsdk/BUILD.bazel
  - pkg/planner/core/issuetest/planner_issue_test.go
  PR Summary: What problem does this PR solve? Problem Summary: When a table has multiple expression indexes backed by different hidden generated columns but sharing the same virtual expression, generated-column substitution may bind predicates to the wrong hidden column. This can produce an invalid IndexLookUp plan and trigger errors such as  on real TiKV. What changed and how does it work? This PR makes generated-column substitution skip ambiguous virtual expressions.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
