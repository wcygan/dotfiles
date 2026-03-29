---
title: Coverage Model
description: Templates for generating coverage checklists based on topic type
tags: [coverage, checklist, framing, topic-type]
---

# Coverage Model

The coverage checklist is the non-code equivalent of a test suite. It defines what "done" looks like for the research. Each item is a specific aspect that must be addressed with sourced findings.

## Topic Type Templates

### Domain Exploration

Use when: the user wants to understand a field, technology, concept, or domain.

Standard (6-8 items):
- [ ] **What it is**: Definition, core concepts, key terminology
- [ ] **Why it exists**: Problem it solves, historical context, motivation
- [ ] **How it works**: Mechanics, architecture, key patterns
- [ ] **Current state**: Maturity, adoption, ecosystem health
- [ ] **Practitioner experience**: Common gotchas, lessons learned, real-world usage
- [ ] **Trade-offs**: Strengths, weaknesses, known limitations
- [ ] **Getting started**: Recommended learning path, key resources

Deep (add 4-6 more):
- [ ] **Ecosystem**: Tools, libraries, frameworks, community
- [ ] **Evolution**: How it has changed over time, version history
- [ ] **Edge cases**: Unusual scenarios, failure modes, boundary conditions
- [ ] **Alternatives**: What else exists in the same space
- [ ] **Future direction**: Roadmap, emerging patterns, open research questions
- [ ] **Case studies**: Specific implementations, success/failure stories

### Approach Evaluation

Use when: the user is comparing strategies, architectures, methods, or tools.

Standard (6-8 items):
- [ ] **Option inventory**: What approaches exist (at least 3)
- [ ] **Evaluation criteria**: What dimensions matter for this comparison
- [ ] **Per-option analysis**: Strengths/weaknesses of each against criteria
- [ ] **Context sensitivity**: When each option is the right choice
- [ ] **Practitioner preferences**: What real users prefer and why
- [ ] **Migration/switching cost**: How hard is it to change later
- [ ] **Decision framework**: A clear "if X then Y" guide

Deep (add 4-6 more):
- [ ] **Benchmarks**: Quantitative comparisons where available
- [ ] **Failure modes**: How each option fails and what the blast radius looks like
- [ ] **Combination strategies**: Can options be mixed?
- [ ] **Historical precedent**: What have similar decisions led to in the past
- [ ] **Emerging options**: New approaches not yet mainstream
- [ ] **Total cost of ownership**: Long-term maintenance, operational overhead

### Application Modeling

Use when: the user is designing a system, product, or workflow.

Standard (6-8 items):
- [ ] **Problem statement**: What exactly needs to be built and why
- [ ] **User/actor model**: Who interacts with this and how
- [ ] **Core entities**: Key data structures, relationships, invariants
- [ ] **Architecture patterns**: Suitable patterns and why (monolith, services, event-driven, etc.)
- [ ] **Technology landscape**: What tools/frameworks fit the requirements
- [ ] **Key constraints**: Performance, scale, security, compliance, budget
- [ ] **MVP scope**: Minimum viable version vs full vision

Deep (add 4-6 more):
- [ ] **Integration points**: External systems, APIs, data sources
- [ ] **Operational model**: Deployment, monitoring, incident response
- [ ] **Scalability path**: How the design grows with load/users
- [ ] **Security model**: Threat surface, authentication, authorization
- [ ] **Data model**: Storage, consistency, backup, migration
- [ ] **Team/skill requirements**: What expertise is needed to build and maintain

### Skill Development

Use when: the user wants to improve at something.

Standard (6-8 items):
- [ ] **Current landscape**: State of the skill/field, what "good" looks like
- [ ] **Learning taxonomy**: Beginner → intermediate → advanced breakdown
- [ ] **Core competencies**: The 3-5 most important sub-skills to develop
- [ ] **Practice patterns**: How experts recommend building the skill
- [ ] **Common mistakes**: What learners typically get wrong
- [ ] **Resources**: Best books, courses, communities, mentors
- [ ] **Measurement**: How to know you're improving

Deep (add 4-6 more):
- [ ] **Deliberate practice**: Specific exercises for each competency level
- [ ] **Learning path**: Recommended sequence and time estimates
- [ ] **Expert interviews**: What top practitioners say about mastery
- [ ] **Adjacent skills**: What complementary skills accelerate growth
- [ ] **Plateaus**: Known sticking points and how to break through
- [ ] **Community**: Where practitioners gather, share, and learn

### General Inquiry

Use when: the topic doesn't fit other categories. Build a custom checklist.

Approach:
1. Identify the core question
2. Break it into 3-4 facets (what, why, how, so-what)
3. For each facet, identify 1-2 specific aspects to cover
4. Ensure at least one item covers practitioner/real-world perspective
5. Ensure at least one item covers trade-offs or limitations

## Checklist Quality Rules

1. **Specific, not vague**: "How does event sourcing handle schema evolution?" not "Event sourcing details"
2. **Independently verifiable**: Each item should be answerable from web sources
3. **Ordered by dependency**: If understanding X requires Y, Y comes first
4. **Balanced perspective**: Include items for both benefits AND limitations
5. **Practical**: At least 2 items should connect to actionable implications
