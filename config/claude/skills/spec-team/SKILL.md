# spec-team

Convert vague feature requests into detailed, implementable specifications through collaborative analysis.

## Usage

```
/spec-team <feature-description>
```

**Example:**
```
/spec-team Add user authentication with OAuth providers
```

## What it does

Orchestrates a team of specialists to transform informal requirements into production-ready specifications:

1. **Product Manager** - Breaks down request into user stories with clear value propositions
2. **API Designer** - Defines interface contracts, endpoints, and data flows
3. **Domain Modeler** - Specifies data structures, relationships, and constraints
4. **Test Strategist** - Creates acceptance criteria and test scenarios

The team works **sequentially with feedback loops**: each phase reviews prior work before proceeding, ensuring consistency and catching gaps early.

## Output

A structured specification document containing:

* **Overview** - Problem statement, goals, non-goals
* **User Stories** - Who/what/why format with acceptance criteria
* **API Contracts** - Endpoints, request/response schemas, error cases
* **Data Models** - Entities, relationships, validation rules
* **Acceptance Tests** - Test scenarios, edge cases, performance criteria

The final spec is ready for implementation with clear acceptance criteria and rollback plan.

## Team composition

* `product-manager` (custom) - Requirements analysis and story writing
* `api-designer` (built-in) - Interface design and contracts
* `domain-modeler` (built-in) - Data modeling and relationships
* `test-strategist` (built-in) - Test scenarios and acceptance criteria

## When to use

* Translating stakeholder requests into technical requirements
* Planning multi-component features that span API + data + UI
* Ensuring alignment before implementation starts
* Creating specs for code review or RFC processes

## When NOT to use

* Simple bug fixes or one-line changes
* Well-defined tasks with existing specs
* Exploratory prototyping (use `/research` instead)
