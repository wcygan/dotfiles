<!--
name: search:smart
purpose: Intelligent code search using modern tools (ripgrep, fd, fzf)
tags: search, code-analysis, modern-tools, productivity
-->

Perform intelligent code search using modern, fast command-line tools. Combines ripgrep (rg), fd, and fzf for efficient pattern matching, file discovery, and interactive selection.

**Context**: $ARGUMENTS (search pattern, file type, or search scope)

## Search Strategy

1. **Pattern-based Search**
   - Use ripgrep for fast content search with regex support
   - File type filtering for language-specific searches
   - Context lines and match highlighting

2. **File Discovery**
   - Use fd for fast file finding with glob patterns
   - Respect .gitignore and common ignore patterns
   - Filter by extension, modification time, or path patterns

3. **Interactive Selection**
   - Integrate with fzf for fuzzy finding and selection
   - Preview matches with bat for syntax highlighting
   - Multi-select capabilities for batch operations

## Search Commands

```bash
# Content search with ripgrep
rg "$PATTERN" --type $FILETYPE --context 3 --color always --heading --line-number

# Advanced pattern search with multiple file types
rg "$PATTERN" --type-add 'config:*.{json,yaml,yml,toml}' --type config --context 2

# File discovery with fd
fd "$PATTERN" --type file --extension $EXT --hidden --follow

# Interactive search with fzf integration
rg --line-number --color=always "$PATTERN" | fzf --ansi --delimiter : --nth 3.. --preview 'bat --color=always --highlight-line {2} {1}'

# Search in specific directories
rg "$PATTERN" src/ tests/ --type rust --context 2

# Case-insensitive search with word boundaries
rg -i "\b$PATTERN\b" --type typescript --context 1

# Search for function definitions
rg "^(function|def|fn|func)\s+$PATTERN" --type-add 'code:*.{js,ts,py,rs,go}' --type code

# Find recent files and search within them
fd --changed-within 7d --type file | xargs rg "$PATTERN" --context 2
```

## Output Processing

```bash
# JSON output for structured processing
rg "$PATTERN" --json | jq '.data | select(.type=="match") | {file: .path.text, line: .line_number, text: .lines.text}'

# Count matches per file
rg "$PATTERN" --count-matches --sort path

# Search with file stats
rg "$PATTERN" --stats --type rust

# Export results for further analysis
rg "$PATTERN" --json > /tmp/search-results.json
```

## Search Modes

### Quick Search

Fast content search with basic filtering:

```bash
rg "$PATTERN" --smart-case --context 1
```

### Deep Search

Comprehensive search with multiple strategies:

```bash
# Search content
rg "$PATTERN" --type-add 'all:*' --type all --context 3
# Search filenames
fd "$PATTERN" --type file
# Search in hidden files
rg "$PATTERN" --hidden --context 2
```

### Interactive Mode

Fuzzy finding with preview:

```bash
rg --line-number --color=always "$PATTERN" | fzf --ansi --preview 'bat --color=always --highlight-line {2} {1}' --preview-window up:50%
```

## Integration Examples

### Language-Specific Searches

- **Rust**: `rg "fn $PATTERN" --type rust --context 2`
- **Go**: `rg "func $PATTERN" --type go --context 2`
- **TypeScript**: `rg "(function|const|let).*$PATTERN" --type typescript --context 2`
- **Config Files**: `rg "$PATTERN" --type-add 'config:*.{json,yaml,toml}' --type config`

### Development Workflows

- **TODO/FIXME**: `rg "(TODO|FIXME|HACK|NOTE)" --context 1`
- **Error Handling**: `rg "(error|Error|err)" --type rust --context 2`
- **Dependencies**: `fd "package.json|Cargo.toml|go.mod|deno.json" | xargs bat`

## Example Usage

```bash
# Search for API endpoints
/search:smart "POST|GET|PUT|DELETE"

# Find configuration files
/search:smart config

# Interactive function search
/search:smart fn main rust

# Search recent changes
/search:smart modified 7d "async function"
```
