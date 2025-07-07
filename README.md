# Dotfiles

[![Mentioned in Awesome Claude Code](https://awesome.re/mentioned-badge.svg)](https://github.com/hesreallyhim/awesome-claude-code)

## Installation

1. Install Deno: https://docs.deno.com/runtime/getting_started/installation/

2. Clone and install:
   ```bash
   git clone https://github.com/wcygan/dotfiles.git && cd dotfiles
   deno task install
   ```

## Agentic Prompt Guidelines

**TL;DR:** Treat slash commands as executable programs, not conversations. Use minimal permissions, unique session IDs (`!`gdate +%s%N``), and explicit control flow (STEP, IF/ELSE, FOR EACH). Follow the `/commit` command as the gold standard example.

### Core Principles

- **Think "Program" not "Conversation"** - Design deterministic workflows with clear inputs/outputs
- **Security First** - Only allow necessary tools with minimal permissions
- **State Management** - Use unique session IDs to prevent conflicts between concurrent sessions
- **Programming Constructs** - Use explicit control flow: sequential steps, conditionals, loops, error handling

### Key Requirements

1. **Session Isolation** - Every command MUST include: `Session ID: !`gdate +%s%N``
2. **Dynamic Context** - Use `!`command`` for real-time data injection
3. **Minimal Permissions** - Only allow required commands in `allowed-tools`
4. **Clear Structure** - Front matter → Context → Task definition with examples

### Best Practices

- **Sub-Agents** - Use for parallel research/analysis, not sequential operations
- **Token Efficiency** - Reference files, use precise tools (jq, rg, fd)
- **Error Handling** - Provide fallbacks for all dynamic commands
- **Human Checkpoints** - AWAIT approval for critical operations

See the full guidelines in `.claude/commands/improve-slash-commands.md` and the `/commit` command as the reference implementation.
