# GitHub CLI Complete Reference

Version: 2.85.0 (January 2026)

## CLI Structure

```
gh
├── auth          # Authentication
├── repo          # Repositories
├── pr            # Pull Requests
├── issue         # Issues
├── run           # Workflow runs
├── workflow      # Workflows
├── release       # Releases
├── gist          # Gists
├── codespace     # Codespaces
├── project       # Projects
├── search        # Search
├── api           # Raw API requests
├── secret        # Secrets
├── variable      # Variables
├── cache         # Actions caches
├── label         # Labels
├── ssh-key       # SSH keys
├── gpg-key       # GPG keys
├── extension     # Extensions
├── alias         # Aliases
├── config        # Configuration
├── status        # Status overview
└── browse        # Open in browser
```

## Authentication

### Login
```bash
gh auth login                              # Interactive
gh auth login --web                        # Web-based
gh auth login --hostname enterprise.local  # GitHub Enterprise
gh auth login --with-token < token.txt     # Token from file
gh auth login --git-protocol ssh           # Use SSH protocol
```

### Status & Management
```bash
gh auth status                    # Show auth status
gh auth status --show-token       # Include token in output
gh auth token                     # Print token
gh auth switch --user username    # Switch accounts
gh auth logout                    # Logout
gh auth refresh --scopes write:org  # Add scopes
gh auth setup-git                 # Configure git credential helper
```

## Repositories

### Create
```bash
gh repo create name                          # Interactive
gh repo create name --public                 # Public repo
gh repo create name --private                # Private repo
gh repo create org/name                      # In organization
gh repo create name --description "Desc"     # With description
gh repo create name --license mit            # With license
gh repo create name --gitignore python       # With gitignore
gh repo create name --clone                  # Clone after creating
gh repo create name --source=.               # From current directory
```

### Clone & Fork
```bash
gh repo clone owner/repo                # Clone
gh repo clone owner/repo dir            # Clone to directory
gh repo fork owner/repo                 # Fork
gh repo fork owner/repo --clone         # Fork and clone
gh repo fork owner/repo --org myorg     # Fork to organization
gh repo sync                            # Sync fork with upstream
gh repo sync --branch main              # Sync specific branch
```

### View & List
```bash
gh repo view                                 # Current repo
gh repo view owner/repo                      # Specific repo
gh repo view --web                           # Open in browser
gh repo view --json name,description         # JSON output
gh repo list                                 # List your repos
gh repo list owner                           # List owner's repos
gh repo list --public                        # Public only
gh repo list --source                        # Non-forks only
gh repo list --json name,visibility          # JSON output
```

### Edit & Delete
```bash
gh repo edit --description "New desc"        # Edit description
gh repo edit --visibility private            # Change visibility
gh repo edit --default-branch main           # Set default branch
gh repo edit --enable-issues                 # Enable issues
gh repo rename new-name                      # Rename
gh repo archive                              # Archive
gh repo unarchive                            # Unarchive
gh repo delete owner/repo --yes              # Delete
```

### Utilities
```bash
gh repo set-default owner/repo    # Set default for directory
gh browse                         # Open repo in browser
gh browse --settings              # Open settings
gh browse --actions               # Open Actions tab
gh browse path/to/file            # Open specific file
gh browse 123                     # Open issue/PR #123
```

## Pull Requests

### Create
```bash
gh pr create                                    # Interactive
gh pr create --title "Title" --body "Body"      # With content
gh pr create --draft                            # As draft
gh pr create --base main                        # Set base branch
gh pr create --assignee user1,user2             # Add assignees
gh pr create --reviewer user1,user2             # Request reviewers
gh pr create --label bug,enhancement            # Add labels
gh pr create --web                              # Create in browser
```

### List & View
```bash
gh pr list                                    # Open PRs
gh pr list --state all                        # All PRs
gh pr list --state merged                     # Merged PRs
gh pr list --author @me                       # Your PRs
gh pr list --assignee username                # Assigned to user
gh pr list --label bug                        # With label
gh pr list --search "is:open review:required" # Search query
gh pr list --json number,title,author         # JSON output
gh pr view 123                                # View PR
gh pr view 123 --comments                     # With comments
gh pr view 123 --web                          # Open in browser
gh pr view 123 --json title,body,commits      # JSON output
gh pr diff 123                                # View diff
gh pr diff 123 --name-only                    # Files only
```

### Checkout & Work
```bash
gh pr checkout 123                # Checkout PR branch
gh pr checkout 123 --branch name  # Custom branch name
gh pr checks 123                  # View CI checks
gh pr checks 123 --watch          # Watch checks live
```

### Review & Merge
```bash
gh pr review 123                              # Interactive review
gh pr review 123 --approve                    # Approve
gh pr review 123 --request-changes --body "x" # Request changes
gh pr review 123 --comment --body "x"         # Comment
gh pr merge 123                               # Merge (interactive)
gh pr merge 123 --merge                       # Merge commit
gh pr merge 123 --squash                      # Squash merge
gh pr merge 123 --rebase                      # Rebase merge
gh pr merge 123 --delete-branch               # Delete branch after
gh pr merge 123 --admin                       # Bypass checks
```

