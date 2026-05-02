#!/usr/bin/env bash
# Bisection script to find which test creates unwanted files/state.
# Auto-detects runner: Rust (cargo) | Vitest | Bun | npm.
#
# Usage:   ./find-polluter.sh <pollution-path> <test-pattern>
# Rust:    ./find-polluter.sh '.git' 'tests/*.rs'
# Vitest:  ./find-polluter.sh '.git' 'src/**/*.test.ts'
# Bun:     ./find-polluter.sh '.git' 'src/**/*.test.ts'
# npm:     ./find-polluter.sh '.git' 'src/**/*.test.ts'
#
# DIVERGES FROM upstream obra/superpowers — Rust/Vitest/Bun dispatch added
# locally. `vendor-superpowers.py --update` will overwrite this file; re-apply
# from this version (search "RUNNER DISPATCH").

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 <pollution-path> <test-pattern>"
  echo "  Rust:   $0 '.git' 'tests/*.rs'"
  echo "  JS/TS:  $0 '.git' 'src/**/*.test.ts'   (auto-detects vitest/bun/npm)"
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_PATTERN="$2"

echo "🔍 Searching for test that creates: $POLLUTION_CHECK"
echo "Test pattern: $TEST_PATTERN"
echo ""

TEST_FILES=$(find . -path "$TEST_PATTERN" -o -path "./$TEST_PATTERN" 2>/dev/null | sort -u)
TOTAL=$(printf '%s\n' "$TEST_FILES" | grep -c .)

if [ "$TOTAL" -eq 0 ]; then
  echo "No files matched '$TEST_PATTERN'"
  exit 1
fi

# --- RUNNER DISPATCH -------------------------------------------------------
# Detection order matters: a Bun project may also configure Vitest. Vitest
# wins when configured because `bun test` can't read vitest.config.
has_bun_lockfile() {
  [ -f bun.lock ] || [ -f bun.lockb ] || [ -f bunfig.toml ]
}

has_vitest_config() {
  for f in vitest.config.ts vitest.config.mts vitest.config.js \
           vitest.config.mjs vitest.config.cjs; do
    [ -f "$f" ] && return 0
  done
  # TanStack Start scaffolds keep Vitest config inline in vite.config.*
  for f in vite.config.ts vite.config.mts vite.config.js \
           vite.config.mjs vite.config.cjs; do
    [ -f "$f" ] && grep -qE 'vitest|[[:space:]]test:' "$f" 2>/dev/null && return 0
  done
  return 1
}

FIRST=$(printf '%s\n' "$TEST_FILES" | head -1)
case "$FIRST" in
  *.rs)
    RUNNER="rust"
    ;;
  *)
    if has_vitest_config; then
      RUNNER="vitest"
    elif has_bun_lockfile; then
      RUNNER="bun"
    else
      RUNNER="node"
    fi
    ;;
esac

# Vitest invoker depends on whether bun is the package manager.
if [ "$RUNNER" = "vitest" ]; then
  if has_bun_lockfile; then
    VITEST_CMD="bunx vitest run"
  else
    VITEST_CMD="npx vitest run"
  fi
fi
# --- END RUNNER DISPATCH ---------------------------------------------------

echo "Found $TOTAL test files (runner: $RUNNER)"
echo ""

COUNT=0
for TEST_FILE in $TEST_FILES; do
  COUNT=$((COUNT + 1))

  if [ -e "$POLLUTION_CHECK" ]; then
    echo "⚠️  Pollution already exists before test $COUNT/$TOTAL"
    echo "   Skipping: $TEST_FILE"
    continue
  fi

  echo "[$COUNT/$TOTAL] Testing: $TEST_FILE"

  case "$RUNNER" in
    rust)
      # Each tests/<stem>.rs compiles to its own integration-test binary.
      # --test-threads=1 keeps side effects deterministic during bisection.
      STEM="$(basename "$TEST_FILE" .rs)"
      cargo test --test "$STEM" -- --test-threads=1 > /dev/null 2>&1 || true
      ;;
    vitest)
      $VITEST_CMD "$TEST_FILE" > /dev/null 2>&1 || true
      ;;
    bun)
      bun test "$TEST_FILE" > /dev/null 2>&1 || true
      ;;
    node)
      npm test "$TEST_FILE" > /dev/null 2>&1 || true
      ;;
  esac

  if [ -e "$POLLUTION_CHECK" ]; then
    echo ""
    echo "🎯 FOUND POLLUTER!"
    echo "   Test: $TEST_FILE"
    echo "   Created: $POLLUTION_CHECK"
    echo ""
    echo "Pollution details:"
    ls -la "$POLLUTION_CHECK"
    echo ""
    echo "To investigate:"
    case "$RUNNER" in
      rust)
        STEM="$(basename "$TEST_FILE" .rs)"
        echo "  cargo test --test $STEM -- --test-threads=1   # Run just this binary"
        echo "  cat $TEST_FILE                                  # Review test code"
        ;;
      vitest)
        echo "  $VITEST_CMD $TEST_FILE   # Run just this test"
        echo "  cat $TEST_FILE                          # Review test code"
        ;;
      bun)
        echo "  bun test $TEST_FILE    # Run just this test"
        echo "  cat $TEST_FILE         # Review test code"
        ;;
      node)
        echo "  npm test $TEST_FILE    # Run just this test"
        echo "  cat $TEST_FILE         # Review test code"
        ;;
    esac
    exit 1
  fi
done

echo ""
echo "✅ No polluter found - all tests clean!"
exit 0
