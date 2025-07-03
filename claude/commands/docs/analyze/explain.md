# /explain

Provide comprehensive explanation of code, architecture, or technical concepts with deep context and examples.

## Usage

```
/explain [code snippet, file path, or concept]
```

## Explanation Process

### 1. Code Analysis

When explaining code:

```bash
# Understand the context
rg "function_name|class_name" -B 5 -A 5
fd "test.*function_name" --type f
rg "import.*module|require.*module" 

# Trace usage patterns
rg "function_name\(" -A 2 -B 2
```

### 2. Explanation Structure

#### Overview

- **Purpose**: What this code/concept achieves
- **Context**: Where it fits in the larger system
- **Dependencies**: What it relies on

#### Detailed Breakdown

```[language]
// Original code with inline annotations
function example(param1, param2) {  // [1] Function signature
    const result = process(param1);  // [2] Processing step
    return transform(result, param2); // [3] Transformation
}
```

**Line-by-line explanation:**

1. Function accepts two parameters for...
2. First parameter undergoes processing to...
3. Result is transformed using second parameter...

#### How It Works

1. **Input Flow**
   - Data enters through...
   - Validation occurs at...
   - Preprocessing includes...

2. **Core Logic**
   - Algorithm/pattern used
   - Time/space complexity
   - Edge cases handled

3. **Output Generation**
   - Result format
   - Error conditions
   - Side effects

#### Real-World Analogy

Compare to familiar concept (e.g., "Think of it like a postal sorting facility where...")

#### Common Patterns

- Design pattern identification
- Idioms and conventions
- Best practices demonstrated

#### Usage Examples

```[language]
// Basic usage
const result = example("input", { option: true });

// Advanced usage with error handling
try {
    const result = await example(data, config);
    console.log(result);
} catch (error) {
    handleError(error);
}
```

#### Related Concepts

- Links to similar functionality
- Alternative approaches
- Evolution from older patterns

#### Gotchas & Tips

- Common mistakes to avoid
- Performance considerations
- Security implications
- Testing strategies

### 3. Visual Aids (when applicable)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Input     │────▶│  Process    │────▶│   Output    │
└─────────────┘     └─────────────┘     └─────────────┘
        │                   │                    │
        ▼                   ▼                    ▼
   Validation          Transform             Format
```

### 4. Learning Resources

- Official documentation references
- Tutorial recommendations
- Deep-dive articles
- Video explanations

## Example Explanations

### Example 1: Rust Lifetime

```
/explain 'fn longest<'a>(x: &'a str, y: &'a str) -> &'a str'
```

### Example 2: Architecture Pattern

```
/explain event-driven architecture in our microservices
```

### Example 3: Complex Algorithm

```
/explain the rate limiting implementation in src/middleware/throttle.rs
```

## Guidelines

- Start with the "why" before the "how"
- Use progressive disclosure (simple → detailed)
- Include concrete examples
- Connect to familiar concepts
- Highlight important edge cases
- Explain trade-offs and design decisions
