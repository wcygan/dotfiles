---
allowed-tools: Bash(gh api:*), Bash(gh auth:*), Bash(base64:*), Bash(grep:*), Bash(head:*)
description: Search GitHub for code using GitHub CLI with precise line number permalinks
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
5. For each result, fetch the file content to determine exact line numbers:
   - `gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d | grep -n "search_pattern"`
6. Parse and format the search results
7. Display the results with:
   - Repository name and description
   - File path and relevant code snippet
   - Direct permalink with exact line number: `{html_url}#L{line_number}`
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

🔗 Permalink: {html_url}#L{estimated_line_number}

---
```

Extract code snippets from the `text_matches` array in the API response. Each text match contains:

- `fragment`: The actual code snippet
- `matches`: Array of highlighted match positions
- Show match highlights using **bold** or similar formatting

**Permalink Generation:**

- Fetch file content using: `gh api repos/{owner}/{repo}/contents/{path}`
- Decode base64 content and search for exact matches with line numbers
- Use `grep -n` to find precise line numbers for code fragments
- Generate permalink format: `{html_url}#L{line_number}`
- Example: `https://github.com/owner/repo/blob/sha/file.rs#L42`

**Line Number Detection Process:**

1. Extract repository owner, name, and file path from search result
2. Fetch file content: `gh api repos/{owner}/{repo}/contents/{path} --jq '.content'`
3. Decode and search: `base64 -d | grep -n "exact_code_pattern"`
4. Use first match line number for permalink generation
5. If multiple matches, show all line numbers or use first occurrence

Limit display to first 10 results for readability.
