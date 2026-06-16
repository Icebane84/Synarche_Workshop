#!/bin/bash
# PHOENIX SYNARCHE: AUTOMATED DOCUMENTATION ENFORCEMENT

echo "[PHOENIX] Initiating Living Document Synchronization..."

# 1. Execute Node.js API Route Extraction
node generate_api_docs.js
if [ $? -ne 0 ]; then
  echo "[ERROR] API documentation generation failed. Commit aborted."
  exit 1
fi

# 2. Execute Python Database Schema Extraction
python generate_schema_docs.py
if [ $? -ne 0 ]; then
  echo "[ERROR] Schema documentation generation failed. Commit aborted."
  exit 1
fi

# 3. Stage the modified Living Document
# Note: Adjust path if "Living Document (Soul).md" is in a specific subdirectory
git add "Living Document/Living Document (Soul).md"

echo "[PHOENIX] Synchronization complete. Living Document updated and staged."
exit 0