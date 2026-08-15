import json
import csv
import sys
from pathlib import Path


def flatten_trunk_output(json_path: str, csv_path: str) -> None:
    """
    Parses Trunk JSON output and flattens it into a CSV for SELT audits.
    Enforces the Phoenix Phase II: FLATTEN_TO_CSV directive.
    """
    json_file = Path(json_path)
    if not json_file.exists():
        print(f"Error: Dissonance Detected. Could not find {json_path}")
        sys.exit(1)

    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)

    # Trunk JSON schema structures issues under a list or a dictionary key depending on the version
    issues = data if isinstance(data, list) else data.get("issues", [])

    if not issues:
        print("Notice: No linting issues found or unrecognized JSON schema.")
        issues = []

    headers = ["File", "Line", "Column", "Linter", "Rule", "Severity", "Message"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for issue in issues:
            # Safely extract fields, mapping Trunk's keys to the SELT audit headers
            file_path = issue.get("file", issue.get("file_path", ""))
            line = issue.get("line", "")
            column = issue.get("column", "")
            linter = issue.get("linter", "")
            rule = issue.get(
                "code", issue.get("rule", "")
            )  # Trunk typically uses 'code' for rule IDs
            severity = issue.get("severity", issue.get("level", ""))
            message = issue.get("message", "")

            writer.writerow(
                {
                    "File": file_path,
                    "Line": line,
                    "Column": column,
                    "Linter": linter,
                    "Rule": rule,
                    "Severity": severity.upper(),
                    "Message": message.replace("\n", " ").strip(),
                }
            )

    print(f"SELT Audit Complete: Flattened {len(issues)} issues to {csv_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python flatten_trunk_csv.py <input_results.json> <output_selt_audit.csv>"
        )
        sys.exit(1)

    flatten_trunk_output(sys.argv[1], sys.argv[2])
