---
description: Create new project-local slash commands with templates and best practices
---

You are helping the user create a new custom slash command for this project.

# Slash Command Architecture

## How Slash Commands Work

When a user types `/command-name` or when this tool invokes a slash command:
1. Claude receives `<command-message>command-name is running…</command-message>`
2. The content of `.claude/commands/command-name.md` is injected as a prompt
3. Claude processes the prompt and responds accordingly
4. The command expansion happens in the next message after invocation

## File Structure

```
.claude/
└── commands/
    ├── command-name.md     # Your custom command
    └── another-cmd.md      # Another command
```

**Naming conventions:**
- Filename (without .md) becomes the command name
- Use lowercase with hyphens: `code-review.md` → `/code-review`
- Keep names short but descriptive (2-3 words max)
- Avoid special characters except hyphens

## Frontmatter Format

Every slash command should start with YAML frontmatter:

```markdown
---
description: Brief one-line description of what this command does
---
```

The description:
- Appears in command lists and autocomplete
- Should be concise (under 80 characters)
- Describes the action/purpose, not implementation
- Examples: "Review code for bugs and improvements", "Generate unit tests"

## Best Practices for Effective Commands

### 1. Be Specific and Directive
✅ **Good**: "Analyze this codebase and create a comprehensive test coverage report. Include percentage covered, untested critical paths, and recommendations."

❌ **Bad**: "Help with testing"

### 2. Provide Context
Include relevant constraints, requirements, or project-specific details:
- Technology stack expectations
- Code style preferences
- Testing frameworks in use
- Output format requirements

### 3. Structure Complex Commands
For multi-step workflows, use numbered lists or sections:

```markdown
1. First, analyze the current implementation
2. Then, identify areas for improvement
3. Finally, propose specific refactorings with code examples
```

### 4. Use Action-Oriented Language
Start with strong verbs: "Analyze", "Generate", "Review", "Refactor", "Document", "Deploy"

### 5. Specify Output Format
Tell Claude exactly how to format the response:
- Markdown structure (headers, lists, code blocks)
- Whether to create files or just provide recommendations
- Whether to use tools (Write, Edit) or just plan

### 6. Leverage Project Context
Reference project-specific files, conventions, or architecture:
- Point to existing patterns to follow
- Reference CLAUDE.md guidelines
- Mention tech stack from deno.json or package files

### 7. Make Commands Composable
Design commands that work well together:
- One command generates, another reviews
- Keep single responsibility principle
- Allow chaining via clear outputs

### 8. Include Examples (When Helpful)
Show expected output format or provide template structure within the command

## Command Templates

### Template 1: Code Review Command

```markdown
---
description: Perform comprehensive code review with security, performance, and maintainability checks
---

Review the code files that are currently open or that the user specifies.

**Review criteria:**
1. **Correctness**: Logic errors, edge cases, potential bugs
2. **Security**: Input validation, authentication, injection risks
3. **Performance**: Algorithmic complexity, unnecessary operations, caching opportunities
4. **Maintainability**: Code clarity, naming, documentation, duplication
5. **Testing**: Test coverage, test quality, missing test cases

**Output format:**
- Use severity levels: 🔴 Critical, 🟡 Warning, 🟢 Suggestion
- Provide specific line numbers when possible
- Include code snippets showing the issue and proposed fix
- Prioritize findings by severity

**Tech stack context:**
This is a [YOUR_TECH_STACK] project. Apply relevant best practices.
```

### Template 2: Test Generation Command

```markdown
---
description: Generate comprehensive unit and integration tests
---

Generate tests for the code the user specifies or currently has open.

**Requirements:**
1. Use [YOUR_TESTING_FRAMEWORK] (e.g., Deno test, Jest, pytest)
2. Follow existing test patterns in `/tests/` directory
3. Achieve 90%+ code coverage
4. Include edge cases and error scenarios
5. Use descriptive test names that document behavior

**Test structure:**
- Group related tests with describe/test blocks
- Use table-driven tests for multiple similar cases
- Mock external dependencies appropriately
- Test both success and failure paths

**Output:**
Create test files adjacent to source or in `/tests/` following project structure.
```

### Template 3: Deployment Checklist Command

```markdown
---
description: Execute pre-deployment checklist and validation
---

Run through the complete deployment checklist for this project.

**Checklist:**
1. ✅ All tests pass: Run `[YOUR_TEST_COMMAND]`
2. ✅ Code is formatted: Run `[YOUR_FORMAT_COMMAND]`
3. ✅ Linter passes: Run `[YOUR_LINT_COMMAND]`
4. ✅ Type checking passes: Run `[YOUR_TYPECHECK_COMMAND]`
5. ✅ Build succeeds: Run `[YOUR_BUILD_COMMAND]`
6. ✅ Security scan: Check dependencies for vulnerabilities
7. ✅ Environment variables: Verify all required env vars are documented
8. ✅ Database migrations: Check for pending migrations
9. ✅ API contracts: Ensure no breaking changes
10. ✅ Documentation: Update changelog and version numbers

**For each item:**
- Run the command
- Report success/failure
- If failure, explain the issue and how to fix it

**Final step:**
If all checks pass, provide the deployment command to execute.
```

