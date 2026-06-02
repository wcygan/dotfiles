# Issue #66623: planner: same plans with different in-list should have the same plan digests

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66623
- Status: closed
- Type: type/bug
- Created At: 2026-03-02T04:09:13Z
- Closed At: 2026-03-04T15:52:21Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- These queries and plans are the same, but the  is flooded with different plans, which significantly affect the user experience: The root cause is that they have different plan digest, we need to update our plan digest algorithm to ignore different length of in-list:

## Linked PRs
- Fix PR #66624: planner: enable tidb_ignore_inlist_plan_digest by default to improve user experience and add more test cases
  URL: https://github.com/pingcap/tidb/pull/66624
  State: closed
  Merged At: 2026-03-04T15:52:18Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/plan_test.go
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_xut.json
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/sysvar_test.go
  PR Summary: What problem does this PR solve? Problem Summary: Queries with the same plan but different IN-list lengths (e.g.,  vs ) produce different plan digests. This causes the Dashboard to show many similar plans and harms usability. What changed and how does it work? See 1. **Default value change:** Set the default of  from  to  in . When enabled, plan digests ignore IN-list length so queries that only differ in IN-list size share the same plan digest.
- Fix PR #66683: planner: enable tidb_ignore_inlist_plan_digest by default to improve user experience and add more test cases (#66624)
  URL: https://github.com/pingcap/tidb/pull/66683
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/plan_test.go
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_xut.json
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/sysvar_test.go
  PR Summary: This is an automated cherry-pick of #66624 What problem does this PR solve? Problem Summary: Queries with the same plan but different IN-list lengths (e.g.,  vs ) produce different plan digests. This causes the Dashboard to show many similar plans and harms usability. What changed and how does it work? See
- Fix PR #66698: planner: enable tidb_ignore_inlist_plan_digest by default to improve user experience and add more test cases (#66624)
  URL: https://github.com/pingcap/tidb/pull/66698
  State: closed
  Merged At: 2026-03-16T23:16:50Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/plan_test.go
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_xut.json
  - pkg/sessionctx/variable/sysvar_test.go
  - pkg/sessionctx/variable/tidb_vars.go
  PR Summary: This is an automated cherry-pick of #66624 What problem does this PR solve? Problem Summary: Queries with the same plan but different IN-list lengths (e.g.,  vs ) produce different plan digests. This causes the Dashboard to show many similar plans and harms usability. What changed and how does it work? See

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
