# /context-load-testing-java

Load comprehensive documentation context for Java testing with JUnit and integration testing frameworks.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **JUnit 5 User Guide**: `https://junit.org/junit5/docs/current/user-guide/`
     - Focus on: annotations, assertions, parameterized tests, extensions
   - **Testcontainers Documentation**: `https://testcontainers.com/`
     - Focus on: integration testing, database testing, Docker integration
   - **Mockito Documentation**: `https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html`
     - Focus on: mocking, stubbing, verification, spy objects
   - **Spring Boot Testing**: `https://spring.io/guides/gs/testing-web/`
     - Focus on: test slices, MockMvc, TestRestTemplate
   - **Quarkus Testing Guide**: `https://quarkus.io/guides/getting-started-testing`
     - Focus on: QuarkusTest, native testing, dependency injection in tests
   - **AssertJ**: `https://assertj.github.io/doc/`
     - Focus on: fluent assertions, custom assertions, soft assertions

3. **Key documentation sections to prioritize**:
   - Modern testing annotations
   - Parameterized and dynamic tests
   - Integration testing strategies
   - Mocking and stubbing patterns
   - Test lifecycle management
   - Performance testing

4. **Focus areas for this stack**:
   - JUnit 5 advanced features
   - Testcontainers integration
   - Spring Boot test slices
   - Quarkus test annotations and extensions
   - Mock object management
   - Database testing patterns
   - REST API testing
   - Native image testing with Quarkus
   - Test data management
   - Parallel test execution

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Writing modern JUnit 5 tests
- Setting up integration testing
- Using Testcontainers effectively
- Implementing proper mocking
- Testing Spring Boot applications
- Testing Quarkus applications and native builds
- Managing test data
- Optimizing test performance
- Structuring test suites

## Usage Example

```
/context-load-testing-java
```
