# Neovim Configuration Reference

Advanced configuration patterns, plugin ecosystems, and comprehensive setup guide for Neovim.

## Table of Contents

1. [Complete Configuration Examples](#complete-configuration-examples)
2. [Advanced Plugin Patterns](#advanced-plugin-patterns)
3. [LSP Deep Dive](#lsp-deep-dive)
4. [Completion & Snippets](#completion--snippets)
5. [Git Integration](#git-integration)
6. [Debugging](#debugging)
7. [Language-Specific Setups](#language-specific-setups)
8. [Performance Optimization](#performance-optimization)
9. [Custom Commands & Functions](#custom-commands--functions)

---

## Complete Configuration Examples

### Minimal Configuration (10 lines)

```lua
-- config/nvim/init.lua
vim.g.mapleader = " "
vim.opt.number = true
vim.opt.mouse = "a"
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.hlsearch = false
vim.opt.wrap = false
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
```

### Full Modular Configuration

**init.lua:**
```lua
-- Set leader keys first
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Load core configuration
require("config.options")
require("config.keymaps")
require("config.autocmds")

-- Bootstrap and load plugins
require("config.lazy")
```

**lua/config/options.lua:**
```lua
local opt = vim.opt

-- UI
opt.number = true
opt.relativenumber = true
opt.signcolumn = "yes"
opt.cursorline = true
opt.termguicolors = true
opt.showmode = false
opt.pumheight = 10
opt.scrolloff = 8
opt.sidescrolloff = 8

-- Tabs & Indentation
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true
opt.autoindent = true
opt.smartindent = true

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true
opt.incsearch = true

-- Split Windows
opt.splitright = true
opt.splitbelow = true

-- Clipboard
opt.clipboard = "unnamedplus"

-- Files
opt.backup = false
opt.swapfile = false
opt.undofile = true
opt.undolevels = 10000

-- Performance
opt.updatetime = 250
opt.timeoutlen = 300
opt.lazyredraw = false

-- Formatting
opt.wrap = false
opt.linebreak = true
opt.breakindent = true

-- Completion
opt.completeopt = "menu,menuone,noselect"
opt.shortmess:append("c")

-- Folds (with treesitter)
opt.foldmethod = "expr"
opt.foldexpr = "nvim_treesitter#foldexpr()"
opt.foldenable = false
```

**lua/config/keymaps.lua:**
```lua
local map = vim.keymap.set

-- Better navigation
map("n", "<C-h>", "<C-w>h", { desc = "Go to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Go to lower window" })
map("n", "<C-k>", "<C-w>k", { desc = "Go to upper window" })
map("n", "<C-l>", "<C-w>l", { desc = "Go to right window" })

-- Resize windows
map("n", "<C-Up>", "<cmd>resize +2<cr>", { desc = "Increase height" })
map("n", "<C-Down>", "<cmd>resize -2<cr>", { desc = "Decrease height" })
map("n", "<C-Left>", "<cmd>vertical resize -2<cr>", { desc = "Decrease width" })
map("n", "<C-Right>", "<cmd>vertical resize +2<cr>", { desc = "Increase width" })

-- Buffer management
map("n", "<S-h>", "<cmd>bprevious<cr>", { desc = "Previous buffer" })
map("n", "<S-l>", "<cmd>bnext<cr>", { desc = "Next buffer" })
map("n", "<leader>bd", "<cmd>bdelete<cr>", { desc = "Delete buffer" })

-- Save/Quit
map("n", "<leader>w", "<cmd>w<cr>", { desc = "Save file" })
map("n", "<leader>q", "<cmd>q<cr>", { desc = "Quit" })
map("n", "<leader>Q", "<cmd>qa!<cr>", { desc = "Quit all without saving" })

-- Clear search
map("n", "<Esc>", "<cmd>nohlsearch<cr>", { desc = "Clear search highlights" })

-- Better indenting
map("v", "<", "<gv")
map("v", ">", ">gv")

-- Move lines
map("n", "<A-j>", "<cmd>m .+1<cr>==", { desc = "Move line down" })
map("n", "<A-k>", "<cmd>m .-2<cr>==", { desc = "Move line up" })
map("i", "<A-j>", "<esc><cmd>m .+1<cr>==gi", { desc = "Move line down" })
map("i", "<A-k>", "<esc><cmd>m .-2<cr>==gi", { desc = "Move line up" })
map("v", "<A-j>", ":m '>+1<cr>gv=gv", { desc = "Move selection down" })
map("v", "<A-k>", ":m '<-2<cr>gv=gv", { desc = "Move selection up" })

-- Quick list
map("n", "<leader>xl", "<cmd>lopen<cr>", { desc = "Location List" })
map("n", "<leader>xq", "<cmd>copen<cr>", { desc = "Quickfix List" })

-- Diagnostic keymaps
map("n", "[d", vim.diagnostic.goto_prev, { desc = "Previous diagnostic" })
map("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })
map("n", "<leader>e", vim.diagnostic.open_float, { desc = "Show diagnostic" })
map("n", "<leader>dl", vim.diagnostic.setloclist, { desc = "Diagnostic list" })

-- Terminal
map("t", "<Esc><Esc>", "<C-\\><C-n>", { desc = "Exit terminal mode" })
map("n", "<leader>tt", "<cmd>terminal<cr>", { desc = "Open terminal" })
```

**lua/config/autocmds.lua:**
```lua
local autocmd = vim.api.nvim_create_autocmd
local augroup = vim.api.nvim_create_augroup

-- Highlight on yank
autocmd("TextYankPost", {
  group = augroup("highlight_yank", { clear = true }),
  callback = function()
    vim.highlight.on_yank()
  end,
})

-- Resize splits on window resize
autocmd("VimResized", {
  group = augroup("resize_splits", { clear = true }),
  callback = function()
    vim.cmd("tabdo wincmd =")
  end,
})

-- Close certain filetypes with 'q'
autocmd("FileType", {
  group = augroup("close_with_q", { clear = true }),
  pattern = { "qf", "help", "man", "notify", "lspinfo", "spectre_panel" },
  callback = function(event)
    vim.bo[event.buf].buflisted = false
    vim.keymap.set("n", "q", "<cmd>close<cr>", { buffer = event.buf, silent = true })
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

-- Auto-create directories when saving
autocmd("BufWritePre", {
  group = augroup("auto_create_dir", { clear = true }),
  callback = function(event)
    if event.match:match("^%w%w+://") then
      return
    end
    local file = vim.loop.fs_realpath(event.match) or event.match
    vim.fn.mkdir(vim.fn.fnamemodify(file, ":p:h"), "p")
  end,
})

-- Format on save (per language)
autocmd("BufWritePre", {
  group = augroup("format_on_save", { clear = true }),
  pattern = { "*.go", "*.rs", "*.lua" },
  callback = function()
    vim.lsp.buf.format()
  end,
})

-- Trim trailing whitespace
autocmd("BufWritePre", {
  group = augroup("trim_whitespace", { clear = true }),
  pattern = "*",
  callback = function()
    local save_cursor = vim.fn.getpos(".")
    vim.cmd([[%s/\s\+$//e]])
    vim.fn.setpos(".", save_cursor)
  end,
})
```

---

## Advanced Plugin Patterns

### Lazy Loading Strategies

**By Command:**
```lua
{
  "nvim-tree/nvim-tree.lua",
  cmd = { "NvimTreeToggle", "NvimTreeFocus" },
}
```

**By Event:**
```lua
{
  "lewis6991/gitsigns.nvim",
  event = { "BufReadPre", "BufNewFile" },
}
```

**By Filetype:**
```lua
{
  "rust-lang/rust.vim",
  ft = "rust",
}
```

**By Keys:**
```lua
{
  "nvim-telescope/telescope.nvim",
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>", desc = "Find Files" },
    { "<leader>fg", "<cmd>Telescope live_grep<cr>", desc = "Live Grep" },
  },
}
```

**Conditional Loading:**
```lua
{
  "github/copilot.vim",
  cond = function()
    return vim.fn.executable("node") == 1
  end,
}
```

### Plugin Dependencies

```lua
{
  "nvim-telescope/telescope.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    {
      "nvim-telescope/telescope-fzf-native.nvim",
      build = "make",
    },
  },
}
```

---

## LSP Deep Dive

### Complete LSP Setup

**lua/plugins/lsp.lua:**
```lua
return {
  "neovim/nvim-lspconfig",
  dependencies = {
    "williamboman/mason.nvim",
    "williamboman/mason-lspconfig.nvim",
    "hrsh7th/cmp-nvim-lsp",
    { "j-hui/fidget.nvim", opts = {} },
  },
  config = function()
    -- Mason setup
    require("mason").setup()
    require("mason-lspconfig").setup({
      ensure_installed = {
        "lua_ls",
        "rust_analyzer",
        "gopls",
        "pyright",
        "ts_ls",
        "clangd",
      },
      automatic_installation = true,
    })

    -- Global diagnostic config
    vim.diagnostic.config({
      virtual_text = {
        prefix = "●",
      },
      signs = true,
      update_in_insert = false,
      underline = true,
      severity_sort = true,
      float = {
        focusable = false,
        style = "minimal",
        border = "rounded",
        source = "always",
        header = "",
        prefix = "",
      },
    })

    -- Diagnostic signs
    local signs = { Error = " ", Warn = " ", Hint = " ", Info = " " }
    for type, icon in pairs(signs) do
      local hl = "DiagnosticSign" .. type
      vim.fn.sign_define(hl, { text = icon, texthl = hl, numhl = "" })
    end

    -- LSP keymaps function
    local on_attach = function(client, bufnr)
      local map = function(keys, func, desc)
        vim.keymap.set("n", keys, func, { buffer = bufnr, desc = "LSP: " .. desc })
      end

      -- Navigation
      map("gd", vim.lsp.buf.definition, "Goto Definition")
      map("gD", vim.lsp.buf.declaration, "Goto Declaration")
      map("gr", require("telescope.builtin").lsp_references, "Goto References")
      map("gI", vim.lsp.buf.implementation, "Goto Implementation")
      map("<leader>D", vim.lsp.buf.type_definition, "Type Definition")

      -- Symbols
      map("<leader>ds", require("telescope.builtin").lsp_document_symbols, "Document Symbols")
      map("<leader>ws", require("telescope.builtin").lsp_dynamic_workspace_symbols, "Workspace Symbols")

      -- Actions
      map("<leader>rn", vim.lsp.buf.rename, "Rename")
      map("<leader>ca", vim.lsp.buf.code_action, "Code Action")

      -- Documentation
      map("K", vim.lsp.buf.hover, "Hover Documentation")
      map("<C-k>", vim.lsp.buf.signature_help, "Signature Documentation")

      -- Workspace
      map("<leader>wa", vim.lsp.buf.add_workspace_folder, "Add Workspace Folder")
      map("<leader>wr", vim.lsp.buf.remove_workspace_folder, "Remove Workspace Folder")
      map("<leader>wl", function()
        print(vim.inspect(vim.lsp.buf.list_workspace_folders()))
      end, "List Workspace Folders")

      -- Format on save for specific clients
      if client.supports_method("textDocument/formatting") then
        vim.api.nvim_create_autocmd("BufWritePre", {
          buffer = bufnr,
          callback = function()
            vim.lsp.buf.format({ bufnr = bufnr })
          end,
        })
      end
    end

    -- Capabilities for completion
    local capabilities = vim.lsp.protocol.make_client_capabilities()
    capabilities = require("cmp_nvim_lsp").default_capabilities(capabilities)

    -- Server configurations
    local lspconfig = require("lspconfig")

    -- Lua
    lspconfig.lua_ls.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        Lua = {
          runtime = { version = "LuaJIT" },
          workspace = {
            checkThirdParty = false,
            library = {
              vim.env.VIMRUNTIME,
              "${3rd}/luv/library",
            },
          },
          diagnostics = {
            globals = { "vim" },
          },
          telemetry = { enable = false },
          format = {
            enable = true,
            defaultConfig = {
              indent_style = "space",
              indent_size = "2",
            },
          },
        },
      },
    })

    -- Rust
    lspconfig.rust_analyzer.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        ["rust-analyzer"] = {
          cargo = {
            allFeatures = true,
            loadOutDirsFromCheck = true,
            runBuildScripts = true,
          },
          checkOnSave = {
            command = "clippy",
            extraArgs = { "--all", "--", "-W", "clippy::all" },
          },
          procMacro = {
            enable = true,
            ignored = {
              ["async-trait"] = { "async_trait" },
              ["napi-derive"] = { "napi" },
              ["async-recursion"] = { "async_recursion" },
            },
          },
        },
      },
    })

    -- Go
    lspconfig.gopls.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        gopls = {
          gofumpt = true,
          codelenses = {
            gc_details = false,
            generate = true,
            regenerate_cgo = true,
            run_govulncheck = true,
            test = true,
            tidy = true,
            upgrade_dependency = true,
            vendor = true,
          },
          hints = {
            assignVariableTypes = true,
            compositeLiteralFields = true,
            compositeLiteralTypes = true,
            constantValues = true,
            functionTypeParameters = true,
            parameterNames = true,
            rangeVariableTypes = true,
          },
          analyses = {
            fieldalignment = true,
            nilness = true,
            unusedparams = true,
            unusedwrite = true,
            useany = true,
          },
          usePlaceholders = true,
          completeUnimported = true,
          staticcheck = true,
          directoryFilters = { "-.git", "-.vscode", "-.idea", "-.vscode-test", "-node_modules" },
          semanticTokens = true,
        },
      },
    })

    -- Python
    lspconfig.pyright.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        python = {
          analysis = {
            autoSearchPaths = true,
            diagnosticMode = "workspace",
            useLibraryCodeForTypes = true,
            typeCheckingMode = "basic",
          },
        },
      },
    })

    -- TypeScript
    lspconfig.ts_ls.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      init_options = {
        preferences = {
          disableSuggestions = false,
        },
      },
    })
  end,
}
```

---

## Completion & Snippets

**lua/plugins/completion.lua:**
```lua
return {
  "hrsh7th/nvim-cmp",
  event = "InsertEnter",
  dependencies = {
    "hrsh7th/cmp-nvim-lsp",
    "hrsh7th/cmp-buffer",
    "hrsh7th/cmp-path",
    "saadparwaiz1/cmp_luasnip",
    {
      "L3MON4D3/LuaSnip",
      version = "v2.*",
      build = "make install_jsregexp",
    },
    "rafamadriz/friendly-snippets",
  },
  config = function()
    local cmp = require("cmp")
    local luasnip = require("luasnip")

    -- Load VSCode-style snippets
    require("luasnip.loaders.from_vscode").lazy_load()

    cmp.setup({
      snippet = {
        expand = function(args)
          luasnip.lsp_expand(args.body)
        end,
      },
      mapping = cmp.mapping.preset.insert({
        ["<C-n>"] = cmp.mapping.select_next_item(),
        ["<C-p>"] = cmp.mapping.select_prev_item(),
        ["<C-b>"] = cmp.mapping.scroll_docs(-4),
        ["<C-f>"] = cmp.mapping.scroll_docs(4),
        ["<C-Space>"] = cmp.mapping.complete(),
        ["<C-e>"] = cmp.mapping.abort(),
        ["<CR>"] = cmp.mapping.confirm({ select = true }),
        ["<Tab>"] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_next_item()
          elseif luasnip.expand_or_jumpable() then
            luasnip.expand_or_jump()
          else
            fallback()
          end
        end, { "i", "s" }),
        ["<S-Tab>"] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_prev_item()
          elseif luasnip.jumpable(-1) then
            luasnip.jump(-1)
          else
            fallback()
          end
        end, { "i", "s" }),
      }),
      sources = {
        { name = "nvim_lsp" },
        { name = "luasnip" },
        { name = "buffer" },
        { name = "path" },
      },
      formatting = {
        format = function(entry, vim_item)
          -- Kind icons
          local kind_icons = {
            Text = "",
            Method = "󰆧",
            Function = "󰊕",
            Constructor = "",
            Field = "󰇽",
            Variable = "󰂡",
            Class = "󰠱",
            Interface = "",
            Module = "",
            Property = "󰜢",
            Unit = "",
            Value = "󰎠",
            Enum = "",
            Keyword = "󰌋",
            Snippet = "",
            Color = "󰏘",
            File = "󰈙",
            Reference = "",
            Folder = "󰉋",
            EnumMember = "",
            Constant = "󰏿",
            Struct = "",
            Event = "",
            Operator = "󰆕",
            TypeParameter = "󰅲",
          }
          vim_item.kind = string.format("%s %s", kind_icons[vim_item.kind], vim_item.kind)
          vim_item.menu = ({
            nvim_lsp = "[LSP]",
            luasnip = "[Snippet]",
            buffer = "[Buffer]",
            path = "[Path]",
          })[entry.source.name]
          return vim_item
        end,
      },
    })
  end,
}
```

---

## Git Integration

**lua/plugins/git.lua:**
```lua
return {
  -- Gitsigns (inline git status)
  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPre", "BufNewFile" },
    opts = {
      signs = {
        add = { text = "│" },
        change = { text = "│" },
        delete = { text = "_" },
        topdelete = { text = "‾" },
        changedelete = { text = "~" },
        untracked = { text = "┆" },
      },
      on_attach = function(bufnr)
        local gs = package.loaded.gitsigns

        local map = function(mode, l, r, opts)
          opts = opts or {}
          opts.buffer = bufnr
          vim.keymap.set(mode, l, r, opts)
        end

        -- Navigation
        map("n", "]c", function()
          if vim.wo.diff then
            return "]c"
          end
          vim.schedule(function()
            gs.next_hunk()
          end)
          return "<Ignore>"
        end, { expr = true, desc = "Next hunk" })

        map("n", "[c", function()
          if vim.wo.diff then
            return "[c"
          end
          vim.schedule(function()
            gs.prev_hunk()
          end)
          return "<Ignore>"
        end, { expr = true, desc = "Previous hunk" })

        -- Actions
        map("n", "<leader>hs", gs.stage_hunk, { desc = "Stage hunk" })
        map("n", "<leader>hr", gs.reset_hunk, { desc = "Reset hunk" })
        map("v", "<leader>hs", function()
          gs.stage_hunk({ vim.fn.line("."), vim.fn.line("v") })
        end, { desc = "Stage hunk" })
        map("v", "<leader>hr", function()
          gs.reset_hunk({ vim.fn.line("."), vim.fn.line("v") })
        end, { desc = "Reset hunk" })
        map("n", "<leader>hS", gs.stage_buffer, { desc = "Stage buffer" })
        map("n", "<leader>hu", gs.undo_stage_hunk, { desc = "Undo stage hunk" })
        map("n", "<leader>hR", gs.reset_buffer, { desc = "Reset buffer" })
        map("n", "<leader>hp", gs.preview_hunk, { desc = "Preview hunk" })
        map("n", "<leader>hb", function()
          gs.blame_line({ full = true })
        end, { desc = "Blame line" })
        map("n", "<leader>tb", gs.toggle_current_line_blame, { desc = "Toggle blame" })
        map("n", "<leader>hd", gs.diffthis, { desc = "Diff this" })
        map("n", "<leader>hD", function()
          gs.diffthis("~")
        end, { desc = "Diff this ~" })
        map("n", "<leader>td", gs.toggle_deleted, { desc = "Toggle deleted" })

        -- Text object
        map({ "o", "x" }, "ih", ":<C-U>Gitsigns select_hunk<CR>", { desc = "GitSigns select hunk" })
      end,
    },
  },

  -- LazyGit integration
  {
    "kdheepak/lazygit.nvim",
    cmd = "LazyGit",
    dependencies = {
      "nvim-lua/plenary.nvim",
    },
    keys = {
      { "<leader>gg", "<cmd>LazyGit<cr>", desc = "LazyGit" },
    },
  },
}
```

---

## Language-Specific Setups

### Go Development

```lua
-- lua/plugins/go.lua
return {
  {
    "ray-x/go.nvim",
    dependencies = {
      "ray-x/guihua.lua",
      "neovim/nvim-lspconfig",
      "nvim-treesitter/nvim-treesitter",
    },
    config = function()
      require("go").setup()
    end,
    event = { "CmdlineEnter" },
    ft = { "go", "gomod" },
    build = ':lua require("go.install").update_all_sync()',
  },
}
```

### Rust Development

```lua
-- lua/plugins/rust.lua
return {
  {
    "simrat39/rust-tools.nvim",
    ft = "rust",
    dependencies = "neovim/nvim-lspconfig",
    config = function()
      local rt = require("rust-tools")
      rt.setup({
        server = {
          on_attach = function(_, bufnr)
            vim.keymap.set("n", "K", rt.hover_actions.hover_actions, { buffer = bufnr })
            vim.keymap.set("n", "<leader>ca", rt.code_action_group.code_action_group, { buffer = bufnr })
          end,
        },
      })
    end,
  },
  {
    "rust-lang/rust.vim",
    ft = "rust",
    init = function()
      vim.g.rustfmt_autosave = 1
    end,
  },
}
```

---

## Performance Optimization

### Startup Time Profiling

```vim
:StartupTime     " With vim-startuptime plugin
```

Or manually:
```bash
nvim --startuptime startup.log
```

### Lazy Loading Best Practices

1. **Always lazy load large plugins**
2. **Use event triggers for UI plugins**
3. **Defer non-essential plugins**
4. **Disable unused built-in plugins**

### Disable Built-in Plugins

```lua
-- In lua/config/lazy.lua
require("lazy").setup({
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip",
        "matchit",
        "matchparen",
        "netrwPlugin",
        "tarPlugin",
        "tohtml",
        "tutor",
        "zipPlugin",
      },
    },
  },
})
```

---

## Custom Commands & Functions

### Custom Commands

```lua
-- lua/config/autocmds.lua
vim.api.nvim_create_user_command("FormatDisable", function(args)
  if args.bang then
    vim.b.disable_autoformat = true
  else
    vim.g.disable_autoformat = true
  end
end, {
  desc = "Disable autoformat-on-save",
  bang = true,
})

vim.api.nvim_create_user_command("FormatEnable", function()
  vim.b.disable_autoformat = false
  vim.g.disable_autoformat = false
end, {
  desc = "Re-enable autoformat-on-save",
})

vim.api.nvim_create_user_command("CopyFilePath", function()
  local path = vim.fn.expand("%:p")
  vim.fn.setreg("+", path)
  print("Copied: " .. path)
end, { desc = "Copy current file path" })
```

### Custom Functions

```lua
-- lua/utils.lua
local M = {}

-- Toggle between light and dark themes
function M.toggle_theme()
  if vim.o.background == "dark" then
    vim.o.background = "light"
  else
    vim.o.background = "dark"
  end
end

-- Quick note taking
function M.quick_note()
  local note_dir = vim.fn.expand("~/notes")
  local date = os.date("%Y-%m-%d")
  local file = note_dir .. "/" .. date .. ".md"
  vim.cmd("edit " .. file)
end

-- Toggle relative line numbers
function M.toggle_relative_number()
  vim.opt.relativenumber = not vim.opt.relativenumber:get()
end

return M
```

---

## Resources

- [Neovim Documentation](https://neovim.io/doc/)
- [lazy.nvim](https://github.com/folke/lazy.nvim)
- [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig)
- [Mason.nvim](https://github.com/williamboman/mason.nvim)
- [LazyVim](https://github.com/LazyVim/LazyVim) (reference config)
- [NvChad](https://github.com/NvChad/NvChad) (reference config)
