# Place this file into `C:\Users\Will\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
# Or create the file with `New-Item -path $profile -type file -force`

# Copy profile.ps1 to Microsoft.PowerShell_profile.ps1 so that it is loaded on startup
function Copy-Profile {
    copy profile.ps1 C:\Users\Will\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
    Write-Output "Profile copied!"
}

Set-Alias -Name cpro -Value Copy-Profile

# Reload the profile after making changes to the development environment
function Reload-Profile {
    . $PROFILE
    Write-Output "Profile reloaded!"
}

Set-Alias -Name rl -Value Reload-Profile

# Switch to the development directory
function Switch-To-Dev {
    cd 'C:\Users\Will\Development'
}

Set-Alias -Name dev -Value Switch-To-Dev

# Clear the screen
function Clear {
    clear
}

Set-Alias -Name c -Value Clear

function Docker-Compose-Up {
    docker-compose up -d
}

Set-Alias -Name dcu -Value Docker-Compose-Up

function Docker-Compose-Down {
    docker-compose down
}

Set-Alias -Name dcd -Value Docker-Compose-Down

function Docker-Compose-Build {
    docker-compose build
}

Set-Alias -Name dcb -Value Docker-Compose-Build

function Cargo-Check {
    cargo check
}

Set-Alias -Name cgc -Value Cargo-Check

function Cargo-Run {
    cargo run
}

Set-Alias -Name cgr -Value Cargo-Run

function Cargo-Test {
    cargo test
}

Set-Alias -Name cgt -Value Cargo-Test

function Cargo-Build {
    cargo build
}

Set-Alias -Name cgb -Value Cargo-Build

function Cargo-Clippy {
    cargo clippy
}

Set-Alias -Name ccl -Value Cargo-Clippy

function Git-Status {
    git status
}

Set-Alias -Name gs -Value Git-Status

function Git-Add {
    git add .
}

Set-Alias -Name gaa -Value Git-Add

function Git-Commit {
    git commit
}

Set-Alias -Name gitc -Value Git-Commit

function Git-Branch {
    git branch
}

Set-Alias -Name gb -Value Git-Branch

function Git-Push {
    git push
}

Set-Alias -Name gpu -Value Git-Push
