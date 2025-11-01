---
description: Interactive wizard to create new agent skills for Claude Code
---

You are helping the user create a new agent skill for this project.

Official reference: https://docs.claude.com/en/docs/claude-code/skills — always read this to understand proper skill formatting

You can see proper examples in https://github.com/anthropics/skills, such as https://raw.githubusercontent.com/anthropics/skills/refs/heads/main/skill-creator/SKILL.md

# Overview

Agent Skills are modular capabilities that Claude automatically uses when relevant to the user's request. Unlike slash commands (user-invoked with `/command`), skills are **model-invoked**—Claude autonomously decides when to activate them based on the skill's description matching the context.

Skills use a progressive loading system:
1. **Metadata** (always loaded): Name and description for discovery
2. **Instructions** (loaded when triggered): Main SKILL.md guidance
3. **Resources** (loaded as needed): Scripts, templates, reference docs

# File Structure

Skills are organized in directories:
```
.claude/skills/<skill-name>/
├── SKILL.md (required - main instructions)
├── REFERENCE.md (optional - detailed guidance)
├── scripts/ (optional - executable helpers)
└── templates/ (optional - file templates)
```

**Location options:**
- `.claude/skills/` - Project-specific, shared with team (git-tracked)

# Skill Creation Process

Follow this interactive workflow to create a new skill:

## STEP 1: Understand Requirements

Ask the user these questions using the AskUserQuestion tool:

1. **What capability should this skill provide?**
   - Header: "Capability"
   - Options:
     - "Code Analysis" / "Analyze code for patterns, quality, security issues"
     - "Test Generation" / "Generate comprehensive test suites"
     - "Documentation" / "Create docs, READMEs, API documentation"
     - "Data Processing" / "Process files like PDFs, CSVs, JSON"
   - Multi-select: false

2. **Skill scope - simple or advanced?**
   - Header: "Complexity"
   - Options:
     - "Simple (single SKILL.md)" / "Just instructions, no scripts or templates"
     - "Advanced (with resources)" / "Include scripts, templates, or reference docs"
   - Multi-select: false

3. **Should tools be restricted?**
   - Header: "Tool Access"
   - Options:
     - "Full access" / "Skill can use all available tools"
     - "Restricted" / "Limit to specific tools (Read, Grep, etc.)"
   - Multi-select: false

## STEP 2: Generate Skill Name

Based on capability, suggest an appropriate name:
- For "Code Analysis" → suggest: `code-quality-analyzer`
- For "Test Generation" → suggest: `test-suite-generator`
- For "Documentation" → suggest: `doc-generator`
- For "Data Processing" → suggest: `data-processor`
- For custom capability → suggest descriptive kebab-case name

**Naming rules:**
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- Descriptive (what it does, not how)
- Examples: `pdf-text-extractor`, `api-doc-generator`, `test-coverage-analyzer`

## STEP 3: Craft the Description

The description is CRITICAL—it determines when Claude activates the skill. Must include:

1. **What it does** (functionality)
2. **When to use it** (trigger conditions)
3. **Trigger keywords** (terms users might mention)

**Template structure:**
```
[Primary function]. [Secondary capabilities]. Use when [trigger scenarios]. Keywords: [comma-separated terms].
```

**Examples of good descriptions:**

✅ "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files, documents, or form processing. Keywords: PDF, extract, document, form, merge"

✅ "Generate comprehensive unit and integration tests with high coverage. Use when adding tests, improving coverage, or implementing TDD. Keywords: test, testing, coverage, unit test, integration test, TDD"

✅ "Analyze code for security vulnerabilities, performance issues, and maintainability problems. Use when reviewing code or conducting security audits. Keywords: security, vulnerability, code review, audit, performance"

❌ "Helps with documents" (too vague)
❌ "Processes things" (no triggers)

## STEP 4: Generate Skill Content

Based on the selected capability, create the skill using one of these templates:

### Code Analysis Skill Template

