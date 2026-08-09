# Lazygit Configuration Reference

Complete reference for advanced lazygit configuration patterns.

## Complete Configuration Schema

Full config structure with all major options:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/jesseduffield/lazygit/master/schema/config.json

gui:
  theme:
    activeBorderColor: [green, bold]
    inactiveBorderColor: [default]
    optionsTextColor: [blue]
    selectedLineBgColor: [blue]
    selectedRangeBgColor: [blue]
    cherryPickedCommitBgColor: [cyan]
    cherryPickedCommitFgColor: [blue]
    unstagedChangesColor: [red]
    defaultFgColor: [default]

  commitLength:
    show: true

  mouseEvents: true
  skipDiscardChangeWarning: false
  skipStashWarning: false
  skipNoStagedFilesWarning: false
  skipRewordInEditorWarning: false
  sidePanelWidth: 0.3333
  expandFocusedSidePanel: false
  mainPanelSplitMode: flexible
  language: auto
  timeFormat: 02 Jan 06
  shortTimeFormat: 3:04PM

  theme:
    lightTheme: false
    activeBorderColor: [green, bold]
    inactiveBorderColor: [default]
    optionsTextColor: [blue]
    selectedLineBgColor: [blue]
    selectedRangeBgColor: [blue]
    cherryPickedCommitBgColor: [cyan]
    cherryPickedCommitFgColor: [blue]
    unstagedChangesColor: [red]

  authorColors:
    "*": "#b8bb26"
    "John Smith": "#ff0000"

  branchColors:
    "feature/*": "#00ff00"
    "bugfix/*": "#ff0000"
    "main": "#0000ff"

git:
  paging:
    colorArg: always
    pager: delta --dark --paging=never
    useConfig: false
    externalDiffCommand: ""

  pagers:
    - pager: delta --dark --paging=never
    - pager: delta --light --paging=never

  commit:
    signOff: false
    autoWrapCommitMessage: true
    autoWrapWidth: 72

  merging:
    manualCommit: false
    args: ""

  mainBranches: [master, main]
  skipHookPrefix: WIP
  autoFetch: true
  autoRefresh: true
  fetchInterval: 60
  branchLogCmd: git log --graph --color=always --abbrev-commit --decorate --date=relative --pretty=medium {{branchName}} --
  allBranchesLogCmd: git log --graph --all --color=always --abbrev-commit --decorate --date=relative --pretty=medium
  overrideGpg: false
  disableForcePushing: false
  commitPrefixes: {}

  parseEmoji: false

  log:
    order: topo-order
    showGraph: always
    showWholeGraph: false

  diff:
    pager: ""
    ignoreWhitespace: false

os:
  edit: ""
  editAtLine: ""
  editAtLineAndWait: ""
  editInTerminal: false
  openDirInEditor: ""
  open: ""
  openLink: ""
  copyToClipboardCmd: ""

refresher:
  refreshInterval: 10
  fetchInterval: 60

update:
  method: prompt
  days: 14

confirmOnQuit: false
quitOnTopLevelReturn: false

disableStartupPopups: false

notARepository: prompt

promptToReturnFromSubprocess: true

