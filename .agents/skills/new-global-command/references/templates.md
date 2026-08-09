# Reusable Skill Templates

Use these templates as starting points when a user asks to convert a common global command idea into a skill. Adapt names, descriptions, and workflow details to the actual request.

## Code Explanation

```markdown
---
name: explain-code
description: "Explain code with clarity, covering purpose, control flow, dependencies, and edge cases. Use when the user asks how code works or wants a readable walkthrough."
---

# Explain Code

Explain the code the user specifies or currently has open.

Cover:

- Purpose: what the code does in 1-2 sentences.
- Key concepts: important patterns, algorithms, or techniques.
- Flow: step-by-step execution.
- Dependencies: external libraries or modules.
- Gotchas: non-obvious behavior or edge cases.

Use concise language, cite file paths and lines when available, and explain why the code is structured this way.
```

## Security Review

```markdown
---
name: security-review
description: "Perform a security-focused code review for common vulnerabilities. Use when the user asks for security risks, OWASP-style review, or hardening guidance."
---

# Security Review

Review the code the user specifies for security risk.

Check for:

- Injection flaws.
- Authentication and authorization issues.
- Sensitive data exposure.
- XML external entities when XML is used.
- Broken access control.
- Security misconfiguration.
- Cross-site scripting.
- Insecure deserialization.
- Vulnerable dependencies.
- Insufficient logging and monitoring.

For each finding, include severity, file and line, explanation, concrete fix, and prevention guidance. If no issues are found, state the remaining review scope and residual risk.
```

## Performance Analysis

```markdown
---
name: performance-analysis
description: "Analyze code for performance bottlenecks and optimization opportunities. Use for algorithmic complexity, memory, IO, concurrency, and profiling questions."
---

# Performance Analysis

Analyze performance characteristics of the code the user specifies.

Cover:

- Algorithmic complexity.
- Data structure choices.
- Memory use and allocations.
- IO, database, file, and network calls.
- Concurrency and contention.
- Caching opportunities.

For each finding, describe the current implementation, expected cost, suggested optimization, tradeoffs, and how to measure the improvement.
```

## Refactoring Advisor

```markdown
---
name: refactoring-advisor
description: "Suggest maintainability-focused refactors for code structure, naming, duplication, and complexity. Use when the user asks for cleanup or refactor guidance."
---

# Refactoring Advisor

Review code structure and propose practical refactors.

Look for:

- Long functions.
- Large classes or modules.
- Duplicate code.
- Deep nesting.
- Magic numbers or strings.
- Poor names.
- Tight coupling.
- Unhelpful abstractions.

For each suggestion, explain the problem, proposed change, effort, benefit, and safest verification path. Prioritize by impact and risk.
```

## Test Strategy

```markdown
---
name: test-strategy
description: "Design a testing strategy for specified code or workflows. Use for unit, integration, end-to-end, edge-case, and regression test planning."
---

# Test Strategy

Create a testing strategy for the code or workflow the user specifies.

Cover:

- Unit tests for isolated behavior.
- Integration tests for component interactions.
- End-to-end tests for complete user workflows.
- Edge cases and error cases.
- Mocking, stubbing, and fixture strategy.

Provide test case outlines with name, setup, action, assertion, and verification command.
```

## Debugging Guide

```markdown
---
name: debugging-guide
description: "Guide systematic debugging from reproduction to root cause, fix, verification, and regression prevention. Use when the user describes a bug or failing behavior."
---

# Debugging Guide

Guide the investigation from symptom to verified fix.

Follow:

1. Understand expected and actual behavior.
2. Reproduce with minimal steps.
3. Isolate the component or function.
4. Inspect code, logs, state, and recent changes.
5. Form hypotheses.
6. Test hypotheses systematically.
7. Implement the smallest fix.
8. Verify the fix.
9. Add regression coverage when appropriate.

Report root cause, fix, verification, and prevention.
```
