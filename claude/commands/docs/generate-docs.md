---
allowed-tools: Read, Write, Bash(fd:*), Bash(rg:*), Bash(git:*)
description: Generate comprehensive project documentation
---

## Context

- Target: $ARGUMENTS (type: api, changelog, readme, onboarding, or specific component)
- Current directory: !`pwd`
- Project type: !`fd "(package.json|Cargo.toml|go.mod|deno.json)" . | head -1 | xargs basename 2>/dev/null || echo "unknown"`
- Existing docs: !`fd "(README|CHANGELOG|API|docs)" . | head -5 || echo "No existing docs"`
- Recent commits: !`git log --oneline -5 2>/dev/null | head -3 || echo "No git history"`

## Your task

Generate comprehensive documentation for the specified target:

1. **Identify Documentation Type** - API docs, README, changelog, or onboarding guide
2. **Analyze Codebase** - Extract relevant information and structure
3. **Generate Content** - Create well-structured, informative documentation
4. **Add Examples** - Include code examples and usage patterns
5. **Ensure Completeness** - Cover all important aspects and edge cases

**Documentation Types:**

- **API Documentation**: Function/method signatures, parameters, return values
- **README**: Project overview, installation, usage, examples
- **Changelog**: Version history, features, breaking changes
- **Onboarding Guide**: Getting started, development setup, contribution guide
- **Component Docs**: Individual module/component documentation

**Generated Content:**

- Clear structure with headers and sections
- Code examples with proper syntax highlighting
- Installation and usage instructions
- API reference with parameter details
- Troubleshooting and FAQ sections

Example: `/generate-docs api` or `/generate-docs readme` or `/generate-docs changelog`
