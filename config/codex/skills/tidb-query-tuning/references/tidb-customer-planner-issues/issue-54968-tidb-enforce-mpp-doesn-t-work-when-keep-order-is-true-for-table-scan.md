# Issue #54968: tidb_enforce_mpp doesn't work when keep order is true for table scan

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54968
- Status: open
- Type: type/bug
- Created At: 2024-07-26T11:50:46Z
- Labels: affects-6.5, affects-7.1, component/tiflash, impact/func-failure, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- tiflash still use cop

## Linked PRs
- Fix PR #61314: planner: fix the wrong plan in thh enforce_mpp
  URL: https://github.com/pingcap/tidb/pull/61314
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/tpch/tpch_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
