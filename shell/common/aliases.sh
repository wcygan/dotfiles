##############################################################################
#   Filename: .aliases.sh                                                    #
# Maintainer: Will Cygan <wcygan.io@gmail.com>                               #
#        URL: http://github.com/wcygan/dotfiles                              #
#                                                                            #
# Sections:                                                                  #
#   01. General ................. General aliases                            #
#   02. Git ..................... Git aliases                                #
#   03. Programming ............. Aliases  for programming                   #
#   04. Networking .............. Networking aliases                         #
#   05. Kubernetes .............. Kubernetes aliases                         #
#   06. Development Tools ....... Modern development tools                   #
#   XX. Misc .................... Miscellaneous aliases                      #
##############################################################################

##############################################################################
# 01. General                                                                #
##############################################################################

alias c='clear'

# Platform-specific open command
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    alias .='open .'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    alias .='xdg-open .'
else
    # Default fallback
    alias .='echo "Open command not configured for this platform"'
fi

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Editor and shell configuration
alias edit='zed'
alias g='gemini'
alias x='claude'
alias xs'claude --model sonnet'
alias xx='cd ~/Development/development-workspace'

# Shell-agnostic aliases - detect current shell and use appropriate config
if [ -n "$ZSH_VERSION" ]; then
    # ZSH-specific aliases
    alias vv='vzsh'
    alias ss='szsh'
    alias vzsh='edit ~/Development/development-workspace/dotfiles'
    alias szsh='source ~/.zshrc'
elif [ -n "$BASH_VERSION" ]; then
    # Bash-specific aliases
    alias vv='vbash'
    alias ss='sbash'
    alias vbash='edit ~/.bashrc'
    alias sbash='source ~/.bashrc'
fi

# Universal shell config aliases (work for both shells)
alias vrc='edit ~/.$(basename $SHELL)rc'
alias src='source ~/.$(basename $SHELL)rc'

# Directory navigation
alias ddd='edit ~/Development/development-workspace'
alias dev='cd ~/Development'
alias will='cd ~'
alias n='edit $HOME/Development/development-workspace/notes'
alias cs='edit $HOME/Development/csgo-config'
alias mn='cd $HOME/Development/manning'
alias oss='cd $HOME/Development/oss'
alias lab='edit $HOME/Development/development-workspace/anton'

# Modern CLI tool replacements
# Use modern tools if available, fallback to traditional ones
if command -v bat > /dev/null; then
    alias cat='bat --paging=never'
fi
if command -v fd > /dev/null; then
    alias find='fd'
fi
if command -v eza > /dev/null; then
    alias ls='eza'
    alias l='eza -l'
else
    alias l='ls -l'
fi

# File operations
alias listdir='find ${1:-.} -type f -not -path "*/.*/*" -print0 | xargs -0 -I {} bash -c '\''echo "$(dirname "{}")/$(basename "{}")"'\'' | sort -t/ -k2 -k3'
# Disk Space Usage
# Platform-specific sort options
if [[ "$OSTYPE" == "darwin"* ]]; then
    alias ds='du -sh * | sort -rh | awk '\''{sum+=$1; print} END {print "Total Size: " sum}'\'
else
    # Linux sort might not have -h flag on older systems
    alias ds='du -sh * | sort -hr 2>/dev/null || du -sh * | sort -nr | awk '\''{sum+=$1; print} END {print "Total Size: " sum}'\'
fi
# Platform-specific clipboard command
if [[ "$OSTYPE" == "darwin"* ]]; then
    alias copydir='rg --no-ignore --no-heading --with-filename --line-number --text --max-columns 500 --binary "" | nl -ba | tee >(pbcopy) | cat'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Use xclip or xsel on Linux
    if command -v xclip > /dev/null; then
        alias copydir='rg --no-ignore --no-heading --with-filename --line-number --text --max-columns 500 --binary "" | nl -ba | tee >(xclip -selection clipboard) | cat'
    elif command -v xsel > /dev/null; then
        alias copydir='rg --no-ignore --no-heading --with-filename --line-number --text --max-columns 500 --binary "" | nl -ba | tee >(xsel --clipboard --input) | cat'
    else
        alias copydir='rg --no-ignore --no-heading --with-filename --line-number --text --max-columns 500 --binary "" | nl -ba | cat'
    fi
fi

# System utilities
alias ff='fastfetch'
# Platform-specific caffeinate command
if [[ "$OSTYPE" == "darwin"* ]]; then
    alias caf='caffeinate'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux alternatives to prevent sleep
    if command -v systemd-inhibit > /dev/null; then
        alias caf='systemd-inhibit --what=idle:sleep:shutdown'
    elif command -v caffeine > /dev/null; then
        alias caf='caffeine'
    else
        alias caf='echo "No sleep prevention tool found. Consider installing caffeine or using systemd-inhibit"'
    fi
fi
alias binary='xxd'
alias py='/usr/bin/python3'

