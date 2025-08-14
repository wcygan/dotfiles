# Helix Editor Configuration

This directory contains a comprehensive Helix editor configuration with advanced features and language server support.

## Features

### ✨ Editor Enhancements

- **Theme**: Catppuccin Mocha (modern dark theme)
- **Visual**: Relative line numbers, rulers at 80/120 columns, bufferline
- **Navigation**: Scrolloff for context, smart search, enhanced file picker
- **LSP**: Full language server integration with inlay hints and signatures
- **Soft wrap**: Intelligent text wrapping with visual indicators

### ⌨️ Power User Keybindings

- **Multi-cursor**: `Ctrl+d` (select next), `Ctrl+D` (select all)
- **Tree-sitter selections**: `Alt+p/n/i/a` for smart selections
- **Quick commands**: `;` for command mode, `Ctrl+s` to save
- **Buffer management**: `Ctrl+b` for buffer picker
- **LSP actions**: `space l` + `d/r/i/t` for definitions/references/implementation/type
- **Code actions**: `space c` + `a/r/f` for actions/rename/format
- **Git integration**: `space g` + `s/l/d` for status/log/diff

### 🛠️ Language Support

Configured language servers for:

- **Rust**: rust-analyzer with clippy integration
- **TypeScript/JavaScript**: Full TS support with prettier formatting
- **Go**: gopls with goimports formatting
- **Python**: Ruff + Pyright for modern Python development
- **Web**: HTML, CSS, JSON, YAML with proper formatting
- **DevOps**: Dockerfile, TOML, Bash scripting
- **Documentation**: Markdown with live preview

## Installation

The configuration is automatically installed via the dotfiles installation script:

```bash
deno task install
```

This will:

1. Backup existing Helix configuration
2. Install enhanced `config.toml` and `languages.toml`
3. Create `~/.config/helix/` directory if needed

## Language Server Installation

To get the most out of this configuration, install the language servers:

### Essential Language Servers

```bash
# Rust (usually installed with rustup)
rustup component add rust-analyzer

# TypeScript/JavaScript
npm install -g typescript-language-server typescript prettier

# Go
go install golang.org/x/tools/gopls@latest
go install golang.org/x/tools/cmd/goimports@latest

# Python
pip install ruff ruff-lsp pyright

# JSON/HTML/CSS
npm install -g vscode-langservers-extracted

# YAML
npm install -g yaml-language-server

# TOML
cargo install taplo-cli --locked

# Markdown
cargo install marksman

# Bash
npm install -g bash-language-server

# Lua
brew install lua-language-server stylua
```

### Optional Formatters

```bash
# Shell formatting
brew install shfmt

# JSON formatting (if not installed)
brew install jq
```

## Quick Start

1. Install language servers (see above)
2. Run `deno task install` to deploy configuration
3. Open Helix: `hx`
4. Check health: `:config-reload` then `hx --health`

## Pro Tips

- Use `:tutor` for interactive Helix tutorial
- Try `space` for the command palette
- Use `%` to select entire file, `x` to select line
- Use `s` to split selections on regex patterns
- Use `mip` to select inside parentheses
- Use `&` to align selections
- Use `:pipe jq` for JSON formatting

## Troubleshooting

- **Theme not found**: Install additional themes or use `theme = "default"`
- **Language server not working**: Check `hx --health` for installation status
- **Keybinding conflicts**: Customize in the `[keys.normal]` section

## Configuration Files

- `config.toml`: Editor settings, theme, keybindings
- `languages.toml`: Language server and formatter configuration
- `README.md`: This documentation

For more information, see the [official Helix documentation](https://docs.helix-editor.com/).
