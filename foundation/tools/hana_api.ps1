$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$reqFile = Join-Path $here 'api_request.json'

if (-not (Test-Path $reqFile)) {
  Write-Output ('ERROR: request file not found: ' + $reqFile)
  exit 1
}

$req = Get-Content $reqFile -Raw | ConvertFrom-Json
$method = 'GET'
if ($req.method) { $method = [string]$req.method }
$path = [string]$req.path
$body = ''
if ($req.body) { $body = [string]$req.body }
$timeout = 60
if ($req.timeoutSec) { $timeout = [int]$req.timeoutSec }

$info = Get-Content 'C:\Users\ZhouXuan\.hanako\server-info.json' -Raw | ConvertFrom-Json
$uri = 'http://127.0.0.1:' + $info.port + $path
$headers = @{ Authorization = 'Bearer ' + $info.token }

Write-Output ('-> ' + $method + ' ' + $path)
try {
  if ($body -ne '') {
    $r = Invoke-WebRequest -Uri $uri -Method $method -Headers $headers -ContentType 'application/json' -Body $body -TimeoutSec $timeout -UseBasicParsing
  } else {
    $r = Invoke-WebRequest -Uri $uri -Method $method -Headers $headers -TimeoutSec $timeout -UseBasicParsing
  }
  Write-Output ('HTTP ' + [int]$r.StatusCode + ' | bytes=' + $r.Content.Length)
  Write-Output $r.Content
} catch {
  Write-Output ('ERROR: ' + $_.Exception.Message)
  if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
    Write-Output ('DETAIL: ' + $_.ErrorDetails.Message)
  }
  if ($_.Exception.Response) {
    try {
      $sr = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream())
      Write-Output $sr.ReadToEnd()
    } catch { }
  }
}
