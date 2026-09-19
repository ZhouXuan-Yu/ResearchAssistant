# run_visual_prepare.ps1 - wait for the poppler download, extract it, then run the
# PaperSpine visual receipt preparation with poppler on PATH.
$ErrorActionPreference = "Continue"
$root   = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools\poppler"
$zip    = Join-Path $root "Release-26.09.0-0.zip"
$dest   = Join-Path $root "extracted"
$log    = Join-Path $root "prepare.log"
$skill  = "C:\Users\ZhouXuan\.hanako\skills\paper-spine\scripts\visual_readiness_check.py"
$outdir = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
$expect = 43709956

"start $(Get-Date -Format o)" | Out-File -Encoding utf8 $log

# 1. wait for a complete download
$last = -1
$stall = 0
while ($true) {
  $size = if (Test-Path $zip) { (Get-Item $zip).Length } else { 0 }
  if ($size -ge $expect) { break }
  if ($size -eq $last) { $stall++ } else { $stall = 0 }
  if ($stall -ge 12) { "download stalled at $size" | Out-File -Encoding utf8 -Append $log; break }
  $last = $size
  Start-Sleep -Seconds 5
}
"zip bytes: $((Get-Item $zip).Length)" | Out-File -Encoding utf8 -Append $log

# 2. extract
if (-not (Test-Path $dest)) { Expand-Archive -Path $zip -DestinationPath $dest -Force }
$bin = Get-ChildItem -Path $dest -Recurse -Filter "pdftoppm.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $bin) { "pdftoppm not found after extraction" | Out-File -Encoding utf8 -Append $log; exit 1 }
$bdir = $bin.DirectoryName
"bin dir: $bdir" | Out-File -Encoding utf8 -Append $log
$env:PATH = "$bdir;$env:PATH"

# 3. sanity check the renderer
& (Join-Path $bdir "pdfinfo.exe") -v *>> $log

# 4. run prepare
"--- prepare ---" | Out-File -Encoding utf8 -Append $log
& python $skill $outdir --prepare --markdown --write *>> $log
"exit=$LASTEXITCODE" | Out-File -Encoding utf8 -Append $log
"done $(Get-Date -Format o)" | Out-File -Encoding utf8 -Append $log
