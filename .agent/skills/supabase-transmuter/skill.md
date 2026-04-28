---
name: "supabase-transmuter"
description: "Interface for the Great Refactor. Reads/Writes to Supabase."
tools:
  - name: "scan_legacy"
    command: "python .agent/skills/supabase-transmuter/alchemy.py fetch"
  - name: "diff_content"
    command: "python .agent/skills/supabase-transmuter/alchemy.py diff {old} {new}"
  - name: "commit_transmutation"
    command: "python .agent/skills/supabase-transmuter/alchemy.py commit {id} {title} {content_file} {meta_json}"
---