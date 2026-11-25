"""Validate the editable config files whose formats have a pinned checker."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def check_kind(path):
    if path == "config/starship.toml":
        return "starship"
    if path == "config/bunfig.toml":
        return "toml"
    if path == "config/git/config":
        return "git"
    if path.startswith(("config/zed/", "config/vscode/")) and path.endswith(".json"):
        return "jsonc"
    if path.startswith(("config/nvim/", "config/rex/")) and path.endswith(".lua"):
        return "lua"
    if path == "config/nvim/lazy-lock.json":
        return "json"
    return None


def validate(path):
    import tomllib

    kind = check_kind(str(path))
    if kind == "starship":
        command = ["bash", ".agents/skills/starship-config/scripts/test-config.sh", str(path)]
    elif kind == "toml":
        with path.open("rb") as stream:
            tomllib.load(stream)
        return
    elif kind == "json":
        json.loads(path.read_text())
        return
    elif kind == "jsonc":
        import rapidjson

        with path.open() as stream:
            rapidjson.load(
                stream,
                allow_nan=False,
                number_mode=rapidjson.NM_NATIVE,
                parse_mode=rapidjson.PM_COMMENTS | rapidjson.PM_TRAILING_COMMAS,
            )
        return
    elif kind == "lua":
        # Compile the file without launching a plugin manager or contacting a server.
        command = ["nvim", "--clean", "--headless", "-l", "-", str(path)]
        subprocess.run(command, input="assert(loadfile(arg[1]))", text=True, check=True)
        return
    elif kind == "git":
        command = ["git", "config", "--no-includes", "--file", str(path), "--list"]
    else:
        raise ValueError(f"No checker for {path}")
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def selected_paths(reasons):
    if all(check_kind(path) and Path(path).is_file() for path in reasons):
        return reasons
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--selection", type=Path)
    args = parser.parse_args()
    if args.selection:
        args.paths = selected_paths(json.loads(args.selection.read_text()))
    paths = args.paths or [
        os.fsdecode(p)
        for p in subprocess.check_output(["git", "ls-files", "-z", "config"]).split(b"\0")
        if p and check_kind(os.fsdecode(p))
    ]
    for path in paths:
        validate(Path(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
