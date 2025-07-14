# Translating Claude Commands to VS Code Prompt Files

This guide explains how to convert Claude command files into VS Code prompt files (`.prompt.md`), adapting for VS Code's capabilities and limitations.

## Key Differences Between Claude and VS Code

### What VS Code Prompt Files **Cannot** Do

- ❌ Execute bash commands dynamically (`!` syntax)
- ❌ Deploy parallel sub-agents
- ❌ Use `/tmp/` directories for session state
- ❌ Generate session IDs or timestamps
- ❌ List or restrict allowed tools
- ❌ Execute arbitrary shell commands

### What VS Code Prompt Files **Can** Do

- ✅ Reference specific files with `#file:path/to/file.ext`
- ✅ Provide structured prompts with clear goals
- ✅ Include requirements and constraints
- ✅ Reference multiple related files for context
- ✅ Create reusable templates for common tasks

## Translation Strategy

### 1. Remove Claude-Specific Elements

**From Claude commands, remove:**

- `---` frontmatter with `allowed-tools` and `description`
- Session ID generation (`!`gdate +%s%N``)
- Dynamic bash command execution (`!`command``)
- Sub-agent deployment instructions
- `/tmp/` directory references
- Tool restriction lists

### 2. Convert Dynamic Context to Static References

**Instead of dynamic context gathering:**

```markdown
<!-- Claude style (remove) -->

- Project type: !`fd -t f 'package.json|deno.json|Cargo.toml' -d 1`
- Git status: !`git status --porcelain`
- Recent changes: !`git log --oneline -5`
```

**Use static file references:**

```markdown
<!-- VS Code style (use) -->

#file:package.json #file:deno.json #file:Cargo.toml #file:.gitignore #file:README.md
```

### 3. Restructure Sub-Agent Tasks as Sequential Steps

**Instead of parallel sub-agents:**

```markdown
<!-- Claude style (remove) -->

IMMEDIATELY launch 8 specialized parallel review agents:

- **Agent 1: Architecture Analysis**: ...
- **Agent 2: Security Assessment**: ...
```

**Use structured sequential approach:**

```markdown
<!-- VS Code style (use) -->

## Analysis Steps

Follow these steps in order:

1. **Architecture Analysis**

   - Analyze component relationships and design patterns
   - Focus on: [specific areas]
   - Output: [expected deliverable]

2. **Security Assessment**
   - Review authentication and authorization patterns
   - Focus on: [specific areas]
   - Output: [expected deliverable]
```

## Translation Templates

### Basic Command Translation

**Claude Command Structure:**

```markdown
---
allowed-tools: Read, Write, Bash(git:*)
description: Review code for issues
---

# /review

## Context

- Session ID: !`gdate +%s%N`
- Git status: !`git status --porcelain`

## Your task

Analyze the code for issues...
```

**VS Code Prompt File:**

```markdown
Your goal is to review code for potential issues and improvements.

## Requirements

- Analyze code quality, security, and performance
- Provide specific recommendations with examples
- Focus on maintainability and best practices

## Context Files

#file:package.json #file:tsconfig.json #file:README.md

Include relevant source files you want to analyze.
```

### Complex Multi-Step Command Translation

**For commands with multiple phases:**

```markdown
Your goal is to [main objective].

Ask for [required inputs] if not provided.

## Analysis Approach

### Step 1: Initial Assessment

- [First set of tasks]
- Focus on: [specific areas]

### Step 2: Detailed Analysis

- [Second set of tasks]
- Consider: [important factors]

### Step 3: Recommendations

- [Final deliverables]
- Format: [output format]

## Requirements

- [List specific requirements]
- [Quality standards]
- [Output format expectations]

## Context Files

#file:relevant/file1.ts #file:relevant/file2.ts #file:docs/architecture.md #file:tests/example.test.ts
```

## File Reference Strategies

### 1. Core Project Files

Always include foundational files:

```markdown
#file:package.json #file:deno.json #file:Cargo.toml #file:go.mod #file:README.md #file:tsconfig.json #file:.gitignore
```

### 2. Domain-Specific References

Include relevant files based on the task:

**For code generation:**

```markdown
#file:src/components/BaseComponent.tsx #file:src/types/common.ts #file:src/utils/helpers.ts
```

**For testing:**

```markdown
#file:src/test-utils.ts #file:tests/example.test.ts #file:jest.config.js
```

**For documentation:**

```markdown
#file:docs/api.md #file:docs/architecture.md #file:CONTRIBUTING.md
```

### 3. Pattern Files

Reference examples of desired patterns:

```markdown
#file:src/components/ExampleComponent.tsx #file:src/hooks/useExample.ts #file:src/services/ExampleService.ts
```

## Common Translation Patterns

### 1. Context Loading Commands

**Claude:** Dynamic context gathering\
**VS Code:** Static file references with instructions

```markdown
Your goal is to load and analyze project context.

## Context Analysis

Review the following files to understand the project structure:

#file:package.json #file:README.md #file:src/index.ts #file:docs/architecture.md

Provide a summary of:

- Project type and technologies used
- Key components and their relationships
- Development workflow and build process
```

### 2. Code Generation Commands

**Claude:** Template with dynamic context\
**VS Code:** Template with example references

```markdown
Your goal is to generate a new [component type].

Ask for the [component name] and [requirements] if not provided.

## Generation Requirements

- Follow existing patterns from referenced files
- Include proper TypeScript types
- Add appropriate error handling
- Follow project conventions

## Reference Files

#file:src/components/ExampleComponent.tsx #file:src/types/component.ts #file:src/styles/components.css
```

### 3. Analysis Commands

**Claude:** Parallel sub-agents\
**VS Code:** Sequential structured analysis

```markdown
Your goal is to perform comprehensive code analysis.

## Analysis Framework

### 1. Structural Analysis

- Component architecture and organization
- Dependency relationships and coupling
- Code organization and modularity

### 2. Quality Analysis

- Code complexity and readability
- Error handling and edge cases
- Testing coverage and quality

### 3. Security Analysis

- Input validation and sanitization
- Authentication and authorization
- Data exposure and privacy

## Context Files

#file:src/index.ts #file:src/components/ #file:tests/ #file:package.json
```

## Best Practices

### 1. File Selection

- **Be specific**: Reference exact files rather than directories
- **Include examples**: Reference files that show desired patterns
- **Add context**: Include configuration and documentation files
- **Stay focused**: Don't reference too many files (aim for 5-10 relevant files)

### 2. Prompt Structure

- **Clear goal**: Start with a clear, actionable goal statement
- **Structured requirements**: Use lists and sections for clarity
- **Context before action**: Provide context files before asking for work
- **Specific outputs**: Define exactly what you want produced

### 3. Naming Conventions

- Use descriptive filenames: `Generate React Component.prompt.md`
- Group by domain: `code-review/Security Analysis.prompt.md`
- Version when needed: `Generate Component v2.prompt.md`

### 4. Template Reusability

- Make prompts generic enough to reuse
- Use placeholder language like "component name" or "feature type"
- Include clear instructions for customization
- Document expected inputs and outputs

## Example Translations

### Simple Command Translation

**Claude `/generate-component`** becomes **`Generate React Component.prompt.md`**

### Complex Command Translation

**Claude `/review` with sub-agents** becomes **`Comprehensive Code Review.prompt.md`** with structured analysis steps

### Context Command Translation

**Claude `/context-load-typescript`** becomes **`TypeScript Project Analysis.prompt.md`** with relevant file references

By following these patterns, you can effectively translate your Claude commands into powerful, reusable VS Code prompt files that work within the platform's capabilities.