**SKILL.md:**
```markdown
---
name: code-quality-analyzer
description: Analyze code for security vulnerabilities, performance issues, code smells, and maintainability problems. Use when reviewing code, conducting security audits, or improving code quality. Keywords: security, vulnerability, code review, audit, performance, code smell, refactor
---

# Code Quality Analyzer

Analyzes code comprehensively across multiple quality dimensions.

## Instructions

When activated, perform the following analysis:

### 1. Security Analysis
- Input validation and sanitization
- Authentication and authorization checks
- Injection vulnerabilities (SQL, XSS, command injection)
- Sensitive data exposure
- Insecure dependencies

### 2. Performance Analysis
- Algorithmic complexity (O(n²) and worse)
- Unnecessary loops or operations
- Memory leaks or excessive allocations
- Database query optimization opportunities
- Caching opportunities

### 3. Maintainability
- Code smells (long methods, large classes, duplicate code)
- Naming conventions and clarity
- Comment quality and documentation
- SOLID principle violations
- Separation of concerns

### 4. Testing
- Test coverage gaps
- Edge cases not covered
- Flaky test patterns
- Missing error scenario tests

## Output Format

Present findings organized by severity:

**🔴 Critical Issues** (security vulnerabilities, major bugs)
**🟡 Warnings** (performance issues, maintainability concerns)
**🟢 Suggestions** (improvements, best practices)

For each issue:
- **File:Line**: `src/auth.ts:45`
- **Issue**: Clear description
- **Impact**: Why it matters
- **Fix**: Code example showing correction

## Project Context

This is a Deno + Fresh + Preact project. Apply Deno/Fresh-specific best practices.
```

### Test Generation Skill Template

**SKILL.md:**
```markdown
---
name: test-suite-generator
description: Generate comprehensive unit and integration tests with high coverage. Use when adding tests, improving test coverage, implementing TDD, or ensuring code quality. Keywords: test, testing, coverage, unit test, integration test, TDD, test-driven
---

# Test Suite Generator

Creates comprehensive test suites following TDD best practices.

## Instructions

### 1. Analyze Code Under Test
- Identify all public interfaces and functions
- Map dependencies and side effects
- List edge cases and error conditions
- Check existing test coverage

### 2. Generate Test Structure

**For Deno projects:**
```typescript
import { assertEquals, assertThrows } from "@std/assert";
import { describe, it } from "@std/testing/bdd";

describe("ComponentName", () => {
  it("should handle normal case", () => {
    // Arrange
    // Act
    // Assert
  });

  it("should handle edge case", () => {
    // Test edge case
  });

  it("should throw on invalid input", () => {
    assertThrows(() => {
      // Test error condition
    });
  });
});
```

### 3. Test Coverage Goals
- 90%+ code coverage
- All public APIs tested
- All error paths tested
- Edge cases covered
- Integration points mocked appropriately

### 4. Test Organization
- Group related tests with describe blocks
- Use table-driven tests for multiple similar cases
- One assertion concept per test
- Descriptive test names (behavior, not implementation)

## Output

Create test files following project structure:
- Adjacent to source: `component.test.ts`
- Or in `/tests/` directory matching structure

Use Write tool to create test files with complete test suite.
```

### Documentation Generation Skill Template

**SKILL.md:**
```markdown
---
name: documentation-generator
description: Generate comprehensive documentation including READMEs, API docs, JSDoc comments, and architecture guides. Use when documenting code, creating READMEs, or writing API documentation. Keywords: documentation, docs, README, API docs, JSDoc, comments, guide
---

# Documentation Generator

Creates clear, comprehensive documentation for code and systems.

## Instructions

### 1. Determine Documentation Type

**Code Documentation (JSDoc):**
- Function/method signatures
- Parameter descriptions with types
- Return value descriptions
- Usage examples for complex functions
- Error conditions

**README Files:**
- Purpose (1-2 sentences)
- Quick start (single command if possible)
- Key commands/usage
- Project structure (if complex)
- Keep under 50 lines total

**API Documentation:**
- Endpoint descriptions
- Request/response schemas
- Authentication requirements
- Example requests and responses
- Error codes and meanings

**Architecture Docs:**
- System overview diagram (ASCII)
- Component responsibilities
- Data flow
- Key architectural decisions

### 2. Documentation Standards

- **Clarity**: Write for developers unfamiliar with the code
- **Examples**: Include concrete usage examples
- **Conciseness**: Be thorough but not verbose
- **Format**: Use proper Markdown formatting
- **Maintenance**: Include version/date information

### 3. Project-Specific Guidelines

From CLAUDE.md:
- README max 50 lines
- Essential sections only
- Single quick-start command when possible
- No excessive emojis

## Output

Use Write or Edit tools to create/update documentation files.
```

