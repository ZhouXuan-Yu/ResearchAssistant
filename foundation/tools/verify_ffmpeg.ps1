$b = 'C:\Users\ZhouXuan\tools\ffmpeg\bin'
$p = [Environment]::GetEnvironmentVariable('Path', 'User')
Write-Output ('user PATH contains bin : ' + ($p -like ('*' + $b + '*')))
Write-Output ('user PATH tail         : ' + $p.Substring([Math]::Max(0, $p.Length - 100)))
Write-Output ('process PATH contains  : ' + (($env:Path -like ('*' + $b + '*'))))

$t = Join-Path $env:TEMP 'ff_smoke'
New-Item -ItemType Directory -Force -Path $t | Out-Null
$src = Join-Path $t 'a.mp4'

& (Join-Path $b 'ffmpeg.exe') -hide_banner -loglevel error -f lavfi -i 'testsrc=duration=1:size=320x240:rate=10' -pix_fmt yuv420p -y $src 2>&1
Write-Output ('encode exit = ' + $LASTEXITCODE)
Write-Output ('output bytes = ' + (Get-Item $src -ErrorAction SilentlyContinue).Length)

& (Join-Path $b 'ffprobe.exe') -hide_banner -v error -select_streams v:0 -show_entries 'stream=codec_name,width,height' -of 'default=nw=1' $src 2>&1
Write-Output ('probe exit = ' + $LASTEXITCODE)

Remove-Item $t -Recurse -Force -ErrorAction SilentlyContinue
Write-Output 'smoke temp removed'
