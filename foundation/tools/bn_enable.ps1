$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$pf   = Join-Path $prof 'prefs.js'
$bak  = Join-Path $prof '_hana_backup'

New-Item -ItemType Directory -Force -Path $bak | Out-Null
Copy-Item $pf (Join-Path $bak 'prefs.js.bak2') -Force -ErrorAction SilentlyContinue
Write-Output ('backup -> ' + (Join-Path $bak 'prefs.js.bak2'))

$p = Get-Process zotero -ErrorAction SilentlyContinue
if ($p) { $p | Stop-Process -Force; Write-Output 'stopped zotero'; Start-Sleep -Seconds 5 } else { Write-Output 'was not running' }

$txt = Get-Content $pf -Raw
if ($txt -notmatch 'extensions\.autoDisableScopes') {
    Add-Content -Path $pf -Value 'user_pref("extensions.autoDisableScopes", 0);'
    Write-Output 'pref added: extensions.autoDisableScopes = 0'
} else {
    Write-Output 'pref already present, leaving as is'
}

Start-Process -FilePath 'D:\Zotero\zotero.exe'
Write-Output 'restarted zotero'
