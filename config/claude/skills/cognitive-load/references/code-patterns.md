# Code-Level Cognitive Load Patterns

Anti-patterns that consume working memory at the code level, with concrete fixes.

---

## 1. Complex Conditionals

**Cognitive cost**: Reader must mentally evaluate and hold multiple boolean states simultaneously.

### Before (high load)
```
if val > someConstant && (condition2 || condition3) && (condition4 && !condition5) {
    // ...
}
```
Reader must hold 5 conditions + their logical relationships — exceeds working memory.

### After (low load)
```
isValid := val > someConstant
isAllowed := condition2 || condition3
isSecure := condition4 && !condition5

if isValid && isAllowed && isSecure {
    // ...
}
```
Reader processes 3 named concepts. Each name is a chunk that encapsulates its internals.

**Rule**: If a conditional has more than 2-3 terms, extract to named intermediates.

---

## 2. Deep Nesting

**Cognitive cost**: Each nesting level adds a precondition the reader must hold in memory. At depth 4+, the reader cannot remember why they're in the current branch.

### Before (high load)
```python
def process(request):
    if request.is_valid():
        user = get_user(request)
        if user is not None:
            if user.has_permission():
                result = do_work(user, request)
                if result.success:
                    return result
                else:
                    return Error("work failed")
            else:
                return Error("no permission")
        else:
            return Error("no user")
    else:
        return Error("invalid request")
```

### After (low load)
```python
def process(request):
    if not request.is_valid():
        return Error("invalid request")

    user = get_user(request)
    if user is None:
        return Error("no user")

    if not user.has_permission():
        return Error("no permission")

    result = do_work(user, request)
    if not result.success:
        return Error("work failed")

    return result
```

Early returns free working memory — the reader only holds the current concern, not accumulated preconditions.

**Rule**: Maximum nesting depth of 2. If deeper, refactor with early returns or extract functions.

---

## 3. Inheritance Chains

**Cognitive cost**: Understanding `AdminController` requires mentally loading `UserController` → `GuestController` → `BaseController`. Each parent class is a chunk.

### Before (high load)
```java
class BaseController { /* 200 lines */ }
class GuestController extends BaseController { /* overrides 5 methods */ }
class UserController extends GuestController { /* overrides 3 methods */ }
class AdminController extends UserController { /* overrides 2 methods */ }
```
To understand `AdminController`, the reader must hold 4 class definitions and track which methods are overridden at which level.

### After (low load)
```java
class AdminController {
    private final AuthService auth;
    private final PermissionService permissions;
    private final ResponseBuilder response;

    // All behavior is explicit, local, and traceable
}
```

**Rule**: Prefer composition over inheritance. If you must inherit, limit to 1 level deep.

---

## 4. Implicit Behavior ("Magic")

**Cognitive cost**: The reader sees code that doesn't do what it appears to do. Hidden interceptors, decorators, middleware, or framework conventions alter behavior invisibly.

### Signs of magic
- A function call triggers 5 other things not visible in the call site
- Annotation/decorator changes method behavior fundamentally
- Convention-based routing that requires framework-specific knowledge
- Auto-wired dependencies with no visible construction

### Fix
- Make side effects explicit at the call site
- Prefer explicit wiring over auto-discovery
- If using a framework, isolate framework-specific code from business logic
- New contributors should be able to trace a request end-to-end without framework docs

**Rule**: If a new developer can't trace execution by reading the code linearly, there's hidden cognitive load.

---

## 5. Numeric/Opaque Codes

**Cognitive cost**: Reader must maintain a mental mapping table (e.g., 401 = expired token, 403 = insufficient access, 418 = rate limited).

### Before (high load)
```python
if response.status == 401:
    # Is this expired? Invalid? Missing?
    handle_auth_error()
elif response.status == 403:
    # Forbidden? Rate limited? IP blocked?
    handle_forbidden()
```

### After (low load)
```json
{"code": "jwt_has_expired"}
{"code": "insufficient_permissions"}
{"code": "rate_limit_exceeded"}
```
```python
if response.code == "jwt_has_expired":
    refresh_token()
```

**Rule**: Use self-describing string codes for application-level errors. Reserve HTTP status codes for HTTP semantics.

---

## 6. Clever Code

**Cognitive cost**: The reader must reverse-engineer the author's intent from non-obvious constructs.

### Signs of cleverness
- Bitwise operations where arithmetic would work
- Ternary chains longer than one level
- Regex used for parsing structured data
- One-liners that replace 5 readable lines
- Variable reuse (same variable means different things at different points)

### Fix
Write code at half your cleverness level. The remaining capacity is needed for debugging.

**Rule**: If you feel proud of how concise your code is, it's probably too clever.

---

## 7. Naming That Requires Context

**Cognitive cost**: Names like `data`, `result`, `tmp`, `val`, `info`, `manager`, `handler`, `processor`, `service` require the reader to infer meaning from surrounding code.

### Weak names (high load)
```
data = fetch(id)
result = process(data)
handle(result)
```

### Strong names (low load)
```
userProfile = fetchUserProfile(userId)
validatedProfile = validateAge(userProfile)
sendWelcomeEmail(validatedProfile)
```

**Rule**: A name should tell the reader what it IS, not what it DOES generically. If you'd need a comment to explain a variable, the name is wrong.

---

## 8. Long Functions

**Cognitive cost**: A function longer than ~40 lines exceeds what a reader can hold in working memory as a single concept.

### Signs
- You need to scroll to understand a function
- Local variables at the top are forgotten by the time you reach the bottom
- Multiple levels of abstraction in the same function

### Fix
Extract sections into well-named functions. Each function should operate at one level of abstraction.

**Rule**: If you can't describe what a function does in one sentence without "and", split it.

---

## Summary Table

| Pattern | Chunks Consumed | Fix |
|---------|----------------|-----|
| Complex conditional | 3-5 per expression | Named intermediates |
| Nested ifs (depth 4) | 4+ preconditions | Early returns |
| Inheritance (3 levels) | 3+ class definitions | Composition |
| Magic/implicit behavior | Unknown (worst case) | Explicit wiring |
| Opaque codes | 1 per mapping | Self-describing strings |
| Clever one-liners | 2-4 per construct | Readable equivalent |
| Generic names | 1 per lookup | Specific names |
| Long functions | 4+ per scroll | Extract sub-functions |
