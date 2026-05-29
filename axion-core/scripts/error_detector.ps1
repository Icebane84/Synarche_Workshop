# error_detector.ps1
# Scans for errors and appends them to .learnings/ERRORS.md

param (
    [string]$ErrorLogPath = "c:\Users\Chris\Synarche_Workspace\_governance\06_Learning\GVRN.Learning.Error.md",
    [string]$TargetDir = "c:\Users\Chris\Synarche_Workspace\_logs"
)

$Timestamp = Get-Date -Format "yyyy-MM-dd"
Write-Host ">>> Scanning for Dissonance in $TargetDir..."

# Find recent log files and scan for "Error", "Exception", "Fail"
if (-not (Test-Path $TargetDir)) {
    Write-Host "Log directory not found: $TargetDir"
    exit
}

$Logs = Get-ChildItem -Path $TargetDir -Filter "*.log" | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-1) }

foreach ($Log in $Logs) {
    $LogContent = Get-Content $Log.FullName
    $Errors = $LogContent | Select-String -Pattern "Error", "Exception", "Fail"
    
    if ($Errors) {
        Write-Host "[!] Found errors in $($Log.Name). Logging to GVRN.Learning.Error.md..."
        
        # Calculate next ERR-LOG-XXX ID dynamically
        $NextNum = 18
        if (Test-Path $ErrorLogPath) {
            $FileContent = [System.IO.File]::ReadAllText($ErrorLogPath, [System.Text.Encoding]::UTF8)
            $Matches = [regex]::Matches($FileContent, 'ERR-LOG-(\d+)')
            if ($Matches.Count -gt 0) {
                $MaxNum = 0
                foreach ($m in $Matches) {
                    $val = [int]$m.Groups[1].Value
                    if ($val -gt $MaxNum) { $MaxNum = $val }
                }
                $NextNum = $MaxNum + 1
            }
        }
        $EntryID = "ERR-LOG-$($NextNum.ToString('000'))"
        
        $ErrDesc = $Errors[0].ToString()
        if ($ErrDesc.Length -gt 80) { $ErrDesc = $ErrDesc.Substring(0,80) + "..." }
        # Escape markdown characters
        $ErrDesc = $ErrDesc -replace '\|', '\|'
        
        # Parse GVRN.Learning.Error.md lines to insert table row and analysis block
        $Lines = [System.Collections.Generic.List[string]]([System.IO.File]::ReadAllLines($ErrorLogPath, [System.Text.Encoding]::UTF8))
        
        # 1. Insert row in Block B table
        $InsertedRow = "| $Timestamp | $EntryID | Identified in $($Log.Name) | $ErrDesc | [PENDING] |"
        $LogHeadingIndex = -1
        for ($i = 0; $i -lt $Lines.Count; $i++) {
            if ($Lines[$i] -match "## .*ERROR LOG") {
                $LogHeadingIndex = $i
                break
            }
        }
        if ($LogHeadingIndex -gt 3) {
            # Insert at empty line before the '---' that precedes the heading
            $Lines.Insert($LogHeadingIndex - 3, $InsertedRow)
        } else {
            $Lines.Add($InsertedRow)
        }
        
        # 2. Append detailed error block before OMNI-Anchor
        $AnchorIndex = -1
        for ($i = $Lines.Count - 1; $i -ge 0; $i--) {
            if ($Lines[$i] -match "\[OMNI-ARTIFACT-ANCHOR\]") {
                $AnchorIndex = $i
                break
            }
        }
        
        $DetailBlock = @(
            ""
            "### ${EntryID}: Error in $($Log.Name)"
            ""
            "---"
            ""
            "- **Analysis:** Automated scan detected exit/crash signatures in log file."
            "- **Remediation:** Investigate the log file ($($Log.Name)) for: `"$ErrDesc`"."
            ""
        )
        
        if ($AnchorIndex -gt 2) {
            # Insert before empty line preceding OMNI-Anchor
            $Lines.InsertRange($AnchorIndex - 2, [string[]]$DetailBlock)
        } else {
            $Lines.AddRange([string[]]$DetailBlock)
        }
        
        # Write back UTF-8 encoded without BOM
        $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllLines($ErrorLogPath, $Lines, $Utf8NoBom)
        Write-Host ">>> Error Logged: $EntryID in GVRN.Learning.Error.md" -ForegroundColor Red
        break # Only log the first file to prevent flooding
    }
}

Write-Host ">>> Error Detection Cycle Complete."

