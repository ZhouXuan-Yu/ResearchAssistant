$prof = 'C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default'

$p = Get-Process zotero -ErrorAction SilentlyContinue
if ($p) {
    $p | Stop-Process -Force
    Write-Output 'stopped zotero'
    Start-Sleep -Seconds 5
} else {
    Write-Output 'zotero was not running'
}

Start-Process -FilePath 'D:\Zotero\zotero.exe'
Write-Output 'started zotero'
