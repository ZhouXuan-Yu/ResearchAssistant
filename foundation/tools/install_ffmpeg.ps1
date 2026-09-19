$ErrorActionPreference = 'Continue'

function L([string]$m) {
  $s = (Get-Date).ToString('HH:mm:ss') + ' ' + $m
  Write-Output $s
  Add-Content -Path $log -Value $s
}

$log  = 'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools\install_ffmpeg.log'
$root = 'C:\Users\ZhouXuan\tools\ffmpeg'
$tmp  = 'C:\Users\ZhouXuan\tools\_ffmpeg_tmp'
$zip  = Join-Path $tmp 'ffmpeg.zip'
$ex   = Join-Path $tmp 'x'
$bin  = Join-Path $root 'bin'

"=== install ffmpeg / ffprobe portable build === $(Get-Date -Format s)" | Set-Content -Path $log
New-Item -ItemType Directory -Force -Path $root, $tmp, $ex | Out-Null

$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User')
Set-Content -Path (Join-Path $root 'PATH.user.bak.txt') -Value $oldPath
L ('old user PATH backed up to ' + (Join-Path $root 'PATH.user.bak.txt'))

$urls = @(
  'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
  'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
)

$ok = $false
foreach ($u in $urls) {
  L ('downloading ' + $u)
  & curl.exe -L --fail --retry 2 --connect-timeout 20 --max-time 900 -o $zip $u 2>&1 | Out-Null
  $code = $LASTEXITCODE
  if ($code -eq 0 -and (Test-Path $zip) -and ((Get-Item $zip).Length -gt 1000000)) {
    $ok = $true
    L ('download ok, bytes=' + (Get-Item $zip).Length)
    break
  }
  L ('download failed, exit=' + $code)
}

if (-not $ok) { L 'FATAL: all download urls failed'; exit 2 }

& tar.exe -xf $zip -C $ex 2>&1 | Out-Null
L ('extract exit=' + $LASTEXITCODE)

$hit = Get-ChildItem $ex -Recurse -Filter 'ffmpeg.exe' -File -ErrorAction SilentlyContinue |
  Where-Object { Test-Path (Join-Path $_.DirectoryName 'ffprobe.exe') } |
  Select-Object -First 1
if (-not $hit) { L 'FATAL: ffmpeg.exe with sibling ffprobe.exe not found in archive'; exit 3 }
L ('found bin dir: ' + $hit.DirectoryName)

New-Item -ItemType Directory -Force -Path $bin | Out-Null
Copy-Item (Join-Path $hit.DirectoryName '*') $bin -Force -Recurse
L 'copied binaries'

$p = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($p -notlike ('*' + $bin + '*')) {
  [Environment]::SetEnvironmentVariable('Path', ($p.TrimEnd(';') + ';' + $bin), 'User')
  L 'user PATH updated (append)'
} else {
  L 'user PATH already contains bin'
}

& (Join-Path $bin 'ffmpeg.exe') -version 2>&1 | Select-Object -First 1 | ForEach-Object { L ('ffmpeg : ' + $_) }
& (Join-Path $bin 'ffprobe.exe') -version 2>&1 | Select-Object -First 1 | ForEach-Object { L ('ffprobe: ' + $_) }

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
L 'temp cleaned'

$env:Path = $env:Path + ';' + $bin
$null = [Environment]::GetEnvironmentVariable('Path', 'Machine')
L 'DONE'
