# RPG Achievement Enhancements & Celestial Chart UI

This plan outlines the steps to finalize the Achievement System and the Celestial Chart sidebar UI, ensuring robust operation even in "offline" mode (no Supabase connection).

## User Review Required

> [!IMPORTANT]
> The current Supabase environment is unreachable. I will be implementing a local persistence layer for achievements (saving to `data/player_achievements.json`) so the UI is fully functional during development.

## Proposed Changes

### [Backend] CLI and RPG Manager Harmonization

#### [MODIFY] [rpg_manager.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/rpg_manager.py)
- Update `claim_achievement` to support local persistence when Supabase is unavailable.
- Save claimed achievement IDs to `data/player_achievements.json`.
- Ensure `get_achievements` reads from this local file as a fallback.
- Enhance `get_status` to return a unified object suitable for JSON serialization.

#### [MODIFY] [cli.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/cli.py)
- Add `do_get_player_state` command that returns JSON state.
- Add `do_get_achievements` command that returns JSON list.
- Update `do_claim_achievement` to handle both CLI and Extension call formats.
- Implement `--json` flag support for all RPG-related commands.

### [UI/UX] Celestial Chart Sidebar

#### [MODIFY] [CelestialChartView.ts](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/CelestialChartView.ts)
- Update HTML to support dynamic rendering of achievements.
- Implement messaging between Webview and Extension for claiming achievements.

#### [NEW] [main.js](file:///c:/Users/Chris/Synarche_Workspace/axion-core/media/main.js)
- Handle message passing from extension.
- Render achievement items dynamically.
- Handle "Claim" button clicks.
- Update stardust and rank displays.

#### [MODIFY] [main.css](file:///c:/Users/Chris/Synarche_Workspace/axion-core/media/main.css)
- Polish "Liquid Glass" effects.
- Add animations for "Stardust Synthesis" and achievement unlocking.

### [Integration] Extension Lifecycle

#### [MODIFY] [extension.ts](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/extension.ts)
- Harmonize CLI calls to match the new `cli.py` syntax.
- Ensure periodic background refresh updates the sidebar correctly.

## Verification Plan

### Automated Tests
- Run `tests/test_rpg_achievements.py` (updating it to handle the local fallback).
- Run `pytest src/logic/rpg_manager.py` (if applicable).

### Manual Verification
- Open the "Celestial Chart" view in VS Code sidebar.
- Verify that stardust count and achievements load correctly from local JSON.
- Click "Claim" on an achievement and verify it updates to "COMPLETED" and awards stardust.
- Use CLI `axion QUERY_LORE "synarche"` to verify lore querying works.
