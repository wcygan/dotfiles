# Issue #65876: planner: non-prep plan cache support "is null"

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65876
- Status: closed
- Type: type/enhancement
- Created At: 2026-01-28T09:41:21Z
- Closed At: 2026-02-11T21:46:48Z
- Labels: epic/plan-cache, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- According to [our official document]() , if a query contains predicates, it can't use non-prepared plan cache:

## Linked PRs
- Fix PR #66134: planner: Support cacheing queries with IS NULL expressions.
  URL: https://github.com/pingcap/tidb/pull/66134
  State: closed
  Merged At: 2026-02-11T21:46:47Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/plancache/plan_cache_suite_test.go
  - pkg/planner/core/casetest/plancache/plan_cacheable_checker_test.go
  - pkg/planner/core/plan_cacheable_checker.go
  PR Summary: What problem does this PR solve? Problem Summary: Non-prepared queries with IS NULL expressions cannot be cached. What changed and how does it work? Added  to the allowlist of AST node types in . Also sorted the type list alphabetically.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
