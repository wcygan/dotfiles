Help debug issue: $ARGUMENTS

Steps:
1. Understand the problem:
   - Parse error messages and stack traces
   - Identify the error type and context
   - Locate the exact file and line where error occurs
   - Understand the expected vs actual behavior

2. Analyze the code path:
   - Trace execution flow leading to the error
   - Identify all variables and their states
   - Check function/method signatures and calls
   - Review recent changes that might have introduced the bug

3. Suggest debugging strategies:
   - Strategic console.log/print/debugger placement
   - Recommend breakpoint locations
   - Suggest assertions to validate assumptions
   - Propose binary search approach for large codebases

4. Identify common pitfalls:
   - Type mismatches (undefined, null, wrong type)
   - Async/await issues and race conditions
   - Off-by-one errors in loops
   - Scope and closure problems
   - Mutation of shared state

5. Create minimal reproduction:
   - Isolate the problem code
   - Remove unnecessary dependencies
   - Create simple test case that reproduces the issue
   - Document steps to reproduce

6. Propose solutions:
   - Provide specific code fixes
   - Suggest defensive programming techniques
   - Recommend validation and error handling
   - Include unit tests to prevent regression

Output format:
- Root cause analysis
- Step-by-step debugging plan
- Specific code changes needed
- Prevention strategies for similar issues