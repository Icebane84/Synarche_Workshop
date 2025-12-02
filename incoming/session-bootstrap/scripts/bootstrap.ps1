# Session Bootstrap Script
# Loads project context and prints a structured SESSION BRIEF.
# Read-only. Always exits 0.

$AgentRoot = "c:\Users\Chris\.gemini\.agent"
$LearningsDir = "c:\Users\Chris\.gemini\.learnings"
$KnowledgeDir = Join-Path $AgentRoot "knowledge"
$SkillsDir = Join-Path $AgentRoot "skills"

# 1. Count active protocols
$ProtocolCount = (Get-ChildItem -Path $KnowledgeDir -Filter "*.md" -ErrorAction SilentlyContinue).Count

# 2. Scan .learnings/LEARNINGS.md for pending items
$LearningsFile = Join-Path $LearningsDir "LEARNINGS.md"
$PendingLearnings = 0
if (Test-Path $LearningsFile) {
    $PendingLearnings = (Select-String -Path $LearningsFile -Pattern "Status\*\*: pending" -ErrorAction SilentlyContinue).Count
}

# 3. Scan .learnings/ERRORS.md for pending errors
$ErrorsFile = Join-Path $LearningsDir "ERRORS.md"
$PendingErrors = 0
$HighPriorityErrors = 0
if (Test-Path $ErrorsFile) {
    $PendingErrors = (Select-String -Path $ErrorsFile -Pattern "Status\*\*: pending"   -ErrorAction SilentlyContinue).Count
    $HighPriorityErrors = (Select-String -Path $ErrorsFile -Pattern "Priority\*\*: high"    -ErrorAction SilentlyContinue).Count
}

# 4. Inventory available skills
$Skills = Get-ChildItem -Path $SkillsDir -Directory -ErrorAction SilentlyContinue |
Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") } |
Select-Object -ExpandProperty Name

# 5. Build the brief (ASCII-safe output)
$Date = Get-Date -Format "yyyy-MM-dd"
$Sep = "-" * 42
$ErrorLine = if ($HighPriorityErrors -gt 0) { " [HIGH: $($HighPriorityErrors)]" } else { "" }

Write-Host ""
Write-Host $Sep -ForegroundColor Cyan
Write-Host "  SESSION BRIEF -- $Date" -ForegroundColor Cyan
Write-Host $Sep -ForegroundColor Cyan
Write-Host "  Protocols : $($ProtocolCount) active" -ForegroundColor White
Write-Host "  Learnings : $($PendingLearnings) pending" -ForegroundColor $(if ($PendingLearnings -gt 0) { "Yellow" } else { "White" })
Write-Host "  Errors    : $($PendingErrors) pending$ErrorLine" -ForegroundColor $(if ($PendingErrors -gt 0) { "Red" } else { "White" })
Write-Host "  Skills    :" -ForegroundColor White

foreach ($skill in $Skills) {
    Write-Host "    * $skill" -ForegroundColor Gray
}

Write-Host $Sep -ForegroundColor Cyan
Write-Host ""

exit 0
