$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$id   = 'Knowledge4Zotero@windingwind.com'

Start-Sleep -Seconds 35

$p = Get-Process zotero -ErrorAction SilentlyContinue
if ($p) { Write-Output ('zotero pids=' + (($p | ForEach-Object { $_.Id }) -join ',')) } else { Write-Output 'zotero NOT running' }

try {
    $j = Get-Content (Join-Path $prof 'extensions.json') -Raw | ConvertFrom-Json
    $found = $false
    $n = 0
    foreach ($a in $j.addons) {
        if ($a.location -notlike 'app-*') {
            $n = $n + 1
            Write-Output ('  thirdparty: ' + $a.id + ' active=' + $a.active + ' loc=' + $a.location + ' ver=' + $a.version)
        }
        if ($a.id -eq $id) {
            $found = $true
            Write-Output ('  MATCH: active=' + $a.active + ' loc=' + $a.location + ' ver=' + $a.version + ' path=' + $a.path)
        }
    }
    Write-Output ('thirdparty_count=' + $n)
    if ($found) { Write-Output 'RESULT=REGISTERED' } else { Write-Output 'RESULT=NOT_REGISTERED' }
} catch {
    Write-Output ('extjson err: ' + $_.Exception.Message)
}
