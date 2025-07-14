Your goal is to extract comprehensive domain knowledge and architectural patterns from a codebase through systematic analysis.

Ask for the target project or directory path if not provided.

## Analysis Framework

### Step 1: Project Structure Assessment

Analyze the project foundation:

- Identify primary technology stacks and build systems
- Assess codebase size and complexity
- Evaluate existing documentation completeness
- Determine architectural boundaries and scope

### Step 2: Domain Model Discovery

Extract core business entities and concepts:

- Analyze struct/class/interface definitions, enums, data transfer objects
- Extract business terminology, entity relationships, data constraints
- Document domain entities, business rules, validation logic
- Map business workflows and state transitions

### Step 3: Service Architecture Analysis

Map service layers and business logic patterns:

- Examine service implementations, controllers, handlers, repositories
- Extract service boundaries, dependency patterns, integration points
- Document service interfaces, business workflows, architectural layers
- Identify cross-cutting concerns and shared patterns

### Step 4: API & Interface Documentation

Discover all external and internal APIs:

- Analyze REST endpoints, RPC services, GraphQL schemas, OpenAPI specs
- Extract API contracts, request/response patterns, authentication flows
- Document endpoint inventory, API documentation, integration guides
- Map external dependencies and integration points

### Step 5: Data Architecture Mapping

Analyze database schemas and data flow:

- Review migration files, ORM models, SQL queries, data transformations
- Extract schema evolution, data relationships, query patterns
- Document database design, data flow diagrams, migration strategies
- Identify data consistency and synchronization patterns

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

Analyze testing strategies and quality assurance:

- Examine test structure, mock patterns, integration tests, quality gates
- Extract testing methodologies, quality standards, coverage patterns
- Document testing guides, quality documentation, best practices
- Review code review processes and static analysis configurations

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

#file:package.json #file:deno.json #file:Cargo.toml #file:go.mod #file:README.md #file:ARCHITECTURE.md #file:docs/ #file:src/ #file:tests/ #file:config/
