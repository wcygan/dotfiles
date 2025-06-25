# Gemini CLI Documentation Summary

This document summarizes the key features and architecture of the Gemini CLI based on the official documentation.

## Deployment

Gemini CLI offers flexible deployment options:

- **Standard Installation:** Recommended for most users via `npm install -g @google/gemini-cli`.
- **Sandbox (Docker/Podman):** For secure, isolated execution of tools using a container.
- **From Source:** For contributors to run directly from the source code with hot-reloading.
- **From GitHub:** Execute the latest commit directly using `npx`.

## Architecture

The CLI has a modular architecture:

- **CLI Package (`packages/cli`):** The user-facing frontend that handles input, rendering, and the overall user experience.
- **Core Package (`packages/core`):** The backend that orchestrates communication with the Gemini API, manages tool execution, and handles state.
- **Tools (`packages/core/src/tools/`):** Extensible modules that allow the AI to interact with the local environment (file system, shell, web).

## Commands

The CLI supports several command types:

- **Slash Commands (`/`):** Meta-commands for controlling the CLI itself (e.g., `/help`, `/chat`, `/memory`, `/restore`, `/tools`, `/quit`).
- **At Commands (`@`):** Injects the content of files or directories into the current prompt (e.g., `@src/my_project/ Summarize this code.`).
- **Shell Mode (`!`):** Executes shell commands directly from the CLI or toggles a persistent shell mode.

## Configuration

Configuration is managed through a hierarchical system, with command-line arguments having the highest precedence.

- **`settings.json`:** Persistent configuration files for user-global (`~/.gemini/settings.json`) and project-specific (`.gemini/settings.json`) settings.
- **`GEMINI.md`:** Hierarchical context files that provide project-specific instructions, style guides, and background information to the AI. The CLI loads these from global, project, and sub-directory locations.
- **Environment Variables:** A comprehensive set of variables for configuration (e.g., `GEMINI_API_KEY`, `GEMINI_MODEL`).
- **Command-Line Arguments:** Flags to override settings for a single session (e.g., `--model`, `--sandbox`).

## Checkpointing

This feature provides a safety net for file system modifications.

- **Automatic Snapshots:** Before a tool modifies a file, the CLI automatically creates a "checkpoint" by committing the project state to a shadow Git repository (`~/.gemini/history/<project_hash>`).
- **Restore:** The `/restore` command can list available checkpoints and revert the project files and conversation history to a previous state.
- **Enabling:** Disabled by default, it can be enabled with the `--checkpointing` flag or in `settings.json`.

## Extensions

Gemini CLI can be extended with custom functionality.

- **Loading:** Extensions are loaded from `<workspace>/.gemini/extensions` and `<home>/.gemini/extensions`.
- **Configuration:** Each extension has a `gemini-extension.json` file to define its servers and context files.

## Telemetry

The CLI uses the OpenTelemetry (OTEL) standard for observability.

- **Purpose:** Provides data on performance, health, and usage to help debug issues and monitor operations.
- **Data:** Collects traces, metrics, and structured logs for events like tool calls, API requests, and user prompts.
- **Configuration:** Can be enabled and configured to send data to a local collector or a compatible backend like Google Cloud.

## Memory Tool (`save_memory`)

The `save_memory` tool allows the AI to retain information across sessions.

- **Functionality:** Appends a given fact to a global `GEMINI.md` file (`~/.gemini/GEMINI.md`).
- **Usage:** `save_memory(fact="My preferred language is Python.")`
- **Purpose:** Useful for remembering user preferences, project details, or other key information to personalize assistance.

## Documentation Links

The official documentation for the Gemini CLI can be found at the following URLs:

- **Deployment:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/deployment.md`
- **Architecture:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/architecture.md`
- **CLI Index:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/cli/index.md`
- **CLI Commands:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/cli/commands.md`
- **CLI Configuration:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/cli/configuration.md`
- **Checkpointing:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/checkpointing.md`
- **Extensions:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/extension.md`
- **Telemetry:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/telemetry.md`
- **Memory Tool:** `https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/tools/memory.md`
