# Will's Dotfiles

A comprehensive shell configuration setup with modular organization, supporting both bash and zsh across macOS, Linux, and Windows (PowerShell).

## 🚀 Quick Installation (Recommended)

### Option 1: Deno TypeScript Scripts (Modern)

The safest and most modern way to install these dotfiles using type-safe Deno scripts:

```bash
git clone https://github.com/wcygan/dotfiles.git && cd dotfiles
deno run --allow-all install-safely.ts
```

**Benefits:**
- ✅ Type-safe with comprehensive error handling
- ✅ Cross-platform compatibility (macOS, Linux, Windows)
- ✅ Modern async/await patterns
- ✅ Better user feedback and validation
- ✅ No shell script dependencies

### Option 2: Shell Scripts (Traditional)

If you prefer traditional shell scripts or don't have Deno installed:

```bash
git clone https://github.com/wcygan/dotfiles.git && cd dotfiles
./install-safely.sh
```

Both installation methods will:
- ✅ Auto-detect your shell (zsh/bash)
- ✅ Backup existing dotfiles with timestamp
- ✅ Install new dotfiles from repository
- ✅ Reload shell configuration
- ✅ Provide rollback instructions

## 🔄 Rollback Support

### Deno TypeScript Rollback
```bash
deno run --allow-all rollback.ts ~/.dotfiles-backup-20240525-102500
```

### Shell Script Rollback
```bash
./rollback.sh ~/.dotfiles-backup-20240525-102500
```

## 📋 What Gets Installed

### Core Shell Files
- `.zshrc` / `.bashrc` - Main shell configuration
- `.bash_profile` - Bash login shell settings
- `.aliases` - Command shortcuts and modern CLI tool replacements
- `.functions` - Useful shell functions
- `.exports` - Environment variables
- `.path` - PATH modifications
- `.extra` - Tool integrations (git, fzf, mise, etc.)

### Editor Configurations
- `.vimrc` - Vim editor configuration
- `cursor/` - Cursor IDE settings
- `zed/` - Zed editor settings  
- `vscode/` - VS Code settings

### Cross-Platform Support
- `profile.ps1` - PowerShell configuration for Windows
- Platform-specific adaptations in `.platform`

## ⚙️ Manual Installation

If you prefer manual control or need to troubleshoot:

### Clone the repo

```bash
git clone https://github.com/wcygan/dotfiles.git
cd dotfiles
```

### For Zsh (Recommended)

```bash
chmod +x bootstrap-zsh.sh
./bootstrap-zsh.sh
```

### For Bash

```bash
chmod +x bootstrap-bash.sh  
./bootstrap-bash.sh
```

### For Windows PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\bootstrap.ps1
```

## 🔧 Customization

### Adding Personal Configurations

Create a `.extra` file in your home directory for personal customizations:

```bash
# Git credentials
GIT_AUTHOR_NAME="Your Name"
GIT_AUTHOR_EMAIL="your.email@example.com"

# Custom aliases  
alias myproject="cd ~/path/to/project"

# API keys and secrets
export API_KEY="your-secret-key"
```

### Shell-Specific Additions

- **Zsh**: Add to `~/.zshrc.local`
- **Bash**: Add to `~/.bashrc.local`  
- **PowerShell**: Add to `$PROFILE.CurrentUserCurrentHost`

## 📦 Included Tools & Integrations

### Modern CLI Replacements
- `bat` instead of `cat` (syntax highlighting)
- `exa`/`eza` instead of `ls` (modern file listing)
- `fd` instead of `find` (faster file search)
- `rg` (ripgrep) for text search
- `fzf` for fuzzy finding

### Development Tools
- **Git**: Enhanced aliases and configuration
- **Docker**: Container management shortcuts
- **Kubernetes**: kubectl aliases and functions  
- **Language Tools**: Go, Rust, Java, Node.js, Python
- **Editors**: Cursor, Zed, VS Code, Vim

### System Integrations
- **mise**: Development environment manager
- **Homebrew**: Package management (macOS/Linux)
- **zsh-syntax-highlighting**: Command syntax highlighting
- **fzf**: Fuzzy file/command search

## 🧪 Testing Your Installation

After installation, test these common shortcuts:

```bash
# Modern CLI tools
ll          # Better ls with exa
cat file    # Syntax highlighted with bat  
find .      # Faster search with fd

# Development shortcuts
d           # Open development workspace in Cursor
k get nodes # kubectl shortcut
cgr         # cargo run
mm          # git main branch helper
dcr web     # docker-compose restart web

# SSH shortcuts (customize in .aliases)
m0          # SSH to main-0 host
k1          # SSH to k8s-1 host
```

## 🔄 Staying Updated

### Automatic Updates
The installation scripts automatically update the repository during installation.

### Manual Updates
```bash
cd ~/dotfiles  # or wherever you cloned
git pull origin main
./install-safely.sh --force  # or use Deno version
```

## 🛠️ Prerequisites

### For Shell Scripts
- Bash or Zsh shell
- Git
- Basic Unix tools (cp, mkdir, etc.)

### For Deno Scripts
- [Deno](https://deno.land) runtime installed
- Git
- Compatible with any shell (zsh, bash, fish, etc.)

### Optional Enhancements
- [Homebrew](https://brew.sh) (macOS/Linux)
- [bat](https://github.com/sharkdp/bat): `brew install bat`
- [exa](https://github.com/ogham/exa): `brew install exa`  
- [fd](https://github.com/sharkdp/fd): `brew install fd`
- [fzf](https://github.com/junegunn/fzf): `brew install fzf`
- [mise](https://github.com/jdx/mise): Development environment manager

## 🚨 Emergency Restore

If something goes wrong:

1. **Find your backup**: `ls ~/.dotfiles-backup-*`
2. **Restore with Deno**: `deno run --allow-all rollback.ts <backup-dir>`
3. **Or restore with shell**: `./rollback.sh <backup-dir>`
4. **Manual restore**: `cp ~/.dotfiles-backup-*/.[a-z]* ~/`

## 🎯 Project Goals

- **Modular**: Each configuration aspect in separate files
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Modern**: Embraces new tools while maintaining compatibility
- **Safe**: Always backup before changes
- **Maintainable**: Clear organization and documentation
- **Type-Safe**: Deno TypeScript scripts for reliability

## 📄 License

MIT License - feel free to fork and customize for your own use!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

---

*These dotfiles represent years of shell customization and modern development tool integration. They're designed to provide a powerful, consistent development environment across all platforms.*