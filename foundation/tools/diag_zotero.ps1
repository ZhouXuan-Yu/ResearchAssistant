$ErrorActionPreference = 'Continue'
$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$data = 'C:\Users\ZhouXuan\Zotero'

Write-Output '[A] profile extensions dir'
$pe = Join-Path $prof 'extensions'
if (Test-Path $pe) {
    Get-ChildItem $pe -ErrorAction SilentlyContinue | ForEach-Object { '    ' + $_.Name + '  ' + $_.Length }
} else {
    Write-Output '    (missing)'
}

Write-Output '[B] data dir extensions'
$de = Join-Path $data 'extensions'
if (Test-Path $de) {
    Get-ChildItem $de -ErrorAction SilentlyContinue | ForEach-Object { '    ' + $_.Name }
} else {
    Write-Output '    (missing)'
}

Write-Output '[C] prefs.js relevant keys'
$pf = Join-Path $prof 'prefs.js'
if (Test-Path $pf) {
    Select-String -Path $pf -Pattern 'autoDisableScopes', 'enabledAddons', 'localAPI', 'extensions.zotero' -ErrorAction SilentlyContinue |
        Select-Object -First 30 | ForEach-Object { '    ' + $_.Line }
} else {
    Write-Output '    (no prefs.js)'
}

Write-Output '[D] third-party addons in extensions.json'
try {
    $raw = Get-Content (Join-Path $prof 'extensions.json') -Raw
    $j = $raw | ConvertFrom-Json
    $n = 0
    foreach ($a in $j.addons) {
        if ($a.location -notlike 'app-*') {
            Write-Output ('    ' + $a.id + ' active=' + $a.active + ' loc=' + $a.location + ' ver=' + $a.version)
            $n = $n + 1
        }
    }
    Write-Output ('    count=' + $n)
} catch {
    Write-Output ('    err: ' + $_.Exception.Message)
}

Write-Output '[E] local API probe without proxy'
try {
    $wc = New-Object System.Net.WebClient
    $wc.Proxy = $null
    $s = $wc.DownloadString('http://127.0.0.1:23119/connector/ping')
    $cut = [Math]::Min(80, $s.Length)
    Write-Output ('    ping OK: ' + $s.Substring(0, $cut))
} catch {
    Write-Output ('    ping ERR: ' + $_.Exception.Message)
}

Write-Output '[F] port 23119 listeners'
$ns = netstat -ano | Select-String ':23119'
if ($ns) {
    $ns | Select-Object -First 5 | ForEach-Object { '    ' + $_.Line.Trim() }
} else {
    Write-Output '    (nothing listening)'
}

Write-Output '[G] zotero processes'
$ps = Get-Process zotero -ErrorAction SilentlyContinue
if ($ps) {
    Write-Output ('    running pids=' + (($ps | ForEach-Object { $_.Id }) -join ','))
} else {
    Write-Output '    not running'
}
