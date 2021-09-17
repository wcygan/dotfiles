# Guide to setting this up: 
# https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.1#how-to-create-a-profile

function pro {code $PROFILE}
function dev { Set-Location ~\Development }
function sem { Set-Location ~\School }
function will { Set-Location ~ }

# https://github.com/kelleyma49/PSFzf
# replace 'Ctrl+t' and 'Ctrl+r' with your preferred bindings:
Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+t' -PSReadlineChordReverseHistory 'Ctrl+r'

function prompt {
    "PS ~\$($executionContext.SessionState.Path.CurrentLocation | Split-Path -Leaf)$('> ' * ($nestedPromptLevel + 1))"
}

function .. {
    Set-Location ..
}

function ... {
    ..
    ..
}

function .... {
    ...
    ..
}

function Get-Git-Status {
    git status
}

function Get-Git-Log {
    git log
}

function Get-Git-Diff {
    git diff
}

function Set-Git-Commit {
    git commit $args
}
function Set-Git-Clone {
    git clone $args
}

function Set-Git-Pull-Rebase {
    git pull --rebase
}

function Set-Git-Add-All {
    git add .
}

function Set-Git-Push {
    git push
}


function Get-Cargo-Build {
    cargo build
}

function Get-Cargo-Test {
    cargo test
}

function Get-Cargo-Run {
    cargo run
}

function Get-Cargo-Check {
    cargo check
}


function Get-Go-Build {
    go build
}

function Get-Go-Test {
    go test
}

function Get-Go-Run {
    go run
}

function Get-Go-Clean {
    go clean
}

function Get-Go-Format {
    go fmt
}

function Get-Go-Install {
    go install
}

function Get-Go-Fix {
    go fix
}

function Get-Go-Doc {
    go doc
}


function Get-Go-Test-Bench {
    go test -bench="."
}

function Get-Go-Test-Cover {
    go test -cover
}

Set-Alias -Name l -Value "ls"
Set-Alias -Name c -Value "clear"
Set-Alias -Name gaa -Value Set-Git-Add-All
Set-Alias -Name gs -Value Get-Git-Status
Set-Alias -Name gitc -Value Set-Git-Commit
Set-Alias -Name glog -Value  Get-Git-Log
Set-Alias -Name gpu -Value  Set-Git-Push
Set-Alias -Name gd -Value  Get-Git-Diff
Set-Alias -Name gcl -Value Set-Git-Clone
Set-Alias -Name gpr -Value Set-Git-Pull-Rebase
Set-Alias -Name cgc -Value Get-Cargo-Check
Set-Alias -Name cgr -Value Get-Cargo-Run
Set-Alias -Name cgb -Value Get-Cargo-Build
Set-Alias -Name cgt -Value Get-Cargo-Test
Set-Alias -Name gob -Value Get-Go-Build
Set-Alias -Name got -Value Get-Go-Test
Set-Alias -Name gotb -Value Get-Go-Test-Bench
Set-Alias -Name gotc -Value Get-Go-Test-Cover
Set-Alias -Name gor -Value Get-Go-Run
Set-Alias -Name goc -Value Get-Go-Clean
Set-Alias -Name gof -Value Get-Go-Format
Set-Alias -Name goi -Value Get-Go-Install
Set-Alias -Name gofix -Value Get-Go-Fix
Set-Alias -Name god -Value Get-Go-Doc
