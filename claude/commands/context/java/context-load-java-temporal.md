---
allowed-tools: WebFetch, Read, Bash(fd:*), Bash(rg:*), Bash(jq:*), Bash(gdate:*), Bash(mvn:*), Bash(gradle:*)
description: Load comprehensive Java Temporal workflow documentation with project-specific optimization
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Java projects: !`fd "(pom\.xml|build\.gradle|build\.gradle\.kts)" . | head -5 || echo "No Java projects found"`
- Temporal usage: !`rg "temporal|workflow|activity" . --type java | wc -l | tr -d ' ' || echo "0"`
- Spring Boot presence: !`rg "@SpringBootApplication|spring-boot" . --type java --type xml | wc -l | tr -d ' ' || echo "0"`
- Dependency management: !`fd "(pom\.xml|build\.gradle)" . -x rg "temporal" {} \; | head -3 || echo "No Temporal dependencies found"`
- Test files: !`fd ".*Test\.java$" . | wc -l | tr -d ' ' || echo "0"`
- Technology stack: !`fd "(deno\.json|package\.json|Cargo\.toml)" . | head -3 || echo "Java-focused project"`
- Git status: !`git status --porcelain | head -3 || echo "Not a git repository"`

## Your Task

STEP 1: Initialize context loading session

- CREATE session state file: `/tmp/java-temporal-context-$SESSION_ID.json`
- SET initial state:
  ```json
  {
    "sessionId": "$SESSION_ID",
    "phase": "discovery",
    "context_sources": [],
    "loaded_topics": [],
    "project_specific_focus": [],
    "documentation_cache": {},
    "temporal_features_detected": []
  }
  ```

STEP 2: Project analysis and documentation prioritization

- ANALYZE project structure from Context section
- DETERMINE specific Temporal features and patterns in use
- IDENTIFY documentation priorities based on project needs

Think deeply about optimal Temporal workflow documentation strategies for this specific project context.

IF Java projects with Temporal usage found:

- FOCUS on project-specific workflow patterns and activity implementations
- PRIORITIZE relevant testing strategies and deployment contexts
- INCLUDE performance optimization and monitoring contexts
  ELSE:
- LOAD foundational Temporal concepts and getting-started guides
- EMPHASIZE workflow design principles and best practices
- INCLUDE project setup and Spring Boot integration patterns

STEP 3: Strategic documentation loading with intelligent prioritization

TRY:

- EXECUTE systematic context loading from prioritized sources
- USE WebFetch tool for each documentation URL
- PROCESS and organize information by functional area
- SAVE loaded context to session state

**Core Documentation Sources (Priority-Ordered):**

FOR EACH priority source:

1. **Temporal Core Concepts**
   - URL: `https://docs.temporal.io/concepts`
   - FETCH: Core workflow concepts, task queues, signals, queries
   - FOCUS: Durable execution model, workflow lifecycle, state management
   - EXTRACT: Mental models and architectural patterns

2. **Java SDK Implementation Guide**
   - URL: `https://docs.temporal.io/dev-guide/java`
   - FETCH: Java-specific implementation patterns and best practices
   - FOCUS: Workflow definition, activity implementation, worker configuration
   - EXTRACT: Code examples and configuration patterns

3. **Java Testing Strategies**
   - URL: `https://docs.temporal.io/dev-guide/java/testing`
   - FETCH: TestWorkflowEnvironment, unit testing, integration testing
   - FOCUS: Time manipulation, mock activities, test determinism
   - EXTRACT: Testing patterns and time-skipping techniques

4. **Temporal Java Samples Repository**
   - URL: `https://github.com/temporalio/samples-java`
   - FETCH: Real-world implementation examples and patterns
   - FOCUS: Production-ready workflow implementations
   - EXTRACT: Complete example applications and integration patterns

5. **Spring Boot Integration Patterns**
   - URL: `https://docs.temporal.io/dev-guide/java/foundations#dependency-injection`
   - FETCH: Spring Boot integration and dependency injection
   - FOCUS: Application configuration, bean management, lifecycle
   - EXTRACT: Production deployment patterns

6. **Production Operations Guide**
   - URL: `https://docs.temporal.io/production-deployment`
   - FETCH: Deployment, monitoring, observability, scaling
   - FOCUS: Production readiness, metrics, alerting
   - EXTRACT: Operational best practices and troubleshooting

7. **Workflow Versioning and Migration**
   - URL: `https://docs.temporal.io/dev-guide/java/versioning`
   - FETCH: Versioning strategies, backward compatibility, migration
   - FOCUS: Production evolution, breaking changes, rollback strategies
   - EXTRACT: Versioning patterns and migration procedures

CATCH (documentation_fetch_failed):

- LOG failed sources to session state
- CONTINUE with available documentation
- PROVIDE manual context loading instructions
- SAVE fallback documentation references

STEP 4: Context organization and project-specific synthesis

- ORGANIZE loaded context by functional area:
  - Workflow design and implementation patterns
  - Activity definition and execution strategies
  - Signal and query handling mechanisms
  - Testing methodologies and time manipulation
  - Worker configuration and scaling patterns
  - Error handling and retry policies
  - Versioning and migration strategies
  - Monitoring and observability integration
  - Spring Boot integration and dependency injection
  - Production deployment and operations

Think harder about advanced Temporal workflow patterns and their applicability to the detected project structure.

