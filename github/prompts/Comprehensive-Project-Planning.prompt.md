Your goal is to create a comprehensive, hierarchical project plan with intelligent analysis and task breakdown.

Ask for the project name, scope (micro/small/medium/large), and specific requirements if not provided.

## Project Analysis Framework

### Step 1: Project Discovery and Context Analysis

Analyze the Java microservices project structure to understand:

- **Project Type**: Java microservices with gRPC communication
- **Complexity Level**: Assess codebase size and service boundaries
- **Development Stage**: Determine current state and development phase
- **Technology Stack**: Java, Gradle, JUnit Jupiter, gRPC, MySQL, jOOQ, Flyway, Temporal, Kafka
- **Documentation State**: Evaluate existing documentation and standards

### Step 2: Architecture and Structure Assessment

Examine the project organization and design patterns:

- **Directory Structure**: Analyze component organization and module hierarchy
- **Design Patterns**: Identify architectural patterns and design principles
- **Component Relationships**: Map dependencies and interaction patterns
- **Code Organization**: Assess modularity and separation of concerns
- **Scalability Considerations**: Evaluate architecture for growth potential

### Step 3: Technology and Dependencies Evaluation

Review the Java microservices technology landscape:

- **Build Systems**: Analyze Gradle build configurations and multi-project setup
- **Runtime Requirements**: Java version, JVM settings, and deployment constraints
- **Dependencies**: Map gRPC services, MySQL databases, Kafka topics, Temporal workflows
- **Development Tools**: Assess tooling for development, testing, and monitoring
- **Compatibility Matrix**: Evaluate version compatibility across the tech stack

### Step 4: Quality and Testing Strategy Analysis

Assess current quality measures and Java testing approaches:

- **Test Structure**: Analyze existing JUnit Jupiter test organization and coverage
- **Quality Gates**: Identify code quality measures and static analysis tools
- **CI/CD Configuration**: Review Gradle-based automation and deployment processes
- **Testing Strategy**: Evaluate unit, integration, and gRPC service testing
- **Performance Considerations**: Assess performance testing for microservices architecture

### Step 5: Development Workflow Assessment

Examine development practices and operational setup:

- **Git Workflows**: Analyze branching strategy and collaboration patterns
- **Development Environment**: Review setup and configuration requirements
- **Documentation Standards**: Assess documentation quality and completeness
- **Team Coordination**: Evaluate collaboration tools and processes
- **Operational Readiness**: Review monitoring and deployment practices

## Planning Strategy Selection

Based on project scope, select the appropriate planning approach:

### For Micro Projects (< 10 files)

- **Linear Task Progression**: Sequential development with minimal overhead
- **Single Developer Focus**: Streamlined workflow for individual work
- **Rapid Iteration**: Emphasis on quick development cycles
- **Essential Features Only**: Focus on core functionality

### For Small Projects (10-100 files)

- **Feature-Based Organization**: Group tasks by functional areas
- **Parallel Development Streams**: Independent feature development
- **Basic Quality Gates**: Essential testing and review processes
- **Agile Sprint Methodology**: Iterative development approach

### For Medium Projects (100-1000 files)

- **Phase-Based Execution**: Structured development phases
- **Component-Based Planning**: Modular task organization
- **Advanced Quality Measures**: Comprehensive testing strategy
- **Team Coordination**: Multi-developer workflow management

### For Large Projects (1000+ files)

- **Enterprise-Scale Planning**: Sophisticated project management
- **Multi-Team Coordination**: Complex team interaction management
- **Risk Management**: Comprehensive risk assessment and mitigation
- **Continuous Integration**: Advanced automation and monitoring

## Hierarchical Plan Generation

### Phase 1: Foundation Setup

**Priority**: High | **Dependencies**: None

- **Project Structure**: Establish Gradle multi-project setup and Java package conventions
- **Development Environment**: Configure Java, Gradle, database connections, and IDE settings
- **Version Control**: Set up repository structure and GitFlow branching strategy
- **Documentation Framework**: Create documentation standards and API documentation templates
- **Quality Foundation**: Establish Checkstyle, SpotBugs, JUnit Jupiter frameworks

### Phase 2: Core Development

**Priority**: High | **Dependencies**: Foundation Setup

- **Architecture Implementation**: Build core microservices components and gRPC interfaces
- **Business Logic**: Implement domain models and service layer with Spring Framework
- **API Development**: Create gRPC service definitions and Protocol Buffer schemas
- **Data Access**: Implement jOOQ repositories and MySQL database connections
- **Integration Points**: Establish Kafka producers/consumers and Temporal workflows

### Phase 3: Feature Enhancement

**Priority**: Medium | **Dependencies**: Core Development

