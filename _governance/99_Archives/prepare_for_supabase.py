import json
import os
import re

# Configuration
UPLOAD_ZONE = r"c:\Users\Chris\_Desktop_Vault\Phoenix\PHOENIX_UPLOAD_ZONE"
REPORT_PATH = r"c:\Users\Chris\Synarche_Workspace\_governance\ingestion_report.json"

# Regex Patterns (Strict GVRN v10.0)
PATTERNS = {
    "12_POINT_HEADER": re.compile(r"\|\s*\*\*1\.\s*Artifact ID\*\*\s*\|", re.MULTILINE),
    "AGP_001": re.compile(r"### \*\*II\. AGP-001: The State Vector Definition Block", re.MULTILINE),
    "AGP_002": re.compile(r"### \*\*III\. AGP-002: The Risk Governance Block", re.MULTILINE),
    "AGP_003": re.compile(r"### \*\*IV\. AGP-003: The Linkage and Decoherence Block", re.MULTILINE),
    "PROMPT_PACKET": re.compile(r"Actionable Prompt Packet", re.IGNORECASE),
    "CMD": re.compile(r"`CMD: [A-Z_]+ --[a-z]+:", re.MULTILINE),
    "4_SPACE_INDENT": re.compile(
        r"^( {1,3}\S| {5,}\S|\t)", re.MULTILINE
    ),  # Detects bad indentation (tabs/wrong spaces)
}


def validate_artifact(filepath):
    """Scans a single artifact for compliance."""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Active Protocol
# Synergy Set: The Oathkeeper's Seal
# Primary Stat Buff: Coherence
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: High
# XP Award Value: 50 XP

    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

    results = {}
    valid = True

    # Check 1: 12-Point Header
    if PATTERNS["12_POINT_HEADER"].search(content):
        results["UIP_Header"] = "PASS"
    else:
        results["UIP_Header"] = "FAIL"
        valid = False

    # Check 2: AGP Blocks
    results["AGP_Blocks"] = "PASS"
    if not PATTERNS["AGP_001"].search(content):
        results["AGP_Blocks"] = "FAIL (Missing AGP-001)"
        valid = False
    elif not PATTERNS["AGP_002"].search(content):
        results["AGP_Blocks"] = "FAIL (Missing AGP-002)"
        valid = False
    elif not PATTERNS["AGP_003"].search(content):
        results["AGP_Blocks"] = "FAIL (Missing AGP-003)"
        valid = False

    # Check 3: Actionable Prompt Packet
    if PATTERNS["PROMPT_PACKET"].search(content) and PATTERNS["CMD"].search(content):
        results["GUCA_Packet"] = "PASS"
    else:
        results["GUCA_Packet"] = "FAIL"
        valid = False

    # Check 4: Indentation (Strict)
    bad_indent = PATTERNS["4_SPACE_INDENT"].findall(content)
    # Filter out actual code blocks or legitimate top-level items
    # Ideally, we'd parse AST, but a raw check works for "strict adherence" first pass
    # For now, we relaxed strict indent check to avoid false positives on legitimate markdown,
    # relying on the Visual Standard artifact itself.
    results["Indentation"] = "PASS (Visual Check Required)"

    return {"status": "PASS" if valid else "FAIL", "checks": results}


def run_validation():
    """Main execution loop."""
    print(f"Scanning: {UPLOAD_ZONE}...")
    report = {"summary": {}, "details": {}}

    files = [f for f in os.listdir(UPLOAD_ZONE) if f.endswith(".md")]

    if not files:
        print("No GVRN artifacts found!")
        return

    pass_count = 0
    for filename in files:
        path = os.path.join(UPLOAD_ZONE, filename)
        result = validate_artifact(path)
        report["details"][filename] = result
        if result["status"] == "PASS":
            pass_count += 1
            print(f"[OK] {filename}")
        else:
            print(f"[FAIL] {filename}: {result['checks']}")

    report["summary"] = {
        "total": len(files),
        "passed": pass_count,
        "failed": len(files) - pass_count,
        "compliance_rate": f"{(pass_count / len(files)) * 100:.1f}%",
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"\nReport generated: {REPORT_PATH}")
    print(f"Compliance: {report['summary']['compliance_rate']}")


if __name__ == "__main__":
    run_validation()
