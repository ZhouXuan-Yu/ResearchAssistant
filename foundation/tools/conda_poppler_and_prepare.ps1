# conda_poppler_and_prepare.ps1 - install poppler into an isolated conda env
# (conda-forge channel; the GitHub release CDN is unreachable here) and then run
# the PaperSpine visual receipt preparation with that poppler on PATH.
$ErrorActionPreference = "Continue"
$root   = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools"
$log    = Join-Path $root "conda_poppler.log"
$conda  = "D:\Anaconda\Scripts\conda.exe"
$envdir = "D:\Anaconda\envs\spine-tools"
$skill  = "C:\Users\ZhouXuan\.hanako\skills\paper-spine\scripts\visual_readiness_check.py"
$outdir = "C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"

"start $(Get-Date -Format o)" | Out-File -Encoding utf8 $log

if (-not (Test-Path (Join-Path $envdir "Library\bin\pdftoppm.exe"))) {
  "--- conda create ---" | Out-File -Encoding utf8 -Append $log
  & $conda create -y -n spine-tools --override-channels -c conda-forge poppler *>> $log
  "create exit=$LASTEXITCODE" | Out-File -Encoding utf8 -Append $log
}

$bin = Join-Path $envdir "Library\bin"
if (-not (Test-Path (Join-Path $bin "pdftoppm.exe"))) {
  "pdftoppm still missing at $bin" | Out-File -Encoding utf8 -Append $log
  exit 1
}
"bin: $bin" | Out-File -Encoding utf8 -Append $log
$env:PATH = "$bin;$env:PATH"
& (Join-Path $bin "pdfinfo.exe") -v *>> $log

"--- prepare ---" | Out-File -Encoding utf8 -Append $log
& python $skill $outdir --prepare --markdown --write *>> $log
"prepare exit=$LASTEXITCODE" | Out-File -Encoding utf8 -Append $log
"done $(Get-Date -Format o)" | Out-File -Encoding utf8 -Append $log
