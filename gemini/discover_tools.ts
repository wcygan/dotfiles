#!/usr/bin/env -S deno run --allow-read --allow-run

/**
 * Gemini CLI Tool Discovery Script
 *
 * This script is designed to be used as a `toolDiscoveryCommand` in the Gemini
 * CLI's settings. It outputs a JSON array of tool definitions that the Gemini
 * CLI can understand and use. This allows you to extend the Gemini CLI with
 * custom tools and commands.
 *
 * For more information on how to configure custom tools, see the Gemini CLI
 * documentation:
 * https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/cli/configuration.md
 *
 * Here's an example of what Gemini will say once you have this configured properly:
 *
 * > What tools are available to you?

 ✦ I have access to the following tools:

    * list_directory: Lists files and directories.
    * read_file: Reads the content of a file.
    * search_file_content: Searches for a pattern within files.
    * glob: Finds files matching a pattern.
    * replace: Replaces text within a file.
    * write_file: Writes content to a file.
    * web_fetch: Fetches content from a URL.
    * read_many_files: Reads content from multiple files.
    * run_shell_command: Executes a shell command.
    * save_memory: Saves a fact to my long-term memory.
    * google_web_search: Performs a web search.
    * rg: Searches for a pattern in files using ripgrep.
    * fd: Finds files using fd.
    * fzf: Uses fzf for interactive fuzzy finding.
    * bat: Views a file with syntax highlighting using bat.
    * eza: Lists files using eza.
    * delta: Provides better git diffs using delta.
    * zoxide: Navigates directories using zoxide.
    * duf: Checks disk usage using duf.
    * btop: Monitors processes using btop.
    * jq: Processes JSON using jq.
    * yq: Processes YAML using yq.
    * hexyl: Views binary files using hexyl.
    * list_directory: Lists files and directories.
    * read_file: Reads the content of a file.
    * search_file_content: Searches for a pattern within files.
    * glob: Finds files matching a pattern.
 */

const tools = [
  {
    "name": "rg",
    "description": "Use ripgrep (rg) to search for a pattern in files. NEVER use grep.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "pattern": {
          "type": "STRING",
          "description": "The pattern to search for.",
        },
        "path": {
          "type": "STRING",
          "description": "The file or directory to search in.",
        },
      },
      "required": ["pattern", "path"],
    },
  },
  {
    "name": "fd",
    "description": "Use fd to find files. NEVER use find.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "pattern": {
          "type": "STRING",
          "description": "The pattern to search for.",
        },
        "path": {
          "type": "STRING",
          "description": "The directory to search in.",
        },
      },
      "required": ["pattern", "path"],
    },
  },
  {
    "name": "fzf",
    "description": "Use fzf for interactive fuzzy finding and selection.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "input": {
          "type": "STRING",
          "description": "The input to pipe to fzf.",
        },
      },
      "required": ["input"],
    },
  },
  {
    "name": "bat",
    "description": "Use bat to view a file with syntax highlighting. NEVER use cat for code.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "file": {
          "type": "STRING",
          "description": "The file to view.",
        },
      },
      "required": ["file"],
    },
  },
  {
    "name": "eza",
    "description": "Use eza to list files. NEVER use plain ls.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "path": {
          "type": "STRING",
          "description": "The directory to list.",
        },
      },
      "required": ["path"],
    },
  },
  {
    "name": "delta",
    "description": "Use delta for better git diffs. NEVER use plain git diff.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "args": {
          "type": "STRING",
          "description": "The arguments to pass to git diff.",
        },
      },
      "required": ["args"],
    },
  },
  {
    "name": "zoxide",
    "description": "Use zoxide to navigate directories.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "query": {
          "type": "STRING",
          "description": "The query to pass to zoxide.",
        },
      },
      "required": ["query"],
    },
  },
  {
    "name": "duf",
    "description": "Use duf to check disk usage. NEVER use df.",
    "parameters": {
      "type": "OBJECT",
      "properties": {},
      "required": [],
    },
  },
  {
    "name": "btop",
    "description": "Use btop to monitor processes. NEVER use top.",
    "parameters": {
      "type": "OBJECT",
      "properties": {},
      "required": [],
    },
  },
  {
    "name": "jq",
    "description": "Use jq to process JSON. REQUIRED for all JSON tasks.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "filter": {
          "type": "STRING",
          "description": "The filter to apply.",
        },
        "file": {
          "type": "STRING",
          "description": "The file to process.",
        },
      },
      "required": ["filter", "file"],
    },
  },
  {
    "name": "yq",
    "description": "Use yq to process YAML. REQUIRED for all YAML tasks.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "filter": {
          "type": "STRING",
          "description": "The filter to apply.",
        },
        "file": {
          "type": "STRING",
          "description": "The file to process.",
        },
      },
      "required": ["filter", "file"],
    },
  },
  {
    "name": "hexyl",
    "description": "Use hexyl to view binary files. NEVER use xxd or hexdump.",
    "parameters": {
      "type": "OBJECT",
      "properties": {
        "file": {
          "type": "STRING",
          "description": "The file to view.",
        },
      },
      "required": ["file"],
    },
  },
];

console.log(JSON.stringify(tools, null, 2));
