-- Configurazione locale Neovim per questo progetto
-- Viene caricata automaticamente se hai `vim.o.exrc = true` nel tuo init.lua

-- Punta il venv locale per Mason/LSP (pyright, ruff-lsp, ecc.)
vim.env.VIRTUAL_ENV = vim.fn.getcwd() .. "/.venv"
vim.env.PATH = vim.fn.getcwd() .. "/.venv/bin:" .. vim.env.PATH

-- Opzionale: messaggio di conferma
vim.notify("🐍 venv locale caricato: .venv", vim.log.levels.INFO)
