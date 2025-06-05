# Create a string of random base64 characters (default length 64)
rng() {
  local length="${1:-64}"
  head -c "$length" /dev/urandom | base64
}

# Create a new directory and enter it
function mkd() {
	mkdir -p "$@" && cd "$_";
}

# Determine size of a file or total size of a directory
function fs() {
	if du -b /dev/null > /dev/null 2>&1; then
		local arg=-sbh;
	else
		local arg=-sh;
	fi
	if [[ -n "$@" ]]; then
		du $arg -- "$@";
	else
		du $arg .[^.]* ./*;
	fi;
}

# Use Git's colored diff when available
hash git &>/dev/null;
if [ $? -eq 0 ]; then
	function diff() {
		git diff --no-index --color-words "$@";
	}
fi;

# Run `dig` and display the most useful info
function digga() {
	dig +nocmd "$1" any +multiline +noall +answer;
}

# Show all the names (CNs and SANs) listed in the SSL certificate
# for a given domain
function getcertnames() {
	if [ -z "${1}" ]; then
		echo "ERROR: No domain specified.";
		return 1;
	fi;

	local domain="${1}";
	echo "Testing ${domain}…";
	echo ""; # newline

	local tmp=$(echo -e "GET / HTTP/1.0\nEOT" \
		| openssl s_client -connect "${domain}:443" -servername "${domain}" 2>&1);

	if [[ "${tmp}" = *"-----BEGIN CERTIFICATE-----"* ]]; then
		local certText=$(echo "${tmp}" \
			| openssl x509 -text -certopt "no_aux, no_header, no_issuer, no_pubkey, \
			no_serial, no_sigdump, no_signame, no_validity, no_version");
		echo "Common Name:";
		echo ""; # newline
		echo "${certText}" | grep "Subject:" | sed -e "s/^.*CN=//" | sed -e "s/\/emailAddress=.*//";
		echo ""; # newline
		echo "Subject Alternative Name(s):";
		echo ""; # newline
		echo "${certText}" | grep -A 1 "Subject Alternative Name:" \
			| sed -e "2s/DNS://g" -e "s/ //g" | tr "," "\n" | tail -n +2;
		return 0;
	else
		echo "ERROR: Certificate not found.";
		return 1;
	fi;
}

