export ZSH="/Users/wcygan/.oh-my-zsh"

ZSH_THEME="robbyrussell"

alias c='clear'
alias gs='git status'
alias gpr='git pull --rebase'
alias cgr='cargo run'
alias cgt='cargo test'
alias cgb='cargo build'
alias cgc='cargo check'
alias es='ember serve'
alias vzsh='vim ~/.zshrc'
alias szsh='source ~/.zshrc'
alias will='cd ~'
alias dev='cd ~/Dev'
alias school='cd ~/School'

plugins=(git)

source $ZSH/oh-my-zsh.sh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
