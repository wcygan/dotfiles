#!/usr/bin/env bash

##############################################################################
#   Filename: .exports.sh                                                    #
# Maintainer: Will Cygan <wcygan.io@gmail.com>                              #
#        URL: http://github.com/wcygan/dotfiles                             #
#                                                                            #
# Sections:                                                                  #
#   01. Editor Settings ......... Default editor configuration              #
#   02. Python Environment ...... Python encoding and settings             #
#   03. History Configuration ... Bash history size and control             #
#   04. Locale Settings ......... Language and UTF-8 configuration         #
#   05. Terminal Settings ....... Manual pages and terminal config         #
##############################################################################

##############################################################################
# 01. Editor Settings                                                        #
##############################################################################

# Make zed the default editor.
export EDITOR='zed';

##############################################################################
# 02. Python Environment                                                     #
##############################################################################

# Make Python use UTF-8 encoding for output to stdin, stdout, and stderr.
export PYTHONIOENCODING='UTF-8';

##############################################################################
# 03. History Configuration                                                  #
##############################################################################

# Increase Bash history size. Allow 32³ entries; the default is 500.
export HISTSIZE='32768';
export HISTFILESIZE="${HISTSIZE}";
# Omit duplicates and commands that begin with a space from history.
export HISTCONTROL='ignoreboth';

##############################################################################
# 04. Locale Settings                                                        #
##############################################################################

# Prefer US English and use UTF-8.
export LANG='en_US.UTF-8';
export LC_ALL='en_US.UTF-8';

##############################################################################
# 05. Terminal Settings                                                      #
##############################################################################

# Highlight section titles in manual pages.
export LESS_TERMCAP_md="${yellow}";

# Don’t clear the screen after quitting a manual page.
export MANPAGER='less -X';

# Avoid issues with `gpg` as installed via Homebrew.
# https://stackoverflow.com/a/42265848/96656
export GPG_TTY=$(tty);