# SSH and remote connections
# Note: Consider adding these hosts to ~/.ssh/config for better portability
alias m0='ssh -i ~/.ssh/trudy_key.pem wcygan@20.51.124.200'
alias trudy='ssh -i ~/.ssh/trudy_key.pem wcygan@20.51.124.200'
alias m1='ssh wcygan@betty'
alias m2='ssh wcygan@barbara'
alias m3='ssh wcygan@shirley'
alias m4='ssh wcygan@raspberrypi'
alias k0='ssh wcygan@k8s-0'
alias k1='ssh wcygan@k8s-1'
alias k2='ssh wcygan@k8s-2'

# Tailscale
alias ts='tailscale status'

##############################################################################
# 02. Git                                                                    #
##############################################################################

# Git defaults
git config --global user.name "Will Cygan"
git config --global user.email "wcygan.io@gmail.com"
git config --global core.editor "vim"

# Dotfile management
alias cfg='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# Git aliases
alias gaa='git add .'
alias gb='git branch'
alias gc='git commit'
alias gm='git merge'
alias gca='git commit --amend --no-edit'
alias gcl='git clone'
alias gco='git checkout'
alias gcb='git checkout'
alias gd='git diff'
alias gds='gd --stat'
alias gfd='git clean -fd'
alias gl='git log --decorate --graph --pretty=format:"%Cgreen%h%Creset [%ar - %Cred%an%Creset], %s %C(auto)%d%Creset"'
alias gll='git log --graph --decorate --pretty=medium'
alias glog='git log'
alias gp='git push'
alias gpu='eval git push -u origin $(git rev-parse --abbrev-ref HEAD)'
alias gpr='git pull --rebase'
alias gpro='git pull --rebase origin master'
alias gppp='gaa && gc -m "fast push" && gp'
alias gpo='git pull --rebase origin master'
alias gpw='git pull --rebase origin will'
alias gr='git revert'
alias gri='git rebase -i origin/master'
alias grco='git rebase --continue'
alias gs='git status'
alias gsw='git switch -c'
alias gbddd='git branch | grep -v "main" | xargs git branch -d'

##############################################################################
# 03. Programming                                                            #
##############################################################################

# Deno
alias d='deno'
alias dt='d task'
alias dtd='d task dev'
  
# Gradle
alias gw='./gradlew'
alias gwr='gw run'
alias gwi='gw idea'
alias gwb='gw build'

# Rust
alias cgr='cargo run'
alias cdo='cargo doc --open'
alias cgt='cargo test'
alias cgb='cargo build'
alias cgc='cargo check'
alias cgwt='cargo watch -x check -x test'
alias cgw='cargo watch -x check -x test -x run'
alias cf='cargo fmt && cargo clippy'
alias cgcm='cgc && cgt && cf'
alias cb='cargo bench'

# Go
alias gob='go build'
alias got='go test'
alias gotb='go test -bench=.'
alias gotc='go test -cover'
alias gor='go run'
alias goc='go clean'
alias gof='go format'
alias goi='go install'
alias gofix='go fix'
alias god='go doc'
alias gcu='$HOME/go/bin/go-coreutils'

# Java
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS with Homebrew
    alias java11='JAVA_HOME=/opt/homebrew/opt/openjdk@11/bin/java'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - common Java 11 locations
    if [ -d "/usr/lib/jvm/java-11-openjdk" ]; then
        alias java11='JAVA_HOME=/usr/lib/jvm/java-11-openjdk'
    elif [ -d "/usr/lib/jvm/java-11" ]; then
        alias java11='JAVA_HOME=/usr/lib/jvm/java-11'
    fi
fi
alias j!=jbang

# NPM/Node
alias p='pnpm'
alias es='ember serve'
alias nps='npm start'
alias npi='npm install'

# AI/Development tools
alias aider='py -m aider --cache-prompts'
alias a='aider'
alias ad='aider'
alias o='ollama'

##############################################################################
# 04. Networking                                                             #
##############################################################################

# IP addresses
alias ip="dig +short myip.opendns.com @resolver1.opendns.com"
# Platform-specific local IP
if [[ "$OSTYPE" == "darwin"* ]]; then
    alias localip="ipconfig getifaddr en0"
else
    # Linux - get IP of default interface
    alias localip="ip route get 1 | awk '{print \$7; exit}' 2>/dev/null || hostname -I | awk '{print \$1}'"
fi
alias ips="ifconfig -a 2>/dev/null | grep -o 'inet6\? \(addr:\)\?\s\?\(\(\([0-9]\+\.\)\{3\}[0-9]\+\)\|[a-fA-F0-9:]\+\)' | awk '{ sub(/inet6? (addr:)? ?/, \"\"); print }' || ip -o addr show | awk '{print \$4}' | cut -d/ -f1"

# Show active network interfaces
if [[ "$OSTYPE" == "darwin"* ]]; then
    alias ifactive="ifconfig | pcregrep -M -o '^[^\t:]+:([^\n]|\n\t)*status: active'"
    # Flush Directory Service cache
    alias flush="dscacheutil -flushcache && killall -HUP mDNSResponder"
else
    # Linux
    alias ifactive="ip link show | grep 'state UP' | cut -d: -f2 | tr -d ' '"
    # Linux DNS cache flush (systemd-resolved)
    alias flush="sudo systemctl restart systemd-resolved 2>/dev/null || sudo service nscd restart 2>/dev/null || echo 'DNS cache flush not available'"