### Edit & Manage
```bash
gh pr edit 123 --title "New title"            # Edit title
gh pr edit 123 --body "New body"              # Edit body
gh pr edit 123 --add-label bug                # Add label
gh pr edit 123 --remove-label stale           # Remove label
gh pr edit 123 --add-assignee user            # Add assignee
gh pr edit 123 --add-reviewer user            # Add reviewer
gh pr ready 123                               # Mark ready for review
gh pr close 123                               # Close PR
gh pr reopen 123                              # Reopen PR
gh pr update-branch 123                       # Update with base
```

### Comments
```bash
gh pr comment 123 --body "Comment text"       # Add comment
```

## Issues

### Create
```bash
gh issue create                               # Interactive
gh issue create --title "Title" --body "Body" # With content
gh issue create --label bug,high-priority     # With labels
gh issue create --assignee user1,user2        # With assignees
gh issue create --web                         # Create in browser
```

### List & View
```bash
gh issue list                                 # Open issues
gh issue list --state all                     # All issues
gh issue list --state closed                  # Closed issues
gh issue list --assignee @me                  # Assigned to you
gh issue list --label bug                     # With label
gh issue list --milestone "v1.0"              # In milestone
gh issue list --search "is:open label:bug"    # Search query
gh issue list --json number,title,labels      # JSON output
gh issue view 123                             # View issue
gh issue view 123 --comments                  # With comments
gh issue view 123 --web                       # Open in browser
```

### Edit & Manage
```bash
gh issue edit 123 --title "New title"         # Edit title
gh issue edit 123 --body "New body"           # Edit body
gh issue edit 123 --add-label bug             # Add label
gh issue edit 123 --remove-label stale        # Remove label
gh issue edit 123 --add-assignee user         # Add assignee
gh issue edit 123 --milestone "v1.0"          # Set milestone
gh issue close 123                            # Close issue
gh issue close 123 --comment "Fixed in #456"  # Close with comment
gh issue reopen 123                           # Reopen issue
gh issue comment 123 --body "Comment"         # Add comment
gh issue pin 123                              # Pin issue
gh issue unpin 123                            # Unpin issue
gh issue lock 123 --reason off-topic          # Lock conversation
gh issue unlock 123                           # Unlock
gh issue transfer 123 --repo owner/new-repo   # Transfer issue
gh issue delete 123 --yes                     # Delete issue
```

### Development
```bash
gh issue develop 123                          # Create branch from issue
gh issue develop 123 --branch fix/issue-123   # Custom branch name
gh issue status                               # Show issue summary
```

## GitHub Actions

### Workflow Runs
```bash
gh run list                                   # List runs
gh run list --workflow ci.yml                 # For specific workflow
gh run list --branch main                     # For specific branch
gh run list --user username                   # By user
gh run list --json databaseId,status          # JSON output
gh run view 123456789                         # View run
gh run view 123456789 --log                   # View logs
gh run view 123456789 --job 987654            # View specific job
gh run view 123456789 --web                   # Open in browser
gh run watch 123456789                        # Watch live
gh run watch 123456789 --interval 5           # Custom interval
gh run rerun 123456789                        # Rerun failed
gh run rerun 123456789 --job 987654           # Rerun specific job
gh run cancel 123456789                       # Cancel run
gh run delete 123456789                       # Delete run
gh run download 123456789                     # Download artifacts
gh run download 123456789 --name build        # Specific artifact
gh run download 123456789 --dir ./artifacts   # To directory
```

### Workflows
```bash
gh workflow list                              # List workflows
gh workflow view ci.yml                       # View workflow
gh workflow view ci.yml --yaml                # View YAML
gh workflow enable ci.yml                     # Enable workflow
gh workflow disable ci.yml                    # Disable workflow
gh workflow run ci.yml                        # Run manually
gh workflow run ci.yml --ref develop          # Run from branch
gh workflow run ci.yml -f version=1.0.0       # With inputs
```

### Caches
```bash
gh cache list                                 # List caches
gh cache list --branch main                   # For branch
gh cache delete 123456789                     # Delete cache
gh cache delete --all                         # Delete all
```

### Secrets & Variables
```bash
gh secret list                                # List secrets
gh secret set MY_SECRET                       # Set secret (prompts)
echo "value" | gh secret set MY_SECRET        # Set from stdin
gh secret set MY_SECRET --env production      # For environment
gh secret delete MY_SECRET                    # Delete secret

gh variable list                              # List variables
gh variable set MY_VAR "value"                # Set variable
gh variable get MY_VAR                        # Get value
gh variable delete MY_VAR                     # Delete variable
```

## Releases

