Your goal is to extract comprehensive domain knowledge and architectural patterns from a codebase through systematic analysis.

Ask for the target project or directory path if not provided.

## Analysis Framework

### Step 1: Project Structure Assessment

Analyze the Java microservices project foundation:

- Identify Gradle multi-project structure and build configurations
- Assess microservices architecture and service boundaries
- Evaluate existing documentation for gRPC, Kafka, and Temporal components
- Determine architectural patterns and Spring Framework usage

### Step 2: Domain Model Discovery

Extract core business entities and concepts from Java domain objects:

- Analyze Java domain classes, entities, value objects, and enums
- Extract business terminology from gRPC Protocol Buffer definitions
- Document domain entities, JPA annotations, and validation constraints
- Map business workflows implemented through Temporal activities

### Step 3: Service Architecture Analysis

Map service layers and business logic patterns in Spring-based microservices:

- Examine Spring service implementations, controllers, gRPC service handlers
- Extract service boundaries, dependency injection patterns, cross-service communication
- Document gRPC service interfaces, Kafka event handlers, Temporal workflow definitions
- Identify cross-cutting concerns like security, monitoring, and error handling

### Step 4: API & Interface Documentation

Discover all gRPC and internal service APIs:

- Analyze Protocol Buffer service definitions and generated Java classes
- Extract gRPC service contracts, streaming patterns, error handling
- Document service endpoint inventory, request/response schemas, authentication
- Map Kafka topic schemas and event-driven communication patterns

### Step 5: Data Architecture Mapping

Analyze MySQL database schemas and jOOQ data access patterns:

- Review Flyway migration files, jOOQ generated classes, and MySQL schema
- Extract database relationships, jOOQ query patterns, transaction boundaries
- Document database design, data flow through Kafka events, migration strategies
- Identify data consistency patterns and eventual consistency via event sourcing

### Step 6: Configuration & Infrastructure Discovery

Map deployment and operational patterns:

- Examine config files, environment variables, deployment manifests
- Extract deployment patterns, configuration management, operational procedures
- Document deployment guides, configuration documentation, operational runbooks
- Analyze infrastructure as code and provisioning strategies

### Step 7: Error Handling & Monitoring Analysis

Document error patterns and observability:

- Review error definitions, logging patterns, metrics, monitoring, alerting
- Extract error handling strategies, observability patterns, debugging guides
- Document error catalogs, monitoring documentation, troubleshooting guides
- Map distributed tracing and performance monitoring approaches

### Step 8: Testing & Quality Patterns

Analyze JUnit Jupiter testing strategies and quality assurance:

- Examine JUnit Jupiter test structure, Testcontainers integration, mock patterns
- Extract testing methodologies for gRPC services, Kafka consumers, database operations
- Document testing guides for microservices, Temporal workflows, integration patterns
- Review code quality tools (Checkstyle, SpotBugs), Gradle test configurations

## Documentation Generation

Create comprehensive knowledge artifacts:

### 1. Architecture Overview

- System purpose, scope, and architectural decisions
- Core architectural patterns and technology choices
- Service decomposition and integration strategies
- Quality attributes and non-functional requirements

### 2. Domain Model Documentation

- Core business entities and their relationships
- Domain services, workflows, and business rules
- Ubiquitous language and terminology
- Business process flows and state machines

### 3. API Reference Guide

- Complete endpoint inventory with schemas
- Service interface definitions and contracts
- Integration patterns and communication protocols
- Authentication and authorization patterns

### 4. Operations Guide

- Development environment setup and configuration
- Deployment strategies and CI/CD processes
- Monitoring, observability, and alerting
- Troubleshooting and maintenance procedures

### 5. Testing Strategy

- Test architecture and organization patterns
- Quality assurance processes and tools
- Test data management and fixtures
- Performance testing and benchmarking

## Output Requirements

Provide structured documentation in the following format:

1. **Executive Summary**: High-level system overview and key insights
2. **Architectural Patterns**: Recurring design patterns and conventions
3. **Domain Knowledge**: Business entities, rules, and terminology
4. **Technical Specifications**: APIs, data models, and interfaces
5. **Operational Procedures**: Deployment, monitoring, and maintenance
6. **Quality Standards**: Testing strategies and best practices
7. **Next Steps**: Actionable recommendations for knowledge utilization

## Knowledge Validation

- Cross-reference findings with actual codebase implementation
- Identify knowledge gaps requiring domain expert input
- Establish documentation maintenance and update procedures
- Integrate with existing development workflows

#file:build.gradle #file:gradle.properties #file:settings.gradle #file:README.md #file:ARCHITECTURE.md #file:docs/ #file:src/ #file:tests/ #file:config/ #file:proto/ #file:migrations/