keybinding:
  universal:
    quit: q
    quit-alt1: <c-c>
    return: <esc>
    quitWithoutChangingDirectory: Q
    togglePanel: <tab>
    prevItem: <up>
    nextItem: <down>
    prevItem-alt: k
    nextItem-alt: j
    prevPage: ','
    nextPage: .
    scrollLeft: H
    scrollRight: L
    gotoTop: <
    gotoBottom: '>'
    prevBlock: <left>
    nextBlock: <right>
    prevBlock-alt: h
    nextBlock-alt: l
    nextMatch: 'n'
    prevMatch: 'N'
    startSearch: /
    optionMenu: x
    optionMenu-alt1: '?'
    select: <space>
    goInto: <enter>
    confirm: <enter>
    remove: d
    new: 'n'
    edit: e
    openFile: o
    scrollUpMain: <pgup>
    scrollDownMain: <pgdown>
    scrollUpMain-alt1: K
    scrollDownMain-alt1: J
    scrollUpMain-alt2: <c-u>
    scrollDownMain-alt2: <c-d>
    executeCustomCommand: ':'
    createRebaseOptionsMenu: m
    pushFiles: P
    pullFiles: p
    refresh: R
    createPatchOptionsMenu: <c-p>
    nextTab: ']'
    prevTab: '['
    nextScreenMode: +
    prevScreenMode: _
    undo: z
    redo: <c-z>
    filteringMenu: <c-s>
    diffingMenu: W
    diffingMenu-alt: <c-e>
    copyToClipboard: <c-o>
    openRecentRepos: <c-r>
    submitEditorText: <enter>
    extrasMenu: '@'
    toggleWhitespaceInDiffView: <c-w>
    increaseContextInDiffView: '}'
    decreaseContextInDiffView: '{'

  files:
    commitChanges: c
    commitChangesWithoutHook: w
    amendLastCommit: A
    commitChangesWithEditor: C
    findBaseCommitForFixup: <c-f>
    confirmDiscard: x
    ignoreFile: i
    refreshFiles: r
    stashAllChanges: s
    viewStashOptions: S
    toggleStagedAll: a
    viewResetOptions: D
    fetch: f
    toggleTreeView: '`'
    openMergeTool: M
    openStatusFilter: <c-b>

  branches:
    createPullRequest: o
    viewPullRequestOptions: O
    copyPullRequestURL: <c-y>
    checkoutBranchByName: c
    forceCheckoutBranch: F
    rebaseBranch: r
    renameBranch: R
    mergeIntoCurrentBranch: M
    viewGitFlowOptions: i
    fastForward: f
    createTag: T
    pushTag: P
    setUpstream: u
    fetchRemote: f

  commits:
    squashDown: s
    renameCommit: r
    renameCommitWithEditor: R
    viewResetOptions: g
    markCommitAsFixup: f
    createFixupCommit: F
    squashAboveCommits: S
    moveDownCommit: <c-j>
    moveUpCommit: <c-k>
    amendToCommit: A
    resetCommitAuthor: a
    pickCommit: p
    revertCommit: t
    cherryPickCopy: C
    pasteCommits: V
    markCommitAsBaseForRebase: B
    tagCommit: T
    checkoutCommit: <space>
    resetCherryPick: <c-R>
    copyCommitAttributeToClipboard: y
    openLogMenu: <c-l>
    openInBrowser: o
    viewBisectOptions: b
    startInteractiveRebase: i

  stash:
    popStash: g
    renameStash: r

  commitFiles:
    checkoutCommitFile: c

  main:
    toggleSelectHunk: a
    pickBothHunks: b
    editSelectHunk: E

  submodules:
    init: i
    update: u
    bulkMenu: b

  commitMessage:
    commitMenu: <c-o>

customCommands: []

services: {}

notARepository: prompt
```

## Delta Advanced Configuration

### Complete Delta Config

```ini
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only --features=interactive

[delta]
    # General
    navigate = true
    hyperlinks = true
    hyperlinks-file-link-format = "vscode://file/{path}:{line}"

    # Appearance
    dark = true
    syntax-theme = Monokai Extended

    # Line numbers
    line-numbers = true
    line-numbers-left-format = "{nm:>4}┊"
    line-numbers-right-format = "{np:>4}│"
    line-numbers-left-style = blue
    line-numbers-right-style = blue
    line-numbers-minus-style = red
    line-numbers-plus-style = green
    line-numbers-zero-style = "#545474"

    # Hunk headers
    hunk-header-style = file line-number syntax
    hunk-header-file-style = "#999999"
    hunk-header-line-number-style = bold "#03a4ff"
    hunk-header-decoration-style = "#00b494" box ul

    # Commit decorations
    commit-decoration-style = bold yellow box ul
    commit-style = raw

    # File decorations
    file-style = yellow
    file-decoration-style = none
    file-added-label = [+]
    file-copied-label = [C]
    file-modified-label = [M]
    file-removed-label = [-]
    file-renamed-label = [R]

    # Grep decorations
    grep-file-style = purple
    grep-line-number-style = green
    grep-match-line-style = normal "#453327"
    grep-match-word-style = black yellow
    grep-separator-symbol = " "

    # Side by side
    side-by-side = false

    # Whitespace
    whitespace-error-style = reverse red

    # Merge conflicts
    merge-conflict-begin-symbol = ⌃
    merge-conflict-end-symbol = ⌄
    merge-conflict-ours-diff-header-style = "#f1fa8c"
    merge-conflict-ours-diff-header-decoration-style = box
    merge-conflict-theirs-diff-header-style = "#f1fa8c"
    merge-conflict-theirs-diff-header-decoration-style = box

    # Blame
    blame-code-style = syntax
    blame-format = "{author:<18} ({commit:>7}) {timestamp:^16} "
    blame-palette = "#2E3440 #3B4252 #434C5E #4C566A"

    # Diff so fancy emulation
    minus-style = syntax "#450a15"
    minus-emph-style = syntax "#600818"
    plus-style = syntax "#0b4820"
    plus-emph-style = syntax "#175c2e"

    # Zero line style (unchanged context)
    zero-style = syntax

