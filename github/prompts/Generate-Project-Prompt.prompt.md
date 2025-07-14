Your goal is to generate a new VS Code prompt file (.prompt.md) for this project, stored in `.github/prompts/`.

Ask for the prompt purpose, name, and requirements if not provided.

## VS Code Prompt File Fundamentals

VS Code prompt files (.prompt.md) are reusable prompt templates that work with GitHub Copilot Chat in VS Code. Understanding their mechanics is crucial for effective prompt creation:

### Technical Specifications

- **File Extension**: Must use `.prompt.md` extension
- **Location Options**:
  - Workspace-specific: Anywhere in your project (commonly `.github/prompts/`)
  - Global: `~/Library/Application Support/Code/User/prompts/` (accessible across all workspaces)
- **Availability**: Currently in public preview, only available in VS Code
- **Integration**: Seamlessly works with Copilot Chat interface

### Prompt Structure Components

1. **Goal Statement** (Required): Clear, concise description starting with "Your goal is to..."
2. **User Input Handling**: Use conditional statements like "Ask for X if not provided"
3. **Context References**: Use `#file:` syntax for file references
4. **Instructions**: Step-by-step process or requirements
5. **Dependencies**: Can reference other prompt files using `#file:` syntax

### Context Reference Syntax

- **Single File**: `#file:path/to/file.ext`
- **Multiple Files**: Space-separated on same line or separate lines
- **Absolute Paths**: Use full paths for reliability
- **Relative Paths**: Relative to workspace root
- **Prompt Dependencies**: Can reference other `.prompt.md` files

## Generation Process

### Step 1: Understand the Prompt Requirements

Gather information about:

- **Prompt Purpose**: What specific task should this prompt accomplish?
- **Target Domain**: Code generation, analysis, documentation, testing, etc.
- **Complexity Level**: Simple template, multi-step process, or complex workflow
- **Required Context**: What files or project information does the prompt need?
- **Expected Output**: What should the prompt produce?

### Step 2: Analyze Project Context

Review the project structure to understand:

- Technology stack and frameworks used
- Existing coding patterns and conventions
- Project organization and architecture
- Available configuration files and documentation

### Step 3: Design Prompt Structure

Create a well-structured prompt following VS Code prompt conventions:

1. **Goal Statement** - Must start with "Your goal is to..." for consistency
2. **Conditional Input Gathering** - Use "Ask for X if not provided" pattern
3. **Context References** - List relevant files that provide examples and patterns
4. **Process Definition** - Clear, numbered steps or requirements sections
5. **Output Specifications** - Define expected deliverables and success criteria
6. **Quality Gates** - Include validation and error handling guidance

#### VS Code Prompt Template Structure

```markdown
Your goal is to [specific objective].

Ask for [required inputs] if not provided.

## [Section Name]

[Content organized in clear sections]

### [Subsection]

[Detailed requirements or steps]

#file:path/to/relevant/file.ext #file:path/to/another/file.ext
```

#### Key Structural Elements

- **Imperative Language**: Use direct, actionable language
- **Sectioned Organization**: Break complex prompts into logical sections
- **Reference Placement**: Place file references where most relevant to content
- **Conditional Logic**: Handle optional inputs and edge cases explicitly

### Step 4: Select Relevant Context Files

Include 5-10 relevant file references that provide:

- **Example patterns** - Files showing desired implementation patterns
- **Configuration files** - Project setup and build configuration
- **Documentation** - Architecture docs, API specs, or contributing guides
- **Type definitions** - Shared types and interfaces
- **Test examples** - Testing patterns and utilities

### Step 5: Generate and Validate

Create the prompt file with:

- **Descriptive filename** indicating the prompt's purpose
- **Reusable structure** that works across similar scenarios
- **Clear requirements** and quality standards
- **Proper file references** using absolute paths where needed
- **Validation criteria** for expected outputs

## Prompt Categories

Choose the appropriate category for your prompt:

### Code Generation

- Component creation (React, Vue, etc.)
- API endpoint generation
- Database schema/migration creation
- Configuration file templates
- Test file generation

### Analysis & Review

