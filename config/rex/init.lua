-- Rex configuration: https://www.superlogical.com/rex/docs/customize/config
-- Validate with `rex config check`, then apply with `rex config reload`.
-- Rex does not watch this file.

-- Shortcuts carried over from config/ghostty/config so muscle memory survives
-- the switch. Action names come from `rex -C <client> actions`.

-- Add / delete terminal tabs
rex.bind("cmd+shift+t", "client.tab.new")
rex.bind("cmd+shift+w", "pane.close")

-- Switch between terminal tabs
rex.bind("cmd+alt+right", "client.tab.next")
rex.bind("cmd+alt+left", "client.tab.previous")

-- Switch between machines
rex.bind("cmd+shift+h", "client.host.switch")

-- Reload the config
rex.bind("cmd+shift+r", "client.config.reload")

-- Project workspaces -------------------------------------------------------
-- Each action opens (or returns to) one session per project on the server
-- that reads this file. See the rex-workflow skill for the conventions.

local shell = "com.superlogical.terminal.shell"
local home = os.getenv("HOME") or ""

local function first_dir(paths)
  for _, path in ipairs(paths) do
    local r = rex.exec({ "test", "-d", path })
    if r and r.ok then
      return path
    end
  end
end

-- Show a session on the app that ran the action; scripts may have no app.
local function show(session_id)
  pcall(rex.client.queue, "session.select", { session_id = session_id })
end

local function find_session(label)
  local result = rex.call("session.list")
  for _, session in ipairs((result and result.sessions) or {}) do
    if session.label == label then
      return session.session_id
    end
  end
end

-- Open Blog Workspace: one tab with the agent, Vite on the tailnet so
-- other devices can open the site, and a shell for checks.
rex.action{
  name = "blog_workspace",
  title = "Open Blog Workspace",
  description = "wcygan.net: agent, dev server on the tailnet, and checks in one tab",
  run = function(ctx, args)
    local label = "wcygan-net"
    local existing = find_session(label)
    if existing then
      show(existing)
      return { session_id = existing, created = false }
    end

    local repo = first_dir({ home .. "/Software/wcygan.net", home .. "/Development/wcygan.net" })
    if not repo then
      error("wcygan.net checkout not found under ~/Software or ~/Development")
    end

    -- Bind Vite to this machine's Tailscale address when Tailscale is
    -- available; Vite rejects hostnames it does not know, so open it by IP.
    local dev = "ts=/Applications/Tailscale.app/Contents/MacOS/Tailscale; "
      .. "host=$([ -x \"$ts\" ] && \"$ts\" ip -4 2>/dev/null | head -1); "
      .. "export HOST=${host:-localhost} PORT=3000; "
      .. "echo \"Blog dev server: http://$HOST:$PORT\"; exec bun run dev-vite"

    local function term(label, options)
      options.cwd = repo
      return rex.layout.block{ flavor = shell, label = label, options = options }
    end

    -- One tab: the agent on the left, the dev server above checks on the right.
    local created, err = rex.call("session.create", {
      label = label,
      initial_windows = {
        { window_label = "blog", layout = rex.layout.horizontal(0.6,
            -- Typed into the shell so quitting the agent leaves a shell.
            term("agent", { initial_input = "codex -m gpt-6-luna\n" }),
            rex.layout.vertical(0.6,
              term("dev", {
                command = { "/bin/zsh", "-lc", dev },
                shell = "none",
                exit = { on_completion = false },
              }),
              term("checks", {}))) },
      },
    })
    if not created then
      error("could not create " .. label .. ": " .. tostring(err))
    end
    show(created.session_id)
    return { session_id = created.session_id, created = true }
  end,
}
rex.bind("cmd+shift+b", "blog_workspace")

rex.action{
  name = "open_pi",
  title = "Open Pi",
  description = "Start Pi in the focused terminal pane",
  category = "Agents",
  keywords = "pi coding agent terminal",
  run = function(ctx, args)
    if not ctx.block_id then
      error("Open Pi needs a focused terminal pane", 0)
    end

    local _, err = rex.block.call("com.superlogical.terminal", "write", {
      block_id = ctx.block_id,
      data = "pi\n",
    })
    if err then
      error(err, 0)
    end
  end,
}

local function open_pi_project(name, title, folder)
  local directory = home .. "/Development/" .. folder

  rex.action{
    name = name,
    title = title,
    description = "Start Pi in ~/Development/" .. folder .. " on the Foobar laptop",
    category = "Agents",
    keywords = "pi coding agent " .. folder,
    run = function(ctx, args)
      if not ctx.session_id then
        error(title .. " needs an active Rex session", 0)
      end

      local host, host_err = rex.exec({ "hostname", "-s" })
      if not host or not host.ok then
        error("could not identify the Rex host: " .. tostring(host_err), 0)
      end
      if host.stdout:match("^%s*(.-)%s*$") ~= "foobar2" then
        error(title .. " is only available on the Foobar laptop (foobar2)", 0)
      end

      local exists = rex.exec({ "test", "-d", directory })
      if not exists or not exists.ok then
        error("project folder is missing on Foobar laptop: " .. directory, 0)
      end

      local window, err = rex.session.new_window{
        window_label = title,
        focus = false,
        layout = rex.layout.block{
          flavor = shell,
          label = title,
          options = { cwd = directory, initial_input = "pi\n" },
        },
      }
      if not window then
        error(err, 0)
      end
      rex.client.queue("session.select", {
        session_id = ctx.session_id,
        window_id = window.window_id,
      })
      return { window_id = window.window_id, block_ids = window.block_ids }

    end,
  }
end

open_pi_project("open_anton", "Anton", "anton")
open_pi_project("open_agent_skills", "Agent Skills", "agent-skills")
open_pi_project("open_dotfiles", "Dotfiles", "dotfiles")
