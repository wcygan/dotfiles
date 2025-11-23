---
description: Explain code or programming concepts with clarity and depth
---

Explain the code, concept, or topic the user specifies.

# Explanation Approach

## For Code Explanations

Provide a structured walkthrough covering:

### 1. Purpose & Context
- **What it does**: High-level description in 1-2 sentences
- **Why it exists**: Problem being solved or requirement fulfilled
- **Scope**: Boundaries of what this code handles

### 2. Key Concepts
- **Patterns**: Design patterns, architectural patterns used
- **Algorithms**: Core algorithms or data structures employed
- **Techniques**: Notable programming techniques or idioms
- **Principles**: SOLID, DRY, or other principles demonstrated

### 3. Code Flow
Step-by-step walkthrough of execution:
```
1. Entry point and initial state
2. Main processing steps (with code snippets)
3. Decision points and branching logic
4. Side effects (I/O, state changes, events)
5. Return values and exit conditions
```

For each step, show relevant code snippet with inline annotations:
```language
// Step 2: Validate input and set defaults
if (!config.timeout) {
  config.timeout = 30000;  // Default 30s timeout
}
```

### 4. Dependencies & Integration
- **External libraries**: What they provide and why they're used
- **Internal modules**: How this code fits into the larger system
- **APIs consumed**: External services or interfaces used
- **Contracts**: Interfaces implemented, types satisfied

### 5. Data Transformations
- **Input**: What data comes in (types, formats, constraints)
- **Processing**: How data is transformed (show intermediate states)
- **Output**: What data goes out (types, formats, guarantees)

Example:
```
Input:  User[] (array of user objects)
  ↓
Filter: active users only
  ↓
Map:    extract email addresses
  ↓
Output: string[] (array of email strings)
```

### 6. Edge Cases & Error Handling
- **Validation**: Input validation and constraints
- **Error paths**: How errors are detected and handled
- **Boundary conditions**: Empty inputs, nulls, limits
- **Failure modes**: What happens when things go wrong

### 7. Performance Characteristics
- **Time complexity**: Big-O analysis of key operations
- **Space complexity**: Memory usage patterns
- **Bottlenecks**: Potential performance concerns
- **Optimizations**: Techniques used to improve performance

### 8. Gotchas & Non-Obvious Behavior
- **Subtle bugs**: Common misunderstandings or pitfalls
- **Implicit assumptions**: Preconditions not explicitly checked
- **Side effects**: Non-obvious state changes or mutations
- **Concurrency**: Thread safety, race conditions, ordering

## For Concept Explanations

Provide a comprehensive overview covering:

### 1. Definition
Clear, precise definition in simple terms

### 2. The Problem It Solves
- What challenges exist without this concept?
- What pain points does it address?
- Why was it created?

### 3. How It Works
- Core mechanism or principles
- Key components or parts
- Step-by-step operation

### 4. When to Use It
- **Good fit**: Scenarios where it excels
- **Poor fit**: When to avoid it
- **Alternatives**: Other approaches and trade-offs

### 5. Practical Examples

**Simple example** (minimal, illustrative):
```language
// Basic usage showing core concept
```

**Real-world example** (practical, realistic):
```language
// Production-like code demonstrating actual use
```

### 6. Common Patterns
- Typical usage patterns
- Best practices
- Anti-patterns to avoid

### 7. Trade-offs
- **Advantages**: Benefits and strengths
- **Disadvantages**: Costs and limitations
- **Complexity**: Learning curve and maintenance burden

### 8. Related Concepts
- Similar or complementary concepts
- Historical context or evolution
- Modern alternatives

# Output Style

**Clarity:**
- Use plain language, avoid jargon (or define it when used)
- Break complex ideas into digestible chunks
- Use analogies for abstract concepts

**Precision:**
- Be technically accurate
- Cite sources for claims when relevant
- Distinguish between "always true" and "usually true"

**Engagement:**
- Show, don't just tell (code examples)
- Use visual representations (ASCII diagrams) when helpful
- Build from simple to complex

**Completeness:**
- Cover the full picture, not just happy path
- Address edge cases and limitations
- Provide context for deeper learning

# Code Annotation Format

When explaining code line-by-line, use this format:

```language
function example(input: string): number {
  // 1. Validate input isn't empty
  if (!input) {
    throw new Error("Input required");
  }
  
  // 2. Parse and transform
  const cleaned = input.trim().toLowerCase();
  //                    ↑ Remove whitespace
  //                          ↑ Normalize case
  
  // 3. Compute result using memoized helper
  return cachedCalculation(cleaned);
  //     ↑ O(1) lookup if previously computed
}
```

# Visual Aids

Use ASCII diagrams for architecture, flow, or relationships:

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP POST /api/data
       ↓
┌─────────────┐
│  API Layer  │──→ Validate
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Database   │
└─────────────┘
```

# Depth Levels

Adjust explanation depth based on context:

- **Quick overview**: 3-5 sentences, core concept only
- **Standard**: Full structure above, balanced detail
- **Deep dive**: Include implementation details, algorithm analysis, edge cases

Default to **standard** depth unless user specifies otherwise.

# Follow-up Prompts

End explanation with relevant follow-up questions:

```
Would you like me to:
- Explain a specific part in more detail?
- Show alternative implementations?
- Discuss related concepts (e.g., X, Y, Z)?
- Review performance implications?
- Suggest improvements or refactorings?
```