- Code quality analysis
- Security review workflows
- Performance analysis
- Dependency auditing
- Architecture evaluation

### Documentation

- API documentation generation
- README updates
- Code commenting
- Architecture documentation
- User guide creation

### Testing & Quality

- Test suite generation
- Coverage analysis
- End-to-end test creation
- Performance benchmarking
- Quality gate validation

### Project Management

- Issue analysis and planning
- Feature specification
- Technical debt assessment
- Refactoring planning
- Release preparation

## File Naming Conventions

Use descriptive names that indicate purpose:

- `Generate React Component.prompt.md`
- `API Security Review.prompt.md`
- `Database Migration Planning.prompt.md`
- `Test Coverage Analysis.prompt.md`
- `Documentation Update.prompt.md`

## Quality Standards

Ensure the generated prompt meets VS Code prompt file requirements:

### Technical Requirements

- **File Extension**: Must use `.prompt.md` extension
- **Goal Statement**: Must start with "Your goal is to..."
- **Conditional Inputs**: Handle missing information gracefully
- **File References**: Use proper syntax and valid paths
- **Markdown Formatting**: Clean, readable markdown structure

### Content Quality

- **Clear Scope**: Single, well-defined purpose
- **Actionable Instructions**: Specific, executable steps
- **Context Relevance**: All referenced files directly support the goal
- **User-Friendly**: Easy to understand and execute
- **Reusable**: Generic enough for multiple use cases

### VS Code Integration

- **Chat Compatibility**: Works seamlessly with Copilot Chat
- **Context Awareness**: Leverages workspace and file context
- **Iterative Friendly**: Supports multi-turn conversations
- **Error Resilient**: Handles missing files and edge cases gracefully

### Validation Checklist

- [ ] Goal statement uses "Your goal is to..." format
- [ ] Conditional input gathering included where needed
- [ ] File references use correct syntax and valid paths
- [ ] Instructions are clear and actionable
- [ ] Output format is well-defined
- [ ] Quality criteria are specified
- [ ] Error handling guidance is included

Include additional relevant files based on the prompt's domain and your project structure.

## File Reference Patterns

VS Code prompts use a specific syntax for referencing files that provide context:

### Reference Syntax Examples

- **Configuration**: Reference setup and build files
- **Examples**: Include files showing desired patterns
- **Types**: Reference shared interfaces and type definitions
- **Tests**: Include testing patterns and utilities
- **Documentation**: Reference specs and architecture docs

### Strategic File Selection

1. **Primary Examples** (2-3 files): Core files showing the main patterns
2. **Supporting Context** (2-4 files): Configuration, types, utilities
3. **Reference Material** (1-3 files): Documentation, specs, guidelines

### File Reference Best Practices

- **Absolute Paths**: Use full workspace paths for reliability
- **Logical Grouping**: Group related files together in references
- **Context Relevance**: Each file should directly support the prompt's goal
- **Freshness**: References are read live, so files reflect current state

### VS Code Prompt Best Practices

#### Effective Context Management

- **File Selection Strategy**: Include 5-10 most relevant files that provide concrete examples
- **Context Hierarchy**: Order references from most to least important
- **Avoid Overloading**: Too many file references can dilute focus
- **Live References**: Files are read in real-time when prompt is executed

#### User Experience Design

- **Progressive Disclosure**: Start with essential inputs, ask for details as needed
- **Smart Defaults**: Provide reasonable defaults when possible
- **Validation Guidance**: Include criteria for validating outputs
- **Error Recovery**: Provide guidance when things don't work as expected

#### Prompt Execution Flow

1. **Prompt Invocation**: User types prompt name in Copilot Chat
2. **Context Loading**: VS Code reads referenced files automatically
3. **Dynamic Processing**: Copilot combines prompt template with current context
4. **Interactive Response**: User can refine and iterate on the output

#### Integration with Copilot Features

- **Chat Context**: Prompts inherit current chat conversation context
- **Workspace Awareness**: Automatically aware of current file and selection
- **Multi-turn Conversations**: Designed for iterative refinement
- **Code Actions**: Can suggest follow-up actions and edits
