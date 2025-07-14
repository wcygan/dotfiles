Your goal is to implement a comprehensive Test-Driven Development (TDD) workflow for a specific component or feature.

Ask for the target component/feature name and expected behavior if not provided.

## Requirements

- Follow Red-Green-Refactor cycle strictly
- Generate JUnit Jupiter test patterns for Java microservices
- Ensure tests fail meaningfully before implementation
- Write minimal Spring service code to pass tests
- Refactor while maintaining green tests

## Context Files

Include relevant files from your project to understand the structure and conventions. Examples:

**Build/Config Files**: Include your Java project's build configuration

- build.gradle (Gradle build configuration)
- gradle.properties (Gradle project properties)
- settings.gradle (Multi-project settings)

**Project Documentation**: Include files that describe testing conventions

- README.md
- CONTRIBUTING.md
- docs/testing.md

**Existing Test Examples**: Reference existing Java test files to understand patterns

- src/test/java/ directory
- \*Test.java files
- Integration test classes
- Testcontainers configurations

**Source Code**: Include relevant Java source directories and files for context

## TDD Workflow

### Step 1: Project Analysis and Language Detection

Analyze the provided context files to determine:

- **Java version**: Based on Gradle build files and project structure
- **Testing framework**: JUnit Jupiter with Spring Boot Test integration
- **Project conventions**: Package naming, Spring annotations, testing strategies
- **Test location**: Tests in `src/test/java/` with parallel package structure

### Step 2: Java Spring Boot TDD Setup

Configure Java-specific TDD environment:

- **Test location**: `src/test/java/` directory with package structure matching source
- **Framework**: JUnit Jupiter with Spring Boot Test, Testcontainers for integration
- **Patterns**: Service layer tests with dependency injection, repository tests with database

### Step 3: RED Phase - Write Failing Tests

Create comprehensive test files using JUnit Jupiter patterns:

#### Java Spring Boot Test Template

```java
package com.example.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@TestPropertySource(properties = {"spring.profiles.active=test"})
class ${ComponentName}Test {

    private ${ComponentName} ${componentName};

    @BeforeEach
    void setUp() {
        // Arrange - Initialize test dependencies
        ${componentName} = new ${ComponentName}();
    }

    @Test
    @DisplayName("Should ${expected_behavior} when ${condition}")
    void test${ComponentName}_${ExpectedBehavior}() {
        // Arrange
        var input = createTestInput();
        var expected = createExpectedOutput();

        // Act
        var actual = ${componentName}.${methodName}(input);

        // Assert
        assertEquals(expected, actual);
    }

    @Test
    @DisplayName("Should throw exception when input is invalid")
    void test${ComponentName}_ThrowsException_WhenInputInvalid() {
        // Arrange
        var invalidInput = createInvalidInput();

        // Act & Assert
        assertThrows(IllegalArgumentException.class,
            () -> ${componentName}.${methodName}(invalidInput));
    }
}
```

#### Spring Boot Integration Test Template

```java
package com.example.integration;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.MySQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
@TestPropertySource(properties = {"spring.profiles.active=test"})
class ${ComponentName}IntegrationTest {

    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }

    @Test
    @DisplayName("Should perform end-to-end ${workflow_name} successfully")
    void testEndToEndWorkflow() {
        // Arrange - Set up test data and dependencies

        // Act - Execute the workflow

        // Assert - Verify expected outcomes
    }
}
```

#### Java Test Template (JUnit 5)

```java
class ${Component}Test {

    private ${Component} ${component};

    @BeforeEach
    void setUp() {
        ${component} = new ${Component}();
    }

    @Test
    @DisplayName("Should ${expected_behavior} when ${condition}")
    void should${ExpectedBehavior}When${Condition}() {
        // Arrange
        var input = createValidInput();
        var expected = createExpectedOutput();

        // Act
        var actual = ${component}.${methodName}(input);

        // Assert
        assertEquals(expected, actual);
    }

    @ParameterizedTest
    @ValueSource(strings = {"invalid1", "invalid2", "invalid3"})
    @DisplayName("Should throw exception for invalid inputs")
    void shouldThrowExceptionForInvalidInputs(String invalidInput) {
        assertThrows(IllegalArgumentException.class, () -> {
            ${component}.${methodName}(invalidInput);
        });
    }
}
```

