$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$id   = 'Knowledge4Zotero@windingwind.com'
$pf   = Join-Path $prof 'prefs.js'

Write-Output '[1] autoDisableScopes persisted?'
$hit = Select-String -Path $pf -Pattern 'autoDisableScopes' -ErrorAction SilentlyContinue
if ($hit) { $hit | ForEach-Object { '    ' + $_.Line } } else { Write-Output '    (not found)' }

Write-Output '[2] addon record'
$j = Get-Content (Join-Path $prof 'extensions.json') -Raw | ConvertFrom-Json
foreach ($a in $j.addons) {
    if ($a.id -eq $id) {
        Write-Output ('    version       = ' + $a.version)
        Write-Output ('    active        = ' + $a.active)
        Write-Output ('    userDisabled  = ' + $a.userDisabled)
        Write-Output ('    appDisabled   = ' + $a.appDisabled)
        Write-Output ('    seen          = ' + $a.seen)
        Write-Output ('    location      = ' + $a.location)
        Write-Output ('    path          = ' + $a.path)
        Write-Output ('    sourceURI     = ' + $a.sourceURI)
        Write-Output ('    targetApps    = ' + ($a.targetApplications | ConvertTo-Json -Compress))
        Write-Output ('    targetPlats   = ' + ($a.targetPlatforms | ConvertTo-Json -Compress))
    }
}

Write-Output '[3] totals'
Write-Output ('    addons in extensions.json = ' + $j.addons.Count)
Write-Output ('    zotero exe version        = ' + (Get-Item 'D:\Zotero\zotero.exe').VersionInfo.ProductVersion)
