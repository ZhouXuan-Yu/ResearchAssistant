# snapshot-configs.ps1
# Purpose: snapshot key Hana configs into the workspace for rollback (F1).
# Security: explicitly EXCLUDES any file that may contain credentials.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File snapshot-configs.ps1
# NOTE: ASCII-only on purpose (PowerShell 5.1 mis-parses UTF-8-no-BOM Chinese comments).

$ErrorActionPreference = 'Stop'

$hana = 'C:\Users\ZhouXuan\.hanako'
$root = 'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\backup'
$ts   = (Get-Date).ToString('yyyyMMdd-HHmmss')
$dst  = Join-Path $root ('snapshots\' + $ts)
New-Item -ItemType Directory -Force -Path $dst | Out-Null

# Allowlist: config files with no credentials.
$files = @()
$files += (Join-Path $hana 'agents\agent-mu42qzfz\config.yaml')
$files += (Join-Path $hana 'user\preferences.json')
$files += (Join-Path $hana 'models.json')
$files += (Join-Path $hana 'provider-catalog.json')
$files += (Join-Path $hana 'server-network.json')
$files += (Join-Path $hana 'agents\agent-mu42qzfz\pinned.md')
$files += (Join-Path $hana 'agents\agent-mu42qzfz\pinned-memory.json')

$copied = @()
foreach ($f in $files) {
  $name = [IO.Path]::GetFileName($f)
  if (Test-Path $f) {
    Copy-Item $f (Join-Path $dst $name) -Force
    $copied += $name
  } else {
    $copied += ('MISSING:' + $name)
  }
}

# Explicit exclude list, written into the snapshot so future readers are not misled.
$excluded = @('server-info.json','auth.json','device-credentials.json','security\*','session-manifest.db','*.db-wal','*.db-shm')

$manifest = [ordered]@{
  snapshotAt = (Get-Date).ToString('s')
  hanaHome   = $hana
  included   = $copied
  excluded   = $excluded
  note       = 'Excluded files may contain credentials; never snapshot them into the workspace.'
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $dst 'MANIFEST.json') -Encoding UTF8

# Keep the latest 30 snapshots only.
$snaps = Get-ChildItem (Join-Path $root 'snapshots') -Directory | Sort-Object Name -Descending
if ($snaps.Count -gt 30) { $snaps | Select-Object -Skip 30 | Remove-Item -Recurse -Force }

Write-Output ('SNAPSHOT_OK ' + $dst)
Write-Output ($copied -join ', ')
