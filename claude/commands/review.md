Perform comprehensive code review on staged/uncommitted changes.

Steps:
1. Analyze current changes:
   - Run `git status` to see modified files
   - Run `git diff --staged` for staged changes
   - Run `git diff` for unstaged changes

2. Security Review:
   - Check for hardcoded credentials or API keys
   - Identify potential SQL injection vulnerabilities
   - Look for XSS vulnerabilities in web code
   - Verify proper input validation
   - Check for exposed sensitive data in logs

3. Code Quality:
   - Verify adherence to project coding standards
   - Check for proper error handling
   - Ensure meaningful variable/function names
   - Look for code duplication
   - Verify SOLID principles adherence

4. Test Coverage:
   - Ensure new code has corresponding tests
   - Check that tests cover edge cases
   - Verify tests are meaningful, not just coverage padding
   - Look for missing integration tests

5. Performance Review:
   - Identify O(n²) or worse algorithms
   - Check for unnecessary database queries (N+1 problems)
   - Look for blocking I/O that should be async
   - Verify efficient data structures are used

6. Documentation:
   - Ensure complex logic is commented
   - Verify API changes are documented
   - Check that README is updated if needed

Generate a review checklist with specific findings and severity levels (High/Medium/Low).