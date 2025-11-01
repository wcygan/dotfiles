-- Neovim configuration entry point
-- Part of dotfiles repository: config/nvim/

-- Set leader keys before loading plugins
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Load core configuration
require("config.options")
require("config.keymaps")
require("config.autocmds")

-- Bootstrap and load plugins
require("config.lazy")
