$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$ex   = Join-Path $prof 'extensions.json'
$pf   = Join-Path $prof 'prefs.js'

$p = Get-Process zotero -ErrorAction SilentlyContinue
if ($p) { $p | Stop-Process -Force; Write-Output 'stopped zotero'; Start-Sleep -Seconds 5 } else { Write-Output 'was not running' }

# 1) restore addon record so Zotero lists the plugin (disabled) and user can enable it
if (Test-Path ($ex + '.bak3')) {
    Copy-Item ($ex + '.bak3') $ex -Force
    Write-Output 'extensions.json restored from bak3'
} else {
    Write-Output 'WARN: bak3 missing'
}

# 2) remove the autoDisableScopes pref I inserted
$lines = Get-Content $pf
$kept = @()
$removed = 0
foreach ($l in $lines) {
    if ($l -match 'extensions\.autoDisableScopes') { $removed++ } else { $kept += $l }
}
if ($removed -gt 0) {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($pf, (($kept -join "`r`n") + "`r`n"), $enc)
    Write-Output ('removed ' + $removed + ' pref line(s) from prefs.js')
} else {
    Write-Output 'no autoDisableScopes pref found in prefs.js'
}

Start-Process -FilePath 'D:\Zotero\zotero.exe'
Write-Output 'restarted zotero'
