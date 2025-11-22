---
description: Create new global slash commands in config/claude/commands/
---

You are helping the user create a new **global** slash command that will be available across all projects.

# Global vs Project Commands

**Global commands** (`config/claude/commands/`):
- Available in ALL projects where these dotfiles are used
- Should be project-agnostic and broadly useful
- Examples: `/explain`, `/optimize`, `/security-check`
- Stored in dotfiles repo and symlinked to `~/.claude/commands/`

**Project commands** (`.claude/commands/`):
- Only available in specific project directory
- Can reference project-specific tech stack, structure, conventions
- Examples: `/deploy`, `/run-tests`, `/db-migrate`

# Creating Global Commands

## Step 1: Gather Requirements

Ask the user:
1. **Command name**: What should it be called? (lowercase, hyphens only)
2. **Purpose**: What task does it perform?
3. **Scope**: Is it truly project-agnostic? (if not, suggest project-local command)
4. **Template**: Does it match one of the standard templates, or is it custom?

## Step 2: Draft the Command

Create the command file at: `config/claude/commands/{name}.md`

**Frontmatter requirements:**
```yaml
---
description: Brief one-line description (under 80 chars)
---
```

**Content guidelines for global commands:**
- Avoid referencing specific project structures
- Don't assume specific tech stacks (or make them conditional)
- Focus on universal development tasks
- Make output format clear
- Keep commands composable and single-purpose

## Step 3: Validate Global Appropriateness

**Good candidates for global commands:**
- Code explanation and analysis
- Generic refactoring patterns
- Security vulnerability scanning
- Performance profiling approaches
- Documentation generation (language-agnostic)
- Git workflow automation
- Debugging methodologies
- Design pattern suggestions

**Bad candidates (use project-local instead):**
- Deployment scripts (project-specific)
- Build commands (tech-stack specific)
- Database operations (schema specific)
- API testing (endpoint specific)
- Environment setup (project dependencies)

## Step 4: Create the File

Use the Write tool to create:
```
/Users/wcygan/Development/dotfiles/config/claude/commands/{command-name}.md
```

## Step 5: Test and Document

After creating:
1. Test by running `/{command-name}` in a test project
2. Verify it works across different project types
3. Consider adding to dotfiles README if it's a core command

# Standard Global Command Templates

## Template 1: Code Explanation

```markdown
---
description: Explain code with clarity, covering purpose, flow, and key concepts
---

Explain the code the user specifies or currently has open.

**Explanation structure:**
1. **Purpose**: What does this code do? (1-2 sentences)
2. **Key concepts**: Important patterns, algorithms, or techniques used
3. **Flow**: Step-by-step walkthrough of execution
4. **Dependencies**: External libraries or modules used
5. **Gotchas**: Non-obvious behavior or edge cases

**Style:**
- Use clear, concise language
- Include code snippets with annotations
- Explain *why*, not just *what*
- Assume reader has basic programming knowledge
```

## Template 2: Security Review

```markdown
---
description: Security-focused code review for common vulnerabilities
---

Perform a security review of the code the user specifies.

**Check for OWASP Top 10:**
1. Injection flaws (SQL, command, LDAP, etc.)
2. Authentication/authorization issues
3. Sensitive data exposure
4. XML external entities (XXE)
5. Broken access control
6. Security misconfiguration
7. Cross-site scripting (XSS)
8. Insecure deserialization
9. Using components with known vulnerabilities
10. Insufficient logging and monitoring

**For each finding:**
- 🔴 Critical / 🟡 Warning / 🔵 Info
- Line numbers and code snippet
- Explanation of the vulnerability
- Concrete fix with code example
- Prevention strategies

**Output:**
Prioritize by severity. If no issues found, confirm security posture.
```

## Template 3: Performance Analysis

```markdown
---
description: Analyze code for performance bottlenecks and optimization opportunities
---

Analyze performance characteristics of the code the user specifies.

**Analysis areas:**
1. **Algorithmic complexity**: Big-O analysis of key operations
2. **Data structures**: Appropriate choices for access patterns
3. **Memory usage**: Allocations, leaks, unnecessary copying
4. **I/O operations**: Database queries, file access, network calls
5. **Concurrency**: Parallelization opportunities, race conditions
6. **Caching**: Opportunities for memoization or caching

**For each finding:**
- Current implementation (code snippet)
- Performance characteristic (e.g., "O(n²) loop")
- Optimization suggestion (code example)
- Expected improvement (e.g., "O(n²) → O(n log n)")
- Trade-offs (complexity, memory, readability)

**Measurement:**
Suggest profiling approaches to validate improvements.
```

## Template 4: Refactoring Advisor

```markdown
---
description: Suggest refactoring improvements for code quality and maintainability
---

Analyze code structure and suggest refactoring improvements.

**Code smells to detect:**
- Long methods/functions (>50 lines)
- Large classes (>300 lines)
- Duplicate code
- Complex conditionals (deep nesting)
- Magic numbers/strings
- Poor naming
- Tight coupling
- Missing abstractions

**Design principles:**
- SOLID principles
- DRY (Don't Repeat Yourself)
- YAGNI (You Aren't Gonna Need It)
- Separation of concerns
- Single responsibility

**For each suggestion:**
- Code smell identified
- Why it's problematic
- Refactoring approach (with code examples)
- Estimated effort (small/medium/large)
- Benefits gained

**Prioritization:**
Order by impact vs. effort ratio.
```

## Template 5: Test Strategy

```markdown
---
description: Design comprehensive testing strategy for given code
---

Create a testing strategy for the code the user specifies.

**Test pyramid approach:**
1. **Unit tests**: Test individual functions/methods in isolation
2. **Integration tests**: Test component interactions
3. **E2E tests**: Test complete user workflows

**For each test level:**
- What to test (specific scenarios)
- How to structure tests
- Mocking/stubbing strategy
- Edge cases to cover
- Expected coverage percentage

**Test cases should include:**
- Happy path (normal operation)
- Edge cases (boundary conditions)
- Error cases (invalid input, failures)
- Concurrency (if applicable)

**Output format:**
Provide test case outlines with:
- Test name (descriptive of behavior)
- Setup/Given
- Action/When
- Assertion/Then
```

## Template 6: Debugging Guide

```markdown
---
description: Systematic debugging approach for tracking down issues
---

Guide the user through debugging the issue they describe.

**Debugging methodology:**
1. **Understand**: Clarify the problem and expected vs. actual behavior
2. **Reproduce**: Identify minimal steps to reproduce
3. **Isolate**: Narrow down to specific component/function
4. **Analyze**: Examine relevant code, logs, state
5. **Hypothesize**: Form theories about root cause
6. **Test**: Verify hypotheses systematically
7. **Fix**: Implement solution
8. **Verify**: Confirm fix resolves issue
9. **Prevent**: Add tests to prevent regression

**Investigation techniques:**
- Add logging/tracing
- Use debugger breakpoints
- Binary search (disable half the code)
- Check assumptions
- Review recent changes
- Compare with working version

**Output:**
- Root cause explanation
- Fix with code changes
- Tests to prevent recurrence
```

# Now Create the Command

Interact with the user to:
1. Understand what they want the global command to do
2. Confirm it's appropriate as a global command
3. Choose a name following conventions
4. Draft the command content
5. Create the file in `config/claude/commands/`

Remember: Global commands should be universally useful across different projects and tech stacks.