```bash
gh release list                               # List releases
gh release view                               # View latest
gh release view v1.0.0                        # View specific
gh release view v1.0.0 --web                  # Open in browser

gh release create v1.0.0                      # Create release
gh release create v1.0.0 --notes "Notes"      # With notes
gh release create v1.0.0 --notes-file notes.md # Notes from file
gh release create v1.0.0 --draft              # As draft
gh release create v1.0.0 --prerelease         # As prerelease
gh release create v1.0.0 --target main        # From branch
gh release create v1.0.0 ./file.tar.gz        # With assets

gh release upload v1.0.0 ./file.tar.gz        # Upload asset
gh release download v1.0.0                    # Download assets
gh release download v1.0.0 --pattern "*.zip"  # Specific pattern
gh release download v1.0.0 --archive zip      # Download source

gh release edit v1.0.0 --notes "Updated"      # Edit release
gh release delete v1.0.0 --yes                # Delete release
gh release delete-asset v1.0.0 file.tar.gz    # Delete asset
```

## Search

```bash
gh search repos "stars:>1000 language:python" # Search repos
gh search repos "topic:api" --limit 50        # With limit
gh search repos "org:github" --json name      # JSON output

gh search issues "label:bug state:open"       # Search issues
gh search prs "is:open review:required"       # Search PRs
gh search commits "fix bug"                   # Search commits
gh search code "TODO" --repo owner/repo       # Search code
gh search code "import" --extension py        # By extension
```

## API Requests

```bash
gh api /user                                  # GET request
gh api /repos/owner/repo                      # Specific endpoint

gh api --method POST /repos/owner/repo/issues \
  --field title="Title" \
  --field body="Body"                         # POST with fields

gh api /user --jq '.login'                    # Filter with jq
gh api /user/repos --paginate                 # Paginate results
gh api /user --json                           # Raw JSON

gh api graphql -f query='
  {
    viewer {
      login
      repositories(first: 5) {
        nodes { name }
      }
    }
  }'                                          # GraphQL query
```

## Gists

```bash
gh gist list                                  # List gists
gh gist view abc123                           # View gist
gh gist create script.py                      # Create gist
gh gist create script.py --public             # Public gist
gh gist create script.py --desc "My script"   # With description
gh gist create file1.py file2.py              # Multiple files
echo "code" | gh gist create                  # From stdin
gh gist edit abc123                           # Edit gist
gh gist delete abc123                         # Delete gist
gh gist clone abc123                          # Clone gist
```

## Codespaces

```bash
gh codespace list                             # List codespaces
gh codespace create                           # Create codespace
gh codespace create --repo owner/repo         # For specific repo
gh codespace create --branch develop          # From branch
gh codespace create --machine premiumLinux    # Specific machine
gh codespace ssh                              # SSH into codespace
gh codespace code                             # Open in browser
gh codespace stop                             # Stop codespace
gh codespace delete                           # Delete codespace
gh codespace logs                             # View logs
gh codespace ports                            # List ports
gh codespace cp file.txt :/workspaces/        # Copy to codespace
gh codespace cp :/workspaces/file.txt ./      # Copy from codespace
```

## Projects

```bash
gh project list                               # List projects
gh project view 123                           # View project
gh project create --title "My Project"        # Create project
gh project edit 123 --title "New Title"       # Edit project
gh project delete 123                         # Delete project
gh project close 123                          # Close project
gh project item-list 123                      # List items
gh project item-create 123 --title "Item"     # Create item
gh project item-add 123 --url <issue-url>     # Add issue to project
gh project field-list 123                     # List fields
```

## Labels

```bash
gh label list                                 # List labels
gh label create bug --color "d73a4a"          # Create label
gh label create bug --description "Bug report" # With description
gh label edit bug --name "bug-report"         # Rename label
gh label delete bug                           # Delete label
gh label clone owner/repo                     # Clone labels from repo
```

## Configuration

```bash
gh config list                                # List config
gh config get editor                          # Get value
gh config set editor vim                      # Set value
gh config set git_protocol ssh                # Set git protocol
gh config set prompt disabled                 # Disable prompts
gh config clear-cache                         # Clear cache
```

### Environment Variables
```bash
export GH_TOKEN=ghp_xxx           # Authentication token
export GH_HOST=github.com         # Default host
export GH_REPO=owner/repo         # Default repository
export GH_EDITOR=vim              # Editor
export GH_PAGER=less              # Pager
export GH_PROMPT_DISABLED=true    # Disable prompts
```

## Extensions & Aliases

```bash
gh extension list                             # List extensions
gh extension install owner/repo               # Install extension
gh extension upgrade extension-name           # Upgrade extension
gh extension remove extension-name            # Remove extension
gh extension search github                    # Search extensions

gh alias list                                 # List aliases
gh alias set prview 'pr view --web'           # Set alias
gh alias delete prview                        # Delete alias
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--help` | Show help |
| `--repo OWNER/REPO` | Target repository |
| `--json FIELDS` | JSON output with fields |
| `--jq EXPR` | Filter JSON with jq |
| `--web` | Open in browser |
| `--paginate` | Fetch all pages |

## JSON Output Examples

```bash
# List PRs with specific fields
gh pr list --json number,title,author,labels

# Filter with jq
gh pr list --json number,title --jq '.[] | select(.number > 100)'

# Complex query
gh issue list --json number,title,labels \
  --jq '.[] | {num: .number, title: .title, tags: [.labels[].name]}'

# Get specific value
gh repo view --json stargazersCount --jq '.stargazersCount'
```
