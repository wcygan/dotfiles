# Issue #63492: Hash aggregation may not be pushed down to TiKV during `ADMIN CHECK TABLE`

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63492
- Status: closed
- Type: type/bug
- Created At: 2025-09-12T09:19:44Z
- Closed At: 2025-10-11T15:41:46Z
- Labels: affects-7.5, affects-8.1, affects-8.5, component/ddl, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Hash aggregation may not be pushed down to TiKV during

## Linked PRs
- Fix PR #63665: executor: force pushdown aggregate to TiKV inside `admin check table` 
  URL: https://github.com/pingcap/tidb/pull/63665
  State: closed
  Merged At: 2025-10-11T15:41:45Z
  Changed Files Count: 4
  Main Modules: pkg/ddl, pkg/executor, pkg/server, pkg/session
  Sample Changed Files:
  - pkg/ddl/tests/partition/multi_domain_test.go
  - pkg/executor/check_table_index.go
  - pkg/server/tests/commontest/tidb_test.go
  - pkg/sessionctx/variable/session.go
  PR Summary: What problem does this PR solve? Problem Summary: The aggregate may not push down to TiKV What changed and how does it work? Force pushdown aggregate to TiKV
- Fix PR #64045: executor: force pushdown aggregate to TiKV inside `admin check table`  (#63665)
  URL: https://github.com/pingcap/tidb/pull/64045
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/ddl, pkg/executor, pkg/server, pkg/session
  Sample Changed Files:
  - pkg/ddl/tests/partition/multi_domain_test.go
  - pkg/executor/check_table_index.go
  - pkg/server/tests/commontest/tidb_test.go
  - pkg/sessionctx/variable/session.go
  PR Summary: This is an automated cherry-pick of #63665 What problem does this PR solve? Problem Summary: The aggregate may not push down to TiKV What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
