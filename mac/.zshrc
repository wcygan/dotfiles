zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}' 'r:|=*' 'l:|=* r:|=*'
autoload -Uz compinit && compinit

# Platform Based
alias will='cd ~'
alias dev='cd ~/Development'

# General
alias c='clear'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias vzsh='vim ~/.zshrc'
alias szsh='source ~/.zshrc'
alias ls='exa'
alias l='exa -l'

# NPM - related
alias es='ember serve'
alias nps='npm start'
alias npi='npm install'

# Git
alias gs='git status'
alias gc='git commit'
alias gaa='git add .'
alias glog='git log'
alias gcb='git checkout branch'
alias gb='git branch'
alias gp='git push'
alias gpr='git pull --rebase'
alias gcl='git clone'
alias gd='git diff'

# Rust
alias cgr='cargo run'
alias cgt='cargo test'
alias cgb='cargo build'
alias cgc='cargo check'

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

source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
