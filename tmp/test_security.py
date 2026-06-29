import sys
import os
sys.path.append(r"c:\Users\Chris\Synarche_Workspace\axion-core\forge")
from security import execute_safe, resolve_path, SovereigntyViolationError

print("Testing normal command...")
try:
    execute_safe(["python", "--version"])
    print("  [PASS] Normal command passed")
except Exception as e:
    print(f"  [FAIL] Normal command failed: {e}")

print("Testing Faraday Cage violation...")
try:
    resolve_path("C:/Windows/System32")
    print("  [FAIL] Traversal failed to block")
except SovereigntyViolationError as e:
    print(f"  [PASS] Traversal blocked successfully: {e}")
