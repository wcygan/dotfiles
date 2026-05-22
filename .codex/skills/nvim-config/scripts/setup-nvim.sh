#!/usr/bin/env bash
# Bootstrap a modern Neovim configuration with lazy.nvim
# Creates a modular Lua-based configuration structure

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
NVIM_CONFIG="$DOTFILES_ROOT/config/nvim"

main() {
    echo "🚀 Setting up Neovim configuration..."
    echo ""

    # Check if config already exists
    if [[ -f "$NVIM_CONFIG/init.lua" ]]; then
        echo "⚠️  init.lua already exists"
        read -p "   Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Setup cancelled"
            exit 1
        fi
    fi

    # Create directory structure
    echo "📁 Creating directory structure..."
    mkdir -p "$NVIM_CONFIG/lua/config"
    mkdir -p "$NVIM_CONFIG/lua/plugins"
    mkdir -p "$NVIM_CONFIG/after/plugin"

    # Create init.lua
    echo "📝 Creating init.lua..."
    cat > "$NVIM_CONFIG/init.lua" <<'EOF'
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
EOF

    # Create options.lua
    echo "📝 Creating lua/config/options.lua..."
    cat > "$NVIM_CONFIG/lua/config/options.lua" <<'EOF'
-- Editor options and settings

local opt = vim.opt

-- UI
opt.number = true
opt.relativenumber = true
opt.signcolumn = "yes"
opt.cursorline = true
opt.termguicolors = true
opt.showmode = false
opt.scrolloff = 8

-- Tabs & Indentation
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true
opt.smartindent = true

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true

-- Split Windows
opt.splitright = true
opt.splitbelow = true

-- Clipboard
opt.clipboard = "unnamedplus"

-- Files
opt.backup = false
opt.swapfile = false
opt.undofile = true

-- Performance
opt.updatetime = 250
opt.timeoutlen = 300

-- Completion
opt.completeopt = "menu,menuone,noselect"
EOF

    # Create keymaps.lua
    echo "📝 Creating lua/config/keymaps.lua..."
    cat > "$NVIM_CONFIG/lua/config/keymaps.lua" <<'EOF'
-- Custom keybindings

local map = vim.keymap.set

-- Window navigation
map("n", "<C-h>", "<C-w>h", { desc = "Go to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Go to lower window" })
map("n", "<C-k>", "<C-w>k", { desc = "Go to upper window" })
map("n", "<C-l>", "<C-w>l", { desc = "Go to right window" })

-- Buffer navigation
map("n", "<S-h>", "<cmd>bprevious<cr>", { desc = "Previous buffer" })
map("n", "<S-l>", "<cmd>bnext<cr>", { desc = "Next buffer" })

-- Save/Quit
map("n", "<leader>w", "<cmd>w<cr>", { desc = "Save file" })
map("n", "<leader>q", "<cmd>q<cr>", { desc = "Quit" })

-- Clear search highlights
map("n", "<Esc>", "<cmd>nohlsearch<cr>", { desc = "Clear highlights" })

-- Better indenting
map("v", "<", "<gv")
map("v", ">", ">gv")

-- Diagnostic keymaps
map("n", "[d", vim.diagnostic.goto_prev, { desc = "Previous diagnostic" })
map("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })
map("n", "<leader>e", vim.diagnostic.open_float, { desc = "Show diagnostic" })
EOF

    # Create autocmds.lua
    echo "📝 Creating lua/config/autocmds.lua..."
    cat > "$NVIM_CONFIG/lua/config/autocmds.lua" <<'EOF'
-- Autocommands

local autocmd = vim.api.nvim_create_autocmd
local augroup = vim.api.nvim_create_augroup

-- Highlight on yank
autocmd("TextYankPost", {
  group = augroup("highlight_yank", { clear = true }),
  callback = function()
    vim.highlight.on_yank()
  end,
})

-- Restore cursor position
autocmd("BufReadPost", {
  group = augroup("restore_cursor", { clear = true }),
  callback = function()
    local mark = vim.api.nvim_buf_get_mark(0, '"')
    local lcount = vim.api.nvim_buf_line_count(0)
    if mark[1] > 0 and mark[1] <= lcount then
      pcall(vim.api.nvim_win_set_cursor, 0, mark)
    end
  end,
})

-- Close certain filetypes with 'q'
autocmd("FileType", {
  group = augroup("close_with_q", { clear = true }),
  pattern = { "qf", "help", "man", "notify", "lspinfo" },
  callback = function(event)
    vim.bo[event.buf].buflisted = false
    vim.keymap.set("n", "q", "<cmd>close<cr>", { buffer = event.buf, silent = true })
  end,
})
EOF

    # Create lazy.lua (plugin manager bootstrap)
    echo "📝 Creating lua/config/lazy.lua..."
    cat > "$NVIM_CONFIG/lua/config/lazy.lua" <<'EOF'
-- Bootstrap lazy.nvim plugin manager

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- Configure plugins
require("lazy").setup({
  spec = {
    { import = "plugins" },
  },
  defaults = {
    lazy = false,
    version = false,
  },
  checker = { enabled = true },
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip",
        "tarPlugin",
        "tohtml",
        "tutor",
        "zipPlugin",
      },
    },
  },
})
EOF

    # Create basic colorscheme plugin
    echo "📝 Creating lua/plugins/colorscheme.lua..."
    cat > "$NVIM_CONFIG/lua/plugins/colorscheme.lua" <<'EOF'
-- Color scheme configuration

return {
  "folke/tokyonight.nvim",
  lazy = false,
  priority = 1000,
  config = function()
    vim.cmd([[colorscheme tokyonight-night]])
  end,
}
EOF

    # Create treesitter plugin
    echo "📝 Creating lua/plugins/treesitter.lua..."
    cat > "$NVIM_CONFIG/lua/plugins/treesitter.lua" <<'EOF'
-- Treesitter configuration (syntax highlighting)

return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  event = { "BufReadPost", "BufNewFile" },
  config = function()
    require("nvim-treesitter.configs").setup({
      ensure_installed = { "lua", "vim", "vimdoc", "query" },
      highlight = { enable = true },
      indent = { enable = true },
    })
  end,
}
EOF

    echo ""
    echo "✅ Neovim configuration created successfully!"
    echo ""
    echo "📂 Structure:"
    echo "   config/nvim/"
    echo "   ├── init.lua"
    echo "   ├── lua/"
    echo "   │   ├── config/"
    echo "   │   │   ├── options.lua"
    echo "   │   │   ├── keymaps.lua"
    echo "   │   │   ├── autocmds.lua"
    echo "   │   │   └── lazy.lua"
    echo "   │   └── plugins/"
    echo "   │       ├── colorscheme.lua"
    echo "   │       └── treesitter.lua"
    echo "   └── after/plugin/"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Open Neovim: nvim"
    echo "   2. lazy.nvim will auto-install plugins"
    echo "   3. Add more plugins in lua/plugins/"
    echo "   4. Configure LSP with :help lsp"
    echo ""
}

main "$@"
