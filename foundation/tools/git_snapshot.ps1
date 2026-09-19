# git_snapshot.ps1 - commit every agent change, write a human-readable digest, then push.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File git_snapshot.ps1 -MessageFile <path>
#   powershell ... -File git_snapshot.ps1 -Message "ascii only - prefer -MessageFile for Chinese"
#
# Steps: stage -> write digest entry -> commit -> push to origin (if configured).
# A push failure is reported but never silently swallowed, and never blocks the commit.
param(
  [string]$Message = "",
  [string]$MessageFile = "",
  [string]$Repo = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace",
  [string]$Digest = "foundation\changelog\auto-changes.md",
  [switch]$NoPush
)

$ErrorActionPreference = "Continue"

if (-not (Test-Path (Join-Path $Repo ".git"))) { Write-Output "not a git repo: $Repo"; exit 1 }

if ($MessageFile) {
  if (-not (Test-Path $MessageFile)) { Write-Output "message file not found: $MessageFile"; exit 1 }
  $Message = [System.IO.File]::ReadAllText($MessageFile, [System.Text.Encoding]::UTF8).Trim()
}
if (-not $Message) { $Message = "snapshot: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") }

git -C $Repo add -A 2>$null | Out-Null
$stagedFiles = @(git -C $Repo diff --cached --name-only)
if ($stagedFiles.Count -eq 0) { Write-Output "no changes to commit"; exit 0 }

# ---------------------------------------------------------------- digest
$digestPath = Join-Path $Repo $Digest
$digestDir = Split-Path $digestPath -Parent
if (-not (Test-Path $digestDir)) { New-Item -ItemType Directory -Force -Path $digestDir | Out-Null }

$stat = @(git -C $Repo diff --cached --shortstat)
$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("")
$lines.Add("## " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
$lines.Add("")
$lines.Add("**说明**：" + $Message)
$lines.Add("")
$lines.Add("**变更规模**：" + ($(if ($stat.Count -gt 0) { $stat[0].Trim() } else { "(无统计)" })))
$lines.Add("")
$lines.Add("**文件清单**：")
foreach ($f in ($stagedFiles | Select-Object -First 40)) { $lines.Add("- ``" + $f + "``") }
if ($stagedFiles.Count -gt 40) { $lines.Add("- …共 " + $stagedFiles.Count + " 个文件") }
$lines.Add("")

$existing = ""
if (Test-Path $digestPath) { $existing = [System.IO.File]::ReadAllText($digestPath, [System.Text.Encoding]::UTF8) }
if (-not $existing.Trim()) {
  $existing = "# 变更自动记录（每次 agent 改动写入）`n`n> 由 foundation/tools/git_snapshot.ps1 自动追加；新条目在文件末尾。`n"
}
$all = $existing.TrimEnd() + "`n" + ($lines -join "`n")
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($digestPath, $all, $utf8NoBom)

git -C $Repo add -A 2>$null | Out-Null

# ---------------------------------------------------------------- commit
$msgFile = Join-Path $env:TEMP ("gitmsg_" + [guid]::NewGuid().ToString("N") + ".txt")
[System.IO.File]::WriteAllText($msgFile, $Message, $utf8NoBom)
git -C $Repo commit -q -F $msgFile
Remove-Item $msgFile -Force -ErrorAction SilentlyContinue
$sha = (git -C $Repo rev-parse --short HEAD)

$stats = @(git -C $Repo show --stat --oneline HEAD | Select-Object -Skip 1 | Select-Object -First 20)
Write-Output ("committed " + $sha + " | files changed: " + $stagedFiles.Count)
$stats

# ---------------------------------------------------------------- push
if ($NoPush) { Write-Output "push skipped (-NoPush)"; exit 0 }
$remote = (git -C $Repo remote) -join ","
if (-not $remote) {
  Write-Output "PUSH SKIPPED: no remote configured (git remote add origin <url>; see foundation/tools/git_remote_setup.md)"
  exit 0
}
$branch = (git -C $Repo rev-parse --abbrev-ref HEAD)
$push = git -C $Repo push -u origin $branch 2>&1
if ($LASTEXITCODE -eq 0) { Write-Output ("pushed " + $sha + " -> origin/" + $branch) }
else {
  Write-Output "PUSH FAILED (commit is safe locally):"
  $push | Select-Object -Last 6
  exit 2
}
