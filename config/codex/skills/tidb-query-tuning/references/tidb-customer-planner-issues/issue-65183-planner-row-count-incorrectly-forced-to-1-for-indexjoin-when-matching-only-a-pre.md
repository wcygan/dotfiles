# Issue #65183: planner: Row count incorrectly forced to 1 for IndexJoin when matching only a prefix of a composite Primary Key

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65183
- Status: closed
- Type: type/bug
- Created At: 2025-12-23T07:22:57Z
- Closed At: 2026-01-16T03:17:03Z
- Labels: report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- **Root Cause Analysis**: The investigation reveals that the optimizer incorrectly handles the row count estimation for the inner (probe) side of an IndexJoin when a Primary Key is involved. The issue is located in pkg/planner/core/exhaust_physical_plans.go within the function constructDS2TableScanTask. The code explicitly forces the row count using: RowCount: math.Min(1.0, countAfterAccess), This logic assumes that any access utilizing Primary Key columns will return at most one row. However, it fails to account for cases where the join condition only covers a prefix of a composite Primary Key. In such scenarios, the operation is actually a range scan that could involve a large number of rows. By forcing the RowCount to 1, the optimizer severely underestimates the scan cost, leading to the selection of an inefficient IndexJoin instead of a more suitable HashJoin.

## Linked PRs
- Related PR #65190: planner: fix the row count for index join use the PK in inner side
  URL: https://github.com/pingcap/tidb/pull/65190
  State: closed
  Merged At: 2026-01-16T03:17:02Z
  Changed Files Count: 8
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_xut.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_out.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/index_join_path.go
  - tests/integrationtest/r/planner/core/indexjoin.result
  - tests/integrationtest/t/planner/core/indexjoin.test
  PR Summary: What problem does this PR solve? Problem Summary: fix the row count for index join use the PK in inner side What changed and how does it work? Use the same way in the  function() which use to handle the unique index. It is very similar here. Check whether we use the full columns in the PK
- Related PR #65745: planner: fix the row count for index join use the PK in inner side (#65190)
  URL: https://github.com/pingcap/tidb/pull/65745
  State: open
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_xut.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_out.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/index_join_path.go
  - tests/integrationtest/r/planner/core/indexjoin.result
  - tests/integrationtest/t/planner/core/indexjoin.test
  PR Summary: This is an automated cherry-pick of #65190 What problem does this PR solve? Problem Summary: fix the row count for index join use the PK in inner side What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