[delta "interactive"]
    keep-plus-minus-markers = false

[delta "decorations"]
    commit-decoration-style = bold yellow box ul
    file-style = bold yellow ul
    file-decoration-style = none
    hunk-header-decoration-style = cyan box ul

[delta "line-numbers"]
    line-numbers-left-format = ""
    line-numbers-right-format = "│ "

[delta "side-by-side"]
    side-by-side = true
    line-numbers-left-format = ""
    line-numbers-right-format = "│ "

[delta "collared-trogon"]
    # A custom theme
    syntax-theme = base16
    file-style = "#999999"
    file-decoration-style = "#00b494" ul
    minus-style = "#500000"
    plus-style = "#004800"
```

### Delta Theme Gallery

**Popular pre-configured themes:**

```ini
# Catppuccin Mocha
[delta]
    syntax-theme = Catppuccin-mocha

# Nord
[delta]
    syntax-theme = Nord
    minus-style = syntax "#3f2d3d"
    minus-emph-style = syntax "#763842"
    plus-style = syntax "#283b4d"
    plus-emph-style = syntax "#316172"

# GitHub (light)
[delta]
    light = true
    syntax-theme = GitHub
    minus-style = "#ffeef0"
    minus-emph-style = "#ff0000"
    plus-style = "#e6ffed"
    plus-emph-style = "#00ff00"

# Dracula
[delta]
    syntax-theme = Dracula
    file-style = "#ff79c6"
    file-decoration-style = none
    hunk-header-decoration-style = "#bd93f9" box ul
```

**List all available themes:**
```bash
delta --list-syntax-themes
delta --show-syntax-themes  # Preview with examples
```

## Lazygit Keybinding Patterns

### Vim-Style Navigation

```yaml
keybinding:
  universal:
    prevItem-alt: k
    nextItem-alt: j
    prevBlock-alt: h
    nextBlock-alt: l
    gotoTop: gg
    gotoBottom: G
    scrollUpMain-alt2: <c-u>
    scrollDownMain-alt2: <c-d>
```

### Colemak Layout

```yaml
keybinding:
  universal:
    prevItem-alt: k
    nextItem-alt: j
    prevBlock-alt: h
    nextBlock-alt: l
    scrollUpMain-alt1: K
    scrollDownMain-alt1: J
    scrollUpMain-alt2: <c-u>
    scrollDownMain-alt2: <c-d>
```

### Emacs-Style

```yaml
keybinding:
  universal:
    prevItem-alt: <c-p>
    nextItem-alt: <c-n>
    prevBlock-alt: <c-b>
    nextBlock-alt: <c-f>
    gotoTop: <c-a>
    gotoBottom: <c-e>
