# Zed Rules System

## Rule File Priority

Zed checks these files at the repository root in order (first match wins):

1. `.rules`
2. `.cursorrules`
3. `.windsurfrules`
4. `.clinerules`
5. `.github/copilot-instructions.md`
6. `AGENT.md`
7. `AGENTS.md`
8. `CLAUDE.md`
9. `GEMINI.md`

Only one rule file activates per project.

## Project-Level Rules

Place at repository root. Automatically included in all Agent Panel conversations as project-level instructions.

## Rules Library

Dedicated interface for creating, managing, and applying rules locally.

**Access**:
- Agent Panel menu > `Rules...`
- Command: `agent: open rules library`
- Keybinding: `cmd-alt-l` / `ctrl-alt-l`

**Features**:
- Built-in editor with syntax highlighting
- Inline assistant support for rule composition
- File duplication and deletion
- Default rule assignment via paper clip icon

## Usage Patterns

**@-mention**: Rules from the library can be @-mentioned in Agent Panel for on-demand insertion.

**Default rules**: Flag any library rule as default to auto-inject into every new Agent Panel interaction.

## Commit Message Rules

Customize commit message format via `agent: open rules library` > "Commit message" rule.
