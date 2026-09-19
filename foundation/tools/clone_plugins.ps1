$ErrorActionPreference = 'Continue'
$log = 'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools\clone_plugins.log'
function L([string]$m) {
  $s = (Get-Date).ToString('HH:mm:ss') + ' ' + $m
  Write-Output $s
  Add-Content -Path $log -Value $s
}

"=== clone plugin sources === $(Get-Date -Format s)" | Set-Content -Path $log
$vendor = 'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\vendor'
New-Item -ItemType Directory -Force -Path $vendor | Out-Null

$repos = @(
  @{ n = 'hana-paper-reader'; u = 'https://github.com/TheEarlyWinter/hana-paper-reader.git' },
  @{ n = 'git-save-load';     u = 'https://github.com/H-i-m-s/git-save-load.git' }
)

foreach ($r in $repos) {
  $d = Join-Path $vendor $r.n
  if (Test-Path (Join-Path $d '.git')) {
    L ($r.n + ': repo exists, fetching')
    & git -C $d fetch --all --tags 2>&1 | Out-Null
    L ($r.n + ': fetch exit=' + $LASTEXITCODE)
  } else {
    L ('cloning ' + $r.n + ' <- ' + $r.u)
    & git clone $r.u $d 2>&1 | Out-Null
    L ($r.n + ': clone exit=' + $LASTEXITCODE)
  }
  if (Test-Path (Join-Path $d '.git')) {
    & git -C $d log -1 --format='%H|%ad|%s' --date=short 2>&1 | ForEach-Object { L ($r.n + ' HEAD: ' + $_) }
    & git -C $d branch -r 2>&1 | ForEach-Object { L ($r.n + ' branch: ' + $_) }
    if (Test-Path (Join-Path $d 'LICENSE')) { L ($r.n + ': LICENSE present') } else { L ($r.n + ': NO LICENSE file') }
  } else {
    L ($r.n + ': CLONE FAILED')
  }
}
L 'DONE'
