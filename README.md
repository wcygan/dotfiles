# Will's Dotfiles

## Installation

### Clone the repo

```bash
git clone https://github.com/wcygan/dotfiles.git && cd dotfiles
```

Depending on which shell you use, run either `bootstrap-zsh.sh` or `bootstrap-bash.sh`

### Install the dotfiles for zsh

```bash
 source bootstrap-zsh.sh
```

### Install the dotfiles for bash

```bash
 source bootstrap-bash.sh
```

## Machine-specific configuration

If you have machine-specific configuration, you can add it to `~/.platform`. This file is loaded last, so it can override any settings.

## Programs to install

Install these programs and add them to either 

- [fzf](https://github.com/junegunn/fzf)
- [ripgrep](https://github.com/BurntSushi/ripgrep)
- [exa](https://github.com/ogham/exa)
- [broot](https://github.com/Canop/broot)
- [fd](https://github.com/sharkdp/fd)
- [bat](https://github.com/sharkdp/bat)
- [tldr](https://github.com/tldr-pages/tldr)
- [delta](https://github.com/dandavison/delta)
- [jq](https://github.com/stedolan/jq)

## Extensions to install

### Zsh

- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)

# How did you do this?

I copied https://github.com/mathiasbynens/dotfiles and modified it