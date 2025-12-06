---
description: Verify that recently completed work functions correctly
---

Verify that the work just completed actually works as intended.

**Verification process:**

1. **Identify what was just done**: Review the recent changes in this conversation
   - Tests written? Run them.
   - Scripts created? Execute them.
   - Code implemented? Run relevant tests or manually verify.
   - Configuration changed? Validate the config loads/applies correctly.
   - Build files modified? Run the build.

2. **Execute appropriate verification**:
   - **Tests**: Run the specific tests that were written or modified
   - **Scripts**: Execute with sample/test inputs
   - **Functions/APIs**: Write a quick smoke test or use existing tests
   - **Configs**: Validate syntax and test loading
   - **Documentation**: Verify code examples actually work

3. **Analyze results**:

   **If successful:**
   - Confirm what was verified
   - Show relevant output/evidence
   - Note any warnings or edge cases observed

   **If failed:**
   - Show the exact error output
   - Investigate the root cause (don't guess)
   - Read relevant code/logs to understand why
   - Present analysis with:
     - What failed
     - Why it failed (root cause)
     - Specific fix needed
   - Ask user if they want the fix applied

4. **Report format**:

   ```
   ## Verification: [what was verified]
   
   **Status**: PASS / FAIL
   
   **Evidence**:
   [command run and output]
   
   **Analysis** (if failed):
   - Error: [exact error]
   - Cause: [root cause explanation]
   - Fix: [specific remediation]
   ```

**Important:**
- Actually run the code/tests - don't just review it
- Use the project's existing test runner/build system
- If no obvious way to verify, ask the user how they'd like to validate
- Be thorough: one passing test doesn't mean all edge cases work
