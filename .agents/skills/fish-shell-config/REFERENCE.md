# Fish Shell Reference

Detailed reference for advanced Fish shell usage patterns.

## Complete Variable Scope Reference

### Scope Combinations

```fish
# Local, unexported (function-only)
set -l VAR value

# Local, exported (function-only, visible to subprocesses)
set -lx VAR value

# Global, unexported (session-wide)
set -g VAR value

# Global, exported (session-wide environment variable)
set -gx VAR value

# Universal, unexported (persistent across sessions)
set -U VAR value

# Universal, exported (persistent + environment)
set -Ux VAR value
```

### Variable Queries

```fish
# Check if variable exists
set -q VARNAME; and echo "exists"

# Show variable value
echo $VARNAME

# Show variable with scope
set --show VARNAME

# List all variables
set

# List only exported variables
set -x

# List only universal variables
set -U
```

### Variable Manipulation

```fish
# Erase variable
set -e VARNAME

# Append to list
set -a VARNAME new_value

# Prepend to list
set -p VARNAME new_value

# Query length
count $VARNAME

# Erase specific index
set -e VARNAME[2]
```

## Advanced Function Patterns

### Named Arguments

```fish
function greet --argument-names name greeting
    echo "$greeting, $name!"
end

greet John Hello  # "Hello, John!"
```

### Default Arguments

```fish
function greet --argument-names name
    set -q name[1]; or set name "World"
    echo "Hello, $name!"
end

greet        # "Hello, World!"
greet Alice  # "Hello, Alice!"
```

### Optional Flags

```fish
function mycommand
    argparse 'h/help' 'v/verbose' 'o/output=' -- $argv
    or return

    if set -q _flag_help
        echo "Usage: mycommand [-v] [-o file] args..."
        return 0
    end

    if set -q _flag_verbose
        echo "Verbose mode enabled"
    end

    if set -q _flag_output
        echo "Output file: $_flag_output"
    end

    echo "Args: $argv"
end
```

### Wrapper Functions

```fish
function docker-run --wraps='docker run'
    docker run --rm -it $argv
end

function gst --wraps='git status'
    git status -sb $argv
end
```

## String Builtin Complete Reference

### Escape/Unescape

```fish
string escape 'foo bar'      # foo\ bar
string unescape 'foo\ bar'   # foo bar
```

### Join/Split

```fish
string join ':' a b c              # a:b:c
string split ':' 'a:b:c'           # a\nb\nc
string split --max 2 ':' 'a:b:c'   # a\nb:c
string split0 < file.txt           # split on null bytes
```

### Length

```fish
string length "hello"         # 5
string length "hello" "world" # 5\n5
```

### Match/Glob

```fish
string match 'a*' apple banana          # apple
string match -i 'A*' apple              # apple (case-insensitive)
string match -r '\d+' 'abc 123 def'     # 123 (regex)
string match -rg '(\w+)' 'hello world'  # hello\nworld (all groups)
```

### Replace

```fish
string replace 'old' 'new' 'old string'        # new string
string replace -a 'a' 'A' 'banana'             # bAnAnA (all)
string replace -r '\s+' '_' 'hello  world'     # hello_world (regex)
```

### Substring

```fish
string sub -s 2 -l 3 'hello'     # ell (start at 2, length 3)
string sub -s -3 'hello'         # llo (last 3 chars)
```

### Trim

```fish
string trim '  hello  '              # 'hello'
string trim -l '  hello  '           # 'hello  '
string trim -r '  hello  '           # '  hello'
string trim -c '/' '/path/to/file/'  # 'path/to/file'
```

### Transform

```fish
string upper 'hello'     # HELLO
string lower 'HELLO'     # hello
```

## Test Command Reference

### File Tests

```fish
test -e /path     # exists
test -f /path     # regular file
test -d /path     # directory
test -L /path     # symbolic link
test -r /path     # readable
test -w /path     # writable
test -x /path     # executable
test -s /path     # non-zero size

# Combine
test -f file.txt -a -r file.txt  # file AND readable
test -d dir1 -o -d dir2          # dir1 OR dir2 exists
```

### String Tests

```fish
test -z "$var"       # zero length
test -n "$var"       # non-zero length
test "$a" = "$b"     # equal
test "$a" != "$b"    # not equal
```

### Numeric Tests

```fish
test $a -eq $b       # equal
test $a -ne $b       # not equal
test $a -lt $b       # less than
test $a -le $b       # less than or equal
test $a -gt $b       # greater than
test $a -ge $b       # greater than or equal
```

## Math Builtin

```fish
math 1 + 2                    # 3
math '1 + 2'                  # 3
math "scale=2; 10 / 3"        # 3.33
math "sqrt(16)"               # 4
math "sin(3.14159/2)"         # 1

set -l count 5
math $count + 1               # 6
set count (math $count + 1)   # increment
```

## Advanced Loops

### Loop Control

```fish
for i in (seq 1 10)
    if test $i -eq 5
        continue  # skip to next iteration
    end
    if test $i -eq 8
        break     # exit loop
    end
    echo $i
end
```

### Parallel Processing Pattern

```fish
# Process files in background
for file in *.txt
    process_file $file &
end
wait  # Wait for all background jobs
```

## Globbing Patterns

```fish
# Single directory
ls *.fish

# Recursive
ls **.fish

# Character class
ls [abc]*.txt

# Negation
ls [^a]*.txt

# Multiple patterns
ls *.{fish,sh,bash}

# Hidden files (opt-in)
ls .*
```

## Command Substitution Edge Cases