```

## Custom Commands Library

### Common Workflows

```yaml
customCommands:
  # Commitizen
  - key: 'C'
    command: 'git cz'
    description: 'Commit with commitizen'
    context: 'files'
    subprocess: true
    loadingText: 'Opening commitizen...'

  # Force push with lease
  - key: '<c-P>'
    command: 'git push --force-with-lease'
    description: 'Force push (safely)'
    context: 'global'
    loadingText: 'Force pushing...'
    prompts:
      - type: 'confirm'
        title: 'Are you sure you want to force push?'

  # Interactive rebase
  - key: 'i'
    prompts:
      - type: 'input'
        title: 'Rebase onto (branch/commit)'
        key: 'Target'
        initialValue: 'main'
    command: 'git rebase -i {{.Form.Target}}'
    context: 'commits'
    description: 'Interactive rebase'
    subprocess: true

  # Create PR (GitHub CLI)
  - key: '<c-o>'
    command: 'gh pr create --web'
    context: 'branches'
    description: 'Create GitHub PR'
    subprocess: true

  # Fixup commit
  - key: '<c-f>'
    prompts:
      - type: 'input'
        title: 'Fixup commit SHA'
        key: 'Sha'
    command: 'git commit --fixup={{.Form.Sha}}'
    context: 'files'
    description: 'Create fixup commit'

  # Amend and force push
  - key: '<c-a>'
    command: 'git commit --amend --no-edit && git push --force-with-lease'
    context: 'files'
    description: 'Amend and force push'
    loadingText: 'Amending and pushing...'

  # Git absorb
  - key: 'A'
    command: 'git absorb --and-rebase'
    context: 'files'
    description: 'Auto-absorb changes'
    loadingText: 'Running git absorb...'

  # Open in GitHub
  - key: 'O'
    command: 'gh repo view --web'
    context: 'global'
    description: 'Open repo in GitHub'
    subprocess: true

  # View file history
  - key: 'H'
    prompts:
      - type: 'menuFromCommand'
        title: 'File history'
        command: 'git ls-files'
        key: 'File'
    command: 'git log --follow -- {{.Form.File}}'
    context: 'global'
    description: 'View file history'
    subprocess: true

  # Create annotated tag
  - key: 'T'
    prompts:
      - type: 'input'
        title: 'Tag name'
        key: 'TagName'
      - type: 'input'
        title: 'Tag message'
        key: 'TagMessage'
    command: 'git tag -a {{.Form.TagName}} -m "{{.Form.TagMessage}}"'
    context: 'commits'
    description: 'Create annotated tag'

  # Squash commits since main
  - key: 'S'
    command: 'git reset --soft $(git merge-base HEAD main) && git commit --edit'
    context: 'commits'
    description: 'Squash all commits since main'
    subprocess: true
```

### Prompt Types

**Input prompt:**
```yaml
prompts:
  - type: 'input'
    title: 'Branch name'
    key: 'BranchName'
    initialValue: 'feature/'
```

**Confirm prompt:**
```yaml
prompts:
  - type: 'confirm'
    title: 'Are you sure?'
    key: 'Confirmed'
```

**Menu from command:**
```yaml
prompts:
  - type: 'menuFromCommand'
    title: 'Select branch'
    command: 'git branch --format="%(refname:short)"'
    key: 'Branch'
```

**Menu (static):**
```yaml
prompts:
  - type: 'menu'
    title: 'Select option'
    options:
      - name: 'Option 1'
        value: 'value1'
      - name: 'Option 2'
        value: 'value2'
    key: 'Choice'
```

## Performance Tuning

### Large Repositories

```yaml
git:
  # Reduce auto-fetch frequency
  autoFetch: false
  fetchInterval: 300  # 5 minutes instead of 1

  # Limit log display
  log:
    showWholeGraph: false

refresher:
  # Reduce refresh rate
  refreshInterval: 30

gui:
  # Hide expensive UI elements
  showBranchCommitHash: false
```

### Fast Navigation

```yaml
gui:
  # Faster scrolling
  scrollHeight: 5
  scrollPastBottom: true
  scrollOffMargin: 5
  scrollOffBehavior: jump

  # Skip confirmations
  skipDiscardChangeWarning: true
  skipStashWarning: true
  skipNoStagedFilesWarning: true
```

## Multi-Pager Strategies

### Cycle Between Views

```yaml
git:
  paging:
    colorArg: always
    pager: delta --dark --paging=never --line-numbers

  pagers:
    # 1. Default: Delta with line numbers
    - pager: delta --dark --paging=never --line-numbers

    # 2. Side-by-side view
    - pager: delta --dark --paging=never --side-by-side

    # 3. Structural diff (difftastic)
    - externalDiffCommand: difft --color=always

    # 4. No pager (raw git diff)
    - pager: ""
```

Press `|` in lazygit to cycle between these views.

### Context-Aware Paging

```yaml
git:
  paging:
    colorArg: always
    pager: delta --dark --paging=never

  diff:
    # Different pager for explicit diff view
    pager: delta --dark --paging=never --side-by-side
```

## Repository-Specific Configs

### Monorepo Configuration

```yaml
# .git/lazygit.yml in monorepo root
git:
  mainBranches: [develop, main]

  log:
    showWholeGraph: true  # See all branches

