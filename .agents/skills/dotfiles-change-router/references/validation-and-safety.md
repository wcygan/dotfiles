# Validation and Safety

## Validation ladder

Run the narrowest relevant check, then broaden according to the change:

1. `make test-pre` is the normal local preflight.
2. Fish changes also require `make test-local` on macOS.
3. Run the Docker matrix when it is available and appropriate.
4. Linux CI supplies Ubuntu and Fedora coverage; macOS-sensitive behavior must
   be checked locally on a Mac.
5. A Nix package-set update uses `make update`, then `make test-pre` and
   `make test-local`.
6. A global Codex skill uses `./tests/test-codex-skills.sh`, then
   `make test-pre`.

## Breaking changes

A breaking behavior change requires:

- a migration note in `AGENTS.md`; and
- a corresponding update under `tests/`.

## Linking and rollback

- Linking operations must be safe to run twice.
- Back up a physical file or directory before replacing it with a symlink.
- Retain an obvious restore or re-link path.
- Never use destructive Git recovery as a rollback mechanism.

## Pi state boundary

Pi discovers shared global skills directly from `~/.agents/skills`; do not
create a duplicate `~/.pi/agent/skills` link. Keep `auth.json`, sessions,
models, logs, caches, and other machine-local runtime state outside the
repository.