- **Advanced Features**: Implement secondary functionality and enhancements
- **Performance Optimization**: Optimize critical paths and resource usage
- **User Experience**: Refine interface design and interaction patterns
- **Error Handling**: Implement comprehensive error management
- **Security Implementation**: Add authentication, authorization, and data protection

### Phase 4: Quality Assurance

**Priority**: Medium | **Dependencies**: Feature Enhancement

- **Testing Implementation**: Create comprehensive test suites
- **Integration Testing**: Validate component interactions and workflows
- **Performance Testing**: Assess system performance under load
- **Security Testing**: Validate security measures and vulnerability assessment
- **User Acceptance Testing**: Validate functionality against requirements

### Phase 5: Production Readiness

**Priority**: Medium | **Dependencies**: Quality Assurance

- **Deployment Automation**: Set up CI/CD pipelines and deployment processes
- **Monitoring Setup**: Implement logging, metrics, and alerting
- **Documentation Completion**: Finalize user and developer documentation
- **Production Configuration**: Configure production environments and settings
- **Launch Preparation**: Final validation and go-live preparation

## Task Breakdown Structure

For each phase, create specific, actionable tasks:

### Foundation Setup Tasks

- [ ] Initialize Gradle multi-project structure with submodules
- [ ] Configure Java build settings and dependency management
- [ ] Set up development environment with database and Kafka
- [ ] Create repository structure and Flyway migration framework
- [ ] Establish code quality standards with Checkstyle and SpotBugs

### Core Development Tasks

- [ ] Design and implement microservices architecture with Spring Boot
- [ ] Create Protocol Buffer definitions and generate gRPC services
- [ ] Develop jOOQ-based data access layer with MySQL
- [ ] Build domain models and business logic components
- [ ] Implement Kafka integration for event-driven communication

### Feature Enhancement Tasks

- [ ] Add advanced functionality and user features
- [ ] Optimize performance and resource utilization
- [ ] Enhance user experience and interface design
- [ ] Implement comprehensive error handling
- [ ] Add security measures and access controls

### Quality Assurance Tasks

- [ ] Create JUnit Jupiter unit tests for all service components
- [ ] Develop integration tests for gRPC services and database operations
- [ ] Perform load testing on Kafka consumers and MySQL queries
- [ ] Conduct security testing for microservices endpoints
- [ ] Execute user acceptance testing for Temporal workflow processes

### Production Readiness Tasks

- [ ] Set up CI/CD pipelines and deployment automation
- [ ] Configure monitoring, logging, and alerting
- [ ] Complete documentation and user guides
- [ ] Configure production environments
- [ ] Perform final validation and launch preparation

## Risk Assessment and Mitigation

Identify and address potential project risks:

### Technical Risks

- **Dependency Issues**: Version conflicts and compatibility problems
- **Performance Bottlenecks**: Scalability and resource constraints
- **Security Vulnerabilities**: Data protection and access control gaps
- **Integration Complexity**: Component interaction and API challenges

### Project Management Risks

- **Scope Creep**: Uncontrolled requirement changes
- **Resource Constraints**: Time, budget, or personnel limitations
- **Communication Gaps**: Team coordination and information sharing
- **Quality Compromises**: Pressure to reduce testing or documentation

### Mitigation Strategies

- **Regular Risk Assessment**: Periodic evaluation of risk factors
- **Contingency Planning**: Alternative approaches for high-risk areas
- **Quality Gates**: Mandatory checkpoints for critical deliverables
- **Communication Protocols**: Clear channels for issue escalation

## Success Metrics and Monitoring

Define measurable success criteria:

### Development Metrics

- **Code Quality**: Test coverage, complexity, and maintainability scores
- **Performance**: Response times, throughput, and resource utilization
- **Security**: Vulnerability assessment and compliance measures
- **Documentation**: Completeness and quality of project documentation

### Project Management Metrics

- **Schedule Performance**: Task completion rates and milestone achievement
- **Resource Utilization**: Team productivity and efficiency measures
- **Risk Management**: Risk identification and mitigation effectiveness
- **Stakeholder Satisfaction**: User and team satisfaction scores

## Deliverables

Provide a comprehensive project plan including:

1. **Executive Summary**: High-level project overview and objectives
2. **Detailed Task Breakdown**: Hierarchical task structure with dependencies
3. **Timeline and Milestones**: Project schedule with key deliverables
4. **Resource Requirements**: Team structure and skill requirements
5. **Risk Management Plan**: Risk assessment and mitigation strategies
6. **Quality Assurance Plan**: Testing strategy and quality measures
7. **Success Criteria**: Measurable objectives and evaluation metrics
