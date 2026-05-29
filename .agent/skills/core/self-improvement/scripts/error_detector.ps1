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

$errorLog = "c:\Users\Chris\Synarche_Workspace\_governance\06_Learning\GVRN.Learning.Error.md"
$timestamp = Get-Date -Format "yyyy-MM-dd"
$detailedTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

if (Test-Path $errorLog) {
    # Calculate next ERR-LOG-XXX ID dynamically
    $NextNum = 18
    $FileContent = [System.IO.File]::ReadAllText($errorLog, [System.Text.Encoding]::UTF8)
    $Matches = [regex]::Matches($FileContent, 'ERR-LOG-(\d+)')
    if ($Matches.Count -gt 0) {
        $MaxNum = 0
        foreach ($m in $Matches) {
            $val = [int]$m.Groups[1].Value
            if ($val -gt $MaxNum) { $MaxNum = $val }
        }
        $NextNum = $MaxNum + 1
    }
    $id = "ERR-LOG-$($NextNum.ToString('000'))"
    
    $cleanCommand = $Command -replace '\|', '\|'
    $cleanOutput = $ErrorOutput
    if ($cleanOutput.Length -gt 80) { $cleanOutput = $cleanOutput.Substring(0,80) + "..." }
    $cleanOutput = $cleanOutput -replace '\|', '\|'

    # Parse GVRN.Learning.Error.md lines to insert table row and analysis block
    $Lines = [System.Collections.Generic.List[string]]([System.IO.File]::ReadAllLines($errorLog, [System.Text.Encoding]::UTF8))
    
    # 1. Insert row in Block B table
    $InsertedRow = "| $timestamp | $id | $cleanCommand | $cleanOutput | [PENDING] |"
    $LogHeadingIndex = -1
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match "## .*ERROR LOG") {
            $LogHeadingIndex = $i
            break
        }
    }
    if ($LogHeadingIndex -gt 3) {
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
        "### ${id}: Error executing command: $Command"
        ""
        "---"
        ""
        "- **Analysis:** Automated scan detected a tool/command failure."
        "- **Remediation:** Exit code $ExitCode. Command context: `"$ErrorOutput`"."
        ""
    )
    
    if ($AnchorIndex -gt 2) {
        $Lines.InsertRange($AnchorIndex - 2, [string[]]$DetailBlock)
    } else {
        $Lines.AddRange([string[]]$DetailBlock)
    }
    
    # Write back UTF-8 encoded without BOM
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($errorLog, $Lines, $Utf8NoBom)
    Write-Host "`n[!] ERROR LOGGED: $id in GVRN.Learning.Error.md" -ForegroundColor Red
} else {
    Write-Host "`n[!] Error Log not found at $errorLog" -ForegroundColor Yellow
}

