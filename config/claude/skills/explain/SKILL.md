---
name: explain
description: >
  Explain code, functions, modules, or programming concepts with structured
  walkthroughs covering purpose, patterns, data flow, edge cases, and
  performance. Use when explaining code, understanding how something works,
  learning a concept, or walking through a codebase. Keywords: explain, how
  does this work, what does this do, walkthrough, understand, code explanation,
  concept, teach, learn
---

# Explanation

Explain the code, concept, or topic: **$ARGUMENTS**

## Two Modes

### Code Explanation

Structured walkthrough with:
1. **Purpose & Context** — what it does, why it exists, scope
2. **Key Concepts** — patterns, algorithms, techniques, principles
3. **Code Flow** — step-by-step execution with code snippets and annotations
4. **Dependencies & Integration** — libraries, internal modules, APIs, contracts
5. **Data Transformations** — input → processing → output with intermediate states
6. **Edge Cases & Error Handling** — validation, error paths, boundary conditions
7. **Performance Characteristics** — time/space complexity, bottlenecks, optimizations
8. **Gotchas & Non-Obvious Behavior** — subtle bugs, implicit assumptions, side effects

### Concept Explanation

Comprehensive overview with:
1. **Definition** — clear, precise definition in simple terms
2. **The Problem It Solves** — challenges without it, why it was created
3. **How It Works** — core mechanism, key components, step-by-step operation
4. **When to Use It** — good fit, poor fit, alternatives
5. **Practical Examples** — simple illustrative + real-world production-like
6. **Common Patterns** — typical usage, best practices, anti-patterns
7. **Trade-offs** — advantages, disadvantages, complexity
8. **Related Concepts** — similar/complementary concepts, historical context

See `references/explanation-templates.md` for full section templates, code annotation format, and visual aids guide.

## Depth Levels

- **Quick overview** — 3-5 sentences, core concept only
- **Standard** — full structure above, balanced detail *(default)*
- **Deep dive** — implementation details, algorithm analysis, full edge cases

## Output Style

**Clarity:** Plain language, break complex ideas into chunks, use analogies for abstract concepts.

**Precision:** Technically accurate, distinguish "always true" from "usually true".

**Engagement:** Show with code examples, use ASCII diagrams for architecture/flow.

**Completeness:** Cover edge cases and limitations, provide context for deeper learning.

## Follow-up Prompts

End each explanation with:

```
Would you like me to:
- Explain a specific part in more detail?
- Show alternative implementations?
- Discuss related concepts (e.g., X, Y, Z)?
- Review performance implications?
- Suggest improvements or refactorings?
```