```fish
# Splits on newlines only
set lines (cat file.txt)          # each line = element

# To split on other delimiters
set words (cat file | string split ' ')

# Preserve exact whitespace in single string
set content (cat file | string collect)

# Exit status available after substitution
set output (command)
echo $status  # exit code of 'command'
```

## Completion System

### Basic Completion Definition

```fish
# ~/.config/fish/completions/mytool.fish
complete -c mytool -s h -l help -d "Show help"
complete -c mytool -s v -l verbose -d "Verbose output"
complete -c mytool -a "start stop restart" -d "Action"
```

### Dynamic Completions

```fish
complete -c git -n '__fish_seen_subcommand_from checkout' \
         -a '(__fish_git_branches)' -d "Branch"

function __fish_git_branches
    git branch --format='%(refname:short)' 2>/dev/null
end
```

## Event System

### Available Events

```fish
# Fish startup
function on_startup --on-event fish_startup
    echo "Shell started"
end

# User login
function on_login --on-event fish_user_login
    echo "User logged in"
end

# Prompt displayed
function on_prompt --on-event fish_prompt
    # Runs before each prompt
end

# Exit
function on_exit --on-event fish_exit
    echo "Goodbye"
end

# Job exit
function on_job_exit --on-event fish_job_exit
    echo "Background job finished"
end
```

### Variable Change Events

```fish
function on_pwd_change --on-variable PWD
    echo "Changed to $PWD"
end

function on_path_change --on-variable PATH
    echo "PATH updated"
end
```

## Process Management

```fish
# Background job
long_command &

# List jobs
jobs

# Bring job to foreground
fg %1

# Send job to background
bg %1

# Disown job (keeps running after shell exit)
disown %1

# Wait for background jobs
wait

# Process ID of last background job
echo $last_pid
```

## Error Handling Patterns

### Try-Catch Pattern

```fish
function try_command
    if command_that_might_fail
        echo "Success"
    else
        echo "Failed with status $status"
        return 1
    end
end
```

### Early Return Pattern

```fish
function validate_and_process
    if not test -f $argv[1]
        echo "File not found: $argv[1]"
        return 1
    end

    if not test -r $argv[1]
        echo "File not readable: $argv[1]"
        return 2
    end

    # Process file
    process_file $argv[1]
end
```

### Error Propagation

```fish
function outer
    inner; or return $status
    echo "inner succeeded"
end

function inner
    failing_command; or return $status
    echo "command succeeded"
end
```

## Performance Tips

### Avoid Subshells When Possible

```fish
# Slower
if test (count $list) -gt 0
    # ...
end

# Faster
if test -n "$list"
    # ...
end
```

### Use Builtins Over External Commands

```fish
# Slower
set length (echo $str | wc -c)

# Faster
set length (string length "$str")
```

### Cache Expensive Operations

```fish
function __cache_nix_packages --on-event fish_startup
    set -g __nix_packages (nix search --json | jq -r 'keys[]')
end

function nix-search-complete
    printf '%s\n' $__nix_packages
end
```

## Universal Variable Storage

Universal variables persist in `~/.config/fish/fish_variables`:

```fish
# View all universal variables
set -U

# Set universal variable
set -U MY_VAR value

# Erase universal variable
set -Ue MY_VAR

# Universal variables sync across all running Fish instances
```

**Note**: Universal variables are shared across all Fish shells, so changes in one terminal affect all others immediately.

## Debugging Techniques

### Trace Execution

```fish
fish -d 3 -c 'your command'  # Debug level 3
fish -d 4 -c 'your command'  # Debug level 4 (very verbose)
```

### Function Tracing

```fish
function debug_trace
    echo "Entering: "(status current-function)
    echo "Arguments: $argv"
    echo "PWD: $PWD"
end
```

### Status Stack

```fish
# Get current function name
status current-command
status current-function

# Check if interactive
status is-interactive; and echo "Interactive shell"

# Check if login shell
status is-login; and echo "Login shell"
```

## Advanced Prompt Techniques

### Multi-line Prompt

```fish
function fish_prompt
    echo
    set_color blue
    echo -n "┌─ "
    set_color cyan
    echo -n (prompt_pwd)
    echo
    set_color blue
    echo -n "└─▶ "
    set_color normal
end
```

### Right Prompt

```fish
function fish_right_prompt
    set -l last_status $status
    if test $last_status -ne 0
        set_color red
        echo "[$last_status]"
    end
    set_color normal
end
```

### Title (Terminal Window Title)

```fish
function fish_title
    echo (status current-command) (prompt_pwd)
end
```

## Keybindings

### View Current Bindings

```fish
bind  # List all bindings
bind -k  # List key names
```

### Custom Bindings

```fish
# Bind Ctrl+F to accept suggestion
bind \cf forward-char

# Bind Alt+E to edit command in $EDITOR
bind \ee edit_command_buffer

# Bind custom function
function my_custom_action
    commandline -i "text to insert"
end
bind \cx my_custom_action
```

## Integration with External Tools

### fzf Integration

```fish
function fzf-history
    history | fzf | read -l result
    commandline -r $result
end
bind \cr fzf-history
```

### direnv with Nix

```fish
# ~/.config/fish/conf.d/20-direnv.fish
if type -q direnv
    direnv hook fish | source
    set -gx DIRENV_LOG_FORMAT ""  # Silence direnv output
end
```

### asdf Version Manager

```fish
# ~/.config/fish/conf.d/asdf.fish
if test -f ~/.asdf/asdf.fish
    source ~/.asdf/asdf.fish
end
```
