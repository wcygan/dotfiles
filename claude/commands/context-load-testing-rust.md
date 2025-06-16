# /context-load-testing-rust

Load comprehensive documentation context for Rust testing patterns and frameworks.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Rust Book Testing**: `https://doc.rust-lang.org/book/ch11-00-testing.html`
     - Focus on: unit tests, integration tests, documentation tests
   - **Testcontainers Rust**: `https://docs.rs/testcontainers/latest/testcontainers/`
     - Focus on: integration testing with containers, database testing
   - **Criterion Benchmarking**: `https://docs.rs/criterion/latest/criterion/`
     - Focus on: performance testing, statistical analysis
   - **PropTest**: `https://docs.rs/proptest/latest/proptest/`
     - Focus on: property-based testing, fuzzing, test generation
   - **Mockall**: `https://docs.rs/mockall/latest/mockall/`
     - Focus on: mocking, test doubles, dependency injection
   - **Tokio Testing**: `https://docs.rs/tokio/latest/tokio/test/index.html`
     - Focus on: async runtime testing, multi-threaded testing, time control

3. **Key documentation sections to prioritize**:
   - Testing organization and structure
   - Async testing patterns with Tokio
   - Multi-threaded async testing
   - Time manipulation in tests
   - Integration testing strategies
   - Performance benchmarking
   - Property-based testing
   - Mocking and test doubles

4. **Focus areas for this stack**:
   - Unit test design patterns
   - Tokio async test setup and configuration
   - Multi-threaded async testing strategies
   - Time-dependent test control (#[tokio::test])
   - Integration test setup
   - Database testing with containers
   - Performance benchmarking
   - Property-based test generation
   - Mock object creation
   - Test coverage analysis
   - CI/CD integration

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Writing comprehensive test suites
- Testing async Tokio applications effectively
- Managing concurrent and multi-threaded test scenarios
- Controlling time in async tests
- Setting up integration testing
- Implementing performance benchmarks
- Using property-based testing
- Creating effective mocks
- Analyzing test coverage
- Optimizing test performance
- Integrating with CI pipelines

## Usage Example

```
/context-load-testing-rust
```
