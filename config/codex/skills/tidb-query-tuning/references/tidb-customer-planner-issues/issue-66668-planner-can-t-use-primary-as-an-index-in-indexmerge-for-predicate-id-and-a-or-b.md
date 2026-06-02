# Issue #66668: planner: can't use primary as an index in IndexMerge for predicate `id=? and (a=? or b=?)`

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66668
- Status: closed
- Type: type/enhancement
- Created At: 2026-03-04T02:53:02Z
- Closed At: 2026-03-18T07:43:13Z
- Labels: affects-8.5, plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Enhancement See the example below, we can use IndexMerge for the second plan, but can't for the first plan:

## Linked PRs
- Fix PR #66670: pkg/planner: allow primary key as IndexMerge partial path for `id=? and (a=? or b=?)`
  URL: https://github.com/pingcap/tidb/pull/66670
  State: closed
  Merged At: 2026-03-18T07:43:11Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/indexmerge_unfinished_path.go
  - tests/integrationtest/r/planner/core/indexmerge_path.result
  - tests/integrationtest/t/planner/core/indexmerge_path.test
  PR Summary: What problem does this PR solve? Problem Summary: IndexMerge cannot use the primary key as a partial path for predicates like . For example,  falls back to TableRangeScan instead of IndexMerge, while  works correctly. What changed and how does it work? In , the table path (primary key for clustered tables) was skipped whenever  returned nil. For conditions such as , each DNF branch (, ) is first handled separately, and the top-level  is merged later. Because  alone cannot build a valid range on primary key ,  failed and the table path was always skipped, so it never got the merged filters. **Fix:** Only skip the table path when  (int-handle tables). For common-handle/clustered tables,  holds the primary key index, so we keep the gradual filter collection and allow filters like  to be merge
- Fix PR #67159: pkg/planner: allow primary key as IndexMerge partial path for `id=? and (a=? or b=?)` (#66670)
  URL: https://github.com/pingcap/tidb/pull/67159
  State: closed
  Merged At: 2026-03-23T09:23:22Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/indexmerge_unfinished_path.go
  - tests/integrationtest/r/planner/core/indexmerge_path.result
  - tests/integrationtest/t/planner/core/indexmerge_path.test
  PR Summary: This is an automated cherry-pick of #66670 What problem does this PR solve? Problem Summary: IndexMerge cannot use the primary key as a partial path for predicates like . For example,  falls back to TableRangeScan instead of IndexMerge, while  works correctly. What changed and how does it work? In , the table path (primary key for clustered tables) was skipped whenever  returned nil. For conditions such as , each DNF branch (, ) is first handled separately, and the top-level  is merged later. Because  alone cannot build a valid range on primary key ,  failed and the table path was always skipped, so it never got the merged filters.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
