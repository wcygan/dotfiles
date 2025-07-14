# Tech Stack for VS Code Prompts

This document outlines the primary technology stack used in this development environment to provide context for AI assistants and VS Code prompts.

## Microservices Architecture

### Core Technologies

#### Programming Language

- **Java** - Primary programming language for microservices development
  - Modern Java features and best practices
  - Object-oriented and functional programming paradigms
  - Enterprise-grade application development

#### Build & Dependency Management

- **Gradle** - Build lifecycle management and dependency resolution
  - Groovy build scripts
  - Multi-project builds for microservices
  - Plugin ecosystem for various tasks
  - Dependency management and version catalogs

#### Testing Framework

- **JUnit Jupiter** - Unit testing framework
  - Modern testing annotations and assertions
  - Parameterized tests and test lifecycles
  - Integration with build tools and IDEs
  - Test-driven development (TDD) practices

#### Service Communication

- **gRPC** - High-performance RPC framework
  - Protocol Buffers for service definitions
  - Type-safe service contracts
  - Streaming capabilities (unary, server streaming, client streaming, bidirectional)
  - Cross-language compatibility
  - HTTP/2 based transport

#### Database & Data Access

- **MySQL** - Relational database management system

  - ACID transactions and data consistency
  - Performance optimization and indexing
  - Replication and clustering capabilities

- **jOOQ** - Type-safe SQL builder and data access layer

  - Code generation from database schema
  - Type-safe query construction
  - Advanced SQL features support
  - Integration with Java type system

- **Flyway** - Database migration and version control
  - Schema versioning and migration scripts
  - Automated database updates
  - Team collaboration on database changes
  - Production deployment safety

#### Workflow Orchestration

- **Temporal** - Distributed workflow orchestration platform
  - Durable workflow execution
  - Activity and workflow definitions
  - State management and persistence
  - Fault tolerance and retry mechanisms
  - Workflow versioning and updates

#### Message Queue & Event Streaming

- **Apache Kafka** - Distributed event streaming platform
  - High-throughput message publishing and consumption
  - Event sourcing and stream processing
  - Partition-based scaling
  - Producer and consumer patterns
  - Topics and event schemas

## Development Practices

### Architecture Patterns

- Microservices architecture
- Event-driven architecture
- Domain-driven design (DDD)
- Clean architecture principles
- Hexagonal architecture (Ports and Adapters)

### Code Quality

- Unit testing with JUnit Jupiter
- Integration testing strategies
- Code coverage analysis
- Static code analysis
- Code reviews and pair programming

### Data Management

- Database migrations with Flyway
- Type-safe queries with jOOQ
- Transaction management
- Database connection pooling
- Data modeling and normalization

### Service Communication

- gRPC service definitions with Protocol Buffers
- Service discovery and load balancing
- Circuit breaker patterns
- Retry and timeout strategies
- API versioning and backward compatibility

### Workflow & Event Processing

- Temporal workflow definitions
- Activity implementations
- Event-driven communication via Kafka
- Message serialization and deserialization
- Error handling and compensation

## Configuration & Deployment Considerations

When working with this stack, consider:

1. **Gradle Configuration**: Multi-project builds, dependency management, and plugin configuration
2. **gRPC Service Definitions**: Protocol Buffer schemas and service contracts
3. **Database Schema**: Flyway migration scripts and jOOQ code generation
4. **Temporal Workflows**: Workflow and activity definitions, worker configuration
5. **Kafka Integration**: Producer/consumer configuration, topic management, serialization
6. **Testing Strategy**: Unit tests, integration tests, and end-to-end testing approaches
7. **Observability**: Logging, metrics, and distributed tracing across microservices

## Common Development Tasks

- Setting up new microservices with the standard tech stack
- Writing and maintaining gRPC service definitions
- Creating database migration scripts with Flyway
- Implementing Temporal workflows and activities
- Configuring Kafka producers and consumers
- Writing comprehensive unit and integration tests
- Managing inter-service communication and dependencies
