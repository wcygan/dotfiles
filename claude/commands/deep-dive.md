# /deep-dive

Perform systematic, multi-perspective exploration of a topic, codebase, or concept to build comprehensive understanding through structured investigation.

## Usage

```
/deep-dive [topic, concept, or codebase area]
```

## Deep Dive Process

### Phase 1: Contextual Foundation

**Establish Baseline Understanding**

- Define scope and boundaries of investigation
- Identify key stakeholders and use cases
- Map existing knowledge and assumptions
- Set exploration objectives and success criteria

**Initial Reconnaissance**

```bash
# Codebase structure analysis
fd . --type f | head -20  # Get file layout overview
rg "TODO|FIXME|HACK" -n   # Find known issues
rg "import|require|use" -n | head -10  # Understand dependencies
```

### Phase 2: Multi-Dimensional Analysis

**Technical Dimension**

- Architecture patterns and design decisions
- Implementation approaches and trade-offs
- Performance characteristics and bottlenecks
- Security considerations and vulnerabilities
- Testing coverage and quality metrics

**Business Dimension**

- User needs and value propositions
- Business rules and constraints
- Market context and competitive landscape
- Compliance and regulatory requirements
- Cost implications and resource constraints

**Operational Dimension**

- Deployment and infrastructure requirements
- Monitoring and observability needs
- Maintenance and support considerations
- Scalability and growth planning
- Risk assessment and mitigation strategies

### Phase 3: Deep Investigation Techniques

**Code Archaeology**

```bash
# Understand evolution and history
git log --oneline --graph -20
git blame [key-file] | head -10
git show --stat HEAD~5..HEAD

# Find patterns and conventions
rg "func|function|def|class" -A 1 | head -20
rg "test|spec" --files | head -10
rg "config|setting|option" -i -A 2
```

**Dependency Mapping**

```bash
# External dependencies
rg "package.json|Cargo.toml|go.mod|requirements.txt" --files
rg "import.*from|require\(|use " -n | head -15

# Internal coupling analysis  
rg "\.\/|\.\.\/|@\/" -n | head -10
fd "index|mod|lib" --type f
```

**Data Flow Tracing**

```bash
# Follow data transformations
rg "map|transform|convert|parse|serialize" -A 2 -B 1
rg "input|output|request|response" -A 1 -B 1
rg "store|save|persist|cache|fetch|load" -A 1

# State management patterns
rg "state|store|reducer|action|event" -A 2
rg "useState|createStore|dispatch" -A 1
```

### Phase 4: Knowledge Synthesis

**Pattern Recognition**

- Common design patterns and anti-patterns
- Recurring implementation strategies
- Consistent naming and organization conventions
- Shared mental models and abstractions

**Gap Analysis**

- Missing functionality or incomplete features
- Technical debt and refactoring opportunities
- Documentation gaps and knowledge silos
- Testing blind spots and quality issues

**Insight Generation**

- Non-obvious connections and relationships
- Emergent properties and system behaviors
- Hidden assumptions and implicit constraints
- Optimization opportunities and quick wins

### Phase 5: Structured Documentation

**Executive Summary**

```markdown
# Deep Dive: [Topic]

## Key Findings

- [3-5 most important discoveries]
- [Critical insights for decision making]
- [Urgent issues requiring attention]

## Strategic Implications

- [Impact on project roadmap]
- [Resource allocation recommendations]
- [Risk mitigation priorities]
```

**Technical Deep Dive**

```markdown
## Architecture Analysis

### Current State

- [Detailed system description]
- [Component responsibilities and interactions]
- [Technology stack evaluation]

### Design Patterns

- [Patterns in use and their effectiveness]
- [Anti-patterns and technical debt]
- [Architectural evolution opportunities]

### Performance Profile

- [Bottlenecks and optimization targets]
- [Scalability characteristics]
- [Resource utilization patterns]
```

**Knowledge Map**

```markdown
## Domain Model

- [Core entities and relationships]
- [Business rules and constraints]
- [Workflow processes and state transitions]

## Integration Points

- [External system dependencies]
- [API contracts and protocols]
- [Data exchange patterns]

## Operational Considerations

- [Deployment requirements]
- [Monitoring and alerting needs]
- [Backup and recovery procedures]
```

### Phase 6: Actionable Insights

**Immediate Actions (Next 1-2 weeks)**

- [ ] Critical fixes or security issues
- [ ] Quick wins and low-hanging fruit
- [ ] Documentation of key findings

**Short-term Improvements (Next 1-3 months)**

- [ ] Refactoring high-impact areas
- [ ] Adding missing test coverage
- [ ] Infrastructure optimizations

**Long-term Evolution (3-12 months)**

- [ ] Architectural improvements
- [ ] Technology upgrades or migrations
- [ ] Process and tooling enhancements

## Deep Dive Methodologies

### Code-First Investigation

- Start with entry points and trace execution flows
- Map data structures and their transformations
- Analyze error handling and edge cases
- Document performance-critical paths

### Problem-First Investigation

- Begin with user pain points or business needs
- Trace backwards to root causes
- Identify all contributing factors
- Evaluate solution alternatives

### Architecture-First Investigation

- Start with high-level system design
- Drill down into component implementations
- Analyze cross-cutting concerns
- Evaluate design pattern effectiveness

### Data-First Investigation

- Begin with data models and schemas
- Trace data lifecycle and transformations
- Analyze data quality and consistency
- Evaluate storage and access patterns

## Investigation Tools and Techniques

**Static Analysis**

```bash
# Code complexity and quality metrics
fd "*.rs" | xargs wc -l | sort -n
rg "match|if|for|while" -c # Complexity indicators
rg "unwrap|panic|todo|unreachable" -n # Risk indicators
```

**Dynamic Analysis**

```bash
# Runtime behavior investigation
strace -c [command] 2>&1 | head -20  # System call analysis
perf stat [command]  # Performance profiling
time [command]  # Execution timing
```

**Dependency Analysis**

```bash
# Dependency tree visualization  
npm ls --depth=2  # Node.js dependencies
cargo tree  # Rust dependencies
go mod graph | head -20  # Go module graph
```

## Output Guidelines

- **Multi-perspective**: Address technical, business, and operational angles
- **Evidence-based**: Support conclusions with concrete examples and data
- **Actionable**: Provide clear next steps and recommendations
- **Comprehensive**: Cover breadth while maintaining useful depth
- **Accessible**: Make insights understandable to different audiences
- **Future-focused**: Consider evolution and long-term implications

## Integration with Other Commands

- Use after `/investigate` for deeper exploration of specific findings
- Combine with `/options` to explore alternative approaches discovered
- Follow with `/plan` to organize implementation of improvements
- Use `/dependencies` to map discovered relationships
- Apply `/monitor` to track key metrics identified during investigation

The goal is to develop expert-level understanding that enables confident decision-making and effective action planning.
