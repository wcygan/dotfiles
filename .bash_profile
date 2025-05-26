#!/bin/bash

# .bash_profile - loaded for login shells
# For interactive shells, source .bashrc which has all the configuration
if [ -n "$PS1" ] && [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Additional login shell specific settings can go here
# (none needed currently since .bashrc handles everything)