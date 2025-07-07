---
allowed-tools: Bash(gh api:*), Bash(gh auth:*)
description: Search GitHub for code using GitHub CLI
---

## Context

- Session ID: !`gdate +%s%N`
- Search query: $ARGUMENTS
- Current directory: !`pwd`
- GitHub CLI auth status: !`gh auth status`

## Your task

Search GitHub for code using the provided query and display the results in a formatted, readable way.

Steps:

1. Validate that a search query was provided
2. Check GitHub CLI authentication status
3. If not authenticated, prompt user to run `gh auth login`
4. Use GitHub CLI to search for code with text matches: `gh api search/code --header "Accept: application/vnd.github.text-match+json" --raw-field q="$ARGUMENTS"`
5. Parse and format the search results
6. Display the results with:
   - Repository name and description
   - File path and relevant code snippet
   - Direct link to the file on GitHub
   - Total number of results found

GitHub CLI command: `gh api search/code --method GET --header "Accept: application/vnd.github.text-match+json" --raw-field q="QUERY"`

Example queries:

- `path:**/*.rs` - Search for Rust files
- `language:javascript react` - Search for JavaScript files containing "react"
- `extension:md documentation` - Search for Markdown files containing "documentation"
- `filename:package.json` - Search for package.json files

Handle errors gracefully:

- If no query provided, show usage examples
- If GitHub CLI not authenticated:
  - Instruct user to run `gh auth login`
  - Explain that GitHub code search requires authentication
- If API rate limit exceeded, inform user to try again later
- If no results found, suggest refining the search query
- If GitHub CLI error occurs, display the error message

**Authentication Setup:**

1. Install GitHub CLI: `brew install gh` (macOS) or equivalent
2. Authenticate: `gh auth login`
3. Verify: `gh auth status`

Format output as:

```
🔍 GitHub Code Search Results for: {query}

Found {total_count} results:

📁 {repository_name} - {repository_description}
📄 {file_path}
🔗 {html_url}

💻 Code snippet:
{text_matches[].fragment with highlighted matches}

---
```

Extract code snippets from the `text_matches` array in the API response. Each text match contains:

- `fragment`: The actual code snippet
- `matches`: Array of highlighted match positions
- Show match highlights using **bold** or similar formatting

Limit display to first 10 results for readability.
