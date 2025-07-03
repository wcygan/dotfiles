---
allowed-tools: Read, Grep, Glob, Bash(fd:*), Bash(rg:*), Bash(bat:*), Edit, MultiEdit
description: Navigate intelligently between related files across the codebase
---

# /code:navigate:related

Intelligently navigates between related files in your codebase, understanding common patterns like test files, API endpoints, components, migrations, and more. Supports creating missing related files and can optionally jump directly to specific functions or sections.

## Current Context

- **Current file**: !`echo "${PWD}/${1:-}" | sed "s|^$HOME|~|"`
- **File type**: !`file -b "${1:-README.md}" 2>/dev/null | cut -d',' -f1`
- **Language**: !`echo "${1:-}" | sed 's/.*\.//' | grep -E "(ts|js|rs|go|java|py|rb|cpp|c|swift|kt)$" || echo "unknown"`
- **Project type**: !`if [ -f "deno.json" ]; then echo "Deno"; elif [ -f "package.json" ]; then echo "Node.js"; elif [ -f "Cargo.toml" ]; then echo "Rust"; elif [ -f "go.mod" ]; then echo "Go"; elif [ -f "pom.xml" ]; then echo "Java"; else echo "Unknown"; fi`

## Usage

```bash
# Navigate from current file to related files
/code:navigate:related

# Navigate from specific file
/code:navigate:related src/models/user.ts

# Go to test file (create if missing)
/code:navigate:related src/models/user.ts test

# Go to specific function in related file
/code:navigate:related src/api/users.ts handler:getUser

# Navigate to implementation from test
/code:navigate:related src/models/user.test.ts impl
```

## Arguments

$ARGUMENTS

## Navigation Patterns

### 1. Test Files

**Common patterns detected:**

```typescript
// Source → Test mappings
"src/models/user.ts" → "src/models/user.test.ts"
"src/models/user.ts" → "tests/models/user.test.ts"
"src/models/user.ts" → "src/models/__tests__/user.test.ts"
"lib/parser.rs" → "tests/parser_test.rs"
"pkg/auth/handler.go" → "pkg/auth/handler_test.go"
"src/User.java" → "test/UserTest.java"

// Test → Source mappings (reverse)
"tests/user.test.ts" → "src/user.ts"
"user_test.go" → "user.go"
```

### 2. API Endpoints

**Frontend ↔ Backend navigation:**

```typescript
// Frontend component → API endpoint
"components/UserProfile.tsx" → "api/users/[id].ts"
"pages/users/[id].tsx" → "routes/api/users/:id.ts"

// API handler → Frontend consumer
"routes/api/auth.ts" → "lib/auth-client.ts"
"server/handlers/users.go" → "client/src/api/users.ts"
```

### 3. Model/Schema Relations

**Database ↔ Application mappings:**

```typescript
// Model → Migration
"models/User.ts" → "migrations/001_create_users.sql"
"src/entities/User.java" → "db/migration/V1__Create_user_table.sql"

// Model → Repository
"models/User.ts" → "repositories/UserRepository.ts"
"domain/user.go" → "repository/user_repository.go"

// Model → Controller
"models/User.ts" → "controllers/UserController.ts"
"pkg/models/user.go" → "pkg/handlers/user_handler.go"
```

### 4. Component Relations

**UI component patterns:**

```typescript
// Component → Story
"components/Button.tsx" → "components/Button.stories.tsx"

// Component → Styles  
"components/Card.tsx" → "components/Card.module.css"
"components/Card.tsx" → "styles/Card.scss"

// Component → Test
"components/Modal.tsx" → "components/Modal.test.tsx"

// Page → Layout
"pages/dashboard.tsx" → "layouts/DashboardLayout.tsx"
```

### 5. Configuration Files

**Code ↔ Config mappings:**

```typescript
// Route handler → Route config
"handlers/webhook.ts" → "config/routes.ts"
"controllers/api.go" → "config/routes.yaml"

// Service → Config
"services/email.ts" → "config/email.ts"
"pkg/cache/redis.go" → "config/redis.yaml"
```

## Implementation

### 1. Parse Arguments

```typescript
// Extract file path and navigation intent
const args = ARGUMENTS.split(" ");
let filePath = args[0] || currentFile;
let navigationType = args[1] || "auto";
let targetLocation = args[2]; // Optional specific location

// Normalize file path
if (!filePath.startsWith("/")) {
  filePath = path.join(process.cwd(), filePath);
}
```

### 2. Detect File Type and Context

```typescript
function detectFileContext(filePath: string) {
  const ext = path.extname(filePath);
  const basename = path.basename(filePath, ext);
  const dir = path.dirname(filePath);

  return {
    isTest: /\.(test|spec|_test)\.[^.]+$/.test(filePath) ||
      dir.includes("__tests__") ||
      dir.includes("tests"),
    isApi: dir.includes("api") ||
      dir.includes("routes") ||
      dir.includes("handlers"),
    isComponent: dir.includes("components") ||
      ext === ".tsx" || ext === ".jsx",
    isModel: dir.includes("models") ||
      dir.includes("entities") ||
      basename.match(/^[A-Z][a-z]+$/),
    isMigration: dir.includes("migrations") ||
      filePath.includes("db/migrate"),
    isConfig: dir.includes("config") ||
      basename.includes("config"),
  };
}
```

