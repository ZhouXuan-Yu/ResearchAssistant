param([string]$Loc = 'profile')

$prof  = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'
$data  = 'C:\Users\ZhouXuan\Zotero'
$id    = 'Knowledge4Zotero@windingwind.com'
$stage = 'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\downloads\better-notes-for-zotero-3.3.3.xpi'

if ($Loc -eq 'data') {
    $root = Join-Path $data 'extensions'
} else {
    $root = Join-Path $prof 'extensions'
}

Write-Output ('target root: ' + $root)
if (-not (Test-Path $stage)) { Write-Output 'ERROR: staged xpi missing'; exit 1 }
New-Item -ItemType Directory -Force -Path $root | Out-Null

# remove any stray xpi so the unpacked dir is the single source
Get-ChildItem $root -Filter '*.xpi' -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Output ('  removing stray: ' + $_.Name)
    Remove-Item $_.FullName -Force
}

$dir = Join-Path $root $id
if (Test-Path $dir) { Remove-Item $dir -Recurse -Force }

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($stage, $dir)

Write-Output ('unpacked -> ' + $dir)
Get-ChildItem $dir | Select-Object -First 10 | ForEach-Object { '  ' + $_.Name }
Write-Output 'OK'
