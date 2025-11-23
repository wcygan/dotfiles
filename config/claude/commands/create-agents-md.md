---
description: Generate AGENTS.md file for a project following agents.md specification
---

Create an AGENTS.md file for the project directory specified in $ARGUMENTS (or current directory if not specified).

AGENTS.md is a standard markdown file that provides context and instructions for AI coding agents working on your project. It complements README.md by containing detailed operational context that agents need.

# Analysis Phase

First, analyze the target directory to understand:

1. **Tech stack**: Detect languages, frameworks, build tools
2. **Project structure**: Monorepo vs single project, key directories
3. **Build system**: Package managers, task runners, build commands
4. **Testing setup**: Test frameworks, test locations, test commands
5. **Existing docs**: README.md, CONTRIBUTING.md, other relevant files
6. **Version control**: Git conventions, branch structure (if .git exists)

Use the Task tool with subagent_type='Explore' for thorough analysis across the project.

# AGENTS.md Generation

Generate a comprehensive AGENTS.md file with relevant sections based on what you discovered:

## Required Sections (adapt to project)

### Mission
- Brief project purpose (1-2 sentences)
- Key goals or constraints

### Principles
- Code style guidelines specific to this project
- Architecture patterns to follow
- Performance or security priorities

### Tech Stack
- Languages and versions
- Frameworks and key libraries
- Build tools and package managers

### Development Workflow

#### Setup
```bash
# Commands to get started (detected from project)
```

#### Build & Run
```bash
# Start development environment
# Run the application
# Build for production
```

#### Testing
```bash
# Run tests (unit, integration, e2e)
# Test file locations and naming conventions
```

### Code Standards
- File organization patterns
- Naming conventions
- Import/dependency guidelines
- Comment and documentation expectations

### Git & Commits (if applicable)
- Branch naming conventions
- Commit message format
- PR requirements
- CI/CD expectations

### Deployment (if relevant)
- Deployment process
- Environment configurations
- Release procedures

### Authority & Guardrails
- What agents MAY edit
- What agents MUST NOT change
- When to ask for clarification

### Troubleshooting
- Common issues and solutions
- Debug commands
- Where to find logs

## Customization Guidelines

**Adapt sections based on project type:**

- **Library/Package**: Emphasize API design, versioning, backward compatibility
- **Web Application**: Include routing, state management, API endpoints
- **CLI Tool**: Focus on command structure, argument parsing, output formats
- **Monorepo**: Note subdirectory AGENTS.md files, cross-project dependencies
- **Infrastructure**: Deployment topology, configuration management, secrets handling

**Include executable commands** that agents can run directly (use code blocks).

**Be specific and actionable**: Instead of "Follow best practices," specify exact patterns used in this codebase.

# Output Format

1. **Create the file** at `{target_directory}/AGENTS.md`
2. **Show the user** a summary of:
   - Tech stack detected
   - Key sections included
   - Notable patterns or conventions documented
3. **Remind the user** that AGENTS.md is living documentation and should be updated as the project evolves

# Special Cases

**Monorepo**: Suggest creating nested AGENTS.md files for major subprojects, with the root AGENTS.md covering cross-cutting concerns.

**Existing AGENTS.md**: If one exists, offer to:
- Review and enhance it
- Migrate it to follow best practices
- Add missing sections

**Minimal projects**: For very simple projects, create a concise AGENTS.md focusing on essentials (don't over-engineer).

# Best Practices

- Keep instructions explicit and agent-focused
- Include copy-pasteable commands
- Document the "why" behind conventions
- Reference specific files/directories with examples
- Update AGENTS.md when project structure changes

Remember: AGENTS.md uses standard Markdown with no required fields. Structure it to be most helpful for agents working on THIS specific project.
