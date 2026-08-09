#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DETERMINATE_PKG_URL="https://install.determinate.systems/determinate-pkg/stable/Universal"
DETERMINATE_INSTALL_URL="https://install.determinate.systems/nix"

install_nix=false
assume_yes=false
forwarded_args=()

while (($#)); do
  case "$1" in
    --install-nix) install_nix=true ;;
    --yes) assume_yes=true ;;
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

if [[ "${DOTFILES_BOOTSTRAP_SKIP_PROFILE:-0}" != 1 ]]; then
  source_nix_profile
fi

if ! command -v nix >/dev/null 2>&1; then
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
      if [[ "${DOTFILES_BOOTSTRAP_SKIP_PROFILE:-0}" != 1 ]]; then
        source_nix_profile
      fi
      ;;
    *)
      echo "Unsupported operating system: $(uname -s)" >&2
      exit 2
      ;;
  esac
fi

if ! command -v nix >/dev/null 2>&1; then
  echo "Nix installation completed, but nix is not available in this shell." >&2
  echo "Restart the shell and rerun ./bootstrap.sh." >&2
  exit 1
fi

if ((${#forwarded_args[@]} == 0)); then
  forwarded_args=(install)
fi

cd "$REPO_ROOT"
unset VIRTUAL_ENV
exec nix \
  --extra-experimental-features "nix-command flakes" \
  develop --no-write-lock-file .#default \
  --command uv run --locked python -m dotfiles_setup "${forwarded_args[@]}"
