# [TITAN-CORE] extract_skill.ps1
# Version: v15.0 [OMEGA]
# Domain: GVRN (Core Systems)
# Protocol: [[GVRN.PROT.SkillExtraction]]
# Status: [CANONIZED]
# Purpose: Transmutes session learnings into actionable skill shards within the .agent/skills runtime.
# HASH: SKILL-EXT-CORE-V15

<#
.SYNOPSIS
    Skill Extraction Helper.
    Transmutes learnings into a new skill directory in the Synarche workspace.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillName,
    [string]$Description = "Extracted from session learnings."
)

$basePath = "c:\Users\Chris\Synarche_Workspace\.agent\skills"
$newSkillPath = Join-Path $basePath $SkillName
$templatePath = Join-Path $basePath "self-improvement\assets\SKILL-TEMPLATE.md"

if (Test-Path $newSkillPath) {
    Write-Error "Skill '$SkillName' already exists."
    return
}

New-Item -ItemType Directory -Path $newSkillPath -Force | Out-Null
$skillFile = Join-Path $newSkillPath "SKILL.md"

if (Test-Path $templatePath) {
    $content = Get-Content $templatePath
    # Handle both {{NAME}} and { { NAME } } patterns
    $content = $content -replace "\{\s*\{\s*NAME\s*\}\s*\}", $SkillName
    $content = $content -replace "\{\s*\{\s*DESCRIPTION\s*\}\s*\}", $Description
    $content = $content -replace "\{\s*\{\s*DATE\s*\}\s*\}", (Get-Date -Format "yyyy-MM-dd")
    Set-Content -Path $skillFile -Value $content
    Write-Host "`n[+] SKILL FORGED: $SkillName" -ForegroundColor Green
    Write-Host "Location: $newSkillPath"
} else {
    Write-Host "`n[!] Template not found. Creating basic SKILL.md"
    "---`nname: $SkillName`ndescription: $Description`n---" | Set-Content $skillFile
}
