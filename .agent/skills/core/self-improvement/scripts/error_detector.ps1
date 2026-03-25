<#
.SYNOPSIS
    Automated Error Detector and Logger.
    Captures tool/command failures into ERRORS.md.
#>

param(
    [string]$Command,
    [string]$ErrorOutput,
    [int]$ExitCode = 1
)

$errorLog = "c:\Users\Chris\Synarche_Workspace\.learnings\ERRORS.md"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$id = "ERR-$(Get-Date -Format 'yyyyMMdd')-$(Get-Random -Minimum 100 -Maximum 999)"

$entry = "`n| $id | $timestamp | $Command | $ExitCode | [ ] |"
$entry += "`n> **Context**: $ErrorOutput`n"

if (Test-Path $errorLog) {
    Add-Content -Path $errorLog -Value $entry
    Write-Host "`n[!] ERROR LOGGED: $id" -ForegroundColor Red
} else {
    Write-Host "`n[!] Error Log not found at $errorLog" -ForegroundColor Yellow
}
