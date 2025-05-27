# Testing GitHub Actions Locally

This guide explains how to test your GitHub Actions workflows locally using [Act](https://github.com/nektos/act) before pushing to GitHub.

## Quick Start

```bash
# Install Act (macOS)
brew install act

# Test all workflows
deno task test:actions --help

# Test specific workflow
deno task test:actions -w ci.yml

# Test specific job
deno task test:actions -w ci.yml -j quality
```

## Available Workflows

### 🔧 CI Workflow (`ci.yml`)

**Purpose**: Comprehensive testing and validation
**Triggers**: Push to main/develop, Pull Requests, Weekly schedule

**Jobs**:

- **Code Quality**: TypeScript linting, formatting, type checking
- **Integration Tests**: Cross-platform testing (Linux, macOS, Windows)
- **Smoke Tests**: Actual installation testing on clean VMs
- **Security**: Vulnerability scanning and secret detection

**Test locally**:

```bash
# Test all CI jobs
deno task test:actions -w ci.yml

# Test just code quality
deno task test:actions -w ci.yml -j quality

# Test integration tests
deno task test:actions -w ci.yml -j integration-tests
```

### 🔄 Maintenance Workflow (`maintenance.yml`)

**Purpose**: Automated maintenance and health checks
**Triggers**: Daily at 2 AM UTC, Manual trigger

**Jobs**:

- **Dependency Updates**: Check for Deno and tool updates
- **Health Checks**: Validate configuration and scripts
- **Performance Monitoring**: Track installation times

**Test locally**:

```bash
deno task test:actions -w maintenance.yml
```

### 📚 Documentation Workflow (`docs.yml`)

**Purpose**: Documentation validation and updates
**Triggers**: Changes to markdown files or core scripts

**Jobs**:

- **Validate Documentation**: Markdown linting and link checking
- **Update Usage Statistics**: Generate repository statistics

**Test locally**:

```bash
deno task test:actions -w docs.yml
```

## Testing Commands

### Basic Testing

```bash
# List all available workflows
deno task test:actions --list-workflows

# Test specific workflow
deno task test:actions -w ci.yml

# Test specific job in workflow
deno task test:actions -w ci.yml -j quality

# Test with specific platform
deno task test:actions -w ci.yml --platform ubuntu-latest
```

### Advanced Testing

```bash
# Dry run (validate without executing)
deno task test:actions -w ci.yml --dry-run

# Verbose output for debugging
deno task test:actions -w ci.yml --verbose

# Test specific event trigger
deno task test:actions -w ci.yml --event push
```

## Common Issues and Solutions

### 1. **Docker Not Running**

```
Error: Cannot connect to the Docker daemon
```

**Solution**: Start Docker Desktop or Docker daemon

### 2. **Git Repository Issues**

```
Error: fatal: not a git repository
```

**Solution**: Some jobs expect a proper git repository. This is normal for local testing.

### 3. **Network Issues**

```
Error: Failed to download action
```

**Solution**: Check internet connection. Act downloads actions on first run.

### 4. **Permission Issues**

```
Error: Permission denied
```

**Solution**: Ensure Docker has proper permissions and Act is installed correctly.

## Best Practices

### Before Pushing

1. **Run code quality checks**:
   ```bash
   deno task test:actions -w ci.yml -j quality
   ```

2. **Run integration tests**:
   ```bash
   deno task test:actions -w ci.yml -j integration-tests
   ```

3. **Validate documentation**:
   ```bash
   deno task test:actions -w docs.yml
   ```

### During Development

1. **Test frequently**: Run relevant jobs after making changes
2. **Use specific jobs**: Don't run entire workflows for small changes
3. **Check logs**: Use `--verbose` for debugging issues

### Performance Tips

1. **Use caching**: Act caches Docker images and actions
2. **Test specific jobs**: Faster than running entire workflows
3. **Clean up**: Occasionally run `docker system prune` to free space

## Workflow Matrix Testing

The CI workflow tests multiple combinations:

| Platform | Shell | Test Type           |
| -------- | ----- | ------------------- |
| Ubuntu   | bash  | Integration + Smoke |
| Ubuntu   | zsh   | Integration         |
| macOS    | bash  | Integration + Smoke |
| macOS    | zsh   | Integration         |
| Windows  | bash  | Integration         |

**Test specific matrix combinations**:

```bash
# Test Ubuntu + bash combination
deno task test:actions -w ci.yml -j integration-tests --platform ubuntu-latest

# Test macOS + zsh combination  
deno task test:actions -w ci.yml -j integration-tests --platform macos-latest
```

## Debugging Failed Tests

### 1. **Check Logs**

```bash
deno task test:actions -w ci.yml -j quality --verbose
```

### 2. **Run Individual Steps**

```bash
# Run linting manually
deno lint

# Run formatting check
deno fmt --check

# Run type checking
deno task check
```

### 3. **Test Integration Scripts**

```bash
# Run integration tests directly
deno task test

# Test bash enhancements
deno task test:bash
```

## Configuration Files

- **`.actrc`**: Act configuration and Docker image settings
- **`.github/workflows/`**: GitHub Actions workflow definitions
- **`scripts/test-actions-locally.ts`**: Local testing helper script
- **`deno.json`**: Task definitions for easy testing

## Resources

- [Act Documentation](https://github.com/nektos/act)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Deno Testing Guide](https://deno.land/manual/testing)

## Support

If you encounter issues:

1. Check this guide for common solutions
2. Review Act documentation
3. Validate your workflow syntax
4. Test individual components manually
5. Check Docker and system requirements
