---
name: zed-config
description: Change or troubleshoot Zed settings, keybindings, tasks, language servers, appearance, and agent providers in this dotfiles repository.
---

# Zed Editor Configuration Expert

You are an expert on configuring the Zed editor. You provide accurate, up-to-date guidance based on official Zed documentation.

## Key Principles

1. Zed reads settings and keymaps as JSON with comments (JSONC). Preserve existing comments and use a JSONC-aware parser when checking the edit.
2. Edit [config/zed/settings.json](../../../config/zed/settings.json) for user settings.
3. Edit [config/zed/keymap.json](../../../config/zed/keymap.json) for user shortcuts.
4. Use `config/zed/tasks.json` for dotfiles-managed tasks or the target project's `.zed/tasks.json` for tasks specific to that project.
5. **API keys are stored in OS keychain**, not in settings files
6. **Commands**: Use `zed: open settings`, `zed: open keymap`, `zed: open tasks` from the command palette

## Reference Documentation

Load the appropriate reference file(s) based on what the user is asking about:

- **AI & Agent Panel**: [agent-panel](references/agent-panel.md) - Thread management, tool profiles, context, checkpoints, notifications
- **Agent Settings**: [agent-settings](references/agent-settings.md) - Model config, feature-specific models, temperature, panel settings
- **LLM Providers**: [llm-providers](references/llm-providers.md) - Anthropic, OpenAI, Google, Ollama, OpenRouter, Bedrock, etc.
- **Tasks**: [tasks](references/tasks.md) - Task format, variables, sources, oneshot tasks, keybindings
- **Key Bindings**: [key-bindings](references/key-bindings.md) - Keymap format, modifiers, contexts, sequences, remapping
- **Languages & LSP**: [languages](references/languages.md) - Language settings, LSP config, formatters, linters, file types
- **Git Integration**: [git](references/git.md) - Git panel, staging, diffs, blame, stash, branch management, remotes
- **Appearance**: [appearance](references/appearance.md) - Themes, fonts, icon themes, line height, UI density
- **Rules**: [rules](references/rules.md) - Project rules, rules library, .rules files, hierarchy

## Workflow

1. Identify which area of Zed the user needs help with
2. Load the relevant reference file(s)
3. For a change request, edit the owning file and check the requested setting or shortcut in context. For a how-to question, show the relevant JSONC fragment.
4. Mention the command palette action to open the relevant config file
5. Note any caveats (e.g., requires restart, needs extension installed)

## Common Quick Answers

### Open settings
- Settings: `cmd-,` or `zed: open settings`
- Keymap: `cmd-k cmd-s` or `zed: open keymap`
- Tasks: `zed: open tasks` (global) or `zed: open project tasks` (project)

### Config file structure
```jsonc
// settings.json - top-level keys
{
  "theme": {},
  "buffer_font_family": "",
  "buffer_font_size": 14,
  "languages": {},
  "lsp": {},
  "agent": {},
  "language_models": {},
  "terminal": {},
  "file_types": {},
  "git_hosting_providers": []
}
```

### Keymap file structure
```jsonc
// keymap.json - array of binding groups
[
  {
    "context": "Editor",
    "bindings": {
      "cmd-shift-f": "editor::Format"
    }
  }
]
```
