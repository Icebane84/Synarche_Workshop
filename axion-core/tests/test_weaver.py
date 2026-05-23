"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-TEST-WEAVER-001`                | The Sovereign ID. |
| **Official Name** | `test_weaver.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import argparse
import os
import subprocess
import sys


def test_weaver(target: str) -> None:
    """Run pytest on the target directory and report results."""
    print(f"\n>>> TEST WEAVER: Running pytest on {target}\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", target, "--tb=short", "-q", "--no-header"],
        capture_output=True,
        text=True,
        check=False,
    )

    output = result.stdout + result.stderr
    lines = output.splitlines()

    sum(1 for l in lines if " passed" in l)
    failed = sum(1 for l in lines if " failed" in l)
    errors = sum(1 for l in lines if " error" in l)

    # Extract final summary line
    summary_line = ""
    for line in reversed(lines):
        if (
            "passed" in line
            or "failed" in line
            or "error" in line
            or "no tests ran" in line
        ):
            summary_line = line.strip()
            break

    print("=" * 60)
    print("  TEST WEAVER — COHERENCE VERIFICATION REPORT".center(60))
    print("=" * 60)
    print(output[:2000] if output else "  No output from pytest.")
    print("-" * 60)
    print(f"  Summary: {summary_line}")

    if failed == 0 and errors == 0:
        print("\n[OK] ALL TESTS PASSING. Coherence Intact.")
    else:
        print(f"\n[!!] COHERENCE BROKEN: {failed} failures, {errors} errors detected.")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test Weaver — Coherence Verification Engine"
    )
    parser.add_argument(
        "target", nargs="?", default=".", help="Directory to test (default: cwd)."
    )
    args = parser.parse_args()
    test_weaver(os.path.abspath(args.target))


if __name__ == "__main__":
    main()
