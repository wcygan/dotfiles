#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DETERMINATE_PKG_URL="https://install.determinate.systems/determinate-pkg/stable/Universal"
DETERMINATE_INSTALL_URL="https://install.determinate.systems/nix"

# This script establishes the Nix boundary. Python owns the setup workflow.
install_nix=false
assume_yes=false
run_command=false
forwarded_args=()

parse_bootstrap_arguments() {
  while (($#)); do
    case "$1" in
      --install-nix) install_nix=true ;;
      --yes) assume_yes=true ;;
      # Run the remaining arguments as a command inside the dev environment.
      --run)
        run_command=true
        shift
        forwarded_args+=("$@")
        break
        ;;
      --)
        shift
        forwarded_args+=("$@")
        break
        ;;
      *)
        forwarded_args+=("$@")
        break
        ;;
    esac
    shift
  done
}

source_nix_profile() {
  local profile
  for profile in \
    /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh \
    /etc/profile.d/nix.sh \
    "$HOME/.nix-profile/etc/profile.d/nix.sh"; do
    if [[ -f "$profile" ]]; then
      # shellcheck disable=SC1090
      source "$profile"
      break
    fi
  done
}

load_nix_profile() {
  if [[ "${DOTFILES_BOOTSTRAP_SKIP_PROFILE:-0}" != 1 ]]; then
    source_nix_profile
  fi
}

install_nix_for_current_platform() {
  case "$(uname -s)" in
    Darwin)
      echo "Nix is required. Opening the recommended Determinate macOS installer."
      if command -v open >/dev/null 2>&1; then
        open "$DETERMINATE_PKG_URL"
      else
        echo "$DETERMINATE_PKG_URL"
      fi
      echo "After installation completes, rerun ./bootstrap.sh."
      exit 2
      ;;
    Linux)
      if [[ "$install_nix" != true || "$assume_yes" != true ]]; then
        echo "Nix is required. To run the official Determinate installer, use:"
        echo "  ./bootstrap.sh --install-nix --yes"
        exit 2
      fi
      command -v curl >/dev/null 2>&1 || {
        echo "curl is required to install Nix." >&2
        exit 1
      }
      curl --proto '=https' --tlsv1.2 -sSf -L "$DETERMINATE_INSTALL_URL" | sh -s -- install
      load_nix_profile
      ;;
    *)
      echo "Unsupported operating system: $(uname -s)" >&2
      exit 2
      ;;
  esac
}

ensure_nix_available() {
  if ! command -v nix >/dev/null 2>&1; then
    install_nix_for_current_platform
  fi

  if ! command -v nix >/dev/null 2>&1; then
    echo "Nix installation completed, but nix is not available in this shell." >&2
    echo "Restart the shell and rerun ./bootstrap.sh." >&2
    exit 1
  fi
}

# Print the path of a reusable copy of the dev shell environment, or fail.
#
# `nix develop` spends seconds per entry even when nothing changed. The
# environment depends only on flake.nix and flake.lock, so one saved copy per
# content of those files is reused. Its Nix profile keeps the store paths alive.
cached_dev_environment() {
  [[ "${DOTFILES_BOOTSTRAP_DEV_CACHE:-1}" == 1 ]] || return 1
  local root key directory
  root="${XDG_CACHE_HOME:-$HOME/.cache}/dotfiles/dev-env"
  key="$({ printf '%s\n' "$REPO_ROOT"; cksum flake.nix flake.lock; } | cksum)" || return 1
  directory="$root/${key%% *}"
  if [[ ! -f "$directory/env.rc" || ! -e "$directory/profile" ]]; then
    rm -rf "$root"
    mkdir -p "$directory" || return 1
    nix --extra-experimental-features "nix-command flakes" \
      print-dev-env --no-write-lock-file --profile "$directory/profile" .#default \
      >"$directory/env.rc.$$" || return 1
    mv "$directory/env.rc.$$" "$directory/env.rc" || return 1
  fi
  printf '%s\n' "$directory/env.rc"
}

# Replace this process with a command running inside the dev environment.
exec_in_dev_environment() {
  cd "$REPO_ROOT"
  unset VIRTUAL_ENV

  local environment dev_bash
  if environment="$(cached_dev_environment)"; then
    # The saved environment needs the Bash it was built for; macOS Bash 3.2
    # cannot parse it.
    dev_bash="$(sed -n "s/^BASH='\(.*\)'\$/\1/p" "$environment" | head -n 1)"
    if [[ -x "$dev_bash" ]]; then
      # Sourcing points the temporary directory at a build directory that
      # only `nix develop` creates, so keep the caller's.
      exec "$dev_bash" -c '
        environment=$1; shift
        restore=$(declare -p TMPDIR TMP TEMP TEMPDIR NIX_BUILD_TOP 2>/dev/null || true)
        source "$environment"
        unset TMPDIR TMP TEMP TEMPDIR NIX_BUILD_TOP
        eval "$restore"
        exec "$@"
      ' bash "$environment" "$@"
    fi
  fi

  exec nix \
    --extra-experimental-features "nix-command flakes" \
    develop --no-write-lock-file .#default \
    --command "$@"
}

run_dotfiles_setup() {
  if ((${#forwarded_args[@]} == 0)); then
    forwarded_args=(install)
  fi

  # Install reports the time spent before Python starts. Bash 5 gives a
  # sub-second clock; older Bash, such as macOS 3.2, gives whole seconds.
  export DOTFILES_BOOTSTRAP_STARTED_AT="${EPOCHREALTIME:-$(date +%s)}"
  exec_in_dev_environment uv run --locked python -m dotfiles_setup "${forwarded_args[@]}"
}

main() {
  parse_bootstrap_arguments "$@"
  if [[ "${forwarded_args[0]:-}" == nightly-run || "${forwarded_args[0]:-}" == nightly-probe ]]; then
    cd "$REPO_ROOT"
    export PYTHONPATH="$REPO_ROOT/src"
    exec "$HOME/.nix-profile/bin/python3" -m dotfiles_setup "${forwarded_args[@]}"
  fi
  load_nix_profile
  ensure_nix_available
  if [[ "$run_command" == true ]]; then
    if ((${#forwarded_args[@]} == 0)); then
      echo "--run needs a command." >&2
      exit 2
    fi
    exec_in_dev_environment "${forwarded_args[@]}"
  fi
  run_dotfiles_setup
}

main "$@"