# `o` with no arguments opens the current directory, otherwise opens the given
# location
function o() {
	if [ $# -eq 0 ]; then
		open .;
	else
		open "$@";
	fi;
}

# `tre` is a shorthand for `tree` with hidden files and color enabled, ignoring
# the `.git` directory, listing directories first. The output gets piped into
# `less` with options to preserve color and line numbers, unless the output is
# small enough for one screen.
function tre() {
	tree -aC -I '.git|node_modules|bower_components' --dirsfirst "$@" | less -FRNX;
}

# exec into a pod
kx() {
  kubectl exec -it $1 -- /bin/sh
}

# yolo commit and push
send-it() {
  git add . && git commit -m "x" && git push
}

# Go to main branch and get latest code
mm() {
    local main_branch=$(git rev-parse --abbrev-ref HEAD)
    if [[ "$main_branch" != "main" && "$main_branch" != "master" ]]; then
        main_branch=$(git remote show origin | sed -n '/HEAD branch/s/.*: //p')
    fi
    git stash && git checkout $main_branch && git pull --rebase origin $main_branch
}

# Open the listed files or directories in Visual Studio Code
open_in_vscode() {
    if [ $# -eq 0 ]; then
        echo "Usage: open_in_vscode <directory_or_file> [<directory_or_file> ...]"
        return 1
    fi

    for item in "$@"; do
        if [ -e "$item" ]; then
            code "$item"
        else
            echo "Warning: '$item' does not exist. Skipping."
        fi
    done
}

# Copy the contents of every file in a directory to the clipboard, filtering by file type
copydirf() {
    local filetype="$1"
    local rg_args=()

    if [[ -n "$filetype" ]]; then
        if [[ "$filetype" == *.* ]]; then
            # Regular file extension
            rg_args+=(-g "*$filetype")
        else
            # File without extension (e.g., Dockerfile)
            rg_args+=(--type-add "$filetype:$filetype*" --type "$filetype")
        fi
    fi

    rg "${rg_args[@]}" --no-ignore --no-heading --with-filename --line-number --text --max-columns 500 --binary "" | nl -ba | tee >(pbcopy) | cat
}

# Docker compose rebuild and restart specific service
dcr() {
  docker-compose down && docker-compose build $1 && docker-compose up -d
}

# Docker compose swap service (stop, remove, rebuild, start)
dswap() {
  docker-compose stop $1 && docker-compose rm -f $1 && docker-compose build $1 && docker-compose up -d $1
}

# Initialize a Go module with github.com/wcygan prefix
gom() {
  go mod init github.com/wcygan/$1
}

# Initialize a protobuf project structure
proto() {
  local structure_exists=false

  # Check and create directories
  if [ ! -d "proto/hello/v1" ]; then
    mkdir -p proto/hello/v1
    echo "Created directory: proto/hello/v1"
  else
    echo "Directory already exists: proto/hello/v1"
    structure_exists=true
  fi

  # Check and create proto/buf.yaml
  if [ ! -f "proto/buf.yaml" ]; then
    cat << EOF > proto/buf.yaml
version: v2
modules:
  - path: .
    name: buf.build/wcygan/hello
EOF
    echo "Created file: proto/buf.yaml"
  else
    echo "File already exists: proto/buf.yaml"
    structure_exists=true
  fi

  # Check and create buf.gen.yaml
  if [ ! -f "buf.gen.yaml" ]; then
    cat << EOF > buf.gen.yaml
version: v2
managed:
  enabled: true
inputs:
  - directory: proto
EOF
    echo "Created file: buf.gen.yaml"
  else
    echo "File already exists: buf.gen.yaml"
    structure_exists=true
  fi

  # Check and create proto/hello/v1/hello.proto
  if [ ! -f "proto/hello/v1/hello.proto" ]; then
    cat << EOF > proto/hello/v1/hello.proto
syntax = "proto3";

package hello.v1;

service GreeterService {
  rpc SayHello (SayHelloRequest) returns (SayHelloResponse) {}
}

message SayHelloRequest {
  string name = 1;
}

message SayHelloResponse {
  string message = 1;
}
EOF
    echo "Created file: proto/hello/v1/hello.proto"
  else
    echo "File already exists: proto/hello/v1/hello.proto"
    structure_exists=true
  fi

  if [ "$structure_exists" = true ]; then
    echo "Buf structure already exists or partially exists. No changes made where files/directories were present."
  else
    echo "Buf structure created successfully."
  fi

  # Hint for the next step
  echo "Run 'buf push proto' to push your schemas."
}

# Shell-specific enhancements
if [ -n "$BASH_VERSION" ]; then
    # Bash-specific functions for better development experience
    
    # Enhanced bash completion for common commands
    _dev_complete() {
        local cur=${COMP_WORDS[COMP_CWORD]}
        local commands="build test lint format check deploy status log"
        COMPREPLY=($(compgen -W "$commands" -- "$cur"))
    }
    complete -F _dev_complete dev
    
    # Quick git branch completion for common commands
    _git_branch_complete() {
        local cur=${COMP_WORDS[COMP_CWORD]}
        local branches=$(git branch 2>/dev/null | sed 's/^[* ] //' | tr '\n' ' ')
        COMPREPLY=($(compgen -W "$branches" -- "$cur"))
    }
    complete -F _git_branch_complete gco gcb
    
    # Enhanced history search for bash
    hg() {
        if [ $# -eq 0 ]; then
            history | tail -20
        else
            history | grep -i "$1"
        fi
    }
    
    # Bash-specific prompt enhancements
    update_bash_prompt() {
        local git_branch=$(parse_git_branch)
        local python_venv=""
        if [ -n "$VIRTUAL_ENV" ]; then
            python_venv=" ($(basename $VIRTUAL_ENV))"
        fi
        
        if [ -t 1 ]; then
            PS1="\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[33m\]${git_branch}\[\033[35m\]${python_venv}\[\033[00m\]\$ "
        else
            PS1="\u@\h:\w${git_branch}${python_venv}\$ "
        fi
    }
    
    # Auto-update prompt with git and virtual env info
    PROMPT_COMMAND="update_bash_prompt"
fi

if [ -n "$ZSH_VERSION" ]; then
    # ZSH-specific enhancements can go here if needed
    :
fi

# Universal shell detection function
current_shell() {
    if [ -n "$ZSH_VERSION" ]; then
        echo "zsh"
    elif [ -n "$BASH_VERSION" ]; then
        echo "bash"
    else
        echo "unknown"
    fi
}

# Shell feature detection
has_feature() {
    local feature="$1"
    case "$feature" in
        "arrays")
            [ -n "$BASH_VERSION" ] || [ -n "$ZSH_VERSION" ] && return 0
            ;;
        "completion")
            [ -n "$BASH_VERSION" ] && command -v complete >/dev/null && return 0
            [ -n "$ZSH_VERSION" ] && return 0
            ;;
        "globstar")
            [ -n "$BASH_VERSION" ] && shopt -q globstar 2>/dev/null && return 0
            [ -n "$ZSH_VERSION" ] && return 0
            ;;
    esac
    return 1
}