fi

for method in GET HEAD POST PUT DELETE TRACE OPTIONS; do
	alias "${method}"="lwp-request -m '${method}'"
done

##############################################################################
# 05. Kubernetes                                                             #
##############################################################################

# kubectl shortcuts
alias k='kubectl'
alias ka='kubectl get all --all-namespaces'
alias kp='kubectl get pods'
alias kdp='kubectl describe pod'
alias ki='kubectl get ing'
alias kd='kubectl get deployments'
alias ks='kubectl get svc'
alias kn='kubectl get nodes'
alias kl='kubectl logs'
alias ksysgpo='kubectl --namespace=kube-system get pod'

# kubectl delete operations
alias krm='kubectl delete'
alias krmf='kubectl delete -f'
alias krming='kubectl delete ingress'
alias krmingl='kubectl delete ingress -l'
alias krmingall='kubectl delete ingress --all-namespaces'

# kubectl service operations
alias kgsvcoyaml='kubectl get service -o=yaml'
alias kgsvcwn='kubectl get service --watch --namespace'
alias kgsvcslwn='kubectl get service --show-labels --watch --namespace'
alias kgwf='kubectl get --watch -f'

# Configuration and tools
alias kc='edit ~/.kube/config'
alias cap='kube-capacity'
alias internal-rpk="kubectl --namespace redpanda exec -i -t redpanda-0 -c redpanda -- rpk"

# Telepresence
alias tp='telepresence'
alias tl='tp list'
alias tc='tp connect'

# Talos
alias td='talosctl dashboard'

##############################################################################
# 06. Development Tools                                                      #
##############################################################################

# Docker and Docker Compose
alias dcd='docker-compose down'
alias dcs='docker-compose stop'
alias dcu='docker-compose up -d'
alias dcb='docker-compose build'
alias dps='docker ps'

# Minikube
alias m='minikube'
alias ms='minikube start'

# Skaffold
alias s='skaffold'
alias sr='s run'
alias sdl='s delete'
alias sd='s dev'

# Editors and IDEs
alias z='zed'
alias nv='nvim'

# File and content operations
alias t='ssh wcygan@betty -t "tmux attach -t main || tmux new -s main"'
# Platform-specific repomix alias
if [[ "$OSTYPE" == "darwin"* ]]; then
    alias rr='repomix && cat repomix-output.xml | pbcopy && rm repomix-output.xml'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v xclip > /dev/null; then
        alias rr='repomix && cat repomix-output.xml | xclip -selection clipboard && rm repomix-output.xml'
    elif command -v xsel > /dev/null; then
        alias rr='repomix && cat repomix-output.xml | xsel --clipboard --input && rm repomix-output.xml'
    else
        alias rr='repomix && cat repomix-output.xml && rm repomix-output.xml'
    fi
fi
alias mcp='edit ~/.cursor/mcp.json'

# Fleet (JetBrains)
alias fl='fleet'

##############################################################################
# XX. Misc                                                                   #
##############################################################################

# Canonical hex dump; some systems have this symlinked
command -v hd > /dev/null || alias hd="hexdump -C"

# Cross-platform hash commands
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS has no `md5sum`, so use `md5` as a fallback
    command -v md5sum > /dev/null || alias md5sum="md5"
    # macOS has no `sha1sum`, so use `shasum` as a fallback
    command -v sha1sum > /dev/null || alias sha1sum="shasum"
fi

# Recursively delete `.DS_Store` files
alias cleanup="find . -type f -name '*.DS_Store' -ls -delete"

# Platform-specific trash management
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Empty the Trash on all mounted volumes and the main HDD.
    # Also, clear Apple's System Logs to improve shell startup speed.
    # Finally, clear download history from quarantine. https://mths.be/bum
    alias emptytrash="sudo rm -rfv /Volumes/*/.Trashes; sudo rm -rfv ~/.Trash; sudo rm -rfv /private/var/log/asl/*.asl; sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV* 'delete from LSQuarantineEvent'"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux trash management
    if command -v trash-empty > /dev/null; then
        alias emptytrash="trash-empty"
    elif command -v gio > /dev/null; then
        alias emptytrash="gio trash --empty"
    else
        alias emptytrash="rm -rf ~/.local/share/Trash/*"
    fi
fi

# macOS-specific Finder commands
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Show/hide hidden files in Finder
    alias show="defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder"
    alias hide="defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder"

    # Hide/show all desktop icons (useful when presenting)
    alias hidedesktop="defaults write com.apple.finder CreateDesktop -bool false && killall Finder"
    alias showdesktop="defaults write com.apple.finder CreateDesktop -bool true && killall Finder"
fi

# URL-encode strings
# Python 3 compatible version
alias urlencode='python3 -c "import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]));"'

# Intuitive map function
# For example, to list all directories that contain a certain file:
# find . -name .gitattributes | map dirname
alias map="xargs -n1"

# Print each PATH entry on a separate line
alias path='echo -e ${PATH//:/\\n}'