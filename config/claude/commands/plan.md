---
description: Analyze goal and create detailed implementation plan without modifications
---

You are in PLANNING MODE. Your job is to research, analyze, and plan - but NOT to implement.

# Mission

Create a comprehensive, actionable plan for: **{the user's goal}**

# What You CAN Do

- 📖 **Read files** to understand current implementation
- 🔍 **Search code** to find relevant patterns and examples
- 🌐 **Web search** for documentation, best practices, examples
- 🧪 **Run tests** to understand current behavior and coverage
- 🔨 **Run builds** to verify environment and dependencies
- 📊 **Analyze** architecture, dependencies, and impact
- 🚀 **Use sub-agents** for parallel exploration when beneficial (2-3 concurrent tasks)

# What You MUST NOT Do

- ❌ Write or modify any files
- ❌ Create new files
- ❌ Make any code changes
- ❌ Run commands that alter state (git commit, deployments, etc.)

# Planning Process

1. **Understand the Goal**
   - Clarify requirements and constraints
   - Identify success criteria
   - Note any ambiguities to resolve

2. **Explore Current State** (use sub-agents for parallel analysis)
   - Read relevant code sections
   - Map existing architecture and patterns
   - Identify related tests
   - Check dependencies and tooling

3. **Research Approaches**
   - Search for similar implementations in codebase
   - Look up documentation and best practices
   - Consider multiple solution approaches
   - Identify potential pitfalls

4. **Assess Impact**
   - What files will need changes?
   - What tests need updates/additions?
   - Are there breaking changes?
   - What's the migration path?

5. **Create Implementation Plan**
   - Break down into atomic, testable steps
   - Order steps logically (dependencies first)
   - Identify test-first opportunities
   - Note rollback strategies

# Output Format

Present the plan in the chat window with:

## 1. Goal Summary
- What we're trying to achieve
- Success criteria
- Key constraints

## 2. Current State Analysis
- Relevant files and their purposes
- Existing patterns to follow
- Current test coverage
- Dependencies involved

## 3. Proposed Approach
- Recommended solution (with rationale)
- Alternative approaches considered (with trade-offs)
- Why this approach is best

## 4. Implementation Steps
For each step:
- **Step N: {Description}**
  - Files to modify: `path/to/file.ext`
  - Changes needed: {brief description}
  - Tests to add/update: {test files}
  - Estimated complexity: [Small/Medium/Large]
  - Dependencies: {what must be done first}

## 5. Testing Strategy
- Unit tests needed
- Integration tests needed
- How to verify each step
- Manual testing required

## 6. Risks & Mitigation
- Potential issues
- Breaking changes
- Rollback approach
- Performance considerations

## 7. Open Questions
- Ambiguities to resolve
- Decisions needed from user
- Areas needing more research

# Style Guidelines

- **Be thorough** - this plan guides implementation
- **Be specific** - name files, functions, approaches
- **Be realistic** - acknowledge complexity and risks
- **Be structured** - make steps actionable and ordered
- **Ask questions** - don't assume; clarify uncertainties

# Sub-Agent Strategy

When exploration tasks can be parallelized, launch 2-3 sub-agents:
- Agent 1: Explore current implementation and architecture
- Agent 2: Search for similar patterns and examples
- Agent 3: Analyze tests and dependencies

Synthesize findings from all agents into the final plan.

# When Complete

Present the plan and ask:
1. Does this approach make sense?
2. Should we proceed with implementation?
3. Any concerns or alternative preferences?

**Remember:** You are analyzing and planning, NOT implementing. No file modifications.
