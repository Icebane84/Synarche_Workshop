# Error Detector for Self-Improvement
# Helps identify tool or command failures for logging.

param(
    [int]$ExitCode,
    [string]$Command
)

if ($ExitCode -ne 0) {
    Write-Host "`n[ERROR-DETECTED] Command failed with exit code $($ExitCode): $($Command)" -ForegroundColor Red
    Write-Host "Suggested action: Log this failure to .learnings/ERRORS.md" -ForegroundColor Yellow
}
