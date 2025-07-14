Your goal is to create a comprehensive, hierarchical project plan with intelligent analysis and task breakdown.

Ask for the project name, scope (micro/small/medium/large), and specific requirements if not provided.

## Project Analysis Framework

### Step 1: Project Discovery and Context Analysis

Analyze the project structure and technology stack from the referenced files to understand:

- **Project Type**: Identify the primary technology stack and architecture
- **Complexity Level**: Assess codebase size and organizational complexity
- **Development Stage**: Determine current state and development phase
- **Technology Stack**: Map frameworks, dependencies, and build systems
- **Documentation State**: Evaluate existing documentation and standards

### Step 2: Architecture and Structure Assessment

Examine the project organization and design patterns:

- **Directory Structure**: Analyze component organization and module hierarchy
- **Design Patterns**: Identify architectural patterns and design principles
- **Component Relationships**: Map dependencies and interaction patterns
- **Code Organization**: Assess modularity and separation of concerns
- **Scalability Considerations**: Evaluate architecture for growth potential

### Step 3: Technology and Dependencies Evaluation

Review the technology landscape and requirements:

- **Build Systems**: Analyze package managers and build configurations
- **Runtime Requirements**: Identify platform and version constraints
- **Dependencies**: Map external libraries and internal modules
- **Development Tools**: Assess tooling for development and testing
- **Compatibility Matrix**: Evaluate version and platform compatibility

### Step 4: Quality and Testing Strategy Analysis

Assess current quality measures and testing approaches:

- **Test Structure**: Analyze existing test organization and coverage
- **Quality Gates**: Identify code quality measures and standards
- **CI/CD Configuration**: Review automation and deployment processes
- **Testing Strategy**: Evaluate unit, integration, and end-to-end testing
- **Performance Considerations**: Assess performance testing and optimization

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

- **Project Structure**: Establish directory organization and conventions
- **Development Environment**: Configure tools, dependencies, and build systems
- **Version Control**: Set up repository structure and branching strategy
- **Documentation Framework**: Create documentation standards and templates
- **Quality Foundation**: Establish linting, formatting, and testing frameworks

### Phase 2: Core Development

**Priority**: High | **Dependencies**: Foundation Setup

- **Architecture Implementation**: Build core system components and interfaces
- **Business Logic**: Implement primary functionality and data models
- **API Development**: Create service interfaces and data access layers
- **User Interface**: Develop user-facing components and interactions
- **Integration Points**: Establish connections between system components

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

- [ ] Initialize project structure and directories
- [ ] Configure build system and dependency management
- [ ] Set up development environment and tooling
- [ ] Create repository structure and initial documentation
- [ ] Establish code quality standards and automation

### Core Development Tasks

- [ ] Design and implement core architecture
- [ ] Create data models and business logic
- [ ] Develop API endpoints and service interfaces
- [ ] Build user interface components
- [ ] Implement component integration and communication

### Feature Enhancement Tasks

- [ ] Add advanced functionality and user features
- [ ] Optimize performance and resource utilization
- [ ] Enhance user experience and interface design
- [ ] Implement comprehensive error handling
- [ ] Add security measures and access controls

### Quality Assurance Tasks

- [ ] Create unit tests for all components
- [ ] Develop integration and end-to-end tests
- [ ] Perform performance and load testing
- [ ] Conduct security testing and vulnerability assessment
- [ ] Execute user acceptance testing and validation

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

## Context Files

#file:package.json #file:deno.json #file:Cargo.toml #file:go.mod #file:pom.xml #file:build.gradle #file:Makefile #file:CMakeLists.txt #file:README.md #file:CONTRIBUTING.md #file:CHANGELOG.md #file:LICENSE #file:.gitignore #file:tsconfig.json #file:jest.config.js #file:src/index.ts #file:src/main.js #file:src/app.py #file:src/main.go #file:src/lib.rs #file:docs/architecture.md #file:docs/api.md #file:tests/ #file:.github/workflows/
