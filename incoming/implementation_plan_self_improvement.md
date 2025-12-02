# Make Self-Improvement Skill Operational

This plan outlines the steps to fully operationalize the `self-improvement` skill on Windows. This involves creating the necessary directory structure for logging learnings and implementing PowerShell scripts to handle skill extraction and error detection.

## Proposed Changes

### Configuration/Documentation

#### [NEW] [.learnings/](file:///c:/Users/Chris/.gemini/.learnings/)

Create this directory in the project root for persistent learning storage.

#### [NEW] [.learnings/ERRORS.md](file:///c:/Users/Chris/.gemini/.learnings/ERRORS.md)

Initialize with header for tracking command and tool failures.

#### [NEW] [.learnings/LEARNINGS.md](file:///c:/Users/Chris/.gemini/.learnings/LEARNINGS.md)

Initialize with header for tracking insights and best practices.

#### [NEW] [.learnings/FEATURE_REQUESTS.md](file:///c:/Users/Chris/.gemini/.learnings/FEATURE_REQUESTS.md)

Initialize with header for tracking missing capabilities.

### Skill Assets

#### [NEW] [skills/self-improvement/assets/SKILL-TEMPLATE.md](file:///c:/Users/Chris/.gemini/.agent/skills/self-improvement/assets/SKILL-TEMPLATE.md)

Provide a standard template for new skills.

### Scripts (Windows Core)

#### [NEW] [skills/self-improvement/scripts/activator.ps1](file:///c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/activator.ps1)

A PowerShell script injected into sessions to remind the agent about self-improvement.

#### [NEW] [skills/self-improvement/scripts/error_detector.ps1](file:///c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/error_detector.ps1)

Utility to help identify and flag errors for logging.

#### [NEW] [skills/self-improvement/scripts/extract_skill.ps1](file:///c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/extract_skill.ps1)

PowerShell version of the skill extraction helper.

## Verification Plan

### Manual Verification

1. Verify that `.learnings/` directory is created with all starting files.
2. Run `extract_skill.ps1` with a dummy name to verify skill creation logic.
3. Check that [SKILL.md](file:///c:/Users/Chris/.gemini/.agent/skills/self-improvement/SKILL.md) in the `self-improvement` folder correctly references these new paths.
