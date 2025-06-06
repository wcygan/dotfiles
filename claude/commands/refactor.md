Analyze code in $ARGUMENTS for refactoring opportunities.

Steps:

1. Read and understand the code structure in the specified file/directory
2. Identify code smells and anti-patterns:

   **Common smells:**
   - Long methods/functions (>20 lines)
   - Duplicate code blocks
   - Complex conditionals
   - Large classes/modules
   - Feature envy
   - Data clumps

   **Java-specific:**
   - Anemic domain models
   - God objects/classes
   - Excessive use of static methods
   - Overuse of inheritance
   - Primitive obsession

   **Go-specific:**
   - Empty interfaces (interface{})
   - Large structs with many methods
   - Missing error handling
   - Goroutine leaks
   - Package dependency cycles

   **Rust-specific:**
   - Overuse of Rc/RefCell
   - Unnecessary cloning
   - Missing trait implementations
   - Improper error handling
   - Excessive unwrap() usage

3. Suggest specific refactoring techniques:

   **Universal patterns:**
   - Extract Method/Function
   - Rename for clarity
   - Replace Magic Numbers with Constants

   **Java patterns:**
   - Replace Conditional with Polymorphism/Strategy
   - Extract Interface
   - Builder pattern for complex objects
   - Replace inheritance with composition
   - Introduce Parameter Object
   - Use Optional instead of null

   **Go patterns:**
   - Interface segregation
   - Table-driven tests
   - Functional options pattern
   - Embed interfaces for composition
   - Error wrapping with context

   **Rust patterns:**
   - Replace Option/Result chains with ? operator
   - Use iterators instead of loops
   - Newtype pattern for type safety
   - Builder pattern with typestate
   - From/Into trait implementations

4. Verify existing test coverage before refactoring:
   - **Java**: Check coverage with JaCoCo/Cobertura
   - **Go**: Use `go test -cover`
   - **Rust**: Use `cargo tarpaulin` or `grcov`
   - Ensure critical paths have tests
   - Add tests if coverage is insufficient

5. Apply refactoring incrementally:
   - Make one change at a time
   - Run tests after each change:
     - **Java**: `mvn test` or `gradle test`
     - **Go**: `go test ./...`
     - **Rust**: `cargo test`
   - Use IDE refactoring tools when available
   - Commit working states with clear messages

6. Document the refactoring rationale in commit messages

Prioritize refactorings by:

- Impact on readability and maintainability
- Risk assessment (use static analysis tools):
  - **Java**: SpotBugs, PMD, SonarQube
  - **Go**: golangci-lint, staticcheck
  - **Rust**: clippy warnings
- Performance improvements (measure with benchmarks)
- Business value and technical debt reduction
- Team expertise and codebase conventions

Deliverables:

- Refactored code with improved structure
- Updated tests maintaining coverage
- Performance benchmarks (if applicable)
- Documentation of changes and rationale
