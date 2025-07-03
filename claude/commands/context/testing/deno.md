# /context-load-testing-deno

Load comprehensive documentation context for Deno testing and mocking frameworks.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Deno Testing Manual**: `https://docs.deno.com/runtime/fundamentals/testing/`
     - Focus on: Deno.test, assertions, test organization, coverage
   - **Fresh Testing Guide**: `https://fresh.deno.dev/docs/concepts/testing`
     - Focus on: component testing, route testing, island testing
   - **Standard Library Testing**: `https://jsr.io/@std/testing`
     - Focus on: assertions, mocking, test utilities
   - **Deno Testing Examples**: `https://docs.deno.com/examples/`
     - Focus on: practical testing patterns, async testing
   - **Testing Best Practices**: `https://docs.deno.com/runtime/fundamentals/testing/#best-practices`
     - Focus on: test organization, performance, debugging

3. **Key documentation sections to prioritize**:
   - Deno.test API usage
   - Assertion library features
   - Mock and stub creation
   - Component testing strategies
   - Async testing patterns
   - Coverage measurement

4. **Focus areas for this stack**:
   - Built-in testing framework
   - Fresh component testing
   - Mock creation and management
   - Async function testing
   - HTTP testing patterns
   - File system testing
   - Coverage analysis
   - Test organization

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Writing Deno native tests
- Testing Fresh applications
- Creating effective mocks
- Testing async operations
- Component testing strategies
- Measuring test coverage
- Organizing test suites
- Debugging test failures

## Usage Example

```
/context-load-testing-deno
```
