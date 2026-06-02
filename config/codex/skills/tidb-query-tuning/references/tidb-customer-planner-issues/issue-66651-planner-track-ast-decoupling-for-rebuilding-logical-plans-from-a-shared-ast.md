# Issue #66651: planner: track AST decoupling for rebuilding logical plans from a shared AST

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66651
- Status: closed
- Type: type/bug
- Created At: 2026-03-03T07:22:52Z
- Closed At: 2026-03-03T11:59:52Z
- Labels: component/expression, may-affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- Several planner paths pass AST-owned  objects directly into expression builders. Some of those builders keep the pointer as , and some code paths may even modify the target type during build.

## Linked PRs
- Fix PR #66652: planner: deep copy AST-owned FieldTypes when building expressions
  URL: https://github.com/pingcap/tidb/pull/66652
  State: closed
  Merged At: 2026-03-03T11:59:51Z
  Changed Files Count: 9
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/expression_rewriter.go
  - pkg/planner/core/expression_test.go
  - pkg/planner/core/operator/logicalop/logical_datasource.go
  - pkg/planner/core/operator/logicalop/logical_lock.go
  - pkg/planner/core/operator/logicalop/logical_show.go
  - pkg/planner/core/operator/physicalop/physical_lock.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/planbuilder_test.go
  PR Summary: What problem does this PR solve? Problem Summary: This PR implements step 1 of issue #66651. It also records the step 2 examination result for the remaining planner-held AST references. When the planner rebuilds logical plans directly from a shared AST, some planner paths still reuse AST-owned mutable  objects. That can make different builds share return-type state through expressions or planner-created constants. What changed and how does it work?
- Fix PR #66743: pkg/planner: build multiple logical plans from shared AST in optimize
  URL: https://github.com/pingcap/tidb/pull/66743
  State: closed
  Merged At: 2026-03-12T02:55:50Z
  Changed Files Count: 1
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/optimize.go
  PR Summary: What problem does this PR solve? Problem Summary: This PR implements step 2 of #66651. Step 1 has already been merged; this step adds the actual multi-build flow in  for rebuilding logical plans from a shared AST. What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
