# Issue #52813: no_join related hints don't work in sql binding

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52813
- Status: closed
- Type: type/bug
- Created At: 2024-04-22T12:31:18Z
- Closed At: 2024-04-24T17:18:38Z
- Labels: affects-6.5, affects-7.1, affects-7.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- In addition to no_merge_join, the other no_join hints like no_hash_join, no_index_join, no_index_hash_join, no_index_merge_join also have the same issue.

## Linked PRs
- Fix PR #53433: parser: ignore schema name if WithoutSchemaNameFlag is set when restoring hints (#49587)
  URL: https://github.com/pingcap/tidb/pull/53433
  State: closed
  Merged At: 2024-05-28T06:56:58Z
  Changed Files Count: 3
  Main Modules: pkg/bindinfo, pkg/parser
  Sample Changed Files:
  - pkg/bindinfo/tests/BUILD.bazel
  - pkg/bindinfo/tests/bind_test.go
  - pkg/parser/ast/misc.go
  PR Summary: This is an automated cherry-pick of #49587 What problem does this PR solve? Problem Summary: parser: ignore schema name if WithoutSchemaNameFlag is set when restoring hints What changed and how does it work? parser: ignore schema name if WithoutSchemaNameFlag is set when restoring hints
- Fix PR #53845: parser: ignore schema name if WithoutSchemaNameFlag is set when restoring hints (#49587) (#53433)
  URL: https://github.com/pingcap/tidb/pull/53845
  State: closed
  Merged At: 2024-06-10T01:08:59Z
  Changed Files Count: 2
  Main Modules: bindinfo/bind_test.go, parser/ast
  Sample Changed Files:
  - bindinfo/bind_test.go
  - parser/ast/misc.go
  PR Summary: This is an automated cherry-pick of #53433 This is an automated cherry-pick of #49587 What problem does this PR solve? Problem Summary: parser: ignore schema name if WithoutSchemaNameFlag is set when restoring hints What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
