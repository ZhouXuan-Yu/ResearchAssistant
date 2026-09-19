# finish_poppler_and_prepare.ps1 - finish the poppler download through the release
# asset API (the release CDN route times out), extract, then prepare visual receipts.
$ErrorActionPreference = "Continue"
$root   = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools\poppler"
$zip    = Join-Path $root "Release-26.09.0-0.zip"
$asset  = "https://api.github.com/repos/oschwartz10612/poppler-windows/releases/assets/566007129"
$dest   = Join-Path $root "extracted"
$log    = Join-Path $root "prepare.log"
$skill  = "C:\Users\ZhouXuan\.hanako\skills\paper-spine\scripts\visual_readiness_check.py"
$outdir = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
$expect = 43709956

"start $(Get-Date -Format o)" | Out-File -Encoding utf8 $log

for ($i = 1; $i -le 40; $i++) {
  $size = (Get-Item $zip).Length
  if ($size -ge $expect) { break }
  & curl.exe -sL --continue-at - --max-time 50 -H "Accept: application/octet-stream" -o $zip $asset 2>&1 | Out-Null
  $new = (Get-Item $zip).Length
  "attempt $i : $size -> $new" | Out-File -Encoding utf8 -Append $log
  if ($new -le $size) { Start-Sleep -Seconds 5 }
}
"zip bytes: $((Get-Item $zip).Length)" | Out-File -Encoding utf8 -Append $log

if (-not (Test-Path $dest)) { Expand-Archive -Path $zip -DestinationPath $dest -Force }
$bin = Get-ChildItem -Path $dest -Recurse -Filter "pdftoppm.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $bin) { "pdftoppm not found after extraction" | Out-File -Encoding utf8 -Append $log; exit 1 }
$bdir = $bin.DirectoryName
"bin dir: $bdir" | Out-File -Encoding utf8 -Append $log
$env:PATH = "$bdir;$env:PATH"
& (Join-Path $bdir "pdfinfo.exe") -v *>> $log

"--- prepare ---" | Out-File -Encoding utf8 -Append $log
& python $skill $outdir --prepare --markdown --write *>> $log
"exit=$LASTEXITCODE" | Out-File -Encoding utf8 -Append $log
"done $(Get-Date -Format o)" | Out-File -Encoding utf8 -Append $log
