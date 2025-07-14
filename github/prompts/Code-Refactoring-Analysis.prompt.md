Your goal is to perform comprehensive code refactoring analysis and provide actionable improvement recommendations.

Ask for the target code files or directory if not provided.

## Analysis Approach

### Step 1: Project Context Assessment

Analyze the Java microservices project structure:

- Review Gradle build files and dependency configurations
- Assess microservices architecture patterns and component boundaries
- Evaluate existing JUnit Jupiter test coverage and quality metrics
- Identify gRPC service interfaces and Protocol Buffer definitions

### Step 2: Multi-Domain Code Analysis

Perform systematic analysis across these key areas:

#### Architectural Analysis

- Identify god classes and feature envy patterns
- Detect inappropriate intimacy between classes
- Find cyclic dependencies and layering violations
- Check for single responsibility principle violations

#### Code Duplication Detection

- Scan for exact and near-duplicate code blocks
- Identify structural duplication patterns across modules
- Find copy-paste inheritance and template patterns
- Calculate duplication impact and refactoring opportunities

#### Complexity Assessment

- Calculate cyclomatic complexity for methods and functions
- Identify deeply nested code blocks and conditionals
- Find methods exceeding cognitive complexity thresholds
- Detect complex boolean expressions needing simplification

#### Type Safety Evaluation

- Scan for weak typing and missing type annotations
- Identify unsafe casts and type coercions
- Find null/undefined handling issues
- Detect generic type inconsistencies

#### Performance Analysis

- Identify inefficient algorithms and O(n²) complexity
- Find potential memory leaks and resource management issues
- Detect database query optimization opportunities with jOOQ
- Analyze MySQL query patterns and connection pooling
- Review Kafka producer/consumer performance patterns
- Identify Temporal workflow efficiency improvements

#### Design Pattern Assessment

- Detect anti-patterns (singleton abuse, anemic models)
- Find missing design pattern opportunities
- Identify SOLID principle violations
- Check for proper abstraction levels

### Step 3: Test Quality Inspection

- Analyze JUnit Jupiter test coverage gaps and blind spots
- Find brittle tests and flaky test patterns in microservices
- Identify missing edge case coverage for gRPC services
- Detect test code smells and duplication
- Review integration test patterns for Kafka and MySQL
- Assess Temporal workflow testing strategies

### Step 4: Dependency and Security Analysis

- Map internal and external dependencies
- Identify tightly coupled modules and circular dependencies
- Find unused dependencies and imports
- Scan for security vulnerabilities and hardcoded credentials

### Step 5: Documentation Assessment

- Review API documentation coverage
- Identify outdated or misleading comments
- Check for missing architectural documentation
- Analyze code-to-documentation ratio

## Refactoring Recommendations

For each identified issue, provide:

1. **Specific refactoring technique** with clear explanation
2. **Before/after code examples** showing the improvement
3. **Effort estimation** (low/medium/high) and risk assessment
4. **Testing strategy** to validate the refactoring
5. **Implementation order** based on impact and dependencies

## Prioritization Matrix

Rank refactoring opportunities using:

- **Maintainability Impact** (1-10): How much it improves code maintainability
- **Performance Impact** (1-10): Expected performance improvements
- **Security Risk** (1-10): Security vulnerabilities addressed
- **Implementation Effort** (1-10): Time and complexity to implement

**Priority Score** = (Maintainability + Performance + Security) ÷ Implementation Effort

## Language-Specific Patterns

### Java Microservices Refactorings

- Convert anemic domain models to rich domain models
- Replace conditionals with strategy pattern
- Extract interfaces for better gRPC service abstraction
- Implement dependency injection patterns with Spring
- Optimize jOOQ query patterns and database access
- Improve Temporal workflow and activity organization
- Enhance Kafka producer/consumer error handling
- Refactor Flyway migration scripts for better maintainability

## Quality Validation

After implementing refactorings:

1. **Run comprehensive test suite** to ensure no regressions
2. **Execute static analysis tools** for the target language
3. **Verify performance benchmarks** maintain or improve metrics
4. **Check code coverage** is maintained or improved
5. **Validate architectural consistency** with project patterns

## Output Format

Provide a structured report including:

1. **Executive Summary** - Key findings and high-impact recommendations
2. **Detailed Analysis** - Comprehensive breakdown by analysis domain
3. **Prioritized Action Plan** - Ordered list of refactoring tasks
4. **Implementation Guide** - Step-by-step refactoring instructions
5. **Quality Metrics** - Before/after complexity and quality measurements

## Requirements

- Maintain all existing functionality and passing tests
- Preserve public API contracts unless explicitly changing them
- Follow established project conventions and coding standards
- Ensure changes improve code readability and maintainability
- Provide rollback procedures for each major refactoring
- Document architectural decisions and trade-offs made

Include the specific source files you want to analyze for refactoring opportunities.
