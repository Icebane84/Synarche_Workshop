import hashlib
import os

files = [
    r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.SevenGates.md",
    r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.CanonizationRitual.md",
    r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.Protocol.md",
    r"c:\Users\Chris\Synarche_Workspace\_governance\04_Finalization\GVRN.Finalization.Index.md",
    r"c:\Users\Chris\Synarche_Workspace\_governance\07_Canonizer\GVRN.Canonizer.Protocol.md",
    r"c:\Users\Chris\Synarche_Workspace\_governance\07_Canonizer\GVRN.Canonizer.Core.md",
    r"c:\Users\Chris\Synarche_Workspace\_governance\07_Canonizer\GVRN.Canonizer.Index.md",
    r"c:\Users\Chris\Synarche_Workspace\_governance\03_AvatarSuite\GVRN.AvatarSuite.Junction.md",
]

for f in files:
    if os.path.exists(f):
        with open(f, "rb") as rb:
            file_hash = hashlib.sha256(rb.read()).hexdigest()
            print(f"{file_hash} | {f}")
    else:
        print(f"NOT_FOUND | {f}")
