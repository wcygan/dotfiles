# Framework Templates

## Framework Detection

| Language | Frameworks | Config Files | Test File Patterns |
|----------|-----------|-------------|-------------------|
| TypeScript/JavaScript | Jest, Vitest, Mocha, Deno.test, Bun.test | `jest.config.*`, `vitest.config.*`, `deno.json` | `*.test.ts`, `*.spec.ts`, `__tests__/` |
| Python | pytest, unittest, nose2 | `pytest.ini`, `setup.cfg`, `pyproject.toml` | `test_*.py`, `*_test.py`, `tests/` |
| Go | go test | `go.mod` | `*_test.go` |
| Rust | cargo test | `Cargo.toml` | `#[cfg(test)]`, `tests/` |
| Java | JUnit, TestNG | `pom.xml`, `build.gradle` | `*Test.java`, `src/test/` |

## Naming Conventions

| Pattern | Example |
|---------|---------|
| Behavior-first | `should_return_empty_array_when_input_is_null` |
| Describe/it (JS) | `describe('fn') → it('should ...')` |
| Given/When/Then | `given_valid_user_when_login_then_returns_token` |
| Go table-driven | `t.Run("returns error for invalid input", ...)` |

---

## Jest / Vitest (TypeScript/JavaScript)

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest'; // or jest
import { functionUnderTest } from '../src/module';

describe('functionUnderTest', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('when given valid input', () => {
    it('should return expected result', () => {
      const result = functionUnderTest(validInput);
      expect(result).toEqual(expectedOutput);
    });
  });

  describe('when given invalid input', () => {
    it('should throw an error', () => {
      expect(() => functionUnderTest(invalidInput)).toThrow(ExpectedError);
    });
  });

  describe('edge cases', () => {
    it('should handle empty input', () => {
      expect(functionUnderTest([])).toEqual([]);
    });
  });
});
```

---

## pytest (Python)

```python
import pytest
from module import function_under_test

class TestFunctionUnderTest:
    """Tests for function_under_test."""

    def test_returns_expected_result_for_valid_input(self):
        result = function_under_test(valid_input)
        assert result == expected_output

    def test_raises_error_for_invalid_input(self):
        with pytest.raises(ExpectedError):
            function_under_test(invalid_input)

    @pytest.mark.parametrize("input,expected", [
        ([], []),
        ([1], [1]),
        ([1, 2, 3], [1, 2, 3]),
    ])
    def test_handles_various_sizes(self, input, expected):
        assert function_under_test(input) == expected
```

---

## Go (go test)

```go
package module_test

import (
    "testing"
    "github.com/stretchr/testify/assert" // if used in project
    "your/module"
)

func TestFunctionUnderTest(t *testing.T) {
    t.Run("returns expected result for valid input", func(t *testing.T) {
        result := module.FunctionUnderTest(validInput)
        assert.Equal(t, expectedOutput, result)
    })

    t.Run("returns error for invalid input", func(t *testing.T) {
        _, err := module.FunctionUnderTest(invalidInput)
        assert.Error(t, err)
    })
}

// Table-driven pattern (preferred for many cases)
func TestFunctionUnderTest_TableDriven(t *testing.T) {
    tests := []struct {
        name     string
        input    InputType
        expected OutputType
        wantErr  bool
    }{
        {"valid input", validInput, expectedOutput, false},
        {"empty input", emptyInput, emptyOutput, false},
        {"invalid input", invalidInput, zeroOutput, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := module.FunctionUnderTest(tt.input)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
                assert.Equal(t, tt.expected, result)
            }
        })
    }
}
```

---

## Rust (cargo test)

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn returns_expected_result_for_valid_input() {
        let result = function_under_test(valid_input);
        assert_eq!(result, expected_output);
    }

    #[test]
    #[should_panic(expected = "error message")]
    fn panics_for_invalid_input() {
        function_under_test(invalid_input);
    }

    #[test]
    fn handles_empty_input() {
        let result = function_under_test(vec![]);
        assert_eq!(result, vec![]);
    }
}
```

---

## Coverage Report Template

```
## Test Coverage Expansion

### Target: <file/module name>

### Existing Coverage (before)
- Tests found: <count>
- Functions covered: <list>
- Gaps identified: <list>

### New Tests Added
| Test Name | Scenario | Type |
|-----------|----------|------|
| should_... | happy path | unit |
| should_... | null input | edge case |
| should_... | network failure | error |

### Coverage Improvement
- New tests: <count>
- Functions now covered: <list>
- Remaining gaps: <list or "none">

### Run Command
<command to run new tests>
```