gui:
  showFileTree: true  # Navigate directory structure
  sidePanelWidth: 0.4  # More space for file tree
```

### Work vs Personal

```yaml
# ~/Code/work/.lazygit.yml
git:
  commit:
    signOff: true  # SOB required at work

gui:
  theme:
    lightTheme: true  # Light theme for office
```

```yaml
# ~/Code/personal/.lazygit.yml
git:
  commit:
    signOff: false

gui:
  theme:
    lightTheme: false  # Dark theme at home
```

## Integration with Other Tools

### Git Hooks

Lazygit respects git hooks. Skip with:

```yaml
customCommands:
  - key: 'w'
    command: 'git commit --no-verify -m "{{.Form.Message}}"'
    context: 'files'
    description: 'Commit without hooks'
    prompts:
      - type: 'input'
        title: 'Commit message'
        key: 'Message'
```

### Git Flow

```yaml
keybinding:
  branches:
    viewGitFlowOptions: 'i'

# Or use custom commands
customCommands:
  - key: 'F'
    prompts:
      - type: 'menu'
        title: 'Git Flow'
        options:
          - name: 'Start feature'
            value: 'feature'
          - name: 'Start hotfix'
            value: 'hotfix'
          - name: 'Finish feature'
            value: 'finish'
        key: 'Action'
    command: 'git flow {{.Form.Action}} start'
    context: 'branches'
```

### GitHub CLI Integration

```yaml
customCommands:
  # Create PR
  - key: 'o'
    command: 'gh pr create --web'
    context: 'branches'
    subprocess: true

  # View PR
  - key: 'O'
    command: 'gh pr view --web'
    context: 'branches'
    subprocess: true

  # PR status
  - key: '<c-p>'
    command: 'gh pr status'
    context: 'global'
    subprocess: true

  # CI status
  - key: '<c-c>'
    command: 'gh run list --limit 5'
    context: 'global'
    subprocess: true
```

## Troubleshooting Common Issues

### Config Not Reloading

Lazygit doesn't hot-reload config. After changes:
1. Press `R` to refresh
2. Or restart lazygit entirely

### Keybinding Conflicts

Check for conflicts:
```bash
# Extract all keybindings from config
yq eval '.keybinding' config.yml

# Find duplicates
yq eval '.keybinding | .. | select(type == "!!str")' config.yml | sort | uniq -d
```

### Pager Not Working on Windows

Windows doesn't support custom pagers natively. Workaround:

```yaml
git:
  paging:
    externalDiffCommand: 'delta --dark --paging=never'
```

### Delta Theme Not Applying

Ensure delta config is in `~/.gitconfig`, not lazygit config:
```bash
git config --global delta.syntax-theme "Nord"
```

## Migration Guides

### From tig to lazygit

Key differences:
- No vi-style command mode (`:` commands)
- Context-based keybindings instead of global
- YAML config instead of tigrc

Equivalent workflows:
- `tig status` → lazygit files panel
- `tig log` → lazygit commits panel
- `tig blame` → lazygit file history (`<c-l>`)

### From gitui to lazygit

Config migration:
```bash
# gitui uses key.ron, lazygit uses config.yml
# No automated migration; manually map keybindings
```

Key differences:
- lazygit has more extensive custom command support
- lazygit has better pager integration
- gitui is faster on large repos (Rust vs Go)

## Advanced Delta Features

### Navigate Between Files

In delta output with `navigate = true`:
- `n` - next file
- `N` - previous file

Configure in lazygit:
```yaml
git:
  paging:
    pager: delta --dark --paging=never --navigate
```

### Hyperlinks to Editor

```ini
[delta]
    hyperlinks = true
    hyperlinks-file-link-format = "vscode://file/{path}:{line}"
```

Change for your editor:
- **VSCode**: `vscode://file/{path}:{line}`
- **Sublime**: `subl://open?url=file://{path}&line={line}`
- **Lazygit**: `lazygit-edit://{path}:{line}`

### Custom Syntax Themes

Create custom theme:
```ini
[delta "my-theme"]
    syntax-theme = base16
    minus-style = "#450a15"
    minus-emph-style = "#600818"
    plus-style = "#0b4820"
    plus-emph-style = "#175c2e"
    file-style = "#999999"
    file-decoration-style = "#00b494" ul
    hunk-header-decoration-style = "#00b494" box ul

[delta]
    features = my-theme
```
