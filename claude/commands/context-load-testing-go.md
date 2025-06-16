# /context-load-testing-go

Load comprehensive documentation context for Go testing patterns and tools.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Go Testing Package**: `https://pkg.go.dev/testing`
     - Focus on: test functions, benchmarks, examples, subtests
   - **Testify Framework**: `https://github.com/stretchr/testify`
     - Focus on: assertions, mocks, suites, require vs assert
   - **Go Testing Blog**: `https://go.dev/blog/`
     - Focus on: testing best practices, advanced patterns
   - **Table-Driven Tests**: `https://go.dev/wiki/TableDrivenTests`
     - Focus on: test organization, data-driven testing
   - **GoMock**: `https://github.com/golang/mock`
     - Focus on: mock generation, interface testing

3. **Key documentation sections to prioritize**:
   - Standard testing library usage
   - Table-driven test patterns
   - Benchmark writing and analysis
   - Mock generation and usage
   - Test organization strategies
   - Coverage analysis

4. **Focus areas for this stack**:
   - Table-driven test design
   - Subtest organization
   - Benchmark optimization
   - Mock generation and usage
   - HTTP testing patterns
   - Race condition detection
   - Coverage measurement
   - Parallel test execution

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Writing idiomatic Go tests
- Implementing table-driven tests
- Creating effective benchmarks
- Using mocks appropriately
- Testing HTTP handlers
- Detecting race conditions
- Measuring test coverage
- Optimizing test performance

## Usage Example

```
/context-load-testing-go
```
