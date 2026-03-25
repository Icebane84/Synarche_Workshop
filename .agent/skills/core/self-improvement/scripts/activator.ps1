<#
.SYNOPSIS
    Session Activator for Self-Improvement Loop.
    Reminds the agent of the current learnings and pending tasks.
#>

$learningsDir = "c:\Users\Chris\Synarche_Workspace\.learnings"
$learningsFile = Join-Path $learningsDir "LEARNINGS.md"
$errorsFile = Join-Path $learningsDir "ERRORS.md"

Write-Host "`n--- [SELF-IMPROVEMENT] SESSION ACTIVATED ---" -ForegroundColor Cyan
Write-Host "Target: $learningsDir"

if (Test-Path $learningsFile) {
    $latest = Get-Content $learningsFile | Select-Object -Last 5
    Write-Host "`n[LATEST INSIGHTS]:" -ForegroundColor Yellow
    $latest | ForEach-Object { Write-Host "  $_" }
}

if (Test-Path $errorsFile) {
    $pendingErrors = Get-Content $errorsFile | Select-String "\[ \]"
    if ($pendingErrors) {
        Write-Host "`n[PENDING ERRORS DETECTED]: $($pendingErrors.Count)" -ForegroundColor Red
    }
}

Write-Host "`n>>> ACTIVE PROTOCOL: COHERENT ASCENSION v15.0" -ForegroundColor Green