- SYNTHESIZE project-specific guidance:
  - Integration with existing Java application architecture
  - Migration strategies from synchronous to workflow-based processing
  - Testing strategies for complex business processes
  - Performance considerations for high-throughput workflows
  - Security and compliance patterns for workflow data

STEP 5: Session state management and completion

- UPDATE session state with loaded context summary
- SAVE context cache: `/tmp/java-temporal-context-cache-$SESSION_ID.json`
- CREATE context summary report
- MARK completion checkpoint

FINALLY:

- ARCHIVE context session data for future reference
- PROVIDE context loading summary
- CLEAN UP temporary session files

## Context Loading Strategy

**Adaptive Loading Based on Project Type:**

CASE project_context:
WHEN "existing_temporal_workflows":

- PRIORITIZE: Advanced workflow patterns, performance optimization, versioning
- FOCUS: Production operations, monitoring, troubleshooting
- EXAMPLES: Complex workflow orchestration, high-throughput patterns

WHEN "spring_boot_integration":

- PRIORITIZE: Dependency injection, configuration management, lifecycle integration
- FOCUS: Bean configuration, application context, transaction management
- EXAMPLES: Spring-based workflow applications, configuration patterns

WHEN "new_temporal_project":

- PRIORITIZE: Getting started, basic concepts, simple workflow patterns
- FOCUS: Project setup, basic workflow implementation, testing foundations
- EXAMPLES: Simple workflows, activity implementation, basic testing

WHEN "microservices_architecture":

- PRIORITIZE: Service orchestration, distributed workflows, fault tolerance
- FOCUS: Inter-service communication, saga patterns, distributed state management
- EXAMPLES: Microservice orchestration, distributed transaction patterns

**Context Validation and Quality Assurance:**

FOR EACH loaded documentation source:

- VERIFY documentation currency and Java version compatibility
- VALIDATE code examples for compilation and execution
- CHECK for deprecated APIs and migration paths
- ENSURE security best practices are highlighted
- CONFIRM examples work with current Temporal SDK versions

## Expected Outcome

After executing this command, you will have comprehensive context on:

**Core Temporal Capabilities:**

- Workflow design patterns and implementation strategies
- Activity definition and execution models
- Signal and query handling mechanisms
- Task queue configuration and worker management
- Durable execution guarantees and fault tolerance

**Java-Specific Implementation:**

- Spring Boot integration and dependency injection patterns
- TestWorkflowEnvironment usage and testing strategies
- Java SDK configuration and optimization
- Type-safe workflow and activity definitions
- Exception handling and retry policy configuration

**Production Operations:**

- Deployment strategies and infrastructure requirements
- Monitoring, metrics, and observability setup
- Versioning and migration procedures
- Performance tuning and scaling considerations
- Security configuration and best practices

**Development Workflow:**

- Local development environment setup
- Testing strategies for workflow logic
- Debugging techniques and troubleshooting
- CI/CD integration and automated testing
- Code generation and build optimization

The context loading adapts to your specific project structure and emphasizes the most relevant Temporal documentation areas for your current Java development needs.

## Session State Management

```json
// /tmp/java-temporal-context-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "project_analysis": {
    "java_projects_found": "count",
    "temporal_usage_detected": "boolean",
    "spring_boot_integration": "boolean",
    "test_files_present": "count",
    "complexity_assessment": "simple|moderate|complex"
  },
  "documentation_strategy": {
    "prioritization_approach": "new_project|existing_workflows|spring_integration|microservices",
    "focus_areas": ["workflow_design", "testing", "production_ops"],
    "loaded_sources": [],
    "failed_sources": [],
    "fallback_strategies": []
  },
  "context_cache": {
    "core_concepts": {},
    "java_implementation": {},
    "testing_strategies": {},
    "production_operations": {},
    "spring_integration": {},
    "versioning_migration": {}
  },
  "project_recommendations": {
    "immediate_next_steps": [],
    "architectural_considerations": [],
    "testing_approach": [],
    "deployment_strategy": []
  }
}
```

**Advanced Features:**

- **Project-Specific Prioritization**: Adapts documentation loading based on detected Java project structure
- **Spring Boot Integration**: Special focus on dependency injection and application lifecycle
- **Testing Framework Integration**: Comprehensive TestWorkflowEnvironment patterns
- **Production Readiness**: Operations, monitoring, and deployment considerations
- **Extended Thinking Integration**: Deep workflow design analysis for complex business processes

## Integration Patterns

### With Existing Java Applications:

- **Spring Boot Integration**: Native dependency injection and configuration management
- **Microservices Architecture**: Workflow-based service orchestration patterns
- **Database Integration**: JPA/Hibernate compatibility and transaction management
- **Message Queue Integration**: Kafka, RabbitMQ, and event-driven workflow patterns

### Development Workflow Integration:

- **IDE Setup**: IntelliJ IDEA and VS Code configuration for Temporal development
- **Build Tools**: Maven and Gradle plugin configuration and optimization
- **Testing Framework**: JUnit 5 integration with TestWorkflowEnvironment
- **CI/CD Pipeline**: GitHub Actions and Jenkins integration patterns

### Monitoring and Observability:

- **Metrics Integration**: Micrometer and Prometheus integration
- **Logging**: SLF4J and Logback configuration for workflow visibility
- **Distributed Tracing**: OpenTelemetry and Jaeger integration
- **Health Checks**: Spring Boot Actuator integration for workflow health
