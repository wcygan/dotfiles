---
name: expand-tests
description: >
  Analyze existing test patterns and create comprehensive, idiomatic tests to
  expand coverage. Detects framework (Jest, Vitest, pytest, Go, Rust, JUnit),
  matches project conventions, and fills coverage gaps. Use when adding tests,
  improving coverage, expanding test suite, or writing tests for untested code.
  Keywords: test, tests, testing, coverage, unit test, integration test, expand
  tests, test coverage, write tests, add tests, test gaps
---

# Test Expansion

Analyze existing test patterns and create comprehensive, idiomatic tests for: **$ARGUMENTS**

## Workflow

### 1. Detect Test Framework and Conventions

Search for test infrastructure and capture:
- Framework (see `references/framework-templates.md` for detection table)
- Directory structure and naming patterns
- Import style, assertion library, mocking patterns
- Setup/teardown conventions

### 2. Locate Existing Tests for Target Code

Find tests via import search and name matching. Analyze:
- Which functions/methods have tests?
- What scenarios are covered (happy path, errors, edge cases)?
- What's missing?

If no tests exist, note conventions from similar files and plan a comprehensive initial suite.

### 3. Analyze Target Code

Read and understand:
- Public API surface (exports, public methods)
- Input parameters and return types
- Side effects (I/O, state mutations, external calls)
- Error conditions and edge cases
- Dependencies that need mocking

### 4. Design Test Cases

For each function/method, consider:

**Happy Path:** Typical valid inputs, expected output, normal flow

**Boundary Conditions:** Empty inputs, single element, max/min values, Unicode

**Error Cases:** Invalid types, out-of-range values, missing params, external failures

**Edge Cases:** Concurrency, timing, resource exhaustion, partial failures

Naming: `should <behavior> when <condition>`

### 5. Write Tests Idiomatically

Match the project's existing style exactly — same imports, describe/it nesting,
assertion methods, setup/teardown, and mocking approach.

See `references/framework-templates.md` for per-framework templates.

### 6. Verify Tests

Run new tests and verify they:
- Pass when code is correct
- Fail when code has the bug they're testing
- Don't create false positives
- Run quickly (mock slow dependencies)

Run full suite to confirm no conflicts with existing tests.

### 7. Report Coverage Improvement

```
## Test Coverage Expansion

### Target: <file/module>
### Existing Coverage (before)
- Tests found: <count>
- Functions covered: <list>
- Gaps identified: <list>

### New Tests Added
| Test Name | Scenario | Type |
|-----------|----------|------|

### Coverage Improvement
- New tests: <count>
- Functions now covered: <list>
- Remaining gaps: <list or "none">

### Run Command
<command to run new tests>
```

## Guidelines

**Quality over quantity:** One thing per test, independent, deterministic, fast.

**Idiomatic is critical:** New tests should look like existing tests.

**Test behavior, not implementation:** Tests should survive refactoring.

**Handle missing infrastructure:** If no tests exist, ask which framework,
set up minimal config, create foundational patterns, document how to run.

## Error Handling

- **No target specified:** Ask user to specify file/function, or suggest analyzing recent changes.
- **No framework detected:** List options for the language, ask user to choose.
- **Tests fail unexpectedly:** Investigate if test is wrong or code has bug; report findings.
