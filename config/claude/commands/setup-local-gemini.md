---
description: Create .gemini/settings.json for local Gemini CLI context configuration
---

Create a `.gemini/settings.json` file in the current project to configure the Gemini CLI tool.

**What this does:**
Sets up local Gemini CLI configuration to use `AGENTS.md` and `GEMINI.md` as context files instead of the default `GEMINI.md` only.

**Configuration created:**
```json
{
  "context": {
    "fileName": ["AGENTS.md", "GEMINI.md"]
  }
}
```

**Context file precedence:**
The Gemini CLI loads context hierarchically:
1. Global: `~/.gemini/AGENTS.md` or `~/.gemini/GEMINI.md`
2. Project root: `./.gemini/AGENTS.md` or `./.gemini/GEMINI.md`
3. Subdirectories: `./subdir/.gemini/AGENTS.md` etc.

**Why use multiple context files:**
- `AGENTS.md`: AI-focused development instructions and patterns
- `GEMINI.md`: Gemini-specific prompts, examples, or project context

**Steps:**
1. Create `.gemini/` directory if it doesn't exist
2. Write `settings.json` with the context configuration
3. Confirm the file was created successfully

**After setup:**
- Add `.gemini/` to `.gitignore` if it contains local-only settings
- Create `AGENTS.md` and/or `GEMINI.md` files as needed
- Use `/memory` command in Gemini CLI to verify context loading
