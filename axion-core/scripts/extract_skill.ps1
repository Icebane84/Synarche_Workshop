# extract_skill.ps1
# Transmutes a learning into a skill template

param (
    [string]$SkillName,
    [string]$TargetDir = "c:\Users\Chris\Synarche_Workspace\.agent\skills"
)

if (-not $SkillName) {
    Write-Error "SkillName parameter is required."
    exit
}

$SkillPath = Join-Path $TargetDir $SkillName
if (-not (Test-Path $SkillPath)) {
    New-Item -ItemType Directory -Path $SkillPath
    Write-Host ">>> Forging New Skill: $SkillName..."
}

$readme = @"
# SKILL: $SkillName

## Purpose
[Describe the purpose of the skill]

## Implementation
[Describe the technical implementation]

## Usage
[Describe how to use the skill]
"@

$readme | Out-File -FilePath (Join-Path $SkillPath "SKILL.md") -Encoding utf8

Write-Host ">>> Skill $SkillName has been forged in $SkillPath."
