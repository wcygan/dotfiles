#!/usr/bin/env fish
# Test Fish shell configuration
# Usage: fish scripts/test-fish-config.fish

set -l errors 0

function test_pass
    set_color green
    echo "✓ $argv"
    set_color normal
end

function test_fail
    set_color red
    echo "✗ $argv"
    set_color normal
    set errors (math $errors + 1)
end

function section
    echo
    set_color blue --bold
    echo "=== $argv ==="
    set_color normal
end

# Test basic Fish functionality
section "Basic Fish Functionality"

# Test variable setting
set test_var "hello"
if test "$test_var" = "hello"
    test_pass "Variable assignment works"
else
    test_fail "Variable assignment failed"
end

# Test list operations
set test_list one two three
if test (count $test_list) -eq 3
    test_pass "List operations work"
else
    test_fail "List operations failed"
end

# Test command substitution
set date_output (date +%Y)
if test -n "$date_output"
    test_pass "Command substitution works"
else
    test_fail "Command substitution failed"
end

# Test string builtin
set upper (string upper "hello")
if test "$upper" = "HELLO"
    test_pass "String builtin works"
else
    test_fail "String builtin failed"
end

# Test config file structure
section "Config File Structure"

set config_home ~/.config/fish

if test -d $config_home
    test_pass "Fish config directory exists: $config_home"
else
    test_fail "Fish config directory missing: $config_home"
end

if test -f $config_home/config.fish
    test_pass "config.fish exists"
else
    echo "ℹ️  config.fish not found (optional)"
end

if test -d $config_home/conf.d
    test_pass "conf.d directory exists"
else
    echo "ℹ️  conf.d directory not found (optional)"
end

if test -d $config_home/functions
    test_pass "functions directory exists"
else
    echo "ℹ️  functions directory not found (optional)"
end

# Test PATH
section "Environment"

if test -n "$PATH"
    test_pass "PATH is set"
else
    test_fail "PATH is not set"
end

if test -n "$HOME"
    test_pass "HOME is set"
else
    test_fail "HOME is not set"
end

# Test functions
section "Functions"

if functions -q fish_prompt
    test_pass "fish_prompt function exists"
else
    test_fail "fish_prompt function missing"
end

# Test builtins
section "Builtins"

set builtins_to_check set test string math count

for builtin_name in $builtins_to_check
    if builtin -n | grep -q "^$builtin_name\$"
        test_pass "Builtin '$builtin_name' available"
    else
        test_fail "Builtin '$builtin_name' missing"
    end
end

# Summary
section "Summary"

if test $errors -eq 0
    set_color green --bold
    echo "All tests passed!"
    set_color normal
    exit 0
else
    set_color red --bold
    echo "$errors test(s) failed"
    set_color normal
    exit 1
end
