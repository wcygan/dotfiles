Set up test-driven development workflow for $ARGUMENTS:

1. Analyze requirements and determine the project language/framework
2. Create appropriate test file based on the language:
   - **Java**: Test class with JUnit/TestNG annotations
   - **Go**: `*_test.go` file with testing package
   - **Rust**: Test module with `#[cfg(test)]`
   - **TypeScript/Deno**: `.test.ts` with Deno.test()

3. Write comprehensive tests following language conventions:
   - **Java**: `@Test` methods with descriptive names
   - **Go**: `Test*` functions with table-driven tests
   - **Rust**: `#[test]` functions with assertions
   - **TypeScript**: Deno.test() with clear descriptions

4. Verify tests fail meaningfully (Red phase)
5. Create skeleton implementation that compiles but fails tests
6. Implement minimum code to pass tests (Green phase)
7. Refactor while keeping tests passing (Refactor phase)

## Language-Specific Test Commands:

**Java (Maven/Gradle):**

```bash
# Maven
mvn test -Dtest=SpecificTest#methodName
mvn test -Dtest=SpecificTest

# Gradle
./gradlew test --tests "SpecificTest.methodName"
./gradlew test --continuous  # Watch mode
```

**Go:**

```bash
go test -run TestSpecificFunction
go test -v ./...
# Watch mode with external tool
reflex -r '\.go$' go test -v ./...
```

**Rust:**

```bash
cargo test test_name
cargo test --lib
cargo watch -x test  # With cargo-watch
```

**TypeScript/Deno:**

```bash
deno test --filter "test name"
deno test --watch
```

## Complex Feature Setup:

```bash
# Create parallel worktrees for test/implementation
git worktree add ../$PROJECT-tests-$FEATURE tests-$FEATURE
git worktree add ../$PROJECT-impl-$FEATURE impl-$FEATURE
```

## TDD Best Practices:

- Write tests before implementation
- One assertion per test when possible
- Use descriptive test names that document behavior
- Test edge cases and error conditions
- Mock external dependencies appropriately
- Keep tests fast and independent
- Follow AAA pattern: Arrange, Act, Assert

What language/framework are we using for $ARGUMENTS, and what specific behavior should we test?