### 3. Find Related Files

```typescript
function findRelatedFiles(filePath: string, context: FileContext) {
  const related = [];

  if (context.isTest) {
    // Find implementation file
    related.push(...findImplementation(filePath));
  } else {
    // Find test files
    related.push(...findTests(filePath));
  }

  if (context.isModel) {
    // Find migrations, repositories, controllers
    related.push(...findModelRelated(filePath));
  }

  if (context.isComponent) {
    // Find stories, styles, tests
    related.push(...findComponentRelated(filePath));
  }

  if (context.isApi) {
    // Find frontend consumers, tests, types
    related.push(...findApiRelated(filePath));
  }

  return related;
}
```

### 4. Search Strategies

**Test file search:**

```bash
# For source file src/models/user.ts
BASE="user"
DIR="src/models"

# Search patterns
fd -t f "(${BASE}[._-]test|test[._-]${BASE}|${BASE}[._-]spec|spec[._-]${BASE})\.(ts|js|tsx|jsx)$"
fd -t f "${BASE}\.(test|spec)\.(ts|js|tsx|jsx)$" "$DIR"
fd -t f "${BASE}\.(test|spec)\.(ts|js|tsx|jsx)$" "tests/"
fd -t f "${BASE}\.(test|spec)\.(ts|js|tsx|jsx)$" "__tests__/"
```

**API endpoint search:**

```bash
# For component using /api/users
rg -l "(/api/users|useUsers|fetchUsers)" --type ts --type js
rg -l "(router\.(get|post|put|delete).*users|app\.(get|post).*users)" routes/ api/
```

**Model relations search:**

```bash
# For model User
fd -t f "User(Repository|Repo|Controller|Handler|Service)\.(ts|js|go|java)$"
fd -t f "create.*user.*\.(sql|migration)" migrations/ db/
```

### 5. Navigation Actions

**Jump to file:**

```typescript
if (relatedFiles.length === 1) {
  // Single match - open directly
  console.log(`📍 Navigating to: ${relatedFiles[0]}`);
  await readFile(relatedFiles[0]);
} else if (relatedFiles.length > 1) {
  // Multiple matches - show options
  console.log("🔍 Found multiple related files:");
  relatedFiles.forEach((file, i) => {
    console.log(`  ${i + 1}. ${file}`);
  });
}
```

**Jump to specific location:**

```typescript
if (targetLocation) {
  // Parse location specifier
  const [type, name] = targetLocation.split(":");

  if (type === "function" || type === "handler") {
    // Find function definition
    const pattern = `(function ${name}|const ${name}|${name}\\s*=|def ${name})`;
    const matches = await searchInFile(targetFile, pattern);

    if (matches.length > 0) {
      console.log(`📍 Found ${name} at line ${matches[0].line}`);
    }
  }
}
```

### 6. Create Missing Files

```typescript
if (navigationType === "test" && relatedFiles.length === 0) {
  console.log("🚫 No test file found");

  // Suggest creating test file
  const testPath = suggestTestPath(filePath);
  console.log(`💡 Create test file at: ${testPath}?`);

  // Generate test template
  const template = generateTestTemplate(filePath);
  await writeFile(testPath, template);
}
```

## Smart Features

### Pattern Learning

The command learns from your project structure:

- Detects custom test directories
- Identifies naming conventions
- Recognizes framework patterns
- Adapts to project layout

### Fuzzy Matching

Handles variations in naming:

- `UserController` ↔ `user-controller`
- `authService` ↔ `auth_service`
- `APIHandler` ↔ `api-handler`

### Framework Awareness

Recognizes framework-specific patterns:

- Next.js: `pages/` ↔ `api/`
- Fresh: `routes/` ↔ `islands/`
- Rails: `app/models/` ↔ `db/migrate/`
- Spring: `controller/` ↔ `repository/`

## Examples

### Example 1: Navigate to Test

```bash
/code:navigate:related src/auth/validator.ts test

# Output:
🔍 Searching for test files...
✅ Found: src/auth/validator.test.ts

📍 Navigating to test file...
[Shows test file content]
```

### Example 2: Navigate from Test to Implementation

```bash
/code:navigate:related tests/user.test.ts impl

# Output:
🔍 Searching for implementation...
✅ Found: src/models/user.ts

📍 Navigating to implementation...
[Shows implementation file]
```

### Example 3: Find API Endpoint

```bash
/code:navigate:related components/UserList.tsx api

# Output:
🔍 Searching for related API endpoints...
✅ Found multiple matches:
  1. routes/api/users/index.ts
  2. routes/api/users/[id].ts
  3. lib/api/users.ts

💡 Specify target: /code:navigate:related components/UserList.tsx api:1
```

### Example 4: Create Missing Test

```bash
/code:navigate:related src/utils/crypto.ts test

# Output:
🚫 No test file found for crypto.ts

💡 Creating test file: src/utils/crypto.test.ts

✅ Test template created with:
  - Import statements
  - Basic test structure
  - Common test cases
```

## Best Practices

1. **Use with keybindings** for quick navigation
2. **Combine with `/go-to-related`** for comprehensive navigation
3. **Let it create missing files** to maintain consistency
4. **Use specific targets** when multiple matches exist
5. **Follow project conventions** for predictable navigation

This command transforms codebase navigation from manual searching to intelligent jumping between conceptually related files.
