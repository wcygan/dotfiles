# config/fish/conf.d/40-aliases.fish
#
# Session-safe aliases and interactive abbreviations.
# Keep wrappers tiny; prefer functions for nontrivial logic.

# ——— Aliases -> define callable functions ———
function __maybe_alias --argument-names name target
    if type -q $target
        alias $name="$target"
    end
end

# Core CLI shorthands (only if binary exists)
__maybe_alias g git
__maybe_alias k kubectl
__maybe_alias d docker
__maybe_alias dc docker-compose
__maybe_alias ll eza
__maybe_alias j just
__maybe_alias o opencode

# Modern replacements for traditional tools
__maybe_alias cat bat       # cat -> bat (syntax highlighting)
__maybe_alias ls eza        # ls -> eza (better listing)
__maybe_alias find fd       # find -> fd (faster, friendlier)
__maybe_alias grep rg       # grep -> ripgrep (faster)
__maybe_alias sed sd        # sed -> sd (simpler syntax)
__maybe_alias du dust       # du -> dust (better disk usage)
__maybe_alias ps procs      # ps -> procs (if available)
__maybe_alias top btop      # top -> btop (better monitoring)
__maybe_alias htop btop     # htop -> btop (even better)
__maybe_alias dig dog       # dig -> dog (DNS lookup)

# Decorated examples using functions (more robust than raw alias)
if type -q eza
    functions -q la; or function la --wraps='eza -la' --description 'list all'
        eza -la $argv
    end
end

# ——— Interactive abbreviations ———
# Use for long flaggy commands; expands on SPACE/TAB in interactive shells.
abbr -a kctx 'kubectl config use-context'
abbr -a kp 'kubectl get pods'
abbr -a kn 'kubectl get nodes'
abbr -a gco 'git checkout'
abbr -a gs 'git status -sb'
abbr -a gl 'git log --oneline --graph --decorate --all'
abbr -a gb 'git branch'
abbr -a gd 'git diff'
abbr -a gp 'git push'
abbr -a dc 'docker compose'
abbr -a l 'eza -la'
abbr -a gcl 'git clone'
abbr -a gc 'git commit'
abbr -a d 'deno'
abbr -a h 'hermes'
abbr -a dt 'deno task'
abbr -a br 'broot'

# Cargo (Rust package manager)
if type -q cargo
    abbr -a cgc 'cargo check'
    abbr -a cgr 'cargo run'
    abbr -a cgb 'cargo build'
    abbr -a cgbr 'cargo build --release'
    abbr -a cgt 'cargo test'
    abbr -a cgd 'cargo doc'
    abbr -a cgdo 'cargo doc --open'
    abbr -a cgcl 'cargo clean'
    abbr -a cgf 'cargo fmt'
    abbr -a cgcli 'cargo clippy'
    abbr -a cga 'cargo add'
    abbr -a cgu 'cargo update'
    abbr -a cgw 'cargo watch'
end

