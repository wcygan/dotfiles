# /context-load-deno-scripting

Load comprehensive documentation context for Deno scripting and automation.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Deno Manual**: `https://docs.deno.com/runtime/`
     - Focus on: runtime APIs, permissions, modules, CLI tools
   - **JSR Registry**: `https://jsr.io/`
     - Focus on: package discovery, standard library modules
   - **Dax Documentation**: `https://github.com/dsherret/dax`
     - Focus on: cross-platform shell commands, process execution
   - **Deno Standard Library**: `https://jsr.io/@std` (examples: `https://jsr.io/@std/cli`, `https://jsr.io/@std/async`, `https://jsr.io/@std/fs`, `https://jsr.io/@std/path`, `https://jsr.io/@std/os`, `https://jsr.io/@std/encoding`) and `https://jsr.io/packages`
     - Focus on: filesystem, networking, CLI, testing utilities
   - **Deno Examples**: `https://docs.deno.com/examples/`
     - Focus on: practical use cases, automation scripts

3. **Key documentation sections to prioritize**:
   - Runtime API and built-in modules
   - Permission system
   - Module system and imports
   - File system operations
   - Network operations
   - Process execution

4. **Focus areas for this stack**:
   - Cross-platform scripting
   - File and directory manipulation
   - HTTP requests and APIs
   - Process spawning and management
   - CLI argument parsing
   - Testing and assertions
   - Performance monitoring
   - Security and permissions

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Writing Deno automation scripts
- Using the standard library effectively
- Managing permissions securely
- File system operations
- Network programming
- Process execution and management
- Testing Deno applications
- Performance optimization

## Usage Example

```
/context-load-deno-scripting
```
