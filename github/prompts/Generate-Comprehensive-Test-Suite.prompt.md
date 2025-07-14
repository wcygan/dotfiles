Your goal is to generate a comprehensive test suite with intelligent framework detection and realistic test scenarios.

Ask for the target component, function, or module name if not provided.

## Analysis Process

### Step 1: Project Analysis and Framework Detection

Analyze the Java microservices project structure to determine:

- Java version and Gradle build configuration
- JUnit Jupiter testing framework and existing test patterns
- Project type: microservices with gRPC, MySQL, Kafka, Temporal integration
- Available testing tools: Testcontainers, MockK, WireMock dependencies

### Step 2: Java Microservices Testing Strategy

Based on the established tech stack, implement comprehensive testing approach:

**JUnit Jupiter Unit Tests:**

- Service layer testing with dependency injection
- Domain object testing with validation
- jOOQ repository testing with database mocks
- Temporal workflow and activity testing

**Integration Tests with Testcontainers:**

- MySQL database integration testing
- Kafka producer/consumer integration testing
- gRPC service integration testing
- End-to-end workflow testing with Temporal

**Performance and Load Tests:**

- Database query performance with jOOQ
- Kafka throughput and latency testing
- gRPC service load testing
- Temporal workflow scalability testing

### Step 3: Test Generation Strategy

Generate comprehensive tests including:

1. **Unit Tests**

   - Happy path scenarios with valid data
   - Error handling and edge cases
   - Boundary condition testing
   - Input validation tests

2. **Integration Tests**

   - gRPC service endpoint testing with protocol buffer validation
   - MySQL database interaction tests with Testcontainers
   - Kafka producer/consumer integration testing
   - Temporal workflow integration testing
   - jOOQ repository integration with real database

3. **End-to-End Tests**

   - Complete microservice workflow testing
   - Cross-service communication validation via gRPC
   - Event-driven process testing through Kafka
   - Database migration testing with Flyway

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

Create JUnit Jupiter tests that cover:

- Spring service components with dependency injection
- Domain model validation and business logic
- jOOQ repository methods with mock databases
- Kafka producer/consumer logic with embedded brokers
- Temporal workflow and activity implementations

### API Test Templates

Generate tests for:

- gRPC service endpoint validation with protocol buffers
- Request/response testing for microservice APIs
- Authentication and authorization via Spring Security
- Error status code handling in gRPC services
- Service mesh communication and timeout testing

### E2E Test Templates

Include scenarios for:

- Complete user workflows
- Cross-browser compatibility
- Mobile responsiveness
- Performance benchmarks
- Accessibility compliance

### Mock and Stub Generation

Create realistic mocks for:

- MySQL database operations with jOOQ
- External gRPC service dependencies
- Kafka message brokers and topics
- Temporal workflow clients and workers
- File system and configuration services

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

**Configuration Files:**

- `#file:build.gradle` - Gradle build configuration and dependencies
- `#file:gradle.properties` - Gradle project properties
- `#file:settings.gradle` - Multi-project Gradle settings

**Test Configuration Files (if they exist):**

- `#file:src/test/resources/application-test.yml` - Test application configuration
- `#file:testcontainers.properties` - Testcontainers configuration
- `#file:src/test/resources/logback-test.xml` - Test logging configuration

**Source Files to Test:** Include the specific Java files or directories you want to generate tests for, such as:

- Service classes: `#file:src/main/java/com/example/service/UserService.java`
- Repository classes: `#file:src/main/java/com/example/repository/UserRepository.java`
- gRPC services: `#file:src/main/java/com/example/grpc/UserGrpcService.java`
- Domain models: `#file:src/main/java/com/example/domain/User.java`
- Existing tests: `#file:src/test/java/` directories
