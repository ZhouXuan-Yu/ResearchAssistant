$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$ex   = Join-Path $prof 'extensions.json'
$id   = 'Knowledge4Zotero@windingwind.com'

$p = Get-Process zotero -ErrorAction SilentlyContinue
if ($p) { $p | Stop-Process -Force; Write-Output 'stopped zotero'; Start-Sleep -Seconds 5 } else { Write-Output 'was not running' }

Copy-Item $ex ($ex + '.bak4') -Force

$j = Get-Content $ex -Raw | ConvertFrom-Json
$keep = @()
foreach ($a in $j.addons) {
    if ($a.id -ne $id) { $keep += $a } else { Write-Output ('dropping record: ' + $a.id) }
}
$j.addons = $keep
Write-Output ('remaining addons = ' + $keep.Count)

$json = $j | ConvertTo-Json -Depth 100 -Compress
$enc = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($ex, $json, $enc)
Write-Output 'extensions.json rewritten'

Start-Process -FilePath 'D:\Zotero\zotero.exe'
Write-Output 'restarted zotero'
