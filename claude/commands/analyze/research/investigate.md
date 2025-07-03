# /investigate

Conduct thorough investigation of a topic, technology, or approach using codebase analysis and web research to determine optimal solutions with up-to-date information.

## Usage

```
/investigate [topic or question]
```

## Investigation Process

### Phase 1: Context Gathering

1. **Understand the Question**
   - Parse the investigation topic
   - Identify key terms and concepts
   - Determine investigation scope

2. **Initial Codebase Scan**
   ```bash
   # Search for existing implementations
   rg "[key terms]" --type-add 'code:*.{rs,go,java,ts,js,py}' -t code

   # Find related configuration
   rg "[key terms]" --type yaml --type json --type toml

   # Look for documentation
   fd "README|ARCHITECTURE|DESIGN" --type f | xargs rg -l "[key terms]"
   ```

### Phase 2: Deep Analysis

#### Codebase Investigation

1. **Pattern Discovery**
   ```bash
   # Find implementation patterns
   rg "impl.*[concept]|class.*[concept]|interface.*[concept]" -A 5 -B 2

   # Analyze dependencies
   rg "[concept]" package.json Cargo.toml go.mod pom.xml requirements.txt

   # Check test coverage
   fd "test|spec" --type f | xargs rg -l "[concept]"
   ```

2. **Architecture Analysis**
   - Map component relationships
   - Identify integration points
   - Document data flows
   - Note design patterns

#### Web Research

1. **Current Best Practices**
   - Search for "[topic] best practices in <current year>"
   - Look for recent blog posts and articles
   - Check official documentation updates

2. **Technology Comparison**
   - Search for "[topic] vs alternatives"
   - Find benchmark comparisons
   - Review case studies
   - Check GitHub star trends

3. **Community Insights**
   - Search Stack Overflow for recent solutions
   - Check Reddit discussions (r/programming, topic-specific subreddits)
   - Review GitHub issues and discussions
   - Analyze npm/crates.io download trends

### Phase 3: Solution Synthesis

#### Evaluation Framework

1. **Technical Criteria**
   - Performance characteristics
   - Scalability potential
   - Security considerations
   - Maintenance burden
   - Learning curve

2. **Project Fit**
   - Alignment with existing stack
   - Team expertise requirements
   - Migration complexity
   - Cost implications

3. **Future-Proofing**
   - Technology maturity
   - Community support
   - Corporate backing
   - Update frequency

### Phase 4: Recommendation Formulation

#### Output Structure

````markdown
# Investigation: [Topic]

## Executive Summary

[2-3 sentence overview of findings and recommendation]

## Current State Analysis

### Existing Implementation

- [What's currently in the codebase]
- [Patterns and approaches used]
- [Identified pain points]

### Industry Standards (2025)

- [Current best practices]
- [Emerging trends]
- [Common pitfalls to avoid]

## Options Evaluation

### Option 1: [Approach Name]

**Pros:**

- [Advantage 1]
- [Advantage 2]

**Cons:**

- [Disadvantage 1]
- [Disadvantage 2]

**Real-world Usage:**

- [Company/Project using this]
- [Performance metrics if available]

### Option 2: [Alternative Approach]

[Similar structure]

## Recommendation

### Optimal Solution: [Chosen Approach]

**Rationale:**

1. [Key reason 1]
2. [Key reason 2]
3. [Key reason 3]

**Implementation Strategy:**

```[language]
// Code example showing recommended approach
```
````

**Migration Path:**

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Supporting Evidence

### Benchmarks

- [Performance comparison data]
- [Resource usage metrics]

### Case Studies

- [Relevant implementation example]
- [Lessons learned]

### Expert Opinions

- [Quote from authority/documentation]
- [Community consensus]

## Risk Mitigation

- **Risk 1**: [Description] → [Mitigation strategy]
- **Risk 2**: [Description] → [Mitigation strategy]

## Next Steps

1. [ ] [Immediate action item]
2. [ ] [Short-term task]
3. [ ] [Long-term consideration]

## Resources

- [Official Documentation](link)
- [Tutorial/Guide](link)
- [Community Forum](link)
- [Example Repository](link)

```
### Investigation Examples

#### Example 1: State Management
```

/investigate What's the best state management solution for our Rust microservices?

```
Investigation would:
- Analyze current state handling in codebase
- Research Rust state management patterns (2025)
- Compare options (Actor model, Event Sourcing, CQRS)
- Recommend based on project needs

#### Example 2: Authentication Strategy
```

/investigate Should we migrate from JWT to PASETO for our authentication?

```
Investigation would:
- Review current JWT implementation
- Research PASETO adoption and security benefits
- Analyze migration complexity
- Provide security comparison and recommendation

#### Example 3: Database Technology
```

/investigate Is ScyllaDB the right choice for our high-throughput event storage?

```
Investigation would:
- Examine current data patterns and volume
- Research ScyllaDB vs alternatives (Cassandra, DynamoDB)
- Analyze performance benchmarks
- Consider operational complexity

### Special Considerations

1. **Time-Sensitive Information**
   - Always search for content from last 12 months
   - Note deprecation warnings
   - Check for breaking changes

2. **Authoritative Sources**
   - Prioritize official documentation
   - Verify claims with multiple sources
   - Check GitHub star/fork counts for adoption

3. **Context Awareness**
   - Consider team's technology preferences (from CLAUDE.md)
   - Account for infrastructure constraints
   - Respect existing architectural decisions

4. **Balanced Perspective**
   - Present multiple viewpoints
   - Include contrarian opinions
   - Acknowledge trade-offs

### Integration with Other Commands

- Use after `/options` to deep-dive into specific choice
- Combine with `/elaborate` for implementation details
- Follow with `/plan` to execute recommendation
- Use `/benchmark` to validate performance claims

### Output Guidelines

- Lead with actionable recommendations
- Support claims with evidence
- Provide clear migration paths
- Include code examples
- Link to authoritative sources
- Acknowledge uncertainty where it exists
- **IMPORTANT**: Return investigation results directly to the user in the response - DO NOT write results to a file unless explicitly requested
```
