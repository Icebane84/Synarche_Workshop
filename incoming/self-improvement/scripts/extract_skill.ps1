# Skill Extraction Helper
# Extracts a learning into a new skill file.

param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName
)

$SkillDir = "c:\Users\Chris\.gemini\.agent\skills\$SkillName"
$TemplateFile = "c:\Users\Chris\.gemini\.agent\skills\self-improvement\assets\SKILL-TEMPLATE.md"

if (Test-Path $SkillDir) {
    Write-Error "Skill $SkillName already exists at $SkillDir"
    return
}

Write-Host "Creating new skill: $SkillName..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $SkillDir -Force | Out-Null
Copy-Item -Path $TemplateFile -Destination "$SkillDir\SKILL.md"

Write-Host "Skill created successfully at $SkillDir\SKILL.md" -ForegroundColor Green
Write-Host "Please customize the SKILL.md file with the learning content." -ForegroundColor Yellow
