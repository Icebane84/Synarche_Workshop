# error_detector.ps1
# Scans for errors and appends them to .learnings/ERRORS.md

param (
    [string]$ErrorLogPath = "c:\Users\Chris\Synarche_Workspace\.learnings\ERRORS.md",
    [string]$TargetDir = "c:\Users\Chris\Synarche_Workspace\_logs"
)

$Timestamp = Get-Date -Format "yyyy-MM-dd"
Write-Host ">>> Scanning for Dissonance in $TargetDir..."

# Logic: Find recent log files and scan for "Error", "Exception", "Fail"
$Logs = Get-ChildItem -Path $TargetDir -Filter "*.log" | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-1) }

foreach ($Log in $Logs) {
    $Content = Get-Content $Log.FullName
    $Errors = $Content | Select-String -Pattern "Error", "Exception", "Fail"
    
    if ($Errors) {
        Write-Host "[!] Found errors in $($Log.Name). Logging to ERRORS.md..."
        $ErrorSummary = "| $Timestamp | ERR-$([guid]::NewGuid().ToString().Substring(0,8)) | $($Errors[0].ToString().Substring(0,50)) | Identified in $($Log.Name) | [NEW] |"
        $ErrorSummary | Out-File -FilePath $ErrorLogPath -Append -Encoding utf8
    }
}

Write-Host ">>> Error Detection Cycle Complete."
