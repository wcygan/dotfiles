# Guide to setting this up: 
# https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.1#how-to-create-a-profile

Set-Location C:\Users\Will

function pro {code $PROFILE}

function dev { Set-Location C:\Users\Will\Development }

function sem { Set-Location C:\Users\Will\School }
function will { Set-Location C:\Users\Will }

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
