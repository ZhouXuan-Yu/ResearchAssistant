# git_snapshot.ps1 - commit every change the agent makes, with a readable summary.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File git_snapshot.ps1 -Message "fix: ..."
#   powershell ... -File git_snapshot.ps1 -MessageFile C:\path\msg.txt   # safer for Chinese/long text
#
# Behaviour: stage everything, commit only when something actually changed, print a summary.
# Never commits nothing; never rewrites history.
param(
  [string]$Message = "",
  [string]$MessageFile = "",
  [string]$Repo = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace"
)

$ErrorActionPreference = "Continue"

if (-not (Test-Path (Join-Path $Repo ".git"))) {
  Write-Output "not a git repo: $Repo"
  exit 1
}

if ($MessageFile) {
  if (-not (Test-Path $MessageFile)) { Write-Output "message file not found: $MessageFile"; exit 1 }
  # read as UTF-8 explicitly: Get-Content defaults to the ANSI codepage in PS 5.1
  # and would double-encode a Chinese message (this bug shipped once, see 15b116f).
  $Message = [System.IO.File]::ReadAllText($MessageFile, [System.Text.Encoding]::UTF8).Trim()
}
if (-not $Message) {
  $Message = "snapshot: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
}

git -C $Repo add -A 2>$null | Out-Null
$staged = (git -C $Repo diff --cached --name-only | Measure-Object).Count
if ($staged -eq 0) {
  Write-Output "no changes to commit"
  exit 0
}

$msgFile = Join-Path $env:TEMP ("gitmsg_" + [guid]::NewGuid().ToString("N") + ".txt")
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($msgFile, $Message, $utf8NoBom)
git -C $Repo commit -q -F $msgFile
Remove-Item $msgFile -Force -ErrorAction SilentlyContinue

$sha = (git -C $Repo rev-parse --short HEAD)
$stat = git -C $Repo show --stat --oneline HEAD | Select-Object -Skip 1
Write-Output ("committed " + $sha + " | files changed: " + $staged)
$stat | Select-Object -First 25
