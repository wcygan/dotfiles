---
title: Skill Templates
description: Four ready-to-use SKILL.md templates for code analysis, test generation, documentation, and data processing
tags: [templates, code-analysis, test-generation, documentation, data-processing]
---

# Skill Templates

Four templates to use as starting points. Customize based on project tech stack.

---

## Code Analysis Skill Template

**SKILL.md:**
```markdown
---
name: code-quality-analyzer
description: Analyze code for security vulnerabilities, performance issues, code smells, and maintainability problems. Use when reviewing code, conducting security audits, or improving code quality. Keywords: security, vulnerability, code review, audit, performance, code smell, refactor
---

# Code Quality Analyzer

Analyzes code comprehensively across multiple quality dimensions.

## Instructions

When activated, perform the following analysis:

### 1. Security Analysis
- Input validation and sanitization
- Authentication and authorization checks
- Injection vulnerabilities (SQL, XSS, command injection)
- Sensitive data exposure
- Insecure dependencies

### 2. Performance Analysis
- Algorithmic complexity (O(n²) and worse)
- Unnecessary loops or operations
- Memory leaks or excessive allocations
- Database query optimization opportunities
- Caching opportunities

### 3. Maintainability
- Code smells (long methods, large classes, duplicate code)
- Naming conventions and clarity
- Comment quality and documentation
- SOLID principle violations
- Separation of concerns

### 4. Testing
- Test coverage gaps
- Edge cases not covered
- Flaky test patterns
- Missing error scenario tests

## Output Format

Present findings organized by severity:

**🔴 Critical Issues** (security vulnerabilities, major bugs)
**🟡 Warnings** (performance issues, maintainability concerns)
**🟢 Suggestions** (improvements, best practices)

For each issue:
- **File:Line**: `src/auth.ts:45`
- **Issue**: Clear description
- **Impact**: Why it matters
- **Fix**: Code example showing correction
```

---

## Test Generation Skill Template

**SKILL.md:**
```markdown
---
name: test-suite-generator
description: Generate comprehensive unit and integration tests with high coverage. Use when adding tests, improving test coverage, implementing TDD, or ensuring code quality. Keywords: test, testing, coverage, unit test, integration test, TDD, test-driven
---

# Test Suite Generator

Creates comprehensive test suites following TDD best practices.

## Instructions

### 1. Analyze Code Under Test
- Identify all public interfaces and functions
- Map dependencies and side effects
- List edge cases and error conditions
- Check existing test coverage

### 2. Generate Test Structure

**For Deno projects:**
```typescript
import { assertEquals, assertThrows } from "@std/assert";
import { describe, it } from "@std/testing/bdd";

describe("ComponentName", () => {
  it("should handle normal case", () => {
    // Arrange
    // Act
    // Assert
  });

  it("should handle edge case", () => {
    // Test edge case
  });

  it("should throw on invalid input", () => {
    assertThrows(() => {
      // Test error condition
    });
  });
});
```

### 3. Test Coverage Goals
- 90%+ code coverage
- All public APIs tested
- All error paths tested
- Edge cases covered
- Integration points mocked appropriately

### 4. Test Organization
- Group related tests with describe blocks
- Use table-driven tests for multiple similar cases
- One assertion concept per test
- Descriptive test names (behavior, not implementation)

## Output

Create test files following project structure:
- Adjacent to source: `component.test.ts`
- Or in `/tests/` directory matching structure

Use Write tool to create test files with complete test suite.
```

---

## Documentation Generation Skill Template

**SKILL.md:**
```markdown
---
name: documentation-generator
description: Generate comprehensive documentation including READMEs, API docs, JSDoc comments, and architecture guides. Use when documenting code, creating READMEs, or writing API documentation. Keywords: documentation, docs, README, API docs, JSDoc, comments, guide
---

# Documentation Generator

Creates clear, comprehensive documentation for code and systems.

## Instructions

### 1. Determine Documentation Type

**Code Documentation (JSDoc):**
- Function/method signatures
- Parameter descriptions with types
- Return value descriptions
- Usage examples for complex functions
- Error conditions

**README Files:**
- Purpose (1-2 sentences)
- Quick start (single command if possible)
- Key commands/usage
- Project structure (if complex)
- Keep under 50 lines total

**API Documentation:**
- Endpoint descriptions
- Request/response schemas
- Authentication requirements
- Example requests and responses
- Error codes and meanings

**Architecture Docs:**
- System overview diagram (ASCII)
- Component responsibilities
- Data flow
- Key architectural decisions

### 2. Documentation Standards

- **Clarity**: Write for developers unfamiliar with the code
- **Examples**: Include concrete usage examples
- **Conciseness**: Be thorough but not verbose
- **Format**: Use proper Markdown formatting
- **Maintenance**: Include version/date information

### 3. Project-Specific Guidelines

From CLAUDE.md:
- README max 50 lines
- Essential sections only
- Single quick-start command when possible
- No excessive emojis

## Output

Use Write or Edit tools to create/update documentation files.
```

---

## Data Processing Skill Template

**SKILL.md:**
```markdown
---
name: data-file-processor
description: Process and transform data files including JSON, CSV, YAML, and structured text. Use when working with data files, transforming formats, or extracting information. Keywords: JSON, CSV, YAML, data, parse, transform, extract
allowed-tools: Read, Write, Bash, Grep
---

# Data File Processor

Processes various data file formats with transformations and analysis.

## Instructions

### 1. Identify File Format
- JSON: Parse and validate structure
- CSV: Handle headers, delimiters, escaping
- YAML: Parse configuration files
- Text: Pattern extraction and transformation

### 2. Common Operations

**Validation:**
- Schema validation
- Format checking
- Data integrity verification

**Transformation:**
- Format conversion (JSON ↔ CSV ↔ YAML)
- Field mapping and renaming
- Data filtering and aggregation
- Normalization

**Extraction:**
- Specific field extraction
- Pattern matching
- Aggregation and statistics

### 3. Processing Approach

```bash
# Use jq for JSON
jq '.field | map(select(.status == "active"))' input.json

# Use standard tools for CSV
awk -F',' '{print $1,$3}' data.csv

# YAML processing
yq eval '.services.*.image' docker-compose.yml
```

### 4. Output Format

- Preserve data integrity
- Clear transformation logs
- Validate output format
- Provide summary statistics

## Error Handling

- Invalid format detection
- Missing field handling
- Data type mismatches
- Encoding issues
```
