# /simplify

Refactor complex code to be more readable, maintainable, and easier to understand while preserving functionality.

## Usage

```
/simplify [file path or code block]
```

## Simplification Process

### 1. Complexity Analysis

```bash
# Identify complexity hotspots
rg "if.*if.*if|for.*for|while.*while" -A 10  # Nested structures
rg "&&.*&&|\\|\\|.*\\|\\|" -A 5              # Complex conditionals
rg "function.*{.*function|=>.*=>" -A 10       # Nested functions
fd "test" --type f | xargs rg -l "skip|todo"  # Untested code
```

### 2. Simplification Strategies

#### Extract Methods

**Before:**

```javascript
function processOrder(order) {
  // 50 lines of validation logic
  // 30 lines of calculation
  // 40 lines of formatting
}
```

**After:**

```javascript
function processOrder(order) {
  const validatedOrder = validateOrder(order);
  const calculations = calculateTotals(validatedOrder);
  return formatOrderResponse(calculations);
}
```

#### Simplify Conditionals

**Before:**

```python
if user.age >= 18 and user.age <= 65 and user.status == "active" and not user.suspended:
    if user.balance > 0 or user.credit_limit > 0:
        return True
return False
```

**After:**

```python
def is_eligible_user(user):
    is_valid_age = 18 <= user.age <= 65
    is_active = user.status == "active" and not user.suspended
    has_funds = user.balance > 0 or user.credit_limit > 0
    
    return is_valid_age and is_active and has_funds
```

#### Replace Loops with Higher-Order Functions

**Before:**

```rust
let mut results = Vec::new();
for item in items {
    if item.is_valid() {
        results.push(item.transform());
    }
}
```

**After:**

```rust
let results: Vec<_> = items
    .into_iter()
    .filter(|item| item.is_valid())
    .map(|item| item.transform())
    .collect();
```

#### Use Early Returns

**Before:**

```go
func process(data Data) (Result, error) {
    if data != nil {
        if data.IsValid() {
            result := compute(data)
            if result != nil {
                return result, nil
            } else {
                return nil, errors.New("computation failed")
            }
        } else {
            return nil, errors.New("invalid data")
        }
    } else {
        return nil, errors.New("nil data")
    }
}
```

**After:**

```go
func process(data Data) (Result, error) {
    if data == nil {
        return nil, errors.New("nil data")
    }
    
    if !data.IsValid() {
        return nil, errors.New("invalid data")
    }
    
    result := compute(data)
    if result == nil {
        return nil, errors.New("computation failed")
    }
    
    return result, nil
}
```

#### Extract Constants and Magic Numbers

**Before:**

```java
if (retries > 3 && delay > 1000) {
    wait(delay * 1.5);
}
```

**After:**

```java
private static final int MAX_RETRIES = 3;
private static final long MIN_DELAY_MS = 1000;
private static final double BACKOFF_MULTIPLIER = 1.5;

if (retries > MAX_RETRIES && delay > MIN_DELAY_MS) {
    wait((long)(delay * BACKOFF_MULTIPLIER));
}
```

### 3. Naming Improvements

- Replace abbreviations with full words
- Use domain-specific terminology
- Make boolean names interrogative
- Avoid generic names (data, info, temp)

### 4. Structure Improvements

#### Before

```typescript
class OrderProcessor {
  // 500 lines of mixed concerns
}
```

#### After

```typescript
class OrderProcessor {
  constructor(
    private validator: OrderValidator,
    private calculator: PriceCalculator,
    private notifier: CustomerNotifier,
  ) {}

  async process(order: Order): Promise<ProcessedOrder> {
    const validated = await this.validator.validate(order);
    const priced = await this.calculator.calculate(validated);
    await this.notifier.notify(priced);
    return priced;
  }
}
```

### 5. Testing Simplification

- Extract test helpers
- Use descriptive test names
- Remove test duplication
- Add missing edge cases

### 6. Documentation

Add clear, concise comments only where necessary:

```python
# Calculate compound interest using the formula: A = P(1 + r/n)^(nt)
def calculate_compound_interest(principal, rate, time, compounds_per_year):
    return principal * (1 + rate/compounds_per_year) ** (compounds_per_year * time)
```

## Validation

After simplification, ensure:

- All tests still pass
- No functionality is lost
- Performance hasn't degraded
- Code coverage is maintained

## Output Format

```markdown
## Simplification Summary

**Complexity Reduced From:** [metrics]
**Complexity Reduced To:** [metrics]

### Changes Made:

1. Extracted X methods for better separation of concerns
2. Simplified Y conditional expressions
3. Replaced Z loops with functional constructs
4. Improved naming for N variables/functions

### Key Improvements:

- Reduced cyclomatic complexity from A to B
- Improved readability score from C to D
- Decreased file length from E to F lines

### Code Diff:

[Show key before/after examples]
```

## Guidelines

- Preserve all functionality
- Maintain or improve performance
- Keep domain logic intact
- Follow language idioms
- Consider team conventions
- Add tests for refactored code
