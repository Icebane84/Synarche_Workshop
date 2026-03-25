import os

files = [
    r"_governance\00_Codex\CORE.Codex.Phoenix.md",
    r"_governance\10_Governance\GVRN.HUD.CommandCenter.md",
    r"_governance\10_Governance\GVRN.HUD.Map.md",
    r"_governance\10_Governance\GVRN.AG.003.md",
    r"_governance\10_Governance\GVRN.Sentinel.Umbra.md",
]
root = r"c:\Users\Chris\Synarche_Workspace"

print("--- Resonance Audit ---")
for f in files:
    path = os.path.join(root, f)
    if not os.path.exists(path):
        print(f"{f}: MISSING")
        continue
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        v15 = "v15.0" in content
        canonized = "[CANONIZED]" in content or "STATUS: CANONIZED" in content
        anchor = "[OMNI-ARTIFACT-ANCHOR]" in content
        ts_25 = "2026-03-25" in content
        print(f"{f}: v15={v15}, canonized={canonized}, anchor={anchor}, ts_25={ts_25}")
