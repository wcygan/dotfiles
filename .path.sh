export PATH="/usr/local/bin:$PATH"

# Go tools
export PATH=$PATH:$(go env GOPATH)/bin

# Homebrew tools
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"

# Kubernetes tools
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"

# Development tools
export PATH="$HOME/.jbang/bin:$PATH"
export PATH="$HOME/.deno/bin:$PATH"

# Rancher Desktop (managed section)
### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
export PATH="/Users/wcygan/.rd/bin:$PATH"
### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)

# pnpm
export PNPM_HOME="/Users/wcygan/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac

echo "path loaded"