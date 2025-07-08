---
sidebar_position: 1
---

# Scripts Reference

The dotfiles repository includes several Deno TypeScript scripts for automation and management.

## Installation Scripts

### install-safely.ts

The main installation script with safety features:

```bash
deno run --allow-all scripts/install-safely.ts [options]

Options:
  --force              Skip confirmation prompts
  --dry-run            Show what would be installed without making changes
  --backup-dir <path>  Custom backup directory (default: ~/.dotfiles-backup)
  --help               Show help information
```

Features:
- Automatic backup creation
- Platform detection
- Parallel file operations
- Validation before installation

### rollback.ts

Restore previous configuration from backups:

```bash
deno run --allow-all scripts/rollback.ts [options]

Options:
  --backup <timestamp>  Specific backup to restore
  --force              Skip confirmation
  --list               List available backups
```

## Testing Scripts

### integration-test.ts

Comprehensive test suite for installation process:

```bash
deno test --allow-all scripts/integration-test.ts
```

Tests include:
- Installation validation
- Backup creation
- Rollback functionality
- Cross-platform compatibility

### pre-commit-check.ts

Pre-commit validation script:

```bash
deno run --allow-all scripts/pre-commit-check.ts [options]

Options:
  --fix                Auto-fix issues where possible
```

Checks:
- TypeScript compilation
- File formatting
- Import validation
- Script permissions

## CI/CD Scripts

### ci-environment-check.ts

Validate CI environment setup:

```bash
deno run --allow-all scripts/ci-environment-check.ts [options]

Options:
  --critical-only      Check only critical items
  --fix               Attempt to fix issues
```

### test-actions-locally.ts

Test GitHub Actions workflows locally:

```bash
deno run --allow-all scripts/test-actions-locally.ts
```

Uses act or similar tools to simulate GitHub Actions environment.

## Utility Scripts

### clean-backups.ts

Manage backup directory size:

```bash
deno run --allow-all scripts/clean-backups.ts [options]

Options:
  --keep <number>      Number of backups to keep (default: 5)
  --older-than <days>  Remove backups older than X days
  --dry-run           Show what would be removed
```

### generate-docs.ts

Generate documentation from Claude commands:

```bash
deno run --allow-read --allow-write scripts/generate-docs.ts
```

Features:
- Parses command YAML frontmatter
- Creates Docusaurus-compatible markdown
- Maintains category structure
- Auto-updates navigation

## Script Development

### Creating New Scripts

Follow these patterns when creating new scripts:

```typescript
#!/usr/bin/env -S deno run --allow-read --allow-write

import { parseArgs } from "@std/cli/parse-args";
import { cyan, green, red } from "@std/fmt/colors";

// Parse command-line arguments
const args = parseArgs(Deno.args, {
  boolean: ["help", "force"],
  string: ["output"],
  default: {
    force: false,
  },
});

// Main function
async function main() {
  if (args.help) {
    showHelp();
    return;
  }
  
  // Script logic here
}

// Run if main module
if (import.meta.main) {
  main().catch((error) => {
    console.error(red(`Error: ${error.message}`));
    Deno.exit(1);
  });
}
```

### Best Practices

1. **Use JSR imports**: Import from `@std/*` packages
2. **Handle errors gracefully**: Provide clear error messages
3. **Add help text**: Include usage examples
4. **Make scripts executable**: Add shebang and set permissions
5. **Use colored output**: Enhance readability with colors
6. **Validate inputs**: Check arguments before processing
7. **Provide dry-run mode**: Allow users to preview changes

### Testing Scripts

Test scripts thoroughly:

```typescript
// In your test file
import { assertEquals } from "@std/assert";
import { main } from "./your-script.ts";

Deno.test("script functionality", async () => {
  // Test implementation
});
```

## Performance Optimization

Scripts use parallel processing where applicable:

```typescript
// Parallel file operations
await Promise.all(
  files.map(async (file) => {
    await processFile(file);
  })
);

// Concurrent directory traversal
const results = await Promise.allSettled(
  directories.map(scanDirectory)
);
```

This approach provides significant speedups for I/O-bound operations.