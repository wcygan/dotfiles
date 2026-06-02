# Issue #67904: read-only user variable is corrupted after SELECT/EXPLAIN when getvar() stays in root plan

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67904
- Status: open
- Type: type/bug
- Created At: 2026-04-20T02:26:39Z
- Labels: contribution, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- I can reproduce two forms of corruption on the same v8.5.6 playground: 1. Running  mutates  from the UUID to: After that, the following  returns  rows because the variable is already corrupted. 2. If I reset  and run the  directly without the preceding , the query returns the expected 2 matching rows, but  is still corrupted afterwards:

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
