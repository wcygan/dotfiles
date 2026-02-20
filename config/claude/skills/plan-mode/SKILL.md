---
name: plan-mode
description: >
  Research, analyze, and create a detailed implementation plan without making
  any code changes. Read-only planning mode with sub-agent exploration. Use when
  planning implementation, designing approach, creating technical plans, or
  analyzing before building. Keywords: plan, design, approach, implementation
  plan, analyze, research, strategy, read-only planning
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(npm *), Bash(cargo *), Bash(go *), Bash(pytest *), Bash(make *), WebSearch, WebFetch, Task
disable-model-invocation: true
---

# Planning Mode

You are in PLANNING MODE. Research, analyze, and plan — but do NOT implement.

## Mission

Create a comprehensive, actionable plan for: **$ARGUMENTS**

## What You CAN Do

- Read files to understand current implementation
- Search code to find relevant patterns and examples
- Web search for documentation, best practices, examples
- Run tests/builds to understand behavior and environment
- Use sub-agents for parallel exploration (2-3 concurrent tasks)

## What You MUST NOT Do

- Write or modify any files
- Create new files
- Make any code changes
- Run commands that alter state (git commit, deployments, etc.)

## Planning Process

### 1. Understand the Goal
- Clarify requirements and constraints
- Identify success criteria
- Note any ambiguities to resolve

### 2. Explore Current State
Use sub-agents for parallel analysis:
- Agent 1: Current implementation and architecture
- Agent 2: Similar patterns and examples in the codebase
- Agent 3: Tests, dependencies, and tooling

### 3. Research Approaches
- Search for similar implementations
- Look up documentation and best practices
- Consider multiple solution approaches
- Identify potential pitfalls

### 4. Assess Impact
- What files will need changes?
- What tests need updates/additions?
- Are there breaking changes?
- What's the migration path?

### 5. Create Implementation Plan
- Break down into atomic, testable steps
- Order steps logically (dependencies first)
- Identify test-first opportunities
- Note rollback strategies

## Output Format

See `references/output-format.md` for the full 7-section output template.

Produce the plan in the chat window, then ask:
1. Does this approach make sense?
2. Should we proceed with implementation?
3. Any concerns or alternative preferences?

## Style Guidelines

- **Be thorough** — this plan guides implementation
- **Be specific** — name files, functions, approaches
- **Be realistic** — acknowledge complexity and risks
- **Be structured** — make steps actionable and ordered
- **Ask questions** — don't assume; clarify uncertainties
