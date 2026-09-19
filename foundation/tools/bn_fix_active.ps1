$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$ex   = Join-Path $prof 'extensions.json'
$id   = 'Knowledge4Zotero@windingwind.com'

$p = Get-Process zotero -ErrorAction SilentlyContinue
if ($p) { $p | Stop-Process -Force; Write-Output 'stopped zotero'; Start-Sleep -Seconds 5 } else { Write-Output 'was not running' }

Copy-Item $ex ($ex + '.bak3') -Force
Write-Output ('backup -> ' + $ex + '.bak3')

$j = Get-Content $ex -Raw | ConvertFrom-Json
$changed = $false
foreach ($a in $j.addons) {
    if ($a.id -eq $id) {
        Write-Output ('before: userDisabled=' + $a.userDisabled + ' seen=' + $a.seen)
        $a.userDisabled = $false
        $a.seen = $true
        $changed = $true
    }
}

if ($changed) {
    $json = $j | ConvertTo-Json -Depth 100 -Compress
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($ex, $json, $enc)
    Write-Output 'extensions.json rewritten (no BOM)'
} else {
    Write-Output 'addon not found, nothing changed'
}

Start-Process -FilePath 'D:\Zotero\zotero.exe'
Write-Output 'restarted zotero'
