# activator.ps1
# Synthesizes session state into .learnings/LEARNINGS.md

param (
    [string]$LearningsPath = "c:\Users\Chris\Synarche_Workspace\.learnings\LEARNINGS.md",
    [Parameter(Mandatory=$true)][string]$Summary,
    [string]$Details = "Manual synthesis executed.",
    [ValidateSet("low", "medium", "high", "critical")][string]$Priority = "medium",
    [string]$Area = "infra"
)

$Date = Get-Date -Format "yyyyMMdd"
$Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$RandomID = Get-Random -Minimum 100 -Maximum 999
$EntryID = "LRN-$Date-$RandomID"

Write-Host ">>> Activating Sovereign Memory Synthesis..."

# Logic: Append a new entry to the Evolutionary Ledger
$NewLearning = @"

## [$EntryID] $Summary

**Logged**: $Timestamp
**Priority**: $Priority
**Status**: pending
**Area**: $Area

### Summary
$Summary

### Details
$Details

### Suggested Action
Evaluate systemic impact and promote to CLAUDE.md if applicable.

### Metadata
- Source: session_outcome
- Workflow: activator.ps1
---
"@

$NewLearning | Out-File -FilePath $LearningsPath -Append -Encoding utf8

Write-Host ">>> Synthesis Complete. Entry $EntryID Persisted to $LearningsPath" -ForegroundColor Green
