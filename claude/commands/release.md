# /release

Automates the entire software release process.

## Usage

```
/release
/release --version <version>
/release --type <patch|minor|major>
/release --prerelease <alpha|beta|rc>
/release --dry-run
```

## Description

This command orchestrates the complete software release workflow, from version bumping and changelog generation to tag creation and distribution. It ensures every release is properly documented, tagged, and published consistently.

### What it does:

#### 1. Version Management

Intelligently determines the next version based on conventional commits or user input:

**Semantic Version Detection:**

- Analyzes commit messages since last release
- Automatically determines version bump type:
  - `patch`: Bug fixes, documentation updates
  - `minor`: New features, backwards-compatible changes
  - `major`: Breaking changes, API modifications

**Version Bump Examples:**

```bash
# Current version: v1.2.3

# Commits since last release:
# - fix: resolve memory leak in auth handler
# - docs: update API documentation
# Result: v1.2.4 (patch release)

# Commits since last release:
# - feat: add user profile endpoints
# - fix: resolve login timeout issue
# Result: v1.3.0 (minor release)

# Commits since last release:
# - feat!: migrate to new authentication system
# - BREAKING CHANGE: removed deprecated /v1/auth endpoint
# Result: v2.0.0 (major release)
```

#### 2. Comprehensive Changelog Generation

Creates detailed, user-friendly changelogs from git history:

**Generated CHANGELOG.md:**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2024-06-06

### Added

