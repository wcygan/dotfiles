---
mode: 'agent'
description: 'Translate a Claude Command into a VSCode Github Copilot Prompt File'
---

Your goal is to translate a Claude command file into a VS Code prompt file (.prompt.md).

Ask for the Claude command content if not provided.

## Translation Process

### Step 1: Remove Claude-Specific Elements

Remove these elements that don't work in VS Code:

- `---` frontmatter with `allowed-tools` and `description`
- Session ID generation (`!`gdate +%s%N``)
- Dynamic bash command execution (`!`command``)
- Sub-agent deployment instructions
- `/tmp/` directory references
- Tool restriction lists

### Step 2: Convert Dynamic Context to Static References

Replace dynamic context gathering with static file references:

- Instead of `!fd -t f 'package.json'` use `#file:package.json`
- Instead of `!git status` describe current state or reference relevant files
- Convert bash commands to file references or structured instructions

### Step 3: Restructure Sub-Agents as Sequential Steps

Transform parallel sub-agents into sequential analysis steps:

- Convert agent deployment into numbered steps
- Maintain the analysis scope but make it sequential
- Preserve the specialized focus of each agent as analysis phases

### Step 4: Structure the VS Code Prompt

Create a well-structured prompt with:

1. **Clear goal statement** - What the prompt accomplishes
2. **Input requirements** - What information is needed
3. **Context files** - Relevant file references using `#file:` syntax
4. **Step-by-step process** - Clear instructions for execution
5. **Output format** - Expected deliverables

## Output Requirements

Provide:

1. **Suggested filename** for the `.prompt.md` file
2. **Complete VS Code prompt content** following best practices
3. **File references** that should be included
4. **Brief explanation** of key changes made during translation

## Translation Guidelines

- Make prompts reusable by using generic language
- Include 5-10 relevant file references
- Structure requirements clearly with lists and sections
- Define specific, actionable outputs
- Preserve the original intent while adapting to VS Code capabilities

#file:/Users/wcygan/Development/development-workspace/dotfiles/.github/context/claude-commands-to-vscode-prompts.md #file:/Users/wcygan/Development/development-workspace/dotfiles/.github/context/prompt-files.md
