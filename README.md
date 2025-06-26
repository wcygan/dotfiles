# Dotfiles

[![Mentioned in Awesome Claude Code](https://awesome.re/mentioned-badge.svg)](https://github.com/hesreallyhim/awesome-claude-code)

## Installation

1. Install Deno: https://docs.deno.com/runtime/getting_started/installation/

2. Clone and install:
   ```bash
   git clone https://github.com/wcygan/dotfiles.git && cd dotfiles
   deno task install
   ```

   **Note:** The installation script now runs with improved concurrency, using parallel processing for backup and installation operations to significantly reduce setup time while maintaining safety through comprehensive error handling.

## Gemini CLI Extensions

This repository includes Gemini CLI extensions located in the `gemini/extensions/` directory. These extensions enhance the Gemini CLI with additional capabilities through MCP (Model Context Protocol) servers.

### Purpose of the `extensions/` Directory

The `gemini/extensions/` directory contains configuration files for Gemini CLI extensions. Each extension is defined by a `gemini-extension.json` file that specifies:

- The extension name
- The MCP server command and arguments to run
- Additional configuration options

### Adding New Gemini CLI Extensions

To add a new extension:

1. Create a new directory under `gemini/extensions/` with your extension name:
   ```bash
   mkdir gemini/extensions/your-extension-name
   ```

2. Create a `gemini-extension.json` file in the new directory:
   ```json
   {
     "name": "your-extension-name",
     "version": "1.0.0",
     "mcpServers": {
       "server-name": {
         "command": "command-to-run",
         "args": ["arg1", "arg2"]
       }
     }
   }
   ```

3. The extension will be automatically discovered and loaded by the Gemini CLI.

### Available Extensions

#### Git Extension

**Location:** `gemini/extensions/git/`

Provides Git repository management capabilities through the MCP Git server.

**Configuration:**

```json
{
  "name": "git",
  "version": "1.0.0",
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"]
    }
  }
}
```

**Example Usage:**

- View repository status and commit history
- Create and manage branches
- Stage and commit changes
- Handle merge conflicts

#### Sequential Thinking Extension

**Location:** `gemini/extensions/sequential-thinking/`

Enables structured thinking and reasoning capabilities for complex problem-solving.

**Configuration:**

```json
{
  "name": "sequential-thinking",
  "version": "1.0.0",
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

**Example Usage:**

- Break down complex problems into manageable steps
- Maintain context across multi-step reasoning
- Track thought processes and decision points
- Generate structured analysis and solutions

### Extension Requirements

- **Git Extension:** Requires `uvx` and `mcp-server-git` package
- **Sequential Thinking Extension:** Requires `npx` and `@modelcontextprotocol/server-sequential-thinking` package

Make sure the required tools and packages are installed on your system before using the extensions.
