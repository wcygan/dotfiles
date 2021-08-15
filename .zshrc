export ZSH="/home/wcygan/.oh-my-zsh"

ZSH_THEME="robbyrussell"

alias c='clear'
alias gs='git status'
alias cgr='cargo run'
alias cgt='cargo test'
alias cgb='cargo build'
alias cgc='cargo check'
alias vzsh='vim ~/.zshrc'
alias szsh='source ~/.zshrc'
alias will='cd /mnt/c/wcygan'
alias dev='cd /mnt/c/wcygan/dev'
alias school='cd /mnt/c/wcygan/school'

plugins=(
	git
)

LS_COLORS=$LS_COLORS:'ow=1;34:' ; export LS_COLORS

source $ZSH/oh-my-zsh.sh


[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
source /mnt/c/Users/Will/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
