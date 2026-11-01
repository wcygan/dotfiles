# Rex command palette actions

The Rex configuration lives in [`init.lua`](init.lua). The dotfiles setup links
this directory to `~/.config/rex`, so edit the repository copy. After an edit,
validate and reload it on the machine running the Rex server:

```sh
rex config check config/rex/init.lua
rex config reload
rex actions --json
```

Rex calls a tab a **window** and a pane a **block**. Custom actions defined
with `rex.action` appear in the command palette. The [Rex custom-action
docs](https://www.superlogical.com/rex/docs/customize/actions) describe the
Lua API and action context.

## What Open Pi does today

**Open Pi** writes `pi` and Return into the currently focused terminal block.
It does not create a tab or pane, change directories, or choose a machine. Pi
starts wherever that terminal's shell is currently located, on the machine
running that terminal. Run it from an idle shell prompt; otherwise the terminal's
foreground program may receive the text.

In Rex's action context, `ctx.block_id` is usually the focused block. The action
uses the terminal block's `write` method to type the command there. See the
[Rex Lua API reference](https://www.superlogical.com/rex/docs/reference/lua).

## Project actions for the Foobar laptop

The command palette has three project-specific actions:

| Title | Directory |
| --- | --- |
| Anton | `~/Development/anton` |
| Agent Skills | `~/Development/agent-skills` |
| Dotfiles | `~/Development/dotfiles` |

Each action checks that its Rex server reports hostname `foobar2` and that the
project directory exists. It creates a new tab in the current session, starts
Pi in that directory, and asks the client that ran the action to show the new
tab. It does not send input to an existing terminal. On another server it
reports an error. Client selection depends on the Rex app accepting the
`session.select` action; verify this on the phone.

## Adding another project action

Create a separate action for each project and machine combination. Before
adding one, record:

| Detail | Example |
| --- | --- |
| Palette title | Open Pi — Website |
| Target machine | Betty or Foobar laptop |
| Rex server label | The label the action will target |
| Working directory | Absolute project path on that machine |
| Launch behavior | Current terminal, new pane, or new tab |

A fixed working directory requires starting a terminal with its `cwd` set (or
otherwise changing directory in a shell known to be idle). A fixed machine
requires an explicit host route; relying on the currently focused terminal
means the action follows whichever machine owns that block.

Rex Lua can declare another server with `rex.host{...}` and route API calls to
it with `rex.server(label)`. Those remote calls need explicit session and block
IDs. Creating a remote session is distinct from showing it in the phone app, so
verify the complete flow on the target client before relying on it. See the
[Lua API reference](https://www.superlogical.com/rex/docs/reference/lua#hosts-and-other-servers)
and [CLI target documentation](https://www.superlogical.com/rex/docs/automate/cli#command-targets).

## Check machine and host labels

Use these read-only commands on each computer before adding a pinned action:

```sh
rex whoami --json
rex hosts --json
rex client ls --json
```

At the last check, the local server identified as `foobar2-rex` (the Mac app
client label was `foobar2`), and the CLI had a reachable remote host alias
`betty`. Confirm these labels on each machine: Rex's saved `rex hosts` entries
are CLI-local and do not sync to the GUI app or other computers. See the [Rex
remote-access docs](https://www.superlogical.com/rex/docs/linux/remote-access#adding-the-server-to-a-client).

The `foobar2` check is based on the laptop's current `hostname -s`; update the
check if the laptop is renamed. These actions check the Rex server host, not a
Rex CLI host alias.
