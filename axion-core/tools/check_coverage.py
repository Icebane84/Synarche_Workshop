import sys
import re

def parse_coverage(report_path: str) -> float:
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return None
    # Matches the standard pytest-cov TOTAL line
    match = re.search(r'^TOTAL\s+.*\s+(\d+)%$', content, re.MULTILINE)
    if not match:
        return None
    return float(match.group(1))

def check_coverage(report_path: str, threshold: float, baseline_path: str = None) -> bool:
    """
    Parses the pytest-cov terminal report and verifies coverage meets the sovereign threshold.
    Optionally compares against a baseline report to track delta.
    """
    coverage_pct = parse_coverage(report_path)
    if coverage_pct is None:
        print(f"[FAIL] Could not parse TOTAL coverage from {report_path}")
        return False
        
    print(f"[*] Detected Total Test Coverage: {coverage_pct}%")
    
    if baseline_path:
        baseline_pct = parse_coverage(baseline_path)
        if baseline_pct is not None:
            delta = coverage_pct - baseline_pct
            sign = "+" if delta > 0 else ""
            delta_str = f"{sign}{delta:.2f}%"
            print(f"[*] Coverage Delta vs Main: {delta_str}")
            with open("coverage_delta.txt", "w", encoding="utf-8") as f:
                f.write(delta_str)
            if delta < 0:
                print(f"[WARNING] Coverage has decreased by {abs(delta):.2f}%.")
        else:
            print(f"[WARNING] Could not parse baseline coverage from {baseline_path}")

    if coverage_pct < threshold:
        print(f"[SOVEREIGNTY VIOLATION] Coverage {coverage_pct}% is below the required minimum of {threshold}%.")
        return False
        
    print(f"[PASS] Coverage {coverage_pct}% meets or exceeds the {threshold}% threshold.")
    return True

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage: python check_coverage.py <report.txt> <threshold> [baseline_report.txt]")
        sys.exit(1)
        
    report = sys.argv[1]
    threshold = float(sys.argv[2])
    baseline = sys.argv[3] if len(sys.argv) == 4 else None
    
    success = check_coverage(report, threshold, baseline)
    # Fails the CI/CD pipeline if the threshold is violated
    sys.exit(0 if success else 1)