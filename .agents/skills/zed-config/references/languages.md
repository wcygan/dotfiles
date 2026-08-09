# Zed Language & LSP Configuration

## Architecture
- **Tree-sitter**: Syntax highlighting, structural features (outline panel)
- **LSP**: Code completion, diagnostics, go-to-definition, refactoring

## Language-Specific Settings

Override global settings per language under `"languages"` in `settings.json`:

```json
{
  "languages": {
    "Python": {
      "tab_size": 4,
      "formatter": "language_server",
      "format_on_save": "on"
    },
    "JavaScript": {
      "tab_size": 2,
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

### Available Per-Language Properties
- `tab_size` — Indentation spacing
- `formatter` — Code formatting tool
- `format_on_save` — `"on"` or `"off"`
- `enable_language_server` — Toggle LSP support
- `hard_tabs` — Use tabs instead of spaces
- `preferred_line_length` — Maximum recommended line width
- `soft_wrap` — Long line wrapping behavior
- `show_completions_on_input` — Completion visibility while typing
- `show_completion_documentation` — Inline documentation display
- `colorize_brackets` — Rainbow bracket detection

## File Type Associations

```json
{
  "file_types": {
    "C++": ["c"],
    "TOML": ["MyLockFile"],
    "Dockerfile": ["Dockerfile*"]
  }
}
```

Glob patterns supported.

## Language Server Management

### Server Selection & Prioritization

```json
{
  "languages": {
    "PHP": {
      "language_servers": ["intelephense", "!phpactor", "!phptools", "..."]
    }
  }
}
```

- Named servers appear in specified order
- `!` prefix disables a server
- `"..."` wildcard for remaining servers

### LSP Configuration

**Initialization options** (set once at startup, requires restart):
```json
{
  "lsp": {
    "rust-analyzer": {
      "initialization_options": {
        "check": { "command": "clippy" }
      }
    }
  }
}
```

**Settings** (can be queried multiple times):
```json
{
  "lsp": {
    "tailwindcss-language-server": {
      "settings": {
        "tailwindCSS": {
          "emmetCompletions": true
        }
      }
    }
  }
}
```

**Always use nested objects**, not dot-delimited strings.

### Custom LSP Binary

```json
{
  "lsp": {
    "rust-analyzer": {
      "binary": {
        "ignore_system_version": false,
        "path": "/path/to/langserver/bin",
        "arguments": ["--option", "value"],
        "env": { "FOO": "BAR" }
      }
    }
  }
}
```

### Disabling Language Servers

```json
{
  "languages": {
    "Markdown": {
      "enable_language_server": false
    }
  }
}
```

## Formatting

### External Formatter
```json
{
  "languages": {
    "JavaScript": {
      "formatter": {
        "external": {
          "command": "prettier",
          "arguments": ["--stdin-filepath", "{buffer_path}"]
        }
      },
      "format_on_save": "on"
    }
  }
}
```

### Language Server Formatter
```json
{
  "languages": {
    "Rust": {
      "formatter": "language_server",
      "format_on_save": "on"
    }
  }
}
```

### Combined Formatters (chained)
```json
{
  "languages": {
    "JavaScript": {
      "formatter": [
        { "code_action": "source.fixAll.eslint" },
        {
          "external": {
            "command": "prettier",
            "arguments": ["--stdin-filepath", "{buffer_path}"]
          }
        }
      ],
      "format_on_save": "on"
    }
  }
}
```

### Disable Formatting
```json
{
  "languages": {
    "Markdown": {
      "format_on_save": "off"
    }
  }
}
```

## Linting

Configure via LSP settings:
```json
{
  "lsp": {
    "eslint": {
      "settings": {
        "codeActionOnSave": {
          "rules": ["import/order"]
        }
      }
    }
  }
}
```

## Semantic Tokens

```json
{ "semantic_tokens": "combined" }
```

Options: `"off"` (Tree-sitter only), `"combined"` (LSP overlaid), `"full"` (LSP replaces Tree-sitter)

## Inlay Hints

```json
{
  "inlay_hints": {
    "enabled": true,
    "show_type_hints": true,
    "show_parameter_hints": true,
    "show_other_hints": true
  }
}
```

## Navigation Commands
- `editor: Go to Definition` — F12
- `editor: Go to Type Definition` — Cmd/Ctrl+F12
- `editor: Find All References` — Shift+F12
- `editor: Rename Symbol` — F2
- `editor: Hover` — Type info and documentation
- `project symbols: toggle` — Codebase-wide symbol search
- `diagnostics: deploy` — Real-time error checking