# JJ (Jujutsu VCS)
if type -q jj
    # Core daily commands (aliases)
    alias js 'jj st'
    alias jd 'jj diff'
    alias jl 'jj log'
    alias jn 'jj new'
    alias ju 'jj undo'
    alias jsh 'jj show'                 # show current change details
    alias jres 'jj resolve'             # resolve conflicts in @
    alias jnx 'jj next --edit'          # walk forward in the stack
    alias jpv 'jj prev --edit'          # walk back in the stack

    # Abbreviations for commands with args
    abbr -a jde 'jj describe -m'
    abbr -a jc 'jj commit -m'           # describe @ + start a fresh change
    abbr -a jnm 'jj new -m'             # new change with a message
    abbr -a jed 'jj edit'
    abbr -a jsq 'jj squash'
    abbr -a jsqi 'jj squash --into'     # squash @ into an arbitrary ancestor
    abbr -a jsp 'jj split'              # split a change (interactive)
    abbr -a jrb 'jj rebase -d'
    abbr -a jrs 'jj restore'
    abbr -a jab 'jj abandon'

    # Operation log (jj's real undo history)
    alias jop 'jj op log'
    abbr -a jor 'jj op restore'

    # Git interop
    abbr -a jgf 'jj git fetch'
    abbr -a jgp 'jj git push'
    abbr -a jgc 'jj git clone'
    abbr -a jgpn 'jj git push -c @-'    # push new auto-named bookmark from committed change
    abbr -a jgpd 'jj git push --deleted' # sync bookmark deletions to remote

    # Put a named bookmark at @- (create if new, move if it exists) and push.
    # Compatible with jj versions that don't have `bookmark set --allow-new`.
    function __jgp_set_bookmark_at_prev --argument-names bookmark
        jj bookmark create $bookmark -r @- 2>/dev/null
        or jj bookmark move $bookmark --to @-
    end

    # Closest equivalent of `git push -u origin <branch>`:
    # - with arg:    put a named bookmark at @- and push it (new or existing)
    # - without arg: push whatever tracked bookmarks already moved (like plain `jgp`).
    #   If that does nothing, you probably need `jgpu <name>` or `jgpn`.
    function jgpu --description 'jj: set/create bookmark at @- and push (git push -u equivalent)' --argument-names bookmark
        if test -n "$bookmark"
            __jgp_set_bookmark_at_prev $bookmark
            or return 1
            jj git push
            return
        end

        jj git push
        set -l rc $status
        if test $rc -ne 0
            return $rc
        end
        # Helpful nudge if nothing actually moved.
        if test -z (jj log --no-graph -r @- -T 'local_bookmarks' 2>/dev/null)
            echo "" >&2
            echo "hint: no bookmark at @-. Use 'jgpu <name>' to name one, or 'jgpn' for an auto-generated name." >&2
        end
    end

    # Commit + set bookmark to new commit + push, in one call.
    # Usage: jgpb <bookmark> "commit message"
    # Works whether <bookmark> is new or already exists.
    function jgpb --description 'jj: commit, set bookmark to new commit, push' --argument-names bookmark message
        if test -z "$bookmark"; or test -z "$message"
            echo "Usage: jgpb <bookmark> \"commit message\"" >&2
            return 1
        end
        jj commit -m "$message"
        or return 1
        __jgp_set_bookmark_at_prev $bookmark
        or return 1
        jj git push
    end

    # Bookmark management (formerly `jj branch`)
    abbr -a jbc 'jj bookmark create'
    abbr -a jbs 'jj bookmark set'
    abbr -a jbl 'jj bookmark list'
    abbr -a jbm 'jj bookmark move'

    # Useful log views
    alias jll 'jj log -r ::@'                   # ancestors of @
    alias jla 'jj log -r "all()"'               # everything
    alias jlt 'jj log -r "trunk()..@"'          # my stack vs main
    alias jds 'jj diff --stat'                  # diff with stats (like gds)
end

# Guard example: only add k* abbr if kubectl is present
if not type -q kubectl
    abbr -e kctx 2>/dev/null
end

# Global editor default if unset (harmless if already set elsewhere)
set -q EDITOR; or set -gx EDITOR nvim

# Initialize zoxide if available and replace cd
if type -q zoxide
    zoxide init fish | source
    # Replace cd with zoxide's z function
    alias cd="z"
end

# User-specific aliases
alias c clear
alias dev 'cd ~/Development/'
alias lg lazygit
alias lj lazyjj
alias ldc lazydocker
alias py python3
alias lfgc 'codex --dangerously-bypass-approvals-and-sandbox'
alias lfg 'claude --dangerously-skip-permissions'
alias lfgt 'claude --dangerously-skip-permissions --tmux --worktree'
alias reload 'exec fish -l'

if type -q lsof
    functions -q murder; or function murder --description 'Kill all processes bound to a TCP port'
        if test (count $argv) -eq 0
            echo "Usage: murder <port>" >&2
            return 1
        end

        set -l port $argv[1]
        set -l pids (lsof -ti "tcp:$port" 2>/dev/null)
        if test -z "$pids"
            echo "No process found on TCP port $port" >&2
            return 0
        end

        command kill -9 $pids
    end
end

# Computers
alias t 'ssh wcygan@betty -t "zellij attach main || zellij -s main"'
alias m1 'ssh wcygan@betty'
alias zt 'ssh wcygan@betty -t "zellij attach main || zellij -s main"'
alias zd 'ssh wcygan@betty -t "zellij attach dev || zellij -s dev --layout dev"'
alias ts 'tailscale status'
alias td 'talosctl dashboard'

# Git stuff
alias gaa 'git add .'
alias gbddd 'git branch | grep -v "main" | xargs git branch -d'
alias gsw 'git switch -c'
alias gpu 'eval git push -u origin $(git rev-parse --abbrev-ref HEAD)'
alias gds 'gd --stat'
alias gca 'git commit --amend --no-edit'
alias grco 'git rebase --continue'
alias gpr 'git pull --rebase'

# General
alias nv 'nvim'
alias vim 'nvim'
alias vi 'nvim'

# Zellij (when using locally)
if type -q zellij
    alias zj 'zellij'
    alias zja 'zellij attach'
    alias zjl 'zellij list-sessions'
    alias zjk 'zellij kill-session'
    alias zjka 'zellij kill-all-sessions'
    abbr -a zjs 'zellij -s'
    abbr -a zjd 'zellij delete-session'
end

# Intuitive map function
# For example, to list all directories that contain a certain file:
# find . -name .gitattributes | map dirname
alias map "xargs -n1"

# Projects
alias dotfiles 'zed /Users/wcygan/Development/dotfiles'
alias n 'zed /Users/wcygan/Development/notes'
