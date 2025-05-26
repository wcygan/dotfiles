#!/bin/bash

# Enhanced .bashrc with status reporting and modern bash features
# Load dotfiles with status reporting similar to .zshrc
loaded_files=()
failed_files=()

for file in ~/.{path,exports,aliases,functions,extra,platform}; do
	if [ -r "$file" ] && [ -f "$file" ]; then
		if source "$file" 2>/dev/null; then
			loaded_files+=("$(basename "$file")")
		else
			failed_files+=("$(basename "$file")")
		fi
	fi
done

# Report results (using bash-compatible syntax)
if [ ${#loaded_files[@]} -gt 0 ]; then
	echo "✓ Loaded dotfiles: ${loaded_files[*]}"
fi

if [ ${#failed_files[@]} -gt 0 ]; then
	echo "✗ Failed to load: ${failed_files[*]}" >&2
else
	echo "🎉 All dotfiles loaded successfully!"
fi

# Modern bash features and settings
# Case-insensitive globbing (used in pathname expansion)
shopt -s nocaseglob

# Append to the bash history file, rather than overwriting it
shopt -s histappend

# Autocorrect typos in path names when using `cd`
shopt -s cdspell

# Enable some Bash 4+ features when possible:
# * `autocd`, e.g. `**/qux` will enter `./foo/bar/baz/qux`
# * Recursive globbing, e.g. `echo **/*.txt`
for option in autocd globstar; do
	shopt -s "$option" 2> /dev/null
done

# Better history control
HISTCONTROL=ignoreboth:erasedups
HISTSIZE=10000
HISTFILESIZE=20000
HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "

# Modern prompt with git support
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

# Enhanced prompt with colors and git branch
if [ -t 1 ]; then
    PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[33m\]$(parse_git_branch)\[\033[00m\]\$ '
else
    PS1='\u@\h:\w$(parse_git_branch)\$ '
fi

# Add tab completion for many bash commands
if command -v brew &> /dev/null && [ -r "$(brew --prefix)/etc/profile.d/bash_completion.sh" ]; then
	# Ensure existing Homebrew v1 completions continue to work
	export BASH_COMPLETION_COMPAT_DIR="$(brew --prefix)/etc/bash_completion.d"
	source "$(brew --prefix)/etc/profile.d/bash_completion.sh"
elif [ -f /etc/bash_completion ]; then
	source /etc/bash_completion
fi

# Add tab completion for SSH hostnames based on ~/.ssh/config, ignoring wildcards
[ -e "$HOME/.ssh/config" ] && complete -o "default" -o "nospace" -W "$(grep "^Host" ~/.ssh/config | grep -v "[?*]" | cut -d " " -f2- | tr ' ' '\n')" scp sftp ssh

# Set vi mode for command line editing (optional - uncomment if desired)
# set -o vi

# Make sure we're using the right shell for non-interactive scripts
[ -n "$PS1" ] && echo "Bash shell ready! 🐚"