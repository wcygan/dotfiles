---
description: Generate SPEC.md for AI-assisted development with clear intent and constraints
---

Create a comprehensive SPEC.md file in the project root that translates user requirements into structured specifications optimized for AI-assisted development.

**Input**: User provides project context via $ARGUMENTS (feature description, requirements, constraints, goals)

**Output**: SPEC.md file with four key sections following spec-driven development principles

---

# Spec-Driven Development Structure

The specification should enable AI agents to understand **intent as source of truth** while providing explicit boundaries and architectural decisions.

## Section 1: Specification (The "What" and "Why")

```markdown
# Project Specification

## Overview
[2-3 sentence description of what this project does and why it exists]

## User Experience
[Describe the user-facing behavior, workflows, or API contracts]
- What interactions are supported?
- What are the success criteria?
- What does "done" look like from a user perspective?

## Functional Requirements
- [Requirement 1]: [Clear, testable statement]
- [Requirement 2]: [Clear, testable statement]
- [Requirement 3]: [Clear, testable statement]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Out of Scope
[Explicitly list what this project will NOT do to prevent scope creep]
```

## Section 2: Technical Plan (The "How")

```markdown
# Technical Architecture

## Technology Decisions
- **Language/Runtime**: [Choice + rationale]
- **Framework**: [Choice + rationale]
- **Database**: [Choice + rationale]
- **Infrastructure**: [Choice + rationale]

## Architectural Constraints
- [Constraint 1]: [Why this boundary exists]
- [Constraint 2]: [Security, compliance, performance requirements]
- [Constraint 3]: [Integration or compatibility requirements]

## Key Design Decisions
1. **[Decision area]**: [Choice made]
   - Rationale: [Why this approach]
   - Trade-offs: [What we're accepting/rejecting]

2. **[Decision area]**: [Choice made]
   - Rationale: [Why this approach]
   - Trade-offs: [What we're accepting/rejecting]

## Dependencies
- [External library/service 1]: [Purpose]
- [External library/service 2]: [Purpose]

## Non-Functional Requirements
- Performance: [Specific targets]
- Security: [Policies and standards]
- Scalability: [Growth expectations]
- Reliability: [Uptime, error handling]
```

## Section 3: Implementation Tasks

```markdown
# Task Breakdown

## Phase 1: Foundation
- [ ] **Task 1.1**: [Specific, testable unit of work]
  - Context: [What needs to exist first]
  - Acceptance: [How to verify completion]

- [ ] **Task 1.2**: [Specific, testable unit of work]
  - Context: [What needs to exist first]
  - Acceptance: [How to verify completion]

## Phase 2: Core Features
- [ ] **Task 2.1**: [Specific, testable unit of work]
  - Context: [Dependencies on Phase 1]
  - Acceptance: [How to verify completion]

## Phase 3: Integration & Polish
- [ ] **Task 3.1**: [Specific, testable unit of work]
  - Context: [Dependencies on previous phases]
  - Acceptance: [How to verify completion]

## Testing Strategy
- Unit tests: [Coverage targets and key areas]
- Integration tests: [Critical paths to test]
- E2E tests: [User workflows to validate]
```

## Section 4: Evolution Notes

```markdown
# Specification Evolution

## Version History
- v1.0 (YYYY-MM-DD): Initial specification
- [Track major changes as spec evolves]

## Open Questions
- [ ] [Unresolved decision 1]
- [ ] [Unresolved decision 2]

## Future Considerations
- [Enhancement 1]: [Why deferred]
- [Enhancement 2]: [Why deferred]
```

---

# Guidelines for AI-Effective Specs

**Make implicit knowledge explicit:**
- Don't assume AI knows your coding standards, security policies, or architectural patterns
- State framework choices, naming conventions, error handling approaches
- Document compliance requirements (GDPR, accessibility, etc.)

**Provide clear boundaries:**
- Specify what technologies/libraries MUST be used
- State what approaches should be AVOIDED
- Define quality gates (test coverage, performance benchmarks)

**Enable verification:**
- Each requirement should be testable
- Each task should have clear acceptance criteria
- Success criteria should be measurable

**Avoid over-specification:**
- Focus on "what" and "why", allow flexibility in implementation details
- Don't write pseudo-code in specs (that's what implementation is for)
- Keep technical decisions at architecture level, not line-by-line

**Treat as living document:**
- Update specs when requirements change
- Track major revisions in version history
- Document learnings and course corrections

---

# Execution Instructions

1. **Analyze $ARGUMENTS** to extract:
   - Project purpose and goals
   - User requirements or feature descriptions
   - Technical constraints or preferences
   - Success criteria

2. **Generate SPEC.md** with all four sections populated

3. **Review for completeness**:
   - Are requirements testable?
   - Are technical decisions justified?
   - Are tasks appropriately scoped?
   - Are boundaries clear?

4. **Write file** to project root

5. **Provide summary**:
   - Key specifications captured
   - Major technical decisions made
   - Next recommended step (review spec, or proceed to implementation)

---

# Example User Inputs

**Input**: "Build a CLI tool that converts markdown to HTML with custom themes"

**Generated spec should include:**
- Specification: CLI interface, input/output behavior, theme system
- Technical plan: Language choice (Go/Rust/Python), parsing library, templating approach
- Tasks: Markdown parser integration, theme loader, CLI scaffolding, tests
- Success criteria: Supports GitHub-flavored markdown, applies themes, handles errors gracefully

**Input**: "REST API for managing user tasks with auth"

**Generated spec should include:**
- Specification: API endpoints, auth flows, data model, success criteria
- Technical plan: Framework, database, auth strategy (JWT/sessions), security policies
- Tasks: Database schema, auth middleware, CRUD endpoints, integration tests
- Success criteria: All endpoints secured, tests at 90%+ coverage, handles concurrent requests
