# /test-gen

Generate comprehensive test suites with intelligent test case creation based on code analysis and testing best practices.

## Usage

```
/test-gen [component|api|e2e|all] [--framework=auto] [--coverage-target=80]
```

## Parameters

- `component` - Generate unit/component tests for specific modules
- `api` - Generate API endpoint tests with realistic scenarios
- `e2e` - Generate end-to-end testing workflows
- `all` - Generate complete test suite across all categories
- `--framework` - Override framework detection (jest, vitest, deno, pytest, cargo, go)
- `--coverage-target` - Set coverage percentage goal (default: 80%)

## Context Intelligence

### Framework Detection

**JavaScript/TypeScript Projects:**

```bash
# Detect testing framework from package.json
fd "package.json" | xargs jq -r '.devDependencies | keys[]' | rg "(jest|vitest|mocha|ava)"

# Deno projects
fd "deno.json" | xargs jq -r '.tasks | keys[]' | rg "test"

# Test file patterns
fd "(test|spec)\.(js|ts|jsx|tsx)$" --max-depth 2
```

**Rust Projects:**

```bash
# Cargo.toml analysis
fd "Cargo.toml" | xargs rg "\[dev-dependencies\]" -A 10
fd "lib.rs|main.rs" | xargs rg "#\[cfg\(test\)\]"
```

**Go Projects:**

```bash
# Test file detection
fd "_test\.go$" 
go list ./... | rg "test"
```

**Python Projects:**

```bash
# Testing framework detection
fd "(requirements|pyproject).(txt|toml)" | xargs rg "(pytest|unittest|nose)"
fd "test_.*\.py$|.*_test\.py$"
```

## Test Generation Strategies

### 1. Unit/Component Test Generation

**Analysis Phase:**

```bash
# Extract function signatures and interfaces
case $DETECTED_LANGUAGE in
  "typescript"|"javascript")
    # Parse TypeScript/JavaScript for functions and classes
    rg "^(export\s+)?(function|class|const|let)\s+\w+" --type ts --type js -A 3
    ;;
  "rust")
    # Extract public functions and structs
    rg "^pub\s+(fn|struct|enum|trait)" --type rust -A 2
    ;;
  "go")
    # Extract public functions and types
    rg "^func\s+[A-Z]\w*|^type\s+[A-Z]\w*" --type go -A 2
    ;;
  "python")
    # Extract classes and functions
    rg "^(class|def)\s+\w+" --type py -A 2
    ;;
esac
```

**Test Template Generation:**

**TypeScript/Deno Example:**

```typescript
// Generated tests for UserService
import { assertEquals, assertRejects } from "@std/assert";
import { UserService } from "../src/user-service.ts";

Deno.test("UserService - createUser with valid data", async () => {
  const userService = new UserService();
  const userData = {
    email: "test@example.com",
    name: "Test User",
  };

  const result = await userService.createUser(userData);

  assertEquals(result.email, userData.email);
  assertEquals(result.name, userData.name);
  assertEquals(typeof result.id, "string");
});

Deno.test("UserService - createUser with invalid email", async () => {
  const userService = new UserService();
  const userData = {
    email: "invalid-email",
    name: "Test User",
  };

  await assertRejects(
    () => userService.createUser(userData),
    Error,
    "Invalid email format",
  );
});

Deno.test("UserService - findUser by ID", async () => {
  const userService = new UserService();

  // Test existing user
  const existingUser = await userService.findUser("user123");
  assertEquals(existingUser.id, "user123");

  // Test non-existing user
  const nonExistingUser = await userService.findUser("nonexistent");
  assertEquals(nonExistingUser, null);
});
```

**Rust Example:**

