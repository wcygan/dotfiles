---
allowed-tools: Read, Write, Edit, Bash(fd:*), Bash(rg:*), Bash(deno:*), Bash(cargo:*), Bash(go:*), Bash(npm:*)
description: Generate comprehensive test suites for any codebase
---

## Context

- Target: $ARGUMENTS (file, directory, or function to test)
- Current directory: !`pwd`
- Existing tests: !`fd "(test|spec)\.(js|ts|rs|go|java|py)$" . | wc -l | tr -d ' '` test files
- Project type: !`fd "(package.json|Cargo.toml|go.mod|deno.json|pom.xml)" . | head -1 | xargs basename 2>/dev/null || echo "unknown"`
- Test framework: !`rg "(jest|vitest|cargo test|go test|deno test)" . | head -1 || echo "unknown"`

## Your task

Generate comprehensive tests for the specified target:

1. **Analyze Target** - Understand the code structure and functionality
2. **Determine Test Strategy** - Unit tests, integration tests, or both
3. **Generate Test Files** - Create appropriate test files with proper naming
4. **Write Test Cases** - Cover happy path, edge cases, and error conditions
5. **Add Test Utilities** - Include mocks, fixtures, and helper functions

**Test Types Generated:**

- **Unit Tests**: Individual function/method testing
- **Integration Tests**: Component interaction testing
- **Error Handling**: Exception and edge case testing
- **Mock Setup**: External dependency mocking
- **Test Data**: Fixtures and sample data

**Framework Support:**

- **Deno**: Built-in test runner with assertions
- **Rust**: Cargo test with unit and integration tests
- **Go**: Go test with table-driven tests and testify
- **Node.js**: Jest, Vitest, or detected framework
- **Java**: JUnit with Spring Boot test support

Focus on practical, maintainable tests that actually validate the code behavior.
