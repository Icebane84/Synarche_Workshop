import hashlib
import os

files = {
    "GVRN.Finalization.SevenGates": r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.SevenGates.md",
    "GVRN.Finalization.CanonizationRitual": r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.CanonizationRitual.md",
    "GVRN.Finalization.Protocol": r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.Protocol.md",
    "GVRN.Finalization.Index": r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.Index.md",
    "GVRN.Canonizer.Protocol": r"c:\Users\Chris\Synarche_Workspace\_governance\07_Canonizer\GVRN.Canonizer.Protocol.md",
    "GVRN.Canonizer.Core": r"c:\Users\Chris\Synarche_Workspace\_governance\07_Canonizer\GVRN.Canonizer.Core.md",
    "GVRN.Canonizer.Index": r"c:\Users\Chris\Synarche_Workspace\_governance\07_Canonizer\GVRN.Canonizer.Index.md",
    "GVRN.AvatarSuite.Junction": r"c:\Users\Chris\Synarche_Workspace\_governance\03_AvatarSuite\GVRN.AvatarSuite.Junction.md",
}

workspace_root = r"c:\Users\Chris\Synarche_Workspace"

for artifact_id, path in files.items():
    if os.path.exists(path):
        with open(path, "rb") as rb:
            file_hash = hashlib.sha256(rb.read()).hexdigest()
        rel_path = path.replace(workspace_root, "").lstrip("\\").replace("\\", "/")
        name = os.path.basename(path)
        print(f"{artifact_id}:")
        print(f"  artifact_id: {artifact_id}")
        print(f"  content_hash: {file_hash}")
        print("  domain: GVRN")
        print(f"  official_name: {name}")
        print(f"  path: {rel_path}")
        print('  status: "[CANONIZED]"')
        print("  version: v15.0 [OMEGA]")
    else:
        print(f"# ERROR: {path} NOT FOUND")
