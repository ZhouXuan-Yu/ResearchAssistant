$ErrorActionPreference = 'Continue'
$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$ext  = Join-Path $prof 'extensions'
$id   = 'Knowledge4Zotero@windingwind.com'
$xpi  = Join-Path $ext ($id + '.xpi')
$dir  = Join-Path $ext $id
$bak  = Join-Path $prof '_hana_backup'

Write-Output '[1] backup profile state'
New-Item -ItemType Directory -Force -Path $bak | Out-Null
Copy-Item (Join-Path $prof 'extensions.json') (Join-Path $bak 'extensions.json.bak') -Force -ErrorAction SilentlyContinue
Copy-Item (Join-Path $prof 'prefs.js') (Join-Path $bak 'prefs.js.bak') -Force -ErrorAction SilentlyContinue
Write-Output '    ok'

Write-Output '[2] stop zotero'
$p = Get-Process zotero -ErrorAction SilentlyContinue
if ($p) { $p | Stop-Process -Force; Write-Output '    stopped' } else { Write-Output '    was not running' }
Start-Sleep -Seconds 6

Write-Output '[3] unpack xpi into extensions dir'
if (-not (Test-Path $xpi)) {
    Write-Output '    ERROR: xpi not found, abort'
    exit 1
}
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path $dir) { Remove-Item $dir -Recurse -Force }
[System.IO.Compression.ZipFile]::ExtractToDirectory($xpi, $dir)
Write-Output ('    extracted to ' + $dir)
Get-ChildItem $dir | Select-Object -First 12 | ForEach-Object { '      ' + $_.Name }

Write-Output '[4] remove stray xpi (avoid double registration)'
Remove-Item $xpi -Force -ErrorAction SilentlyContinue
Write-Output '    done'

Write-Output '[5] restart zotero'
Start-Process -FilePath 'D:\Zotero\zotero.exe'
Start-Sleep -Seconds 45

Write-Output '[6] verify registration'
$ex = Join-Path $prof 'extensions.json'
try {
    $j = Get-Content $ex -Raw | ConvertFrom-Json
    $n = 0
    foreach ($a in $j.addons) {
        if ($a.location -notlike 'app-*') {
            Write-Output ('    ADDON ' + $a.id + ' active=' + $a.active + ' loc=' + $a.location + ' ver=' + $a.version)
            $n = $n + 1
        }
    }
    Write-Output ('    thirdparty_count=' + $n)
    if ($n -eq 0) { Write-Output '    RESULT: sideload NOT accepted' } else { Write-Output '    RESULT: sideload ACCEPTED' }
} catch {
    Write-Output ('    err: ' + $_.Exception.Message)
}
