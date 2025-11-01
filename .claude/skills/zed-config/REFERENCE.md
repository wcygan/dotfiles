# Zed Configuration Reference

Advanced configuration patterns and complete settings reference for Zed editor.

## Table of Contents

1. [Configuration File Locations](#configuration-file-locations)
2. [Advanced LSP Configuration](#advanced-lsp-configuration)
3. [Theme Customization](#theme-customization)
4. [Complex Keybinding Patterns](#complex-keybinding-patterns)
5. [Multi-Language Projects](#multi-language-projects)
6. [External Agent Configuration](#external-agent-configuration)
7. [Performance Tuning](#performance-tuning)
8. [File Type Associations](#file-type-associations)

---

## Configuration File Locations

### User Settings
- **macOS/Linux:** `~/.config/zed/settings.json`
- **Windows:** `~\AppData\Roaming\Zed\settings.json`

### Project Settings
- `.zed/settings.json` in project root
- Overrides user settings for that project
- Useful for team-wide configuration

### Access Methods
1. **Settings UI:** `cmd-,` (macOS) or `ctrl-,` (Windows/Linux)
2. **Settings JSON:** `cmd-alt-,` or `ctrl-alt-,`
3. **Keymap Editor:** `cmd-k cmd-s` or `ctrl-k ctrl-s`
4. **Keymap JSON:** Command palette → "zed: open keymap"
5. **Project Settings:** Command palette → "zed: open project settings"

---

## Advanced LSP Configuration

### Multiple Language Servers per Language

```json
{
  "languages": {
    "Python": {
      "language_servers": ["pyright", "ruff"],
      "format_on_save": "on",
      "formatter": [
        {
          "language_server": {
            "name": "ruff"
          }
        }
      ]
    }
  },
  "lsp": {
    "pyright": {
      "initialization_options": {
        "python": {
          "analysis": {
            "typeCheckingMode": "strict"
          }
        }
      }
    },
    "ruff": {
      "initialization_options": {
        "settings": {
          "lineLength": 120
        }
      }
    }
  }
}
```

### Custom LSP Binary

```json
{
  "lsp": {
    "rust-analyzer": {
      "binary": {
        "path": "/usr/local/bin/rust-analyzer",
        "arguments": ["--log-file", "/tmp/ra.log"],
        "env": {
          "RUST_LOG": "info"
        }
      }
    }
  }
}
```

### Language Server Priority

```json
{
  "languages": {
    "PHP": {
      "language_servers": [
        "intelephense",      // Primary
        "!phpactor",         // Disabled
        "..."                // Remaining registered servers
      ]
    }
  }
}
```

### Initialization Options vs Configuration Requests

**Initialization Options** (sent once at startup):
```json
{
  "lsp": {
    "rust-analyzer": {
      "initialization_options": {
        "cargo": {
          "features": "all"
        }
      }
    }
  }
}
```

**Configuration Requests** (queried multiple times):
```json
{
  "lsp": {
    "eslint": {
      "settings": {
        "validate": "on",
        "run": "onType"
      }
    }
  }
}
```

### Disable Inlay Hints Globally

```json
{
  "inlay_hints": {
    "enabled": false
  }
}
```

### Per-Language Inlay Hints

```json
{
  "languages": {
    "Rust": {
      "show_inline_completions": true,
      "inlay_hints": {
        "enabled": true,
        "show_type_hints": true,
        "show_parameter_hints": true
      }
    }
  }
}
```

---

## Theme Customization

### System-Aware Theme

```json
{
  "theme": {
    "mode": "system",
    "light": "One Light",
    "dark": "Zedokai"
  }
}
```

### Per-Release Channel Themes

```json
{
  "theme": "Zedokai",
  "nightly": {
    "theme": "Tokyo Night",
    "vim_mode": true
  }
}
```

### Syntax Highlighting Overrides

```json
{
  "theme_overrides": {
    "One Dark": {
      "syntax": {
        "comment": {
          "color": "#5C6370",
          "font_style": "italic"
        },
        "string": {
          "color": "#98C379"
        },
        "keyword": {
          "color": "#C678DD",
          "font_weight": 700
        },
        "function": {
          "color": "#61AFEF"
        },
        "type": {
          "color": "#E5C07B"
        }
      }
    }
  }
}
```

### UI Theme Overrides

```json
{
  "theme_overrides": {
    "Zedokai": {
      "editor.background": "#1E1E1E",
      "editor.foreground": "#D4D4D4",
      "editor.line_number": "#858585",
      "editor.active_line.background": "#282828"
    }
  }
}
```

---

## Complex Keybinding Patterns

### Context-Based Bindings

```json
[
  {
    "context": "Editor && mode == full",
    "bindings": {
      "cmd-r": "editor::Rename",
      "f12": "editor::GoToDefinition",
      "shift-f12": "editor::FindAllReferences"
    }
  },
  {
    "context": "Terminal",
    "bindings": {
      "cmd-k": ["terminal::SendKeystroke", "ctrl-l"]
    }
  },
  {
    "context": "!Editor && !Terminal",
    "bindings": {
      "cmd-p": "file_finder::Toggle"
    }
  }
]
```

### Key Sequences

```json
{
  "bindings": {
    "cmd-k cmd-s": "zed::OpenKeymap",
    "cmd-k cmd-m": "editor::ToggleCodeActions",
    "g d": "editor::GoToDefinition"      // vim-style sequence
  }
}
```

### Remapping with SendKeystokes

```json
{
  "bindings": {
    "ctrl-a": ["workspace::SendKeystrokes", "cmd-a"]
  }
}
```

### Arguments in Actions

```json
{
  "bindings": {
    "cmd-1": ["workspace::ActivatePane", 0],
    "cmd-2": ["workspace::ActivatePane", 1],
    "cmd-3": ["agent::NewExternalAgentThread", {
      "agent": "claude_code"
    }]
  }
}
```

### Non-QWERTY Layout Support

```json
{
  "use_key_equivalents": true    // Supports Cyrillic, Hebrew, etc.
}
```

---

## Multi-Language Projects

### Per-Language Configuration Matrix

```json
{
  "languages": {
    "JavaScript": {
      "tab_size": 2,
      "formatter": {
        "external": {
          "command": "prettier",
          "arguments": ["--stdin-filepath", "{buffer_path}"]
        }
      },
      "format_on_save": "on"
    },
    "TypeScript": {
      "tab_size": 2,
      "language_servers": ["typescript-language-server"],
      "formatter": "language_server",
      "format_on_save": "on"
    },
    "Python": {
      "tab_size": 4,
      "language_servers": ["pyright", "ruff"],
      "formatter": [
        {
          "language_server": { "name": "ruff" }
        }
      ],
      "format_on_save": "on"
    },
    "Go": {
      "tab_size": 4,
      "hard_tabs": true,
      "language_servers": ["gopls"],
      "formatter": "language_server",
      "format_on_save": "on"
    },
    "Rust": {
      "tab_size": 4,
      "language_servers": ["rust-analyzer"],
      "formatter": "language_server",
      "format_on_save": "on"
    }
  }
}
```

### Deno + Node.js Coexistence

```json
{
  "languages": {
    "TypeScript": {
      "language_servers": ["deno", "!typescript-language-server"],
      "formatter": "language_server"
    }
  },
  "lsp": {
    "deno": {
      "settings": {
        "deno": {
          "enable": true,
          "unstable": true,
          "importMap": "./import_map.json"
        }
      }
    }
  }
}
```

**Project-Specific Override (.zed/settings.json in Node.js project):**
```json
{
  "languages": {
    "TypeScript": {
      "language_servers": ["typescript-language-server", "!deno"],
      "formatter": {
        "external": {
          "command": "prettier",
          "arguments": ["--stdin-filepath", "{buffer_path}"]
        }
      }
    }
  }
}
```

---

## External Agent Configuration

### Claude Code Agent

```json
{
  "agent_servers": {
    "claude": {
      "env": {
        "CLAUDE_CODE_EXECUTABLE": "/usr/local/bin/claude"
      }
    }
  }
}
```

### Gemini CLI Agent

```json
{
  "agent_servers": {
    "gemini": {
      "ignore_system_version": false
    }
  }
}
```

### Custom Agent (Node.js)

```json
{
  "agent_servers": {
    "my-custom-agent": {
      "command": "node",
      "args": [
        "/Users/username/projects/my-agent/index.js",
        "--acp",
        "--model", "gpt-4"
      ],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "DEBUG": "true"
      }
    }
  }
}
```

### Agent Default Settings

```json
{
  "agent": {
    "default_profile": "write",
    "always_allow_tool_actions": true,
    "use_modifier_to_send": true,
    "play_sound_when_agent_done": true,
    "default_model": {
      "provider": "anthropic",
      "model": "claude-opus-4-1-20250805"
    },
    "profiles": {
      "write": {
        "name": "Writer",
        "tools": {
          "search": true,
          "web_fetch": false
        },
        "enable_all_context_servers": false,
        "context_servers": {
          "mcp-server-name": true
        }
      }
    }
  }
}
```

### Debugging Agents

Access logs via command palette:
- `dev: open acp logs` - View Agent Client Protocol logs

---

## Performance Tuning

### Optimize for Large Files

```json
{
  "file_scan_exclusions": [
    "**/.git",
    "**/node_modules",
    "**/target",
    "**/.next",
    "**/build",
    "**/dist"
  ],
  "git": {
    "git_gutter": "tracked_files"    // Only show for tracked files
  }
}
```

### Limit Inlay Hints

```json
{
  "lsp": {
    "rust-analyzer": {
      "initialization_options": {
        "inlayHints": {
          "maxLength": 25          // Truncate long hints
        }
      }
    }
  }
}
```

### Reduce Autosave Frequency

```json
{
  "autosave": {
    "after_delay": {
      "milliseconds": 1000        // Default: 200ms
    }
  }
}
```

### Disable Git Status in Tabs

```json
{
  "tabs": {
    "git_status": false
  }
}
```

---

## File Type Associations

### Custom File Extensions

```json
{
  "file_types": {
    "Dockerfile": ["Dockerfile*", "*.dockerfile"],
    "TOML": ["Cargo.lock", "Pipfile"],
    "JSON": ["*.jsonc", ".eslintrc"],
    "TypeScript": ["*.mts", "*.cts"]
  }
}
```

### Language Detection by Path

```json
{
  "file_types": {
    "C++": ["c"],                  // Treat .c files as C++
    "TypeScript": ["**/*.config.js"]  // Treat config.js as TS
  }
}
```

---

## Complete Settings Example

Comprehensive configuration combining all features:

```json
{
  // UI & Appearance
  "theme": {
    "mode": "system",
    "light": "One Light",
    "dark": "Zedokai"
  },
  "ui_font_size": 14,
  "buffer_font_size": 14.0,
  "buffer_font_weight": 430.0,
  "icon_theme": "Catppuccin Frappé",

  // Editor Behavior
  "preferred_line_length": 120,
  "soft_wrap": "preferred_line_length",
  "autosave": {
    "after_delay": {
      "milliseconds": 200
    }
  },
  "show_completions_on_input": true,
  "show_edit_predictions": false,

  // Base Keymap
  "base_keymap": "JetBrains",

  // Terminal
  "terminal": {
    "shell": {
      "program": "fish"
    }
  },

  // Tabs
  "tabs": {
    "git_status": true,
    "file_icons": true
  },

  // AI & Agents
  "agent": {
    "always_allow_tool_actions": true,
    "use_modifier_to_send": true,
    "play_sound_when_agent_done": true,
    "default_profile": "write",
    "default_model": {
      "provider": "google",
      "model": "gemini-2.5-pro-exp-03-25"
    }
  },
  "edit_predictions": {
    "mode": "eager",
    "enabled_in_text_threads": false
  },

  // Language Servers
  "lsp": {
    "deno": {
      "settings": {
        "deno": {
          "enable": true
        }
      }
    },
    "rust-analyzer": {
      "initialization_options": {
        "inlayHints": {
          "maxLength": null,
          "lifetimeElisionHints": {
            "enable": "skip_trivial",
            "useParameterNames": true
          }
        }
      },
      "enable_lsp_tasks": true
    },
    "ruff": {
      "initialization_options": {
        "settings": {}
      }
    }
  },

  // Language-Specific Settings
  "languages": {
    "Python": {
      "language_servers": ["ty", "ruff"],
      "format_on_save": "on",
      "formatter": [
        {
          "language_server": {
            "name": "ruff"
          }
        }
      ]
    },
    "TypeScript": {
      "language_servers": ["deno", "!typescript-language-server"],
      "formatter": "language_server"
    },
    "TSX": {
      "language_servers": ["deno", "!typescript-language-server"],
      "formatter": "language_server"
    }
  },

  // SSH Connections
  "ssh_connections": [
    {
      "host": "remote-server",
      "projects": [
        {
          "paths": ["/home/user/project"]
        }
      ]
    }
  ]
}
```

---

## Debugging Configuration Issues

### Check Default Settings

Command palette → `zed: open default settings`

View all available settings with their default values.

### Validate JSON Syntax

Zed supports extended JSON:
- `//` comments allowed
- Trailing commas allowed in objects/arrays
- Invalid JSON will show error in status bar

### LSP Troubleshooting

1. Check language server is installed
2. Verify `initialization_options` structure
3. Check LSP logs: Command palette → `lsp: show logs`
4. Restart language server: Command palette → `lsp: restart`

### Keybinding Conflicts

1. Open keymap editor: `cmd-k cmd-s`
2. Search for keybinding to see all assignments
3. Use `null` to disable conflicting bindings
4. Check `base_keymap` setting

### Agent Issues

1. Check agent logs: `dev: open acp logs`
2. Verify agent command and args
3. Check environment variables
4. Test agent outside Zed first

---

## Resources

- [Official Zed Documentation](https://zed.dev/docs)
- [Configuring Zed](https://zed.dev/docs/configuring-zed)
- [Key Bindings Guide](https://zed.dev/docs/key-bindings)
- [Configuring Languages](https://zed.dev/docs/configuring-languages)
- [External Agents](https://zed.dev/docs/ai/external-agents)
- [Default Settings](https://github.com/zed-industries/zed/blob/main/assets/settings/default.json)
- [Default Keymap](https://github.com/zed-industries/zed/blob/main/assets/keymaps/default.json)
