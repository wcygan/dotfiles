Your goal is to generate a comprehensive test suite with intelligent framework detection and realistic test scenarios.

Ask for the target component, function, or module name if not provided.

## Analysis Process

### Step 1: Project Analysis and Framework Detection

Analyze the project structure to determine:

- Primary programming language and testing frameworks
- Existing test patterns and coverage gaps
- Project type (web app, API, library, etc.)
- Available testing tools and dependencies

### Step 2: Multi-Language Framework Detection

Based on project files, identify the appropriate testing approach:

**JavaScript/TypeScript Projects:**

- Detect frameworks: Jest, Vitest, Mocha, Deno Test
- Check for E2E tools: Playwright, Cypress
- Analyze package.json dependencies

**Rust Projects:**

- Check Cargo.toml for test dependencies
- Look for existing test modules with `#[cfg(test)]`
- Identify web frameworks: Axum, Actix-web, Warp

**Go Projects:**

- Find `_test.go` files and testing patterns
- Check for web frameworks: Gin, Echo, Fiber
- Analyze module structure

**Python Projects:**

- Detect pytest, unittest, or other frameworks
- Check requirements.txt or pyproject.toml
- Look for existing test files

**Java Projects:**

- Analyze Maven/Gradle dependencies
- Check for JUnit, TestNG, Mockito
- Find existing test classes

### Step 3: Test Generation Strategy

Generate comprehensive tests including:

1. **Unit Tests**

   - Happy path scenarios with valid data
   - Error handling and edge cases
   - Boundary condition testing
   - Input validation tests

2. **Integration Tests**

   - API endpoint testing
   - Database interaction tests
   - Service integration testing
   - External dependency mocking

3. **End-to-End Tests**

   - User workflow testing
   - Critical path validation
   - UI interaction testing
   - Performance testing

4. **Test Data Management**
   - Realistic test data generation
   - Mock and stub implementations
   - Test fixtures and factories
   - Database seeding utilities

## Generation Requirements

- Follow existing project conventions and patterns
- Include proper error handling and edge case coverage
- Generate realistic test data using appropriate libraries
- Create comprehensive mock implementations
- Include performance and load testing scenarios
- Add proper test configuration files
- Generate CI/CD integration examples

## Test Types to Generate

### Unit Test Templates

Create tests that cover:

- Function input/output validation
- Error condition handling
- Edge cases and boundary conditions
- State management and side effects
- Asynchronous operation testing

### API Test Templates

Generate tests for:

- HTTP endpoint validation
- Request/response testing
- Authentication and authorization
- Error status code handling
- Rate limiting and timeout testing

### E2E Test Templates

Include scenarios for:

- Complete user workflows
- Cross-browser compatibility
- Mobile responsiveness
- Performance benchmarks
- Accessibility compliance

### Mock and Stub Generation

Create realistic mocks for:

- Database operations
- External API services
- File system operations
- Network requests
- Time-dependent functions

## Output Requirements

Provide:

1. **Test Files**: Complete test suites with realistic scenarios
2. **Test Configuration**: Framework-specific setup files
3. **Mock Services**: Database and external service mocks
4. **Test Data**: Generators and fixtures for realistic data
5. **CI Integration**: GitHub Actions or similar workflow files
6. **Documentation**: Test running and maintenance instructions

## Context Files

Reference the following types of files to understand the project structure:

**Configuration Files (include relevant ones):**

- `#file:package.json` - Node.js projects
- `#file:deno.json` - Deno projects
- `#file:Cargo.toml` - Rust projects
- `#file:go.mod` - Go projects
- `#file:pom.xml` or `#file:build.gradle` - Java projects
- `#file:pyproject.toml` or `#file:requirements.txt` - Python projects

**Test Configuration Files (if they exist):**

- `#file:jest.config.js` - Jest configuration
- `#file:vitest.config.ts` - Vitest configuration
- `#file:playwright.config.ts` - Playwright configuration
- `#file:cypress.config.js` - Cypress configuration

**Source Files to Test:** Include the specific files or directories you want to generate tests for, such as:

- Component files: `#file:src/components/ComponentName.tsx`
- Service files: `#file:src/services/ServiceName.ts`
- Utility functions: `#file:src/utils/utilityName.ts`
- Type definitions: `#file:src/types/TypeName.ts`
- Existing tests: `#file:tests/` or `#file:__tests__/` directories
