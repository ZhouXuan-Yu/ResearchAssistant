param(
  [Parameter(Mandatory = $true, Position = 0)][string]$LocalDir,
  [Parameter(Mandatory = $true, Position = 1)][string]$UpstreamDir
)

$script:TextExt = @('.js', '.mjs', '.cjs', '.css', '.html', '.htm', '.md', '.json', '.txt', '.yml', '.yaml', '.ps1', '.py', '.sh', '.svg')

function Get-NormalizedHash([string]$file, [bool]$isText) {
  if (-not $isText) { return (Get-FileHash $file -Algorithm SHA256).Hash }
  $raw = [IO.File]::ReadAllBytes($file)
  $ms = New-Object IO.MemoryStream
  for ($i = 0; $i -lt $raw.Length; $i++) {
    if ($raw[$i] -eq 13 -and ($i + 1) -lt $raw.Length -and $raw[$i + 1] -eq 10) { continue }
    $ms.WriteByte($raw[$i])
  }
  $bytes = $ms.ToArray()
  $ms.Dispose()
  $sha = [Security.Cryptography.SHA256]::Create()
  try { return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '') } finally { $sha.Dispose() }
}

function Get-TreeMap([string]$root) {
  $root = (Resolve-Path $root).Path.TrimEnd('\')
  $map = @{}
  Get-ChildItem $root -Recurse -File -Force |
    Where-Object { $_.FullName -notmatch '\\\.git\\' -and $_.Name -ne '.gitignore' } |
    ForEach-Object {
      $rel = $_.FullName.Substring($root.Length).TrimStart('\')
      $isText = $script:TextExt -contains $_.Extension.ToLower()
      $map[$rel] = @{
        Raw = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
        Norm = Get-NormalizedHash $_.FullName $isText
        Size = $_.Length
      }
    }
  return $map
}

$a = Get-TreeMap $LocalDir
$b = Get-TreeMap $UpstreamDir

Write-Output ('local files    : ' + $a.Count)
Write-Output ('upstream files : ' + $b.Count)
Write-Output ''

$onlyLocal = @($a.Keys | Where-Object { -not $b.ContainsKey($_) } | Sort-Object)
$onlyUp = @($b.Keys | Where-Object { -not $a.ContainsKey($_) } | Sort-Object)
$eolOnly = @()
$content = @()
foreach ($k in ($a.Keys | Where-Object { $b.ContainsKey($_) })) {
  if ($a[$k].Norm -eq $b[$k].Norm) {
    if ($a[$k].Raw -ne $b[$k].Raw) { $eolOnly += $k }
  } else {
    $content += $k
  }
}

Write-Output ('--- only local (' + $onlyLocal.Count + ') ---')
$onlyLocal | ForEach-Object { Write-Output ('  <= ' + $_) }
Write-Output ('--- only upstream (' + $onlyUp.Count + ') ---')
$onlyUp | ForEach-Object { Write-Output ('  => ' + $_) }
Write-Output ('--- content differs (' + $content.Count + ') ---')
$content | Sort-Object | ForEach-Object { Write-Output ('  <> ' + $_ + '  (local ' + $a[$_].Size + ' B / upstream ' + $b[$_].Size + ' B)') }
Write-Output ('--- line-ending only (' + $eolOnly.Count + ') ---')
if ($eolOnly.Count -le 8) { $eolOnly | ForEach-Object { Write-Output ('  ~~ ' + $_) } }
else { $eolOnly | Select-Object -First 8 | ForEach-Object { Write-Output ('  ~~ ' + $_) }; Write-Output ('  ... and ' + ($eolOnly.Count - 8) + ' more') }
