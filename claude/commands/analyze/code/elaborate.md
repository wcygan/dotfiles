---
allowed-tools: Read, Write, Bash(fd:*), Bash(rg:*), Bash(git:*), Bash(gdate:*), Task
description: Generate comprehensive technical analysis and implementation guide
---

## Context

- Session ID: !`gdate +%s%N`
- Analysis target: $ARGUMENTS
- Project structure: !`fd . -t d -d 2 | head -10`
- Technology indicators: !`fd package.json Cargo.toml go.mod pom.xml deno.json -d 3`
- Recent changes: !`git log --oneline -5 || echo "No git repository"`

## Your task

STEP 1: Initialize analysis session

- Create analysis workspace: /tmp/elaborate-analysis-$SESSION_ID/
- Document target: $ARGUMENTS
- Analyze project context for technology stack

STEP 2: Determine analysis complexity
IF approach requires multi-domain expertise:

- Use Task tool to delegate parallel research:
  - Agent 1: Architecture and design patterns
  - Agent 2: Implementation strategies and code examples
  - Agent 3: Testing and deployment approaches
  - Agent 4: Risk analysis and alternatives
    ELSE:
- Proceed with single-agent deep analysis
- Think deeply about architectural implications

STEP 3: Generate comprehensive analysis
FOR EACH analysis domain:

- Research current best practices
- Identify implementation patterns
- Document concrete examples
- Assess risks and alternatives

STEP 4: Create implementation roadmap

- Break down into phases with realistic timelines
- Identify dependencies and prerequisites
- Define success criteria and checkpoints
- Include testing and validation steps

STEP 5: Synthesize findings

- Combine research from all domains
- Create actionable implementation guide
- Include code examples and configuration
- Document deployment and monitoring strategy

STEP 6: Save analysis artifacts

- Write comprehensive guide to /tmp/elaborate-analysis-$SESSION_ID/guide.md
- Create implementation checklist
- Document key decisions and rationale

## Analysis Framework

### Core Sections (generate programmatically)

1. **Executive Summary** (2-3 sentences)
2. **Technical Architecture** (components, data flow, tech stack)
3. **Implementation Phases** (3-phase approach with timelines)
4. **Code Examples** (2-3 concrete implementations)
5. **Integration Strategy** (APIs, dependencies, deployment)
6. **Testing Approach** (unit, integration, performance)
7. **Risk Assessment** (technical and operational risks)
8. **Alternative Approaches** (2-3 variations with trade-offs)
9. **Production Considerations** (monitoring, scaling, maintenance)
10. **Resource Library** (docs, tools, references)

### Quality Standards

- Provide specific, actionable guidance
- Include realistic effort estimates
- Address common implementation pitfalls
- Balance theoretical concepts with practical details
- Consider long-term maintenance and evolution
- Include concrete code examples in appropriate languages

## Extended Thinking Integration

For complex architectural decisions:

- Think deeply about system design trade-offs
- Consider scalability and performance implications
- Analyze security and compliance requirements
- Evaluate maintenance and operational complexity

## Output Format

Generate structured markdown with:

- Clear section headers
- Actionable checklists
- Code examples with explanations
- Visual diagrams where helpful (ASCII art)
- Time estimates and effort projections
- Risk mitigation strategies
