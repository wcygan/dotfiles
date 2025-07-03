# /standardize

Apply consistent coding standards, naming conventions, and architectural patterns across the entire codebase.

## Usage

```
/standardize [aspect: code|naming|structure|all] [scope]
```

## Standardization Process

### 1. Codebase Analysis

```bash
# Detect inconsistencies
rg "class|interface|struct|type" --type-add 'code:*.{ts,js,go,rs,java}' -t code | sort | uniq -c

# Find naming patterns
rg "^(const|let|var|def|fn|func)" -o | sort | uniq -c

# Check file organization
fd . --type f | sed 's|.*/||' | sed 's|\..*||' | sort | uniq -c

# Identify formatting issues
deno fmt --check
go fmt ./...
cargo fmt -- --check
```

### 2. Code Style Standards

#### Naming Conventions

```typescript
// standardize-naming.ts
interface NamingRules {
  files: {
    components: "PascalCase"; // UserProfile.tsx
    utilities: "kebab-case"; // string-utils.ts
    constants: "SCREAMING_SNAKE"; // API_ENDPOINTS.ts
    types: "PascalCase"; // UserTypes.ts
  };

  variables: {
    constants: "SCREAMING_SNAKE_CASE"; // MAX_RETRY_COUNT
    booleans: "is/has/should prefix"; // isLoading, hasError
    functions: "camelCase verb"; // getUserData, validateInput
    classes: "PascalCase noun"; // UserService, DataProcessor
  };

  database: {
    tables: "snake_case plural"; // user_accounts, order_items
    columns: "snake_case"; // created_at, user_id
    indexes: "idx_table_columns"; // idx_users_email
    constraints: "fk_table_column"; // fk_orders_user_id
  };
}

async function standardizeNaming(directory: string) {
  const renames: Array<{ from: string; to: string }> = [];

  for await (const entry of walk(directory)) {
    if (entry.isFile) {
      // Check file naming
      const standardName = getStandardFileName(entry.name);
      if (standardName !== entry.name) {
        renames.push({
          from: entry.path,
          to: entry.path.replace(entry.name, standardName),
        });
      }

      // Check content naming
      const content = await Deno.readTextFile(entry.path);
      const standardContent = standardizeCodeNaming(content);
      if (content !== standardContent) {
        await Deno.writeTextFile(entry.path, standardContent);
      }
    }
  }

  // Execute renames
  for (const rename of renames) {
    await Deno.rename(rename.from, rename.to);
    // Update imports
    await updateImports(rename.from, rename.to);
  }
}
```

#### Import Organization

```typescript
// standardize-imports.ts
const IMPORT_ORDER = [
  // 1. Node/Deno built-ins
  /^(node:|https:\/\/deno\.land\/std)/,

  // 2. External packages
  /^(@|[a-z])/,

  // 3. Internal aliases
  /^@\//,

  // 4. Relative imports
  /^\./,
];

function standardizeImports(content: string): string {
  const lines = content.split("\n");
  const imports: Map<number, string[]> = new Map();
  const otherLines: string[] = [];

  // Categorize imports
  for (const line of lines) {
    if (line.startsWith("import")) {
      const category = IMPORT_ORDER.findIndex((regex) => regex.test(line));
      if (!imports.has(category)) {
        imports.set(category, []);
      }
      imports.get(category)!.push(line);
    } else {
      otherLines.push(line);
    }
  }

  // Rebuild with organized imports
  const organized: string[] = [];
  for (let i = 0; i < IMPORT_ORDER.length; i++) {
    const categoryImports = imports.get(i);
    if (categoryImports?.length) {
      organized.push(...categoryImports.sort());
      organized.push(""); // blank line between categories
    }
  }

  return [...organized, ...otherLines].join("\n");
}
```

### 3. Project Structure Standards

```typescript
// standardize-structure.ts
const STANDARD_STRUCTURE = {
  "src/": {
    "components/": "React/UI components",
    "services/": "Business logic",
    "utils/": "Helper functions",
    "types/": "TypeScript types",
    "hooks/": "React hooks",
    "api/": "API clients",
    "config/": "Configuration",
  },
  "tests/": {
    "unit/": "Unit tests",
    "integration/": "Integration tests",
    "e2e/": "End-to-end tests",
  },
  "scripts/": "Build and utility scripts",
  "docs/": "Documentation",
};

async function standardizeStructure(rootPath: string) {
  // Create standard directories
  for (const [dir, subdirs] of Object.entries(STANDARD_STRUCTURE)) {
    const dirPath = join(rootPath, dir);
    await ensureDir(dirPath);

    if (typeof subdirs === "object") {
      for (const subdir of Object.keys(subdirs)) {
        await ensureDir(join(dirPath, subdir));
      }
    }
  }

  // Move files to appropriate locations
  const moves: Array<{ from: string; to: string }> = [];

  for await (const entry of walk(rootPath)) {
    if (entry.isFile) {
      const standardPath = getStandardPath(entry.path);
      if (standardPath !== entry.path) {
        moves.push({ from: entry.path, to: standardPath });
      }
    }
  }

  // Execute moves and update imports
  for (const move of moves) {
    await Deno.rename(move.from, move.to);
    await updateImports(move.from, move.to);
  }
}
```

### 4. Code Pattern Standards

#### Error Handling