#### TypeScript/Deno Test Template

```typescript
import { assertEquals, assertThrows } from "@std/assert";
import { ${Component} } from "./${component}.ts";

Deno.test({
    name: "${Component} - should ${expected_behavior} when ${condition}",
    fn() {
        // Arrange
        const input = createValidInput();
        const expected = createExpectedOutput();
        const ${component} = new ${Component}();

        // Act
        const actual = ${component}.${methodName}(input);

        // Assert
        assertEquals(actual, expected);
    },
});

Deno.test({
    name: "${Component} - should handle edge cases",
    fn() {
        const ${component} = new ${Component}();

        assertThrows(
            () => ${component}.${methodName}(invalidInput),
            Error,
            "Expected error message"
        );
    },
});
```

### Step 4: Run Tests and Verify Failure

Execute tests using Gradle commands:

- **All tests**: `./gradlew test`
- **Specific test class**: `./gradlew test --tests "*${Component}Test"`
- **Specific test method**: `./gradlew test --tests "${Component}Test.test${methodName}"`
- **Integration tests**: `./gradlew integrationTest`

Ensure tests fail with meaningful error messages, not compilation errors.

### Step 5: GREEN Phase - Minimal Implementation

Create the simplest possible Spring service implementation that makes tests pass:

1. **Create Spring service skeleton** with proper annotations
2. **Implement minimal business logic** to satisfy test assertions
3. **Add dependency injection** only for tested components
4. **Run tests** to verify they pass with `./gradlew test`

### Step 6: REFACTOR Phase - Improve Code Quality

While keeping tests green:

1. **Improve code readability** and maintainability
2. **Apply design patterns** where appropriate
3. **Optimize performance** if needed
4. **Add documentation** and comments
5. **Run tests frequently** to ensure nothing breaks

### Step 7: Watch Mode Setup (Optional)

For continuous testing with Gradle:

- **Continuous build**: `./gradlew test --continuous`
- **Specific test watching**: `./gradlew test --tests "*${Component}Test" --continuous`
- **File watching**: Use IDE integration or `entr` command-line tool

## Output Format

Provide:

1. **Test file(s)** with comprehensive JUnit Jupiter test cases following Spring Boot conventions
2. **Minimal Spring service implementation** that passes all tests
3. **Refactored version** with improved code quality and Spring best practices
4. **Next steps** for additional test cases or gRPC/Kafka integration features
5. **Gradle testing commands** for continuous development

## TDD Best Practices

### Core Principles

- **One test at a time**: Focus on single behavior per test
- **Descriptive names**: Test names should describe expected behavior
- **AAA Pattern**: Arrange, Act, Assert structure
- **Fast and independent**: Tests should run quickly and independently
- **Edge cases**: Test boundary conditions and error scenarios

### Quality Guidelines

- Maintain high test coverage (aim for >90% on critical paths)
- Write tests that document intended behavior
- Keep tests simple and focused
- Use meaningful assertions with clear error messages
- Test public interfaces, not implementation details

### Language-Specific Tips

- **Java/Spring Boot**: Use `@MockBean` for Spring context mocking, leverage `@TestPropertySource` for test configuration
- **JUnit Jupiter**: Take advantage of `@DisplayName`, `@ParameterizedTest`, and lifecycle annotations
- **Integration Testing**: Use Testcontainers for database and Kafka testing in realistic environments
- **gRPC Testing**: Use gRPC testing utilities and in-process servers for service testing
- **Go**: Leverage table-driven tests, use build tags for integration tests
- **Java**: Use `@ParameterizedTest` for multiple inputs, consider Mockito for mocking
- **TypeScript/Deno**: Take advantage of built-in assertions, consider using test doubles for external dependencies
