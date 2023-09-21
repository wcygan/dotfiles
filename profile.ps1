# Place this file into `C:\Users\Will\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
# Or create the file with `New-Item -path $profile -type file -force`

function Switch-To-Dev {
    cd 'C:\Users\Will\Development'
}

Set-Alias -Name dev -Value Switch-To-Dev

function Clear {
    clear
}

Set-Alias -Name c -Value Clear

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