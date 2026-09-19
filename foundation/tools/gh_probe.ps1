$ProgressPreference = 'SilentlyContinue'
$H = @{ 'User-Agent' = 'hana-probe'; 'Accept' = 'application/vnd.github+json' }

function Get-Json($url) {
    try {
        return Invoke-RestMethod -Uri $url -Headers $H -TimeoutSec 40
    } catch {
        Write-Output ('  ERR ' + $url + ' -> ' + $_.Exception.Message.Split("`n")[0])
        return $null
    }
}

foreach ($repo in @('WUBING2023/PaperSpine', 'PKUMichael/PaperSpine')) {
    Write-Output ('===== REPO ' + $repo + ' =====')
    $r = Get-Json ('https://api.github.com/repos/' + $repo)
    if ($r) {
        Write-Output ('  desc      = ' + $r.description)
        Write-Output ('  stars     = ' + $r.stargazers_count + '  forks=' + $r.forks_count)
        Write-Output ('  license   = ' + $r.license.spdx_id + ' (' + $r.license.name + ')')
        Write-Output ('  branch    = ' + $r.default_branch)
        Write-Output ('  updated   = ' + $r.updated_at + '  pushed=' + $r.pushed_at)
        Write-Output ('  size_kb   = ' + $r.size)
    }

    $t = Get-Json ('https://api.github.com/repos/' + $repo + '/git/trees/HEAD?recursive=1')
    if ($t) {
        Write-Output ('  --- tree (' + $t.tree.Count + ' entries) ---')
        $t.tree | Where-Object { $_.type -eq 'blob' } | ForEach-Object { '    ' + $_.path + '  ' + $_.size }
    }
}

Write-Output '===== repos of WUBING2023 ====='
$u = Get-Json 'https://api.github.com/users/WUBING2023/repos?per_page=100'
if ($u) {
    $u | ForEach-Object { '  ' + $_.name + '  |  ' + $_.description + '  |  stars=' + $_.stargazers_count + '  updated=' + $_.updated_at }
}
