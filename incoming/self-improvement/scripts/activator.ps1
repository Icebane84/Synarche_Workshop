# Self-Improvement Activator
# Reminds the agent to evaluate learnings after each task.

$CurrentTime = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
Write-Host "`n[SELF-IMPROVEMENT] Evaluated at $CurrentTime" -ForegroundColor Green
Write-Host "Consider if anything learned in this session should be logged to .learnings/" -ForegroundColor Cyan
Write-Host "Check SKILL.md for categories: correction, knowledge_gap, best_practice, error, feature_request" -ForegroundColor Gray
