---
name: "sentinel-audit"
description: "Enforces compliance, lints artifacts, and verifies 'Zero Entropy'."
tools:
  - name: "run_audit"
    command: "python tools/compliance_audit.py --target {target_file}"
---
