# Synarche Knowledge Export Manifest
Generated: 2026-07-18T08:06:03.075533

## Upload Order (OpenWebUI → Workspace → Knowledge → New Collection)

| File | Size | Status |
|------|------|--------|
| `SYKB_01_SynarcheCore.md` | 6.4 KB | [OK] |
| `SYKB_02_Architecture.md` | 21.6 KB | [OK] |
| `SYKB_03_Registries.md` | 7.9 KB | [OK] |
| `SYKB_04_CodingStandards.md` | 342.8 KB | [LARGE] |

## How to Use in OpenWebUI
1. Go to **Workspace → Knowledge → + New Collection**
2. Name it: `Synarche-Core`
3. Upload all `SYKB_*.md` files
4. In any chat, type `#Synarche-Core` to ground the model in these docs

## How to Use in Continue
The `@codebase` context provider in your config.json already indexes your
source files. For governance context, use `@docs` and reference the
Phoenix Codex or PRS-001 PathMapping.
