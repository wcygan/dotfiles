-- Treesitter configuration (syntax highlighting)

return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  event = { "BufReadPost", "BufNewFile" },
  config = function()
    require("nvim-treesitter.configs").setup({
      ensure_installed = { "lua", "vim", "vimdoc", "query", "rust", "go", "python", "typescript", "javascript" },
      highlight = { enable = true },
      indent = { enable = true },
    })
  end,
}
