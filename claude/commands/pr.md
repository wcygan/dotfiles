# /pr

Automates creation of high-quality, descriptive pull requests.

## Usage

```
/pr
/pr --draft
/pr --template <template_name>
/pr --reviewers <@user1,@user2>
```

## Description

This command analyzes your current branch changes and creates a comprehensive pull request with proper formatting, context, and metadata. It enforces team conventions and improves communication efficiency.

### What it does:

#### 1. Change Analysis

Analyzes the current branch to understand the scope and nature of changes:

**Git Analysis:**

- Compares current branch against main/master using `git diff main...HEAD`
- Identifies modified, added, and deleted files
- Analyzes commit history since branch divergence
- Detects code patterns and architectural changes

**Code Impact Assessment:**

- Identifies breaking changes in public APIs
- Detects database migrations or schema changes
- Recognizes new dependencies or version updates
- Flags potential security implications

#### 2. Intelligent Title Generation

Creates conventional commit-style titles based on change analysis:

**Title Patterns:**

```
feat(api): add user profile management endpoints
fix(auth): resolve JWT token expiration handling
refactor(database): migrate from REST to GraphQL
docs(readme): update installation instructions
chore(deps): upgrade axios to v1.6.0
```

**Scope Detection:**

- Analyzes changed files to determine scope (api, frontend, auth, etc.)
- Uses directory structure and file patterns for context
- Considers framework conventions (controllers, services, components)

#### 3. Comprehensive Description Generation

Generates structured PR descriptions with multiple sections:

**Standard Template:**

```markdown
## Summary

- **What**: Brief description of the changes made
- **Why**: Business justification or problem being solved
- **How**: Technical approach and implementation details

## Changes Made

- [ ] Added user profile API endpoints (`/api/v1/profile/*`)
- [ ] Implemented profile validation middleware
- [ ] Updated database schema with profile fields
- [ ] Added comprehensive test coverage (95% line coverage)

## Testing

- [ ] Unit tests pass (`npm test`)
- [ ] Integration tests pass (`npm run test:integration`)
- [ ] Manual testing completed for profile CRUD operations
- [ ] Security testing for authentication edge cases

## Breaking Changes

⚠️ **BREAKING**: Modified `/api/v1/user` response format

- Old: `{ "user": { "name": "...", "email": "..." } }`
- New: `{ "user": { "profile": { "name": "...", "email": "..." } } }`

## Migration Guide

For API consumers:

1. Update response parsing logic to access `user.profile.*`
2. Update any hardcoded field references
3. Test against staging environment before production deployment

## Screenshots/Demo

<!-- Add screenshots for UI changes -->
<!-- Add API response examples for backend changes -->

## Checklist

- [x] Code follows project style guidelines
- [x] Tests added/updated for new functionality
- [x] Documentation updated
- [x] No merge conflicts
- [ ] Security review completed (if applicable)
- [ ] Performance impact assessed
```

#### 4. Issue Linking

Automatically links related issues and tickets:

**Branch Name Analysis:**

- Detects patterns like `feature/JIRA-123-user-profiles`
- Extracts issue numbers from branch names
- Generates appropriate closing keywords

**Generated Links:**

```markdown
Closes #123
Fixes JIRA-456
Resolves https://github.com/org/repo/issues/789
```

#### 5. Smart Reviewer Suggestions

Suggests relevant reviewers based on code analysis:

**Review Assignment Logic:**

- Analyzes `git blame` on changed files to find frequent contributors
- Considers CODEOWNERS file if present
- Suggests domain experts based on file paths (frontend, backend, DevOps)
- Balances review load across team members

**Team Detection:**

```yaml
# .github/CODEOWNERS
/src/api/ @backend-team @alice
/src/frontend/ @frontend-team @bob
/k8s/ @devops-team @charlie
*.md @docs-team
```

#### 6. Template System

Supports custom PR templates for different change types:

**Template Detection:**

- Analyzes changes to determine appropriate template
- Supports feature, bugfix, hotfix, and documentation templates
- Uses `.github/pull_request_template/` directory structure

**Custom Templates:**

```markdown
<!-- .github/pull_request_template/feature.md -->

## New Feature Checklist

- [ ] Feature flag implemented (if applicable)
- [ ] A/B testing configuration added
- [ ] Analytics events implemented
- [ ] Feature documentation written
- [ ] Rollback plan documented
```

### Advanced Features

#### CI/CD Integration

Generates PR descriptions that trigger appropriate CI workflows:

**Workflow Triggers:**

```markdown
<!-- Trigger specific test suites -->

/test backend
/test frontend\
/test e2e

<!-- Deploy to staging -->

/deploy staging

<!-- Security scan -->

/security-scan
```

#### Performance Impact Analysis

Analyzes potential performance implications:

**Bundle Size Analysis:**

- Detects new dependencies that might increase bundle size
- Warns about large file additions
- Suggests code splitting opportunities

**Database Impact:**

- Identifies new queries or schema changes
- Warns about N+1 query patterns
- Suggests indexing for new query patterns

#### Security Considerations

Flags potential security implications:

**Security Checklist:**

- Authentication/authorization changes
- New external dependencies
- Input validation modifications
- Environment variable changes

## Examples

### Create a standard PR:

```
/pr
```

### Create a draft PR for early feedback:

```
/pr --draft
```

### Use a specific template:

```
/pr --template hotfix
```

### Specify reviewers:

```
/pr --reviewers @alice,@backend-team
```

## Configuration

Supports team-specific configuration via `.github/pr-config.yml`:

```yaml
teams:
  backend: ["alice", "bob"]
  frontend: ["charlie", "diana"]
  devops: ["eve"]

templates:
  feature: ".github/pull_request_template/feature.md"
  bugfix: ".github/pull_request_template/bugfix.md"
  hotfix: ".github/pull_request_template/hotfix.md"

auto_reviewers:
  min_reviewers: 2
  exclude_author: true
  balance_load: true

required_checks:
  - "ci/build"
  - "ci/test"
  - "security/scan"

labels:
  auto_assign: true
  size_labels: true # small, medium, large based on diff size
  type_labels: true # feature, bugfix, docs, etc.
```

## Quality Assurance

### PR Title Validation

- Enforces conventional commit format
- Validates scope against known project modules
- Suggests improvements for unclear titles

### Description Quality Checks

- Ensures minimum description length
- Validates required sections are present
- Checks for TODO items or placeholder text

### Change Validation

- Warns about large PRs (suggests splitting)
- Flags missing tests for new features
- Detects missing documentation updates

## Integration with Other Commands

- Use after `/refactor` to document architectural changes
- Combine with `/test` results to include coverage information
- Use with `/document` to ensure documentation is updated
- Integrate with `/review` findings to address code quality issues
