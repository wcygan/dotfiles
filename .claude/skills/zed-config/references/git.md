# Zed Git Integration

## Git Panel
- **Toggle**: `git panel: toggle focus` or status bar Git icon
- **Views**: Flat file listing (default) or tree view
- **Panel position**: Settings Editor > Panels > Git Panel (left, right, or bottom)

## Settings
- **Inline Git Blame**: Customizable delay or disable
- **Git Gutter**: Hide colored added/modified/deleted line markers
- **Commit message wrapping**: Default 72 characters (search "Git Commit" in settings)
- **Word diff**: Disable globally or per-language:

```json
{
  "languages": {
    "Markdown": {
      "word_diff_enabled": false
    }
  }
}
```

## Diff Viewing
- **Split view** (side-by-side, default) or **unified view** (inline)
- **Project diff**: `git: diff` via Command Palette

### Diff Hunk Keybindings
| Action | macOS | Linux/Windows |
|--------|-------|---------------|
| Expand all hunks | `cmd-"` | `ctrl-"` |
| Collapse all | Escape | Escape |
| Toggle selected | `cmd-'` | `ctrl-'` |
| Go to next hunk | `editor: go to hunk` | `editor: go to hunk` |
| Go to prev hunk | `editor: go to previous hunk` | `editor: go to previous hunk` |

## Staging

### Project Diff Method
- Individual hunk: click buttons or `git: stage and next` (`cmd-y` / `alt-y`)
- Stage all: `git: stage all` (`cmd-ctrl-y` / `ctrl-space`)

### Git Panel Method
- Type commit message, hit commit button
- Auto-stages tracked files (indicated by `[·]` checkbox)
- Individual file staging via checkboxes

## Committing
- **Git Panel**: `cmd-enter` / `ctrl-enter`
- **Expanded editor**: `git: expand commit editor` or `shift-escape`
- **Undo**: "Uncommit" button executes `git reset HEAD^ --soft`
- **Line length**: `preferred-line-length` setting (default: 72)

## Branch Management
- **Create**: `git: branch`
- **Switch**: `git: switch` or `git: checkout branch`
- **Delete**: Delete option in branch switcher (prevents deleting current branch)

## Merge Conflict Resolution
- Conflicting files flagged with warning icon
- Color coding: Green = current branch, Blue = incoming branch
- Resolution buttons: Keep current, Keep incoming, Use both
- Or manually edit and remove conflict markers

## Stashing
- **Create**: `git: stash all`
- **View**: `git: view stash` or Git Panel overflow menu
- **Apply**: `git: stash apply`
- **Pop**: `git: stash pop`

### Stash Diff Keybindings
- Apply: `ctrl-space`
- Pop: `ctrl-shift-space`
- Drop: `ctrl-shift-backspace`

## Remote Operations
- **Fetch**: `git: fetch` (`ctrl-g ctrl-g`)
- **Push**: `git: push` (`ctrl-g up`)
- **Force push**: `git: force push` (`ctrl-g shift-up`)
- **Pull**: `git: pull` (`ctrl-g down`)
- **Pull rebase**: `git: pull rebase` (`ctrl-g shift-down`)

Push checks in order: `pushRemote` (branch), `remote.pushDefault` (config), tracking remote.

## File History
- Right-click file in Project/Git Panel, or right-click editor tab
- Shows commit history with author, timestamp, message

## AI Commit Messages
- **Trigger**: Pencil icon or `git: generate commit message` (`alt-tab` / `alt-l`)
- **Model config**:
```json
{
  "agent": {
    "commit_message_model": {
      "provider": "anthropic",
      "model": "claude-3-5-haiku"
    }
  }
}
```
- **Customize format**: `agent: open rules library` > "Commit message" rule

## Git Hosting Providers
Supported: GitHub, GitLab, Bitbucket, SourceHut, Codeberg

**Self-hosted**:
```json
{
  "git_hosting_providers": [
    {
      "provider": "gitlab",
      "name": "Corp GitLab",
      "base_url": "https://git.example.corp"
    }
  ]
}
```

Providers: `github`, `gitlab`, `bitbucket`, `gitea`, `forgejo`, `sourcehut`

## Permalinks
- Command Palette: search `permalink`
- Actions: `editor::CopyPermalinkToLine`, `editor::OpenPermalinkToLine`
- Or right-click menu

## CLI Integration
```bash
git config --global core.editor "zed --wait"
# Or:
export GIT_EDITOR="zed --wait"
```

## Complete Keybinding Reference
| Action | Keybinding |
|--------|-----------|
| `git: stage all` | `cmd-ctrl-y` / `ctrl-space` |
| `git: unstage all` | `cmd-ctrl-shift-y` |
| `git: toggle staged` | `space` |
| `git: stage and next` | `cmd-y` / `alt-y` |
| `git: unstage and next` | `cmd-shift-y` |
| `git: commit` | `cmd-enter` / `ctrl-enter` |
| `git: expand commit editor` | `shift-escape` |
| `git: push` | `ctrl-g up` |
| `git: force push` | `ctrl-g shift-up` |
| `git: pull` | `ctrl-g down` |
| `git: pull rebase` | `ctrl-g shift-down` |
| `git: fetch` | `ctrl-g ctrl-g` |
| `git: diff` | `ctrl-g d` |
| `git: restore` | `cmd-alt-z` |
| `git: restore file` | `cmd-delete` |
| `git: blame` | `cmd-alt-g b` |
