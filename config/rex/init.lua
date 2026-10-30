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

-- Reload the config
rex.bind("cmd+shift+r", "client.config.reload")
