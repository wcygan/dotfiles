---
description: Investigate an issue by analyzing relevant code, tests, and history
---

Systematically investigate the issue the user describes by exploring the codebase, tests, and git history.

# Investigation Workflow

## Phase 1: Understand the Problem

**Gather information:**
- What is the expected behavior?
- What is the actual behavior?
- What are the exact error messages or symptoms?
- When did this start happening? (recent change or long-standing?)
- Can you reproduce it consistently?

## Phase 2: Parallel Investigation (Launch 2-3 agents)

**Agent 1: Code Analysis**
- Search for relevant source files using grep/glob
- Identify the code path involved in the issue
- Examine recent changes to those files (git log/blame)
- Look for obvious bugs (null checks, type mismatches, logic errors)

**Agent 2: Test Analysis**
- Find existing tests related to the failing functionality
- Check if tests are passing/failing
- Identify gaps in test coverage
- Look for similar test cases that work correctly

**Agent 3: Pattern Search**
- Search for similar error messages in the codebase
- Find similar issues in git history (fixed bugs)
- Look for related TODO/FIXME comments
- Check for known workarounds or related issues

## Phase 3: Synthesize Findings

**Root cause analysis:**
1. Most likely cause based on evidence
2. Supporting evidence from code/tests/history
3. Alternative hypotheses if uncertain
4. File paths and line numbers for all relevant code

**Impact assessment:**
- Which components are affected?
- Are there related issues this might cause?
- What are the failure modes?

## Phase 4: Propose Solution

**Recommendation:**
- Minimal fix to address root cause
- Code changes with file:line references
- Tests to verify the fix
- Tests to prevent regression

**Verification plan:**
- How to reproduce the issue before fix
- How to verify fix resolves it
- What existing tests should still pass

# Output Format

```
## Issue Summary
[Brief description of the problem]

## Root Cause
[Explanation of what's causing the issue]
Evidence:
- file.ext:123 - [specific code snippet]
- test_file.ext:45 - [relevant test]

## Proposed Fix
1. [Change description]
   file.ext:123
   ```
   [code change]
   ```

2. [Test addition]
   test_file.ext:67
   ```
   [test code]
   ```

## Verification Steps
1. Reproduce issue: [steps]
2. Apply fix
3. Run tests: [specific test commands]
4. Verify resolution: [expected outcome]
```

# Investigation Principles

- **Evidence-based**: Every hypothesis backed by code/logs/tests
- **Systematic**: Cover code, tests, and history in parallel
- **Minimal fix**: Smallest change that solves root cause
- **Regression prevention**: Always include test coverage
- **Clear communication**: Reference exact file:line locations

# When to Use This Command

✅ **Good for:**
- Mysterious failures or unexpected behavior
- "It worked before" regressions
- Failing tests with unclear cause
- Performance degradations
- Integration issues between components

❌ **Not for:**
- Simple syntax errors (just read the error message)
- Missing dependencies (check package manager)
- Configuration issues (check environment)
- Questions about how code works (use /explain instead)