### Template 4: Refactoring Guide Command

```markdown
---
description: Analyze code and provide strategic refactoring recommendations
---

Analyze the specified code for refactoring opportunities.

**Analysis areas:**
1. **Code smells**: Long methods, large classes, duplicate code, complex conditionals
2. **Design patterns**: Where patterns would improve structure
3. **SOLID violations**: Single responsibility, open/closed, etc.
4. **Performance**: Inefficient algorithms or data structures
5. **Testability**: Hard-to-test code that needs restructuring

**For each recommendation:**
- Explain why the refactoring is valuable
- Estimate effort (small/medium/large)
- Provide before/after code examples
- Identify risks and mitigation strategies
- Suggest incremental steps if large refactoring

**Prioritization:**
Order recommendations by impact vs. effort ratio.
```

### Template 5: Documentation Generator Command

```markdown
---
description: Generate comprehensive documentation for code, APIs, or architecture
---

Generate documentation for the code or system the user specifies.

**Documentation types:**
1. **Code documentation**: JSDoc/docstrings for functions and classes
2. **API documentation**: Endpoints, parameters, responses, examples
3. **Architecture docs**: System overview, component diagrams, data flow
4. **README**: Purpose, setup, usage, examples
5. **Changelog**: Version history and changes

**Content requirements:**
- Clear, concise explanations
- Code examples for non-trivial usage
- Link related concepts
- Include troubleshooting tips
- Keep under [YOUR_MAX_LENGTH] lines for README

**Format:**
Use Markdown with appropriate headers, code blocks, and lists.
```

### Template 6: Debugging Assistant Command

```markdown
---
description: Debug issues with systematic analysis and solution proposals
---

Help debug the issue the user describes or is experiencing.

**Debugging process:**
1. **Understand the problem**: Ask clarifying questions if needed
2. **Reproduce**: Identify steps to reproduce (if not already clear)
3. **Analyze**:
   - Check error messages and stack traces
   - Review relevant code sections
   - Check logs, configs, environment
4. **Hypothesize**: Form theories about root cause
5. **Test**: Verify hypotheses with targeted investigation
6. **Solve**: Provide fix with explanation

**Output format:**
- Root cause explanation
- Immediate fix (code changes)
- Prevention strategy (how to avoid in future)
- Related issues to check

**Investigation tools:**
Use Read, Grep, and Bash tools to gather information. Be systematic.
```

### Template 7: Feature Planning Command

```markdown
---
description: Plan and design new feature implementation with technical specifications
---

Plan the implementation of the feature the user describes.

**Planning phases:**
1. **Requirements analysis**: Clarify functional and non-functional requirements
2. **Design**: Architecture, data models, API contracts
3. **Implementation steps**: Break down into small, testable increments
4. **Testing strategy**: Unit, integration, e2e test plans
5. **Rollout plan**: Deployment approach, feature flags, monitoring

**Design artifacts:**
- Data schema changes (if applicable)
- API endpoint specifications
- Component/module structure
- Sequence diagrams for complex flows

**Implementation task list:**
Create ordered, atomic tasks following incremental development (from CLAUDE.md).

**Considerations:**
- Backward compatibility
- Performance implications
- Security considerations
- Error handling
```

## Creating Your New Command

**Step 1: Determine command purpose**
What specific task or workflow should this command automate or assist with?

**Step 2: Choose a name**
Pick a clear, concise name (2-3 words max, use hyphens).

**Step 3: Draft the prompt**
Write what Claude should do when this command is invoked:
- Be specific and directive
- Include context and constraints
- Specify output format
- Reference project-specific conventions

**Step 4: Add frontmatter**
Include the description for discoverability.

**Step 5: Create the file**
Save as `.claude/commands/your-command-name.md`

**Step 6: Test**
Try running `/your-command-name` and iterate on the prompt.

## Command Scoping

**Project-local commands** (`.claude/commands/`):
- Specific to this project
- Not available in other projects
- Can reference project structure, tech stack, conventions
- Version controlled with the project

**Global commands** (`~/.claude/commands/`):
- Available in all projects
- Should be project-agnostic
- Use for general workflows (e.g., /explain, /optimize)
- Not shown here, but same file structure

## Tips and Tricks

1. **Start simple**: Create a basic version, then iterate based on usage
2. **Reference existing patterns**: Tell Claude to "follow patterns in /tests/ directory"
3. **Use conditionals**: "If the user provides a file path, analyze that. Otherwise, analyze open files."
4. **Combine with agents**: "Use the Task tool with subagent_type=Explore to..."
5. **Set expectations**: "Provide a concise summary (max 4 lines)" or "Be comprehensive"
6. **Make it conversational**: Commands can ask follow-up questions if needed

## Example Usage

After creating a command named `review.md`:

```
User: /review
Claude: <command-message>review is running…</command-message>
        [Claude receives the review.md content and executes it]
```

## Now Create Your Command

Ask the user:
1. What should this command do?
2. What should it be named?
3. Should it follow one of the templates above, or be custom?

Then help them create the command file with appropriate content based on their answers.