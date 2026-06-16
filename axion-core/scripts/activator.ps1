# activator.ps1
# Synthesizes session state into .learnings/LEARNINGS.md

param (
    [string]$LearningsPath = "c:\Users\Chris\Synarche_Workspace\_governance\06_Learning\GVRN.Learning.Shard.md",
    [Parameter(Mandatory=$true)][string]$Summary,
    [string]$Details = "Manual synthesis executed.",
    [ValidateSet("low", "medium", "high", "critical")][string]$Priority = "medium",
    [string]$Area = "infra"
)

$Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
Write-Host ">>> Activating Sovereign Memory Synthesis..."

# Dynamic GEM ID calculation by scanning the target Shard file
$NextNum = 21
if (Test-Path $LearningsPath) {
    $Content = [System.IO.File]::ReadAllText($LearningsPath, [System.Text.Encoding]::UTF8)
    $Matches = [regex]::Matches($Content, '\[GEM-(\d+)\]')
    if ($Matches.Count -gt 0) {
        $MaxNum = 0
        foreach ($m in $Matches) {
            $val = [int]$m.Groups[1].Value
            if ($val -gt $MaxNum) { $MaxNum = $val }
        }
        $NextNum = $MaxNum + 1
    }
}
$EntryID = "GEM-$($NextNum.ToString('000'))"

# Logic: Splice new entry before [OMNI-ARTIFACT-ANCHOR] in GVRN.Learning.Shard.md
if (Test-Path $LearningsPath) {
    $Lines = [System.Collections.Generic.List[string]]([System.IO.File]::ReadAllLines($LearningsPath, [System.Text.Encoding]::UTF8))
    $AnchorIndex = -1
    for ($i = $Lines.Count - 1; $i -ge 0; $i--) {
        if ($Lines[$i] -match "\[OMNI-ARTIFACT-ANCHOR\]") {
            $AnchorIndex = $i
            break
        }
    }
    
    $DetailBlock = @(
        ""
        "### **[$EntryID] [$($Summary.ToUpper())] [$($Area.ToUpper())]**"
        ""
        "**Timestamp**: $Timestamp **Oracle**: OGLN Artificer-Agent **Domain**: CORE (Self-Improvement Loop)"
        ""
        "#### **The Catalyst (Dissonance)**"
        ""
        "$Details"
        ""
        "#### **The Synthesis (Resolution)**"
        ""
        "- **Session Learning Sync**: Captured during task execution with priority '$Priority'."
        "- **Suggested Action**: Evaluate and promote to CLAUDE.md if applicable."
        ""
        "#### **The Transcendence (Insight)**"
        ""
        "> `"$Summary`""
        ""
        "**[STATUS: ACTIVE] [XP: +250]**"
        ""
        "---"
    )
    
    if ($AnchorIndex -gt 2) {
        # Insert before empty line preceding OMNI-Anchor
        $Lines.InsertRange($AnchorIndex - 1, [string[]]$DetailBlock)
    } else {
        $Lines.AddRange([string[]]$DetailBlock)
    }
    
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($LearningsPath, $Lines, $Utf8NoBom)
    Write-Host ">>> Synthesis Complete. Entry $EntryID Spliced into $LearningsPath" -ForegroundColor Green
} else {
    Write-Error "Learnings target path not found: $LearningsPath"
}

