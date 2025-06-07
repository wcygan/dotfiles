# /elaborate

Provide an in-depth analysis and implementation guide for a specific technical approach or solution.

## Usage

```
/elaborate [approach or solution description]
```

## Instructions

For the given approach, provide a comprehensive deep-dive following this format:

### 1. Approach Overview

**Summary**: 2-3 sentence high-level description

**Core Concept**: Explain the fundamental idea and why it works

**Key Principles**: List 3-5 guiding principles of this approach

### 2. Technical Architecture

#### Component Breakdown

- List major components/modules
- Describe responsibilities of each
- Show component interactions (consider ASCII diagram)

#### Technology Stack

- **Core Technologies**: Primary languages/frameworks
- **Supporting Tools**: Build tools, testing frameworks, etc.
- **Infrastructure**: Deployment and runtime requirements

#### Data Flow

- Describe how data moves through the system
- Identify transformation points
- Note persistence layers

### 3. Implementation Roadmap

#### Phase 1: Foundation (Days 1-X)

- [ ] Setup and scaffolding tasks
- [ ] Core infrastructure
- [ ] Basic functionality

#### Phase 2: Core Features (Days X-Y)

- [ ] Primary feature implementation
- [ ] Integration points
- [ ] Initial testing

#### Phase 3: Hardening (Days Y-Z)

- [ ] Error handling and edge cases
- [ ] Performance optimization
- [ ] Security measures

### 4. Code Examples

Provide 2-3 concrete code snippets demonstrating:

- Key patterns or abstractions
- Critical implementation details
- Configuration examples

```[language]
// Example code with explanatory comments
```

### 5. Integration Points

**APIs/Interfaces**:

- Define public contracts
- Specify protocols and formats
- Document authentication/authorization

**Dependencies**:

- External services required
- Library dependencies
- System requirements

### 6. Testing Strategy

**Unit Testing**:

- What to test and why
- Mocking strategies
- Coverage targets

**Integration Testing**:

- Key integration scenarios
- Test data management
- Environment setup

**Performance Testing**:

- Load testing approach
- Benchmarking methodology
- Performance targets

### 7. Deployment Considerations

**Environment Requirements**:

- Development setup
- Staging configuration
- Production specifications

**Deployment Process**:

- Build pipeline
- Deployment steps
- Rollback procedures

**Monitoring & Observability**:

- Key metrics to track
- Logging strategy
- Alerting thresholds

### 8. Risk Analysis

**Technical Risks**:

- Potential failure points
- Mitigation strategies
- Contingency plans

**Operational Risks**:

- Maintenance complexity
- Team knowledge requirements
- Vendor lock-in concerns

### 9. Alternative Variations

Describe 2-3 variations of this approach:

- When to use each variation
- Trade-offs between variations
- Migration paths between them

### 10. Real-World Examples

- Reference implementations
- Case studies
- Lessons learned from production deployments

### 11. Resources & References

- Official documentation
- Tutorials and guides
- Community resources
- Related tools and libraries

## Guidelines

- Provide actionable, specific guidance
- Include realistic timelines and effort estimates
- Address common pitfalls and how to avoid them
- Balance theory with practical implementation details
- Consider maintenance and evolution, not just initial build

## Example

```
/elaborate Implement event-driven architecture using Apache Kafka
```

## Relationship to /options

This command complements `/options` by:

- Taking one option from `/options` and expanding it fully
- Providing implementation-ready details vs high-level comparison
- Focusing on "how" rather than "which"
- Offering concrete code and configuration examples
