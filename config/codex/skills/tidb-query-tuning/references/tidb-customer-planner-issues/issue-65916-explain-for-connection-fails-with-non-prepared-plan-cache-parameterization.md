# Issue #65916: EXPLAIN FOR CONNECTION fails with non‑prepared plan cache parameterization

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65916
- Status: closed
- Type: type/bug
- Created At: 2026-01-29T13:34:26Z
- Closed At: 2026-04-21T06:24:02Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- ERROR 1815 (HY000): expression eq(test.status, ?) cannot be pushed down

## Linked PRs
- Fix PR #67835: executor: skip rebuilding explain-for-connection target plans
  URL: https://github.com/pingcap/tidb/pull/67835
  State: closed
  Merged At: 2026-04-21T06:24:01Z
  Changed Files Count: 2
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/builder.go
  - pkg/executor/explainfor_test.go
  PR Summary: What problem does this PR solve? Problem Summary: may fail for a non-prepared plan cache query because the recorded target plan still contains parameterized predicates, but the explain session no longer has the live parameter values needed to rebuild that executor.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
