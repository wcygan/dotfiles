# /translate

Convert code between programming languages, frameworks, or paradigms while maintaining functionality and idiomatic patterns.

## Usage

```
/translate [source code/file] to [target language/framework]
```

## Translation Process

### 1. Source Analysis

```bash
# Understand source patterns
rg "import|require|use|include" source_file
rg "class|struct|interface|trait" source_file
rg "test|spec|describe" test_files

# Identify dependencies
fd "package.json|Cargo.toml|go.mod|pom.xml|requirements.txt"
```

### 2. Translation Mappings

#### Language Constructs

| Source (JS/TS) | Target (Rust)   | Target (Go)     | Target (Java)       |
| -------------- | --------------- | --------------- | ------------------- |
| `async/await`  | `async/await`   | `goroutines`    | `CompletableFuture` |
| `Promise`      | `Future`        | `channel`       | `Future<T>`         |
| `array.map()`  | `.iter().map()` | `for range`     | `.stream().map()`   |
| `try/catch`    | `Result<T, E>`  | `if err != nil` | `try/catch`         |

#### Framework Patterns

**Express.js → Axum (Rust)**

```javascript
// Express.js
app.get("/users/:id", async (req, res) => {
  const user = await db.getUser(req.params.id);
  res.json(user);
});
```

```rust
// Axum
async fn get_user(Path(id): Path<u64>, State(db): State<Database>) -> Json<User> {
    let user = db.get_user(id).await;
    Json(user)
}
```

**Spring Boot → Quarkus (Java)**

```java
// Spring Boot
@RestController
@RequestMapping("/api")
public class UserController {
    @Autowired
    private UserService userService;
    
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}
```

```java
// Quarkus
@Path("/api")
@Produces(MediaType.APPLICATION_JSON)
public class UserResource {
    @Inject
    UserService userService;
    
    @GET
    @Path("/users/{id}")
    public User getUser(@PathParam("id") Long id) {
        return userService.findById(id);
    }
}
```

### 3. Idiomatic Conversions

#### Error Handling

**JavaScript → Rust**

```javascript
// JavaScript
function divide(a, b) {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}
```

```rust
// Rust (idiomatic)
fn divide(a: f64, b: f64) -> Result<f64, &'static str> {
    if b == 0.0 {
        Err("Division by zero")
    } else {
        Ok(a / b)
    }
}
```

#### Collections

**Python → Go**

```python
# Python
users = [u for u in all_users if u.active]
names = [u.name for u in users]
```

```go
// Go (idiomatic)
var users []User
for _, u := range allUsers {
    if u.Active {
        users = append(users, u)
    }
}

names := make([]string, len(users))
for i, u := range users {
    names[i] = u.Name
}
```

### 4. Testing Translation

**Jest (JavaScript) → Deno Test**

```javascript
// Jest
describe("Calculator", () => {
  beforeEach(() => {
    calculator = new Calculator();
  });

  it("should add numbers", () => {
    expect(calculator.add(2, 3)).toBe(5);
  });
});
```

```typescript
// Deno Test
Deno.test("Calculator", async (t) => {
  let calculator: Calculator;

  await t.step("setup", () => {
    calculator = new Calculator();
  });

  await t.step("should add numbers", () => {
    assertEquals(calculator.add(2, 3), 5);
  });
});
```

### 5. Dependency Management

| From     | To         | Command                        |
| -------- | ---------- | ------------------------------ |
| npm/yarn | Cargo      | Map package.json → Cargo.toml  |
| pip      | Go modules | requirements.txt → go.mod      |
| Maven    | Gradle     | pom.xml → build.gradle         |
| npm      | Deno       | package.json → import_map.json |

### 6. Architecture Translation

#### REST API → gRPC

**REST Definition**

```yaml
paths:
  /users/{id}:
    get:
      parameters:
        - name: id
          in: path
          type: integer
```

**gRPC Proto**

```proto
service UserService {
    rpc GetUser(GetUserRequest) returns (User);
}

message GetUserRequest {
    int64 id = 1;
}
```

### 7. Translation Validation

```bash
# Run tests in both versions
deno test           # Source
cargo test          # Target

# Compare outputs
diff <(node original.js) <(cargo run)

# Benchmark performance
hyperfine 'node original.js' 'cargo run --release'
```

## Output Format

```markdown
## Translation Summary

**From:** [Source Language/Framework]
**To:** [Target Language/Framework]
**Files Translated:** X

### Key Conversions:

1. [Pattern A] → [Pattern B]
2. [Library X] → [Library Y]
3. [Idiom M] → [Idiom N]

### Dependencies Mapped:

- package-a (npm) → crate-a (crates.io)
- library-b → library-b-rust

### Code Examples:

[Show 2-3 key translation examples]

### Migration Steps:

1. Install [target language toolchain]
2. Run [build command]
3. Execute tests with [test command]

### Notes:

- [Any functionality differences]
- [Performance considerations]
- [Missing features requiring alternatives]
```

## Common Translations

1. **JavaScript → TypeScript**: Add type annotations
2. **Python → Go**: Replace dynamic typing with interfaces
3. **Java → Kotlin**: Leverage null safety and data classes
4. **REST → GraphQL**: Schema-first design
5. **Callbacks → Promises/Async**: Modernize async patterns
6. **Class-based → Functional**: Extract pure functions
7. **SQL → NoSQL**: Denormalize data models

## Guidelines

- Preserve business logic exactly
- Use target language idioms
- Maintain test coverage
- Document non-obvious conversions
- Consider performance characteristics
- Respect target ecosystem conventions
