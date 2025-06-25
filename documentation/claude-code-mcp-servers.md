# Claude Code MCP Server Configuration and Scopes

This document explains how Claude Code recognizes and manages MCP (Model Context Protocol) servers, including the scope system that determines where servers are available.

## Table of Contents

- [Overview](#overview)
- [MCP Server Configuration](#mcp-server-configuration)
- [Configuration File Locations](#configuration-file-locations)
- [Scope System](#scope-system)
- [Command Line Interface](#command-line-interface)
- [Automatic Configuration](#automatic-configuration)
- [Troubleshooting](#troubleshooting)

## Overview

Claude Code uses MCP servers to extend its capabilities with external tools and services. These servers can provide access to:

- File system operations (`mcp-server-git`)
- Time and date utilities (`mcp-server-time`)
- Sequential thinking capabilities (`@modelcontextprotocol/server-sequential-thinking`)
- Memory persistence (`@modelcontextprotocol/server-memory`)
- Web automation (`@modelcontextprotocol/server-puppeteer`)

## MCP Server Configuration

### Configuration Structure

MCP servers are configured with the following properties:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable-command",
      "args": ["argument1", "argument2"],
      "type": "stdio", // optional, defaults to stdio
      "env": {} // optional environment variables
    }
  }
}
```

### Example Configuration

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"]
    },
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"]
    }
  }
}
```

## Configuration File Locations

Claude Code stores MCP server configurations in different locations depending on the scope:

### 1. Main Configuration File

- **Location**: `~/.claude.json`
- **Purpose**: Stores all Claude Code settings including MCP servers
- **Structure**: MCP servers are nested under project paths in the `projects` object

#### Finding the Exact File Location

```bash
# Get the exact path to your Claude configuration file
echo "$HOME/.claude.json"

# Or using the username dynamically
echo "/Users/$(whoami)/.claude.json"

# Check if the file exists
if [ -f "$HOME/.claude.json" ]; then
    echo "Claude config found at: $HOME/.claude.json"
else
    echo "Claude config not found"
fi
```

#### Querying for Global (User-Scoped) MCP Servers

Global MCP servers are stored differently than project-specific ones. Here's how to find them:

```bash
# View all MCP servers across all scopes
claude mcp list

# Query the configuration file directly for user-scoped servers
# Note: User-scoped servers are stored in a special section
jq '.userMcpServers // empty' "$HOME/.claude.json" 2>/dev/null

# Alternative: Search for all MCP server configurations in the file
jq -r '.. | objects | select(has("mcpServers")) | .mcpServers' "$HOME/.claude.json" 2>/dev/null

# Get a specific user-scoped server configuration
claude mcp get <server-name> | grep "Scope: User"

# List only user-scoped servers using CLI
for server in $(claude mcp list | awk '{print $1}' | sed 's/:$//'); do
    if claude mcp get "$server" 2>/dev/null | grep -q "Scope: User"; then
        echo "User-scoped server: $server"
    fi
done
```

#### Understanding the File Structure

The `.claude.json` file is a large JSON file containing:

- Project-specific configurations (including local MCP servers)
- User preferences and settings
- Tips history and usage statistics
- MCP servers organized by scope

Example structure:

```json
{
  "projects": {
    "/path/to/project": {
      "mcpServers": {
        // Local/project-specific MCP server configurations
      }
    }
  },
  "userMcpServers": {
    // User-scoped (global) MCP server configurations
    // Note: This structure may vary based on Claude Code version
  }
}
```

#### Backup and Inspection Commands

```bash
# Create a backup of your Claude configuration
cp "$HOME/.claude.json" "$HOME/.claude.json.backup"

# View file size (it can be quite large)
ls -lh "$HOME/.claude.json"

# Count total number of configured projects
jq '.projects | length' "$HOME/.claude.json"

# Extract all MCP server names
jq -r '.. | objects | select(has("mcpServers")) | .mcpServers | keys[]' "$HOME/.claude.json" | sort | uniq

# Pretty print a specific section
jq '.projects | to_entries | .[] | select(.value.mcpServers != {}) | {project: .key, servers: .value.mcpServers}' "$HOME/.claude.json"
```

### 2. Project-Level Configuration

- **Location**: `.mcp.json` in project root
- **Purpose**: Share MCP server configurations with team members
- **Visibility**: Committed to version control

### 3. Settings Files (Migration in Progress)

- **Global**: `~/.claude/settings.json`
- **Local**: `.claude/settings.local.json`
- **Purpose**: New location for Claude Code settings (replacing `claude config` command)

## Scope System

Claude Code uses three scope levels to determine where MCP servers are available:

### 1. Local Scope (Default)

- **Availability**: Only in the current project
- **Privacy**: Private to your user account
- **Use Case**: Project-specific tools or experimental servers
- **Command**: `claude mcp add server-name command` (no scope flag needed)

### 2. User Scope (Global)

- **Availability**: Across all projects on your machine
- **Privacy**: Private to your user account
- **Use Case**: Personal utility servers you use everywhere
- **Command**: `claude mcp add -s user server-name command`

### 3. Project Scope (Team)

- **Availability**: Current project only
- **Privacy**: Shared with team members via version control
- **Use Case**: Team-wide tools for a specific project
- **Command**: `claude mcp add -s project server-name command`
- **Storage**: Creates/updates `.mcp.json` in project root

## Command Line Interface

### Adding MCP Servers

```bash
# Add with default local scope
claude mcp add git uvx mcp-server-git

# Add with user scope (global)
claude mcp add -s user git uvx mcp-server-git

# Add with project scope (team)
claude mcp add -s project git uvx mcp-server-git

# Add with arguments (use -- for flags)
claude mcp add time npx -- -y @modelcontextprotocol/server-time

# Add with custom transport type
claude mcp add -t sse my-server http://localhost:3000

# Add with environment variables
claude mcp add -e API_KEY=secret my-server ./server.js
```

### Managing MCP Servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get server-name

# Remove a server (specify scope)
claude mcp remove server-name -s local
claude mcp remove server-name -s user
claude mcp remove server-name -s project

# Test server connection
claude mcp test server-name

# Restart a server
claude mcp restart server-name
```

### Importing from Claude Desktop

```bash
# Import servers from Claude Desktop configuration
claude mcp add-from-claude-desktop
```

## Automatic Configuration

### Using the Dotfiles Installation Script

The `install-safely.ts` script can automatically configure MCP servers from a `mcp.json` file:

```typescript
async function configureMcpServers(claudeConfigDir: string): Promise<boolean> {
  const mcpConfigPath = join(claudeConfigDir, "mcp.json");

  // Read mcp.json
  const mcpConfig = JSON.parse(await Deno.readTextFile(mcpConfigPath));

  // Configure each server with user scope (global)
  for (const [serverName, serverConfig] of Object.entries(mcpConfig.mcpServers)) {
    const args = ["claude", "mcp", "add", "-s", "user", serverName, config.command];

    // Add arguments with -- separator for complex args
    if (config.args && config.args.length > 0) {
      const hasFlags = config.args.some((arg) => arg.startsWith("-"));
      if (hasFlags) args.push("--");
      args.push(...config.args);
    }

    await runCommand(args);
  }
}
```

### Benefits of Automatic Configuration

1. **Consistency**: Same MCP servers across all development environments
2. **Speed**: Configure all servers with one command
3. **Version Control**: Track MCP server configurations in dotfiles
4. **Team Sharing**: Easy onboarding for new team members

## Practical Examples: Finding Global MCP Servers

### Quick Commands to List Global Servers

```bash
# Method 1: Using Claude CLI to list user-scoped servers
claude mcp list | while read line; do
    server=$(echo "$line" | cut -d: -f1)
    if [ ! -z "$server" ]; then
        scope=$(claude mcp get "$server" 2>/dev/null | grep "Scope:" | awk '{print $2}')
        if [ "$scope" = "User" ]; then
            echo "Global server: $server"
        fi
    fi
done

# Method 2: Create an alias for easy access
alias claude-global-servers='claude mcp list | while read line; do server=$(echo "$line" | cut -d: -f1); if [ ! -z "$server" ]; then scope=$(claude mcp get "$server" 2>/dev/null | grep "Scope:" | awk "{print \$2}"); if [ "$scope" = "User" ]; then echo "$line"; fi; fi; done'

# Method 3: Export global servers to a file
claude mcp list > /tmp/all-servers.txt
while IFS= read -r line; do
    server=$(echo "$line" | cut -d: -f1)
    if claude mcp get "$server" 2>/dev/null | grep -q "Scope: User"; then
        echo "$line" >> /tmp/global-servers.txt
    fi
done < /tmp/all-servers.txt
```

### Inspecting the Configuration File

```bash
# Find your username dynamically
USERNAME=$(whoami)
CONFIG_FILE="/Users/$USERNAME/.claude.json"

# Alternative for Linux systems
# CONFIG_FILE="$HOME/.claude.json"

# Check file size and last modified
stat -f "Size: %z bytes, Modified: %Sm" "$CONFIG_FILE" 2>/dev/null || \
stat -c "Size: %s bytes, Modified: %y" "$CONFIG_FILE" 2>/dev/null

# Search for MCP server configurations
# This finds all objects containing mcpServers key
jq -r 'paths(objects) as $p | getpath($p) | select(has("mcpServers")?) | {path: $p, servers: .mcpServers}' "$CONFIG_FILE" 2>/dev/null

# Count MCP servers by project
jq -r '.projects | to_entries[] | select(.value.mcpServers != null) | "\(.key): \(.value.mcpServers | length) servers"' "$CONFIG_FILE" 2>/dev/null
```

### Creating a MCP Server Report

```bash
#!/bin/bash
# Save this as check-mcp-servers.sh

CONFIG_FILE="$HOME/.claude.json"
echo "=== Claude Code MCP Server Report ==="
echo "Configuration file: $CONFIG_FILE"
echo "File size: $(du -h "$CONFIG_FILE" 2>/dev/null | cut -f1)"
echo ""

echo "=== Global (User-Scoped) Servers ==="
claude mcp list | while read line; do
    server=$(echo "$line" | cut -d: -f1)
    if [ ! -z "$server" ]; then
        details=$(claude mcp get "$server" 2>/dev/null)
        if echo "$details" | grep -q "Scope: User"; then
            echo "$line"
        fi
    fi
done

echo ""
echo "=== Local (Project-Scoped) Servers ==="
claude mcp list | while read line; do
    server=$(echo "$line" | cut -d: -f1)
    if [ ! -z "$server" ]; then
        details=$(claude mcp get "$server" 2>/dev/null)
        if echo "$details" | grep -q "Scope: Local"; then
            echo "$line"
        fi
    fi
done
```

## Troubleshooting

### Common Issues

#### 1. "No MCP servers configured"

- **Cause**: No servers added or wrong scope checked
- **Solution**: Use `claude mcp list` to verify configuration
- **Fix**: Add servers with appropriate scope

#### 2. "Bad substitution" Error

- **Cause**: Shell expansion syntax in configuration files
- **Solution**: Use Claude CLI commands instead of direct file editing
- **Example**: `config.args.join` syntax not supported

#### 3. Servers Not Available in Other Projects

- **Cause**: Servers added with local scope (default)
- **Solution**: Re-add with user scope: `claude mcp add -s user ...`

#### 4. Arguments with Flags Not Working

- **Cause**: CLI parsing treats flags as command options
- **Solution**: Use `--` separator: `claude mcp add server npx -- -y package`

### Debugging Commands

```bash
# Check Claude Code version
claude --version

# Verify MCP support
claude mcp --help

# Test specific server
claude mcp test server-name

# Check server logs
claude mcp logs server-name
```

### Best Practices

1. **Use User Scope for Personal Tools**: Add commonly used servers with `-s user`
2. **Document Team Servers**: Include `.mcp.json` in project README
3. **Version Control**: Commit `.mcp.json` for project-scoped servers
4. **Security**: Never commit servers with API keys or secrets
5. **Testing**: Use `claude mcp test` before relying on new servers

## Server Lifecycle

### Startup

- Claude Code starts MCP servers when launched
- Servers run with your user permissions
- Failed servers retry with exponential backoff

### Runtime

- Servers communicate via stdio, SSE, or HTTP
- Claude Code manages server processes automatically
- Servers restart if they crash

### Shutdown

- Servers stop when Claude Code exits
- Clean shutdown ensures no orphaned processes
- State is preserved for next session

## Security Considerations

1. **Permissions**: MCP servers run with your user account permissions
2. **Code Review**: Only add servers from trusted sources
3. **Environment Variables**: Use `-e` flag for sensitive configuration
4. **Network Access**: Some servers may access external services
5. **File System**: Servers may read/write local files

## Future Developments

Claude Code is migrating from `claude config` to `settings.json` files. The MCP system will continue to evolve with:

- Better error messages and debugging tools
- More built-in server types
- Enhanced security controls
- Improved team collaboration features

For the latest updates, check the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code).