- User profile management endpoints for enhanced user experience (#123)
- Real-time notification system with WebSocket support (#145)
- Advanced search functionality with full-text indexing (#156)
- Export functionality for user data (GDPR compliance) (#167)

### Changed

- Improved authentication token refresh mechanism (#134)
- Updated database connection pooling for better performance (#142)
- Enhanced error messages for better debugging (#151)

### Fixed

- Resolved memory leak in background job processor (#129)
- Fixed race condition in concurrent user registration (#138)
- Corrected timezone handling in scheduled tasks (#149)

### Security

- Updated JWT library to address security vulnerability CVE-2024-1234 (#161)
- Implemented rate limiting for authentication endpoints (#165)

### Breaking Changes

- Removed deprecated `/v1/auth/login` endpoint (use `/v2/auth/login`)
- Changed response format for `/api/users` - now returns `{ users: [...] }`

### Migration Guide

For users upgrading from v1.2.x:

1. Update authentication endpoints to use `/v2/auth/*`
2. Update API response parsing for user list endpoints
3. Review and update any hardcoded API paths

### Contributors

- @alice (8 commits)
- @bob (5 commits)
- @charlie (3 commits)

## [1.2.3] - 2024-05-15

### Fixed

- Critical security fix for SQL injection vulnerability (#118)
- Resolved Docker build issues on ARM64 platforms (#121)

[Full Changelog](https://github.com/org/repo/compare/v1.2.2...v1.2.3)
```

#### 3. Multi-Language Version Updates

Updates version information across different project files:

**Go Projects:**

````go
// cmd/version.go
package main

const (
    Version = \"1.3.0\"\n    BuildDate = \"2024-06-06T14:30:00Z\"\n    GitCommit = \"abc123def456\"\n)\n```\n\n**Rust Projects:**\n```toml\n# Cargo.toml\n[package]\nname = \"myapp\"\nversion = \"1.3.0\"\nedition = \"2021\"\n\n# Also updates Cargo.lock automatically\n```\n\n**Node.js/Deno Projects:**\n```json\n// package.json\n{\n  \"name\": \"myapp\",\n  \"version\": \"1.3.0\",\n  \"description\": \"My awesome application\"\n}\n\n// deno.json\n{\n  \"name\": \"@org/myapp\",\n  \"version\": \"1.3.0\",\n  \"exports\": \"./mod.ts\"\n}\n```\n\n**Java Projects:**\n```xml\n<!-- pom.xml -->\n<project>\n    <groupId>com.example</groupId>\n    <artifactId>myapp</artifactId>\n    <version>1.3.0</version>\n</project>\n\n<!-- gradle.properties -->\nversion=1.3.0\n```\n\n#### 4. Git Tag Creation and Management\nCreates annotated git tags with comprehensive metadata:\n\n**Tag Creation:**\n```bash\n# Creates annotated tag with changelog excerpt\ngit tag -a v1.3.0 -m \"Release v1.3.0\n\nNew Features:\n- User profile management endpoints\n- Real-time notification system\n- Advanced search functionality\n\nBreaking Changes:\n- Removed deprecated /v1/auth/login endpoint\n\nSee CHANGELOG.md for complete release notes.\"\n\n# Push tag to remote\ngit push origin v1.3.0\n```\n\n#### 5. GitHub Release Creation\nGenerates comprehensive GitHub releases with assets:\n\n**Release Creation Script:**\n```bash\n# Create GitHub release with gh CLI\ngh release create v1.3.0 \\\n  --title \"Release v1.3.0 - Enhanced User Management\" \\\n  --notes-file release-notes.md \\\n  --target main\n\n# Upload release artifacts\ngh release upload v1.3.0 \\\n  dist/myapp-linux-amd64.tar.gz \\\n  dist/myapp-darwin-amd64.tar.gz \\\n  dist/myapp-windows-amd64.zip \\\n  dist/checksums.txt\n```\n\n**Generated Release Notes:**\n```markdown\n## 🚀 What's New in v1.3.0\n\n### ✨ New Features\n- **User Profiles**: Complete user profile management system\n- **Real-time Notifications**: WebSocket-based notification system\n- **Advanced Search**: Full-text search with filtering and sorting\n- **Data Export**: GDPR-compliant user data export functionality\n\n### 🔧 Improvements\n- Enhanced authentication with automatic token refresh\n- Improved database performance with connection pooling\n- Better error messages for easier debugging\n\n### 🐛 Bug Fixes\n- Fixed memory leak in background job processor\n- Resolved race condition in user registration\n- Corrected timezone handling in scheduled tasks\n\n### 🔒 Security Updates\n- Updated JWT library (addresses CVE-2024-1234)\n- Implemented rate limiting for auth endpoints\n\n### ⚠️ Breaking Changes\n- Removed deprecated `/v1/auth/login` endpoint\n- Changed response format for `/api/users` endpoint\n\n### 📥 Installation\n\n#### Docker\n```bash\ndocker pull ghcr.io/org/myapp:v1.3.0\n```\n\n#### Binary Downloads\n- [Linux (AMD64)](https://github.com/org/myapp/releases/download/v1.3.0/myapp-linux-amd64.tar.gz)\n- [macOS (AMD64)](https://github.com/org/myapp/releases/download/v1.3.0/myapp-darwin-amd64.tar.gz)\n- [Windows (AMD64)](https://github.com/org/myapp/releases/download/v1.3.0/myapp-windows-amd64.zip)\n\n#### Package Managers\n```bash\n# Homebrew (macOS)\nbrew install org/tap/myapp\n\n# npm\nnpm install -g @org/myapp\n\n# Go\ngo install github.com/org/myapp/cmd/myapp@v1.3.0\n```\n\n### 🔄 Migration Guide\n\nFor users upgrading from v1.2.x, please review our [migration guide](MIGRATION.md).\n\n### 👥 Contributors\n\nSpecial thanks to all contributors who made this release possible:\n- @alice - User profile system implementation\n- @bob - Real-time notification architecture\n- @charlie - Search functionality and performance optimizations\n\n**Full Changelog**: https://github.com/org/myapp/compare/v1.2.3...v1.3.0\n```\n\n#### 6. Artifact Building and Distribution\nBuilds and distributes release artifacts across platforms:\n\n**Multi-Platform Build:**\n```bash\n#!/bin/bash\n# Generated build script\n\nVERSION=\"1.3.0\"\nPROJECT=\"myapp\"\n\n# Build for multiple platforms\nplatforms=(\"linux/amd64\" \"linux/arm64\" \"darwin/amd64\" \"darwin/arm64\" \"windows/amd64\")\n\nfor platform in \"${platforms[@]}\"; do\n    OS=$(echo $platform | cut -d'/' -f1)\n    ARCH=$(echo $platform | cut -d'/' -f2)\n    \n    echo \"Building for $OS/$ARCH...\"\n    \n    if [ \"$OS\" = \"windows\" ]; then\n        EXT=\".exe\"\n    else\n        EXT=\"\"\n    fi\n    \n    env GOOS=$OS GOARCH=$ARCH go build \\\n        -ldflags=\"-X main.Version=$VERSION -X main.BuildDate=$(date -u +%Y-%m-%dT%H:%M:%SZ)\" \\\n        -o \"dist/${PROJECT}-${OS}-${ARCH}${EXT}\" \\\n        ./cmd/main.go\n    \n    # Create archive\n    if [ \"$OS\" = \"windows\" ]; then\n        zip \"dist/${PROJECT}-${OS}-${ARCH}.zip\" \"dist/${PROJECT}-${OS}-${ARCH}${EXT}\"\n    else\n        tar -czf \"dist/${PROJECT}-${OS}-${ARCH}.tar.gz\" -C dist \"${PROJECT}-${OS}-${ARCH}${EXT}\"\n    fi\ndone\n\n# Generate checksums\ncd dist\nsha256sum *.tar.gz *.zip > checksums.txt\ncd ..\n\necho \"Build completed for version $VERSION\"\n```\n\n### 7. Package Publishing\nAutomatically publishes to relevant package registries:\n\n**Registry Publishing:**\n```bash\n# Docker Registry\ndocker build -t myapp:$VERSION .\ndocker tag myapp:$VERSION ghcr.io/org/myapp:$VERSION\ndocker tag myapp:$VERSION ghcr.io/org/myapp:latest\ndocker push ghcr.io/org/myapp:$VERSION\ndocker push ghcr.io/org/myapp:latest\n\n# NPM Registry (for Node.js/Deno packages)\nnpm publish --access public\n\n# Cargo Registry (for Rust crates)\ncargo publish\n\n# Go Module (automatic via git tags)\n# GOPROXY will automatically index the new tag\n\n# Homebrew Tap Update\n# Updates formula with new version and checksums\n```\n\n### 8. Notification and Communication\nNotifies teams and stakeholders about the release:\n\n**Automated Notifications:**\n```bash\n# Slack notification\ncurl -X POST -H 'Content-type: application/json' \\\n  --data '{\n    \"text\": \"🚀 Release v1.3.0 is now available!\",\n    \"blocks\": [\n      {\n        \"type\": \"section\",\n        \"text\": {\n          \"type\": \"mrkdwn\",\n          \"text\": \"*MyApp v1.3.0* has been released!\\n\\n✨ New user profile management\\n📊 Real-time notifications\\n🔍 Advanced search functionality\\n\\n<https://github.com/org/myapp/releases/tag/v1.3.0|View Release Notes>\"\n        }\n      }\n    ]\n  }' \\\n  $SLACK_WEBHOOK_URL\n\n# Email notification to stakeholders\n# Discord webhook\n# Teams notification\n```\n\n## Release Types\n\n### Standard Release\n```\n/release\n```\nAnalyzes commits and creates appropriate version bump.\n\n### Patch Release\n```\n/release --type patch\n```\nForces a patch version increment (bug fixes only).\n\n### Minor Release\n```\n/release --type minor\n```\nForces a minor version increment (new features).\n\n### Major Release\n```\n/release --type major\n```\nForces a major version increment (breaking changes).\n\n### Prerelease\n```\n/release --prerelease beta\n```\nCreates prerelease version (v1.3.0-beta.1).\n\n### Custom Version\n```\n/release --version 2.0.0-rc.1\n```\nSpecifies exact version number.\n\n### Dry Run\n```\n/release --dry-run\n```\nShows what would be released without making changes.\n\n## Configuration\nSupports project-specific configuration via `.releaserc.yml`:\n\n```yaml\n# Release configuration\nrelease:\n  # Version bumping strategy\n  version_strategy: \"conventional\"  # conventional, manual, calendar\n  \n  # Changelog generation\n  changelog:\n    include_authors: true\n    group_by_type: true\n    breaking_changes_section: true\n    migration_guide: true\n  \n  # Build and distribution\n  build:\n    platforms: [\"linux/amd64\", \"darwin/amd64\", \"windows/amd64\"]\n    archive_format: \"tar.gz\"  # zip for windows\n    include_checksums: true\n  \n  # Publishing targets\n  publish:\n    github_releases: true\n    docker_registry: \"ghcr.io\"\n    npm_registry: true\n    homebrew_tap: \"org/homebrew-tap\"\n  \n  # Notifications\n  notifications:\n    slack_webhook: \"${SLACK_WEBHOOK_URL}\"\n    email_recipients: [\"releases@company.com\"]\n    discord_webhook: \"${DISCORD_WEBHOOK_URL}\"\n  \n  # Git settings\n  git:\n    tag_format: \"v{version}\"\n    commit_message: \"chore(release): {version}\"\n    sign_tags: true\n```\n\n## Pre-Release Validation\nPerforms comprehensive checks before releasing:\n\n**Release Checklist:**\n- [ ] All tests pass in CI\n- [ ] No uncommitted changes in working directory\n- [ ] Current branch is main/master\n- [ ] Local branch is up to date with remote\n- [ ] No security vulnerabilities in dependencies\n- [ ] Documentation is up to date\n- [ ] Breaking changes are documented\n- [ ] Migration guide is provided (if needed)\n\n## Integration with Other Commands\n- Uses `/document` to update documentation before release\n- Integrates with `/ci-gen` to ensure proper CI/CD pipeline\n- Combines with `/containerize` for Docker image releases\n- Uses `/harden` security checks before release
````
