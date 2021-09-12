export ZSH="/Users/wcygan/.oh-my-zsh"

ZSH_THEME="robbyrussell"

# Platform Based
alias will='cd ~'
alias dev='cd ~/Dev'
alias school='cd ~/School'

# General
alias c='clear'
alias vzsh='vim ~/.zshrc'
alias szsh='source ~/.zshrc'

# NPM - related
alias es='ember serve'
alias nps='npm start'
alias npi='npm install'

# Git
alias gs='git status'
alias gpr='git pull --rebase'
alias rbs='git pull --rebase'

# Rust
alias cgr='cargo run'
alias cgt='cargo test'
alias cgb='cargo build'
alias cgc='cargo check'

# Go
alias gob='go build'
alias got='go test'
alias gor='go run'
alias goc='go clean'
alias gof='go format'
alias goi='go install'
alias gofix='go fix'
alias god='go doc'

plugins=(git)

source $ZSH/oh-my-zsh.sh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
