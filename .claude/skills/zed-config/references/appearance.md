# Zed Appearance Configuration

## Quick Setup
1. Theme Selector: `cmd-k cmd-t`
2. Light/dark toggle: `cmd-k ctrl-shift-t`
3. Icon theme selector: command palette
4. Buffer font: `buffer_font_family` setting
5. Font size: `buffer_font_size` setting

## Theme Configuration

```json
{
  "theme": {
    "mode": "system",
    "light": "One Light",
    "dark": "One Dark"
  }
}
```

`mode` options: `"system"`, `"dark"`, `"light"`

Install themes via Extensions page. Preview in real-time through Theme Selector.

## Icon Themes

```json
{
  "icon_theme": {
    "mode": "system",
    "light": "Zed (Default)",
    "dark": "Zed (Default)"
  }
}
```

Command: `icon theme selector: toggle`

## Font Settings

Three font contexts:

| Setting | Purpose |
|---------|---------|
| `buffer_font_family` | Editor text |
| `buffer_font_size` | Editor font size |
| `ui_font_family` | Interface elements |
| `ui_font_size` | Interface font size |
| `terminal.font_family` | Terminal display |
| `terminal.font_size` | Terminal font size |

```json
{
  "buffer_font_family": "JetBrains Mono",
  "buffer_font_size": 14,
  "ui_font_family": "Inter",
  "ui_font_size": 16,
  "terminal": {
    "font_family": "JetBrains Mono",
    "font_size": 14
  }
}
```

### Font Ligatures
Disable: `"buffer_font_features": { "calt": false }`

### Line Height
`buffer_line_height` options:
- `"comfortable"` (default, 1.618 ratio)
- `"standard"` (1.3 ratio)
- `{ "custom": 1.5 }` (custom ratio)

## Syntax Highlighting Overrides

```json
{
  "theme_overrides": {
    "One Dark": {
      "syntax": {
        "comment": { "font_style": "italic" },
        "string": { "color": "#00AA00" }
      }
    }
  }
}
```

Custom themes: create JSON files in `~/.config/zed/themes/`

## Semantic Tokens

```json
{ "semantic_tokens": "combined" }
```

Options: `"off"`, `"combined"` (LSP overlaid on Tree-sitter), `"full"` (LSP replaces Tree-sitter)
