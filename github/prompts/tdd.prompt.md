Your goal is to implement a comprehensive Test-Driven Development (TDD) workflow for a specific component or feature.

Ask for the target component/feature name and expected behavior if not provided.

## Requirements

- Follow Red-Green-Refactor cycle strictly
- Generate language-appropriate test patterns
- Ensure tests fail meaningfully before implementation
- Write minimal code to pass tests
- Refactor while maintaining green tests

## Context Files

Include relevant files from your project to understand the structure and conventions. Examples:

**Build/Config Files**: Include your project's build configuration

- package.json (Node.js/TypeScript)
- Cargo.toml (Rust)
- go.mod (Go)
- pom.xml or build.gradle (Java)
- deno.json (Deno)

**Project Documentation**: Include files that describe testing conventions

- README.md
- CONTRIBUTING.md
- docs/testing.md

**Existing Test Examples**: Reference existing test files to understand patterns

- tests/ directory
- \*\_test.go files
- \*.test.ts files
- \*Test.java files
- #[cfg(test)] modules in Rust

**Source Code**: Include relevant source directories and files for context

#file:README.md

## TDD Workflow

### Step 1: Project Analysis and Language Detection

Analyze the provided context files to determine:

- **Primary language**: Based on build files and project structure
- **Testing framework**: Existing test patterns and dependencies
- **Project conventions**: Naming, organization, and testing strategies
- **Test location**: Where tests should be created (inline vs separate files)

### Step 2: Language-Specific Setup

Based on detected language, follow the appropriate pattern:

#### Rust Projects

- **Test location**: Inline (`#[cfg(test)]` modules) or `tests/` directory
- **Framework**: Built-in `cargo test` with potential `criterion` for benchmarks
- **Patterns**: Unit tests in modules, integration tests in separate files

#### Go Projects

- **Test location**: `*_test.go` files alongside source
- **Framework**: Standard library `testing` package, possibly `testify`
- **Patterns**: Table-driven tests, subtests with `t.Run()`

#### Java Projects

- **Test location**: `src/test/java/` directory
- **Framework**: JUnit 5, TestNG, or legacy JUnit 4 (check dependencies)
- **Patterns**: Class-based tests with setup/teardown methods

#### TypeScript/JavaScript Projects

- **Deno**: Built-in `Deno.test()` with `@std/assert`
- **Node.js**: Jest, Vitest, Mocha (check package.json)
- **Patterns**: Describe/it blocks or function-based tests

### Step 3: RED Phase - Write Failing Tests

Create comprehensive test files using language-specific patterns:

#### Rust Test Template

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_${component}_${expected_behavior}() {
        // Arrange
        let input = create_test_input();
        let expected = create_expected_output();

        // Act
        let actual = ${component}(input);

        // Assert
        assert_eq!(actual, expected);
    }

    #[test]
    fn test_${component}_edge_cases() {
        // Test boundary conditions and error cases
        assert!(${component}(invalid_input).is_err());
    }
}
```

#### Go Test Template

```go
func Test${Component}_${ExpectedBehavior}(t *testing.T) {
    tests := []struct {
        name     string
        input    InputType
        expected ExpectedType
        wantErr  bool
    }{
        {
            name:     "valid input",
            input:    validInput,
            expected: expectedOutput,
            wantErr:  false,
        },
        {
            name:     "invalid input",
            input:    invalidInput,
            expected: zeroValue,
            wantErr:  true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := ${component}(tt.input)

            if tt.wantErr {
                assert.Error(t, err)
                return
            }

            assert.NoError(t, err)
            assert.Equal(t, tt.expected, result)
        })
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

Execute tests using language-specific commands:

- **Rust**: `cargo test ${component} --lib`
- **Go**: `go test -v -run Test${Component}`
- **Java**: `mvn test -Dtest=${Component}Test` or `./gradlew test --tests "*${Component}Test"`
- **Deno**: `deno test --filter "${component}" --fail-fast`

Ensure tests fail with meaningful error messages, not compilation errors.

### Step 5: GREEN Phase - Minimal Implementation

Create the simplest possible implementation that makes tests pass:

1. **Create skeleton structure** that compiles
2. **Implement minimal logic** to satisfy test assertions
3. **Avoid over-engineering** - resist adding features not tested
4. **Run tests** to verify they pass

### Step 6: REFACTOR Phase - Improve Code Quality

While keeping tests green:

1. **Improve code readability** and maintainability
2. **Apply design patterns** where appropriate
3. **Optimize performance** if needed
4. **Add documentation** and comments
5. **Run tests frequently** to ensure nothing breaks

### Step 7: Watch Mode Setup (Optional)

For continuous testing, set up watch mode:

- **Rust**: `cargo install cargo-watch && cargo watch -x "test ${component} --lib"`
- **Go**: `go install github.com/cespare/reflex@latest && reflex -r '\.go$' go test -v ./...`
- **Java**: `mvn test-compile compile && mvn surefire:test -Dtest=${Component}Test` (or Gradle continuous)
- **Deno**: `deno test --watch --filter "${component}"`

## Output Format

Provide:

1. **Test file(s)** with comprehensive test cases following language conventions
2. **Minimal implementation** that passes all tests
3. **Refactored version** with improved code quality
4. **Next steps** for additional test cases or features
5. **Testing commands** specific to the detected language/framework

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

- **Rust**: Use `#[should_panic]` for error testing, consider `proptest` for property-based testing
- **Go**: Leverage table-driven tests, use build tags for integration tests
- **Java**: Use `@ParameterizedTest` for multiple inputs, consider Mockito for mocking
- **TypeScript/Deno**: Take advantage of built-in assertions, consider using test doubles for external dependencies