```rust
// Generated tests for user_service module
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_create_user_with_valid_data() {
        let user_service = UserService::new();
        let user_data = CreateUserRequest {
            email: "test@example.com".to_string(),
            name: "Test User".to_string(),
        };
        
        let result = user_service.create_user(user_data).await.unwrap();
        
        assert_eq!(result.email, "test@example.com");
        assert_eq!(result.name, "Test User");
        assert!(!result.id.is_empty());
    }
    
    #[tokio::test]
    async fn test_create_user_with_invalid_email() {
        let user_service = UserService::new();
        let user_data = CreateUserRequest {
            email: "invalid-email".to_string(),
            name: "Test User".to_string(),
        };
        
        let result = user_service.create_user(user_data).await;
        
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("Invalid email"));
    }
    
    #[test]
    fn test_validate_email() {
        assert!(validate_email("test@example.com"));
        assert!(!validate_email("invalid-email"));
        assert!(!validate_email(""));
    }
}
```

### 2. API Test Generation

**API Endpoint Discovery:**

```bash
# Analyze API routes and endpoints
case $FRAMEWORK in
  "axum"|"actix")
    rg "Router::new\(\)|\.route\(" --type rust -A 2
    ;;
  "express"|"fastify")
    rg "(app|router)\.(get|post|put|delete|patch)" --type js --type ts -A 2
    ;;
  "spring"|"quarkus")
    rg "@(GetMapping|PostMapping|PutMapping|DeleteMapping)" --type java -A 2
    ;;
  "connectrpc"|"gin")
    rg "func.*Handler|router\.(GET|POST|PUT|DELETE)" --type go -A 2
    ;;
esac
```

**Generated API Tests:**

**Deno/Fresh Example:**

```typescript
// Generated API tests for user endpoints
import { assertEquals } from "@std/assert";
import { createHandler } from "../routes/api/users/index.ts";

Deno.test("POST /api/users - create user successfully", async () => {
  const request = new Request("http://localhost:8000/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: "test@example.com",
      name: "Test User",
    }),
  });

  const response = await createHandler(request);

  assertEquals(response.status, 201);
  const body = await response.json();
  assertEquals(body.email, "test@example.com");
  assertEquals(body.name, "Test User");
});

Deno.test("POST /api/users - validation error", async () => {
  const request = new Request("http://localhost:8000/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: "invalid-email",
      name: "",
    }),
  });

  const response = await createHandler(request);

  assertEquals(response.status, 400);
  const body = await response.json();
  assertEquals(body.error, "Validation failed");
});
```

**Rust/Axum Example:**

```rust
// Generated integration tests for user API
#[cfg(test)]
mod integration_tests {
    use super::*;
    use axum::{
        body::Body,
        http::{Request, StatusCode},
    };
    use tower::ServiceExt;
    use serde_json::json;
    
    #[tokio::test]
    async fn test_create_user_success() {
        let app = create_app().await;
        
        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/users")
                    .header("content-type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&json!({
                            "email": "test@example.com",
                            "name": "Test User"
                        })).unwrap()
                    ))
                    .unwrap()
            )
            .await
            .unwrap();
            
        assert_eq!(response.status(), StatusCode::CREATED);
        
        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let user: User = serde_json::from_slice(&body).unwrap();
        
        assert_eq!(user.email, "test@example.com");
        assert_eq!(user.name, "Test User");
    }
}
```

### 3. End-to-End Test Generation

**E2E Test Setup:**

**Playwright/Deno Example:**

```typescript
// Generated E2E tests with Playwright
import { expect, test } from "@playwright/test";

test.describe("User Management Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("http://localhost:8000");
  });

  test("complete user registration flow", async ({ page }) => {
    // Navigate to registration
    await page.click('[data-testid="register-link"]');
    await expect(page).toHaveURL(/.*\/register/);

    // Fill registration form
    await page.fill('[data-testid="email-input"]', "test@example.com");
    await page.fill('[data-testid="name-input"]', "Test User");
    await page.fill('[data-testid="password-input"]', "SecurePass123!");

    // Submit form
    await page.click('[data-testid="register-button"]');

    // Verify success
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page).toHaveURL(/.*\/dashboard/);
  });

  test("user login and logout flow", async ({ page }) => {
    // Login
    await page.click('[data-testid="login-link"]');
    await page.fill('[data-testid="email-input"]', "test@example.com");
    await page.fill('[data-testid="password-input"]', "SecurePass123!");
    await page.click('[data-testid="login-button"]');

    // Verify dashboard access
    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.locator('[data-testid="user-name"]')).toContainText("Test User");

    // Logout
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL(/.*\/login/);
  });
});
```