```typescript
// Before
try {
  const data = getData();
  return data;
} catch (e) {
  console.log(e);
  return null;
}

// After (standardized)
class DataError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = "DataError";
  }
}

async function getDataSafe(): Promise<Result<Data, DataError>> {
  try {
    const data = await getData();
    return { ok: true, value: data };
  } catch (error) {
    logger.error("Failed to get data", { error });
    return {
      ok: false,
      error: new DataError("Data retrieval failed", "DATA_FETCH_ERROR"),
    };
  }
}
```

#### API Response Format

```typescript
// Standardized API response
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    timestamp: string;
    version: string;
    requestId: string;
  };
}

function standardizeApiHandler<T>(
  handler: () => Promise<T>
): async (req: Request) => Promise<Response> {
  return async (req: Request) => {
    const requestId = crypto.randomUUID();
    
    try {
      const data = await handler();
      return Response.json({
        success: true,
        data,
        meta: {
          timestamp: new Date().toISOString(),
          version: APP_VERSION,
          requestId,
        },
      });
    } catch (error) {
      logger.error('API handler error', { error, requestId });
      return Response.json({
        success: false,
        error: {
          code: error.code || 'INTERNAL_ERROR',
          message: error.message || 'An error occurred',
        },
        meta: {
          timestamp: new Date().toISOString(),
          version: APP_VERSION,
          requestId,
        },
      }, { status: error.status || 500 });
    }
  };
}
```

### 5. Configuration Standards

```typescript
// config-standard.ts
interface StandardConfig {
  app: {
    name: string;
    version: string;
    environment: "development" | "staging" | "production";
  };

  server: {
    host: string;
    port: number;
    cors: {
      origins: string[];
      credentials: boolean;
    };
  };

  database: {
    host: string;
    port: number;
    name: string;
    user: string;
    password: string;
    ssl: boolean;
  };

  logging: {
    level: "debug" | "info" | "warn" | "error";
    format: "json" | "pretty";
  };
}

// Standardized config loading
function loadConfig(): StandardConfig {
  return {
    app: {
      name: Deno.env.get("APP_NAME") || "app",
      version: Deno.env.get("APP_VERSION") || "0.0.0",
      environment: (Deno.env.get("APP_ENV") || "development") as any,
    },
    server: {
      host: Deno.env.get("HOST") || "0.0.0.0",
      port: parseInt(Deno.env.get("PORT") || "8000"),
      cors: {
        origins: (Deno.env.get("CORS_ORIGINS") || "*").split(","),
        credentials: Deno.env.get("CORS_CREDENTIALS") === "true",
      },
    },
    // ... more config
  };
}
```

### 6. Testing Standards

```typescript
// test-standards.ts
// Standardized test structure
Deno.test("ComponentName", async (t) => {
  // Setup
  await t.step("setup", () => {
    // Common setup
  });

  // Feature tests
  await t.step("should handle normal case", () => {
    // Arrange
    const input = createTestInput();

    // Act
    const result = functionUnderTest(input);

    // Assert
    assertEquals(result, expectedOutput);
  });

  await t.step("should handle error case", () => {
    // Test error scenarios
  });

  // Cleanup
  await t.step("cleanup", () => {
    // Cleanup resources
  });
});

// Standardized test utilities
const TestUtils = {
  createMockUser: (overrides = {}) => ({
    id: "test-id",
    email: "test@example.com",
    name: "Test User",
    ...overrides,
  }),

  createMockRequest: (overrides = {}) =>
    new Request("http://localhost", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      ...overrides,
    }),
};
```

### 7. Documentation Standards

````typescript
/**
 * Processes user data according to business rules.
 *
 * @param userData - The user data to process
 * @param options - Processing options
 * @returns Processed user data
 *
 * @example
 * ```typescript
 * const result = await processUser(userData, { validate: true });
 * ```
 *
 * @throws {ValidationError} If userData is invalid
 * @throws {ProcessingError} If processing fails
 */
async function processUser(
  userData: UserData,
  options: ProcessOptions = {},
): Promise<ProcessedUser> {
  // Implementation
}
````

## Output Format

````markdown
# Standardization Report

## Summary

- **Files Analyzed**: X
- **Changes Made**: Y
- **Patterns Fixed**: Z

## Changes Applied

### Naming Conventions

- ✅ Renamed X files to follow conventions
- ✅ Updated Y variable names
- ✅ Standardized Z function names

### Code Structure

- ✅ Reorganized imports in X files
- ✅ Moved Y files to standard locations
- ✅ Created Z missing directories

### Patterns Standardized

- ✅ Error handling (X occurrences)
- ✅ API responses (Y endpoints)
- ✅ Configuration loading (Z files)

### Before/After Examples

```typescript
// Before
const get_user_data = (userId) => { ... }

// After  
const getUserData = (userId: string): Promise<UserData> => { ... }
```
````

## Remaining Issues

- [ ] Manual review needed for X complex cases
- [ ] Y files have custom patterns that need discussion
- [ ] Z deprecated patterns need migration plan

## Next Steps

1. Review and commit changes
2. Update documentation
3. Configure linters/formatters
4. Set up pre-commit hooks

```
## Standards Checklist

- [ ] Consistent file naming
- [ ] Organized imports
- [ ] Standard error handling
- [ ] Unified API responses
- [ ] Common logging format
- [ ] Shared type definitions
- [ ] Test structure consistency
- [ ] Documentation format

## Guidelines

- Apply changes incrementally
- Preserve functionality
- Update tests alongside code
- Document exceptions
- Configure automated checks
- Train team on standards
```
