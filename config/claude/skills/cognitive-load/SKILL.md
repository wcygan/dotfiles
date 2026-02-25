# Cognitive Load Reviewer & Guide

Review code through a cognitive load lens and provide actionable guidance for reducing extraneous complexity. Based on zakirullin's Cognitive Load Developer framework.

Use when reviewing code for complexity, simplifying architecture, reducing mental overhead, making code more understandable, onboarding optimization, PR review for readability, or asking about cognitive load principles. Keywords: cognitive load, complexity, simplify, understandable, readable, mental model, deep module, shallow module, extraneous, abstraction, composition, early return.

## Core Concept

Cognitive load = mental effort to understand and complete a task. Working memory holds ~4 chunks. Every unnecessary concept, pattern, or indirection consumes a slot.

**Intrinsic load** — inherent task difficulty. Cannot be reduced.
**Extraneous load** — created by how code is written/organized. Target for elimination.

The goal: minimize extraneous cognitive load so developers spend working memory on the actual problem.

## Operating Modes

### Mode 1: Code Review

When asked to review code, diffs, or files for cognitive load:

1. Read the target code thoroughly
2. Evaluate against each category in the references
3. Report findings grouped by severity:
   - **High** — patterns that force readers to hold 4+ chunks simultaneously
   - **Medium** — unnecessary indirection or mental mapping
   - **Low** — minor readability improvements
4. For each finding, cite the specific principle and suggest a concrete fix
5. End with an overall cognitive load score: **Low / Moderate / High / Severe**

Scoring guide:
- **Low**: New developer productive within minutes. Linear reading, few abstractions.
- **Moderate**: Some patterns require context. Productive within a session.
- **High**: Multiple mental models required. Days to become productive.
- **Severe**: Architecture itself is the problem. Weeks to onboard.

### Mode 2: Principles Guide

When asked about cognitive load principles, best practices, or "how should I design X":

1. Identify which principles from the references apply
2. Provide the principle with its rationale
3. Give a concrete before/after example
4. Cite the source (Ousterhout, Pike, Brooks, etc.) where applicable

## Quick Reference: The Seven Deadly Complexities

1. **Complex conditionals** — extract to named intermediates
2. **Deep nesting** — flatten with early returns
3. **Inheritance chains** — prefer composition
4. **Shallow modules** — design deep modules with simple interfaces
5. **Premature microservices** — start monolithic, split when team scaling demands it
6. **Abstraction layers** — each layer costs a working memory slot
7. **DRY abuse** — a little copying beats a little dependency

References: [principles](references/principles.md), [code-patterns](references/code-patterns.md), [architecture](references/architecture.md), [review-checklist](references/review-checklist.md)
