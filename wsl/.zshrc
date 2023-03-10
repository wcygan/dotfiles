export ZSH="/home/wcygan/.oh-my-zsh"

ZSH_THEME="robbyrussell"



alias will='cd /mnt/c/wcygan'
alias dev='cd /mnt/c/wcygan/dev'
alias school='cd /mnt/c/wcygan/school'

# TODO put all of these in a different file and source them
alias vzsh='vim ~/.zshrc'
alias szsh='source ~/.zshrc'
alias c='clear'

# Git
alias gs='git status'
alias gpr='git pull --rebase'
alias rbs='git pull --rebase'

alias cgr='cargo run'
alias cgt='cargo test'
alias cgb='cargo build'
alias cgc='cargo check'
alias es='ember serve'

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

# mac / linux (tbd)

plugins=(
	git
)

# Make sure to...
# 0. `sudo apt update`
# 1. Install brew: https://brew.sh/
# 2. Install https://github.com/zsh-users/zsh-syntax-highlighting
# 3. `brew install fzf` -- then install keybinds
# 4. `brew install yadm`
# 5. `brew install gh`
# 6. `brew install java`
# 7. `brew install npm`
# 8. `npm install -g ember-cli`

LS_COLORS=$LS_COLORS:'ow=1;34:' ; export LS_COLORS

source $ZSH/oh-my-zsh.sh


[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
source /mnt/c/Users/Will/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