## Test Data Generation

### Realistic Test Data Creation

**Faker Integration:**

```typescript
// Generated test data utilities
import { faker } from "@faker-js/faker";

export class TestDataGenerator {
  static generateUser() {
    return {
      id: faker.string.uuid(),
      email: faker.internet.email(),
      name: faker.person.fullName(),
      createdAt: faker.date.recent().toISOString(),
      isActive: faker.datatype.boolean(),
    };
  }

  static generateProduct() {
    return {
      id: faker.string.uuid(),
      name: faker.commerce.productName(),
      price: parseFloat(faker.commerce.price()),
      category: faker.commerce.department(),
      inStock: faker.number.int({ min: 0, max: 100 }),
    };
  }

  static generateBulkUsers(count: number) {
    return Array.from({ length: count }, () => this.generateUser());
  }
}
```

## Mock and Stub Generation

### Database Mocks

**TypeScript/Deno Example:**

```typescript
// Generated database mocks
export class MockUserRepository implements UserRepository {
  private users: Map<string, User> = new Map();

  async create(user: CreateUserRequest): Promise<User> {
    const newUser: User = {
      id: crypto.randomUUID(),
      ...user,
      createdAt: new Date().toISOString(),
    };
    this.users.set(newUser.id, newUser);
    return newUser;
  }

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }

  async findByEmail(email: string): Promise<User | null> {
    for (const user of this.users.values()) {
      if (user.email === email) return user;
    }
    return null;
  }

  clear() {
    this.users.clear();
  }
}
```

### External Service Mocks

**HTTP Mocks with MSW:**

```typescript
// Generated API mocks
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

export const handlers = [
  http.get("https://api.external-service.com/users/:id", ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id,
      name: "Mock User",
      email: "mock@example.com",
    });
  }),

  http.post("https://api.payment-service.com/charge", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      id: "charge_123",
      amount: body.amount,
      status: "succeeded",
    });
  }),
];

export const server = setupServer(...handlers);
```

## Test Configuration Generation

### Framework-Specific Configuration

**Deno Test Configuration:**

```json
{
  "tasks": {
    "test": "deno test --allow-all --coverage=coverage",
    "test:watch": "deno test --allow-all --watch",
    "test:unit": "deno test --allow-all tests/unit/",
    "test:integration": "deno test --allow-all tests/integration/",
    "test:e2e": "deno test --allow-all tests/e2e/",
    "coverage": "deno coverage coverage --html"
  },
  "exclude": ["coverage/"]
}
```

**Rust Test Configuration:**

```toml
# Generated test configuration in Cargo.toml
[dev-dependencies]
tokio-test = "0.4"
mockall = "0.12"
rstest = "0.18"
fake = "2.9"

[[test]]
name = "integration"
path = "tests/integration/mod.rs"

[[test]]
name = "api"
path = "tests/api/mod.rs"
```

## CI/CD Integration

### Test Automation in CI

**GitHub Actions Integration:**

```yaml
# Generated test workflow
- name: Run tests with coverage
  run: |
    case ${{ matrix.language }} in
      "deno")
        deno task test
        deno task coverage
        ;;
      "rust")
        cargo test --all-features
        cargo tarpaulin --out Xml
        ;;
      "go")
        go test -v -race -coverprofile=coverage.out ./...
        go tool cover -html=coverage.out -o coverage.html
        ;;
    esac

- name: Upload coverage reports
  uses: codecov/codecov-action@v3
  with:
    file: coverage.xml
```

## Output

The command generates:

1. **Test Files**: Comprehensive test suites with realistic scenarios
2. **Test Data Utilities**: Faker integration and mock data generators
3. **Mock Services**: Database and external service mocks
4. **Configuration**: Framework-specific test configuration
5. **CI Integration**: Automated testing workflows
6. **Coverage Reports**: HTML and XML coverage reporting setup

## Integration with Other Commands

- Use with `/coverage` for detailed coverage analysis
- Combine with `/flaky-fix` for test reliability improvements
- Integrate with `/ci-gen` for automated test execution
- Use with `/debug` for test troubleshooting
