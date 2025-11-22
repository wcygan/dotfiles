---
description: TDD workflow - write failing test, implement fix, suggest commit
---

Guide the user through a complete red-green-refactor cycle for implementing a feature or fixing a bug.

## Workflow Steps

### 1. RED - Write Failing Test

**Create a test that:**
- Reproduces the bug or defines the new feature behavior
- Fails for the right reason (not syntax errors)
- Is minimal and focused on one behavior
- Follows the project's test conventions

**Ask the user:**
- What specific behavior are we testing?
- What should the expected outcome be?
- Where should this test live?

**After writing the test:**
- Autonomously run the test to verify it fails
- Observe the failure output
- Confirm it fails with the expected error message
- Add logging/debug output if needed to understand the failure
- Ensure failure is due to missing/broken functionality, not test bugs

### 2. GREEN - Minimal Implementation

**Implement the simplest fix that makes the test pass:**
- Focus on making THIS test pass
- Avoid over-engineering or premature optimization
- Don't add features not covered by tests
- Follow existing code patterns in the project
- Add logging/tracing if needed to verify behavior

**After implementation:**
- Autonomously run the specific test to verify it passes
- Run related tests to ensure no regressions
- Observe all test output for any warnings or failures
- Add debug logging if tests behave unexpectedly
- Confirm all tests are green before proceeding

### 3. REFACTOR - Clean Up (if needed)

**Optional cleanup while maintaining green tests:**
- Remove duplication
- Improve naming
- Extract methods/functions
- Add documentation
- Clean up any debug/logging added during development
- **Rule**: Tests must stay green throughout

**After each refactor step:**
- Autonomously run tests to ensure still green
- Iterate until code quality is satisfactory

### 4. COMMIT - Suggest Atomic Change

**Pre-commit checks:**
- Run full test suite to ensure green build
- Format and lint code (if project has these commands)
- Review all changes

**Suggest semantic commit message:**
```
feat: <what feature was added>
fix: <what bug was fixed>
test: <what test coverage was added>

- Test: <describe test scenario>
- Implementation: <describe changes made>
- Closes #<issue> (if applicable)
```

**Present to user:**
"Ready to commit? Run this command:
```bash
git add <files>
git commit -m "<suggested message>"
```

Or would you like to modify the message?"

## Key Principles

- **Never suggest commit without green tests**
- **Test describes behavior, not implementation**
- **Minimal fix over clever fix**
- **One logical change per commit**
- **Test and code committed together**
- **Autonomously run and observe all test output**
- **Add debug logging when needed to understand failures**

## Output Format

For each step, clearly indicate:
- 🔴 RED - Test failing as expected
- 🟢 GREEN - Test passing, no regressions
- 🔄 REFACTOR - Code improved, tests still green
- ✅ READY - All checks passed, ready to commit
- ❌ BLOCKED - Issue found, needs fixing

Keep the user informed of progress and test results through each phase of the cycle.
