#!/usr/bin/env python3
"""# TOOL-AES-002: Luminous Coherence Aesthetic Auditor
# Domain: ARCH | Tag: AES
# Purpose: Audits UI/Config files for strict adherence to the Luminous Coherence "Sacred Canon" (METRIC-AES-002).
# Differentiates from TOOL-AES-001 (Algorithmic Elegance) by focusing on Visual Design compliance.
"""

import argparse
import os
import re

# --- THE SACXHRED CANON (METRIC-AES-002) ---
SACRED_COLORS = {
    # Base
    "base-black": ["#000000"],
    "deep-void": ["rgb(12 10 17)", "rgb(12, 10, 17)", "#0c0a11"],
    # Accent (Coherence)
    "coherence-high": ["rgb(52 211 255)", "rgb(52, 211, 255)", "#34d3ff"],  # Cyan-400
    "coherence-mid": ["rgb(139 92 246)", "rgb(139, 92, 246)", "#8b5cf6"],  # Violet-500
    "coherence-low": ["rgb(99 102 241)", "rgb(99, 102, 241)", "#6366f1"],  # Indigo-500
    # Status
    "warning": ["rgb(251 191 36)", "rgb(251, 191, 36)", "#fbbf24"],  # Amber-400
    "error": ["rgb(239 68 68)", "rgb(239, 68, 68)", "#ef4444"],  # Red-500
}

SACRED_MOTION = ["geode-pulse", "data-flow"]
SACRED_FONTS = ["Inter", "Fira Code"]

# Regex for finding hex codes and rgb values
HEX_REGEX = r"#[0-9a-fA-F]{6}"
RGB_REGEX = r"rgb\(\s*\d+\s*,?\s*\d+\s*,?\s*\d+\s*\)"


def audit_file(filepath):
    print(f"\n[AES-VISUAL] Auditing Luminous Coherence: {os.path.basename(filepath)}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        return

    score = 10.0
    violations = []
    compliance_points = 0

    # 1. Color Audit
    # flattened list of sacred values
    [val for sublist in SACRED_COLORS.values() for val in sublist]

    # Find all colors in file
    found_hex = re.findall(HEX_REGEX, content)
    found_rgb = re.findall(RGB_REGEX, content)
    all_found_colors = found_hex + found_rgb

    for color in all_found_colors:
        # Normalize for comparison (simple lower case and strip spaces for rgb)
        norm_color = color.lower().replace(" ", "")
        is_sacred = False

        for _name, values in SACRED_COLORS.items():
            for val in values:
                if norm_color == val.lower().replace(" ", ""):
                    is_sacred = True
                    compliance_points += 1
                    break
            if is_sacred:
                break

        if not is_sacred:
            violations.append(f"Unauthorized Color: {color}")
            score -= 0.5

    # 2. Motion Audit
    # Simple keyword check for sacred motion tokens
    for motion in SACRED_MOTION:
        if motion in content:
            compliance_points += 2

    # 3. Typography Audit
    for font in SACRED_FONTS:
        if font in content:
            compliance_points += 2

    # Final Verification
    if compliance_points == 0 and len(violations) == 0:
        print("  > No Aesthetic definitions found. (Neutral)")
        return

    # Cap Score
    score = max(0.0, min(10.0, score))

    print(f"  > Compliance Points: {compliance_points}")
    print(f"  > Violations: {len(violations)}")
    print(f"  > Visual AES: {score:.1f}/10.0")

    if violations:
        print("  > [!] Dissonance Detected:")
        for v in violations[:5]:  # Show top 5
            print(f"      - {v}")
        ifbw = len(violations) > 5
        if ifbw:
            print(f"      ... and {len(violations) - 5} more.")

    if score >= 9.0:
        print("  💎 Status: LUMINOUS (Coherent)")
    elif score >= 6.0:
        print("  🔹 Status: DIM (Partial Coherence)")
    else:
        print("  🌑 Status: VOID (Dissonant)")


def main():
    parser = argparse.ArgumentParser(
        description="Audit Luminous Coherence (AES-Visual)"
    )
    parser.add_argument("target", help="File to audit (css, js, tsx, etc.)")
    args = parser.parse_args()

    if os.path.isfile(args.target):
        audit_file(args.target)
    else:
        print("Target is not a file.")


if __name__ == "__main__":
    main()
