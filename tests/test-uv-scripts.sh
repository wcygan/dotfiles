#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
SKILL_DIR="$ROOT/config/codex/skills/uv-scripts"
SCRIPTS_DIR="$SKILL_DIR/scripts"
TEST_DIR="$(mktemp -d /tmp/uv-scripts-test.XXXXXX)"

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

add_linux_runtime_library_paths() {
    [[ "$(uname -s)" == "Linux" ]] || return 0

    local dir
    local lib_dirs=()

    if [[ -n "${NIX_PROFILE:-}" ]]; then
        lib_dirs+=("$NIX_PROFILE/lib")
    fi

    lib_dirs+=(
        "$HOME/.nix-profile/lib"
        /nix/var/nix/profiles/default/lib
    )

    for dir in "${lib_dirs[@]}"; do
        [[ -e "$dir/libstdc++.so.6" ]] || continue
        case ":${LD_LIBRARY_PATH:-}:" in
            *":$dir:"*) ;;
            *) export LD_LIBRARY_PATH="$dir${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ;;
        esac
    done
}

add_linux_runtime_library_paths

pass() {
    echo "✓ $1"
}

fail() {
    echo "✗ $1" >&2
    exit 1
}

run_step() {
    local name="$1"
    shift

    local log="$TEST_DIR/${name//[^a-zA-Z0-9_.-]/_}.log"
    echo "→ $name"
    if (cd "$TEST_DIR" && "$@") >"$log" 2>&1; then
        pass "$name"
    else
        cat "$log" >&2
        fail "$name"
    fi
}

echo "uv-scripts exemplar test"
echo "========================"
echo ""

command -v uv >/dev/null 2>&1 || fail "uv is not available"

expected_scripts=(
    analyze_duckdb.py
    cli_click_rich.py
    config_and_secrets.py
    document_assets.py
    fetch_http.py
    inspect_files.py
    orchestrate_dev.py
    render_template.py
    script_quality_gate.py
    watch_and_run.py
)

for script in "${expected_scripts[@]}"; do
    path="$SCRIPTS_DIR/$script"
    [[ -f "$path" ]] || fail "$script is missing"
    [[ -x "$path" ]] || fail "$script is not executable"
done
pass "all expected scripts exist and are executable"

run_step "quality gate help checks" \
    uv run --script "$SCRIPTS_DIR/script_quality_gate.py" "$SCRIPTS_DIR" --run-help

run_step "quality gate ruff checks" \
    uv run --script "$SCRIPTS_DIR/script_quality_gate.py" "$SCRIPTS_DIR" --ruff

run_step "click rich demo" \
    uv run --script "$SCRIPTS_DIR/cli_click_rich.py" demo

run_step "http fetch demo" \
    uv run --script "$SCRIPTS_DIR/fetch_http.py" --demo \
        --cache-dir "$TEST_DIR/cache/fetch-http" \
        --output "$TEST_DIR/fetch.json"
[[ -s "$TEST_DIR/fetch.json" ]] || fail "fetch demo did not write output"
pass "fetch demo wrote output"

run_step "duckdb analysis demo" \
    uv run --script "$SCRIPTS_DIR/analyze_duckdb.py" --demo

run_step "file inspection demo" \
    uv run --script "$SCRIPTS_DIR/inspect_files.py" --demo

run_step "template render demo" \
    uv run --script "$SCRIPTS_DIR/render_template.py" --demo --output "$TEST_DIR/report.md"
grep -Fq "Demo Report" "$TEST_DIR/report.md" || fail "render demo output missing expected title"
pass "template render demo wrote expected output"

run_step "config paths demo" \
    uv run --script "$SCRIPTS_DIR/config_and_secrets.py" --demo paths

run_step "config token demo" \
    uv run --script "$SCRIPTS_DIR/config_and_secrets.py" --demo get-token

run_step "dev orchestration demo" \
    uv run --script "$SCRIPTS_DIR/orchestrate_dev.py" --demo \
        --duration 3 \
        --plain \
        --log-dir "$TEST_DIR/logs/orchestrator"

run_step "watch command demo" \
    uv run --script "$SCRIPTS_DIR/watch_and_run.py" --demo

run_step "document asset demo" \
    uv run --script "$SCRIPTS_DIR/document_assets.py" --demo

echo ""
echo "All uv-scripts exemplar checks passed."
