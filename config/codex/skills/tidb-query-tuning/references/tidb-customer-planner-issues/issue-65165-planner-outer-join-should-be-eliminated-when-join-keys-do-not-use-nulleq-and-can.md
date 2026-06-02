# Issue #65165: planner: outer join should be eliminated when join keys do not use NULLEQ and can hit a nullable unique index

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65165
- Status: closed
- Type: type/enhancement
- Created At: 2025-12-22T09:27:30Z
- Closed At: 2026-02-06T04:22:22Z
- Labels: plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- We should eliminate the Join for both queries above. Although could be , it doesn't affect the final result.

## Linked PRs
- Fix PR #65843: planner: eliminate outer join on nullable unique keys under EQ
  URL: https://github.com/pingcap/tidb/pull/65843
  State: closed
  Merged At: 2026-02-06T04:22:21Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cascades/old/transformation_rules.go
  - pkg/planner/core/casetest/plan_test.go
  - pkg/planner/core/rule_join_elimination.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Outer join elimination relies on the inner side join keys guaranteeing at most one match. Previously we only considered Schema.PKOrUK and unique secondary indexes, which effectively excluded nullable unique keys (Schema.NullableUK). This missed the safe case where join keys use normal equality '=': when the inner unique key is nullable, rows with NULL do not match under '=' so the join still cannot introduce extra matches and the outer join can be removed when the parent doesn't reference inner columns.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
