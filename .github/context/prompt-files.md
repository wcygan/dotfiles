# GitHub Copilot Prompt Files

GitHub Copilot supports two main types of prompt files to provide context and customize behavior:

## 1. Repository Custom Instructions (`.github/copilot-instructions.md`)

A single file that provides repository-wide context and instructions to Copilot.

### Availability

- Copilot Chat in Visual Studio, VS Code, and GitHub website
- Copilot coding agent
- Copilot code review

### Features

- Located at `.github/copilot-instructions.md` in your repository
- Contains short, self-contained statements that add context
- Automatically applied to all Copilot interactions in that repository
- Instructions are not displayed in chat but are available to Copilot for generating better responses

### Use Cases

- **Test generation**: Specify test frameworks or testing patterns
- **Code review**: Define what reviewers should look for
- **Commit message generation**: Set format and content preferences
- **Team conventions**: Document coding standards and tool preferences

### Example

```markdown
We use Bazel for managing our Java dependencies, not Maven, so when talking about Java packages, always give me instructions and code samples that use Bazel.

We always write JavaScript with double quotes and tabs for indentation, so when your responses include JavaScript code, please follow those conventions.

Our team uses Jira for tracking items of work.
```

## 2. Prompt Files (`.prompt.md` files) - Public Preview

Reusable prompt templates stored in your workspace that you can reference in Copilot Chat.

### Availability

- Currently only available in VS Code
- Public preview feature

### Template Features

- Markdown files with `.prompt.md` extension
- Can be stored anywhere in your workspace
- Mimic the existing Copilot Chat prompt format
- Can reference other files and even other prompt files as dependencies
- Allow blending natural language with context and references

### Template Use Cases

- **Code generation**: Reusable templates for components, tests, or migrations
- **Domain expertise**: Share specialized knowledge like security practices
- **Team collaboration**: Document patterns with references to specs
- **Onboarding**: Create step-by-step guides for complex processes

### Example Prompt File (`New React form.prompt.md`)

```markdown
Your goal is to generate a new React form component.

Ask for the form name and fields if not provided.

Requirements for the form:

- Use form design system components
- Include proper TypeScript types
- Add form validation
- Follow accessibility best practices

#file:src/components/forms/BaseForm.tsx #file:src/types/form.ts
```

## Best Practices

### Repository Instructions

- Keep instructions concise and specific
- Focus on project-specific conventions and tools
- Include information about coding standards and preferred libraries
- Document team workflow preferences

### Prompt Templates

- Use descriptive filenames that indicate the prompt's purpose
- Include relevant file references using `#file:` syntax
- Structure prompts with clear goals and requirements
- Store commonly used prompts in a dedicated directory for easy discovery

## Usage Tips

1. **Start with repository instructions** for general project context
2. **Create prompt files** for repeatable tasks and patterns
3. **Reference relevant files** in prompt files to provide context
4. **Keep prompts focused** on specific tasks or domains
5. **Version control** both types of files to share with your team
