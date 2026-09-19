# fetch_poppler.ps1 - download the portable poppler Windows build into the workspace
# (no admin required; nothing is installed system-wide)
$ErrorActionPreference = "Continue"
$root = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools\poppler"
$zip  = Join-Path $root "Release-26.09.0-0.zip"
$url  = "https://github.com/oschwartz10612/poppler-windows/releases/download/v26.09.0-0/Release-26.09.0-0.zip"
$log  = Join-Path $root "download.log"

New-Item -ItemType Directory -Force -Path $root | Out-Null

if((Test-Path $zip) -and ((Get-Item $zip).Length -lt 25000000)){ Remove-Item $zip -Force }

if(-not (Test-Path $zip)){
  "start $(Get-Date -Format o)" | Out-File -Encoding utf8 $log
  $curl = (Get-Command curl.exe -ErrorAction SilentlyContinue).Source
  if($curl){
    & $curl -L --retry 3 --retry-delay 2 -o $zip $url *>> $log
  } else {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  }
  "end $(Get-Date -Format o)" | Out-File -Encoding utf8 -Append $log
}

$size = (Get-Item $zip).Length
"zip bytes: $size" | Out-File -Encoding utf8 -Append $log

$dest = Join-Path $root "extracted"
if($size -gt 25000000 -and -not (Test-Path $dest)){
  Expand-Archive -Path $zip -DestinationPath $dest -Force
}
$bin = Get-ChildItem -Path $root -Recurse -Filter "pdftoppm.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if($bin){ "pdftoppm: $($bin.FullName)" | Out-File -Encoding utf8 -Append $log } else { "pdftoppm: NOT FOUND" | Out-File -Encoding utf8 -Append $log }