### Data Processing Skill Template

**SKILL.md:**
```markdown
---
name: data-file-processor
description: Process and transform data files including JSON, CSV, YAML, and structured text. Use when working with data files, transforming formats, or extracting information. Keywords: JSON, CSV, YAML, data, parse, transform, extract
allowed-tools: Read, Write, Bash, Grep
---

# Data File Processor

Processes various data file formats with transformations and analysis.

## Instructions

### 1. Identify File Format
- JSON: Parse and validate structure
- CSV: Handle headers, delimiters, escaping
- YAML: Parse configuration files
- Text: Pattern extraction and transformation

### 2. Common Operations

**Validation:**
- Schema validation
- Format checking
- Data integrity verification

**Transformation:**
- Format conversion (JSON ↔ CSV ↔ YAML)
- Field mapping and renaming
- Data filtering and aggregation
- Normalization

**Extraction:**
- Specific field extraction
- Pattern matching
- Aggregation and statistics

### 3. Processing Approach

```bash
# Use jq for JSON
jq '.field | map(select(.status == "active"))' input.json

# Use standard tools for CSV
awk -F',' '{print $1,$3}' data.csv

# YAML processing
yq eval '.services.*.image' docker-compose.yml
```

### 4. Output Format

- Preserve data integrity
- Clear transformation logs
- Validate output format
- Provide summary statistics

## Error Handling

- Invalid format detection
- Missing field handling
- Data type mismatches
- Encoding issues
```

## STEP 5: Create Skill Directory and Files

1. Create directory: `.claude/skills/<skill-name>/`
2. Create `SKILL.md` with the generated template
3. If advanced scope:
   - Create `REFERENCE.md` for detailed docs
   - Create `scripts/` for helper scripts
   - Create `templates/` for file templates
4. Customize based on:
   - Project tech stack (deno.json, CLAUDE.md)
   - Existing patterns in codebase
   - User's specific requirements
   - Tool restrictions if specified

## STEP 6: Add Tool Restrictions (if needed)

If user chose "Restricted" tools, add to frontmatter:

```yaml
---
name: skill-name
description: Description here
allowed-tools: Read, Grep, Glob, Bash(jq:*), Bash(yq:*)
---
```

Common tool combinations:
- **Read-only analysis**: `Read, Grep, Glob`
- **Data processing**: `Read, Write, Bash(jq:*), Bash(yq:*)`
- **Code review**: `Read, Grep, Glob`
- **File generation**: `Read, Write, Grep`

## STEP 7: Confirm and Test

After creating the skill:

1. Show the created file structure
2. Explain the skill's description and triggers
3. Provide example user requests that would activate it:
   - "Can you review this code for security issues?" → code-quality-analyzer
   - "I need tests for this module" → test-suite-generator
   - "Generate a README for this project" → documentation-generator
   - "Parse this JSON file and extract the IDs" → data-file-processor
4. Suggest testing with a relevant request

# Best Practices for Skills

When generating skills, ensure:

✅ **Descriptive names** - What it does, not how (max 64 chars)
✅ **Rich descriptions** - Functionality + triggers + keywords (max 1024 chars)
✅ **Clear instructions** - Step-by-step guidance for Claude
✅ **Project context** - Reference tech stack, conventions, CLAUDE.md
✅ **Structured output** - Specify format, tools, file locations
✅ **Examples** - Show expected patterns and formats
✅ **Tool specification** - Mention which tools to use
✅ **Progressive disclosure** - Main SKILL.md + optional REFERENCE.md

# Skill Activation

Skills activate when user requests match the description. Good trigger phrases:

- "Review this code" → code-quality-analyzer
- "Add tests" / "Improve coverage" → test-suite-generator
- "Document this" / "Create README" → documentation-generator
- "Parse this JSON" / "Transform CSV" → data-file-processor

---

**Now execute the workflow above, starting with STEP 1 to gather requirements from the user.**
