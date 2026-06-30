<#
.SYNOPSIS
    Session Activator for Self-Improvement Loop.
    Reminds the agent of the current learnings and pending tasks.
#>

$learningsDir = "c:\Users\Chris\Synarche_Workspace\_governance\06_Learning"
$learningsFile = Join-Path $learningsDir "GVRN.Learning.Shard.md"
$errorsFile = Join-Path $learningsDir "GVRN.Learning.Error.md"

Write-Host "`n--- [SELF-IMPROVEMENT] SESSION ACTIVATED ---" -ForegroundColor Cyan
Write-Host "Target Subsystem: $learningsDir"

if (Test-Path $learningsFile) {
    $gems = Get-Content $learningsFile | Select-String -Pattern "### \*\*\[GEM-"
    if ($gems) {
        $latest = $gems | Select-Object -Last 3
        Write-Host "`n[LATEST FORGED SHARDS]:" -ForegroundColor Yellow
        $latest | ForEach-Object { Write-Host "  $($_.ToString().Trim('#* '))" }
    }
}

if (Test-Path $errorsFile) {
    $pendingErrors = Get-Content $errorsFile | Select-String "\[PENDING\]"
    if ($pendingErrors) {
        Write-Host "`n[PENDING L5 ERRORS DETECTED]: $($pendingErrors.Count)" -ForegroundColor Red
        $pendingErrors | Select-Object -First 3 | ForEach-Object {
            $parts = $_.ToString().Split('|')
            if ($parts.Count -gt 4) {
                Write-Host "  - $($parts[2].Trim()): $($parts[3].Trim())" -ForegroundColor DarkRed
            }
        }
    }
}

Write-Host "`n>>> ACTIVE PROTOCOL: COHERENT ASCENSION v15.0" -ForegroundColor Green

