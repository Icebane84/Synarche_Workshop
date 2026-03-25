import os
import re
from typing import List, Dict, Any

# IDENTIFICATION: SYNG.DIAG.LinkAuditor
# VERSION: v1.0 [BETA]
# STATUS: [OPERATIONAL]
# TIMESTAMP: 2026-03-24


class LinkAuditor:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.search_roots = ["_governance", ".agent", "axion-core", "nova_forge"]
        self.broken_links: List[Dict[str, Any]] = []
        self.total_links_scanned = 0

    def scan(self):
        print(f"--- Starting Link Audit: {self.root_dir} ---")

        # Also include root-level .md files
        for item in os.listdir(self.root_dir):
            if item.endswith(".md"):
                self._audit_file(os.path.join(self.root_dir, item))

        for sub_root in self.search_roots:
            full_sub_root = os.path.join(self.root_dir, sub_root)
            if not os.path.exists(full_sub_root):
                continue

            for root, _, files in os.walk(full_sub_root):
                for file in files:
                    if file.endswith(".md"):
                        self._audit_file(os.path.join(root, file))

    def _audit_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Regex for markdown links: [text](url)
        # Excludes images: ![text](url) - Actually, checking images is good too.
        matches = re.finditer(r"\[(.*?)\]\((.*?)\)", content)

        for match in matches:
            self.total_links_scanned += 1
            link_text = match.group(1)
            link_url = match.group(2).strip()

            if self._is_external(link_url) or link_url.startswith("#"):
                continue

            # Strip fragment / query
            clean_url = link_url.split("#")[0].split("?")[0]
            if not clean_url:
                continue

            # Resolve relative path
            file_dir = os.path.dirname(file_path)
            # Handle Windows-style and Unix-style paths
            clean_url = clean_url.replace("/", os.sep)

            resolved_path = os.path.normpath(os.path.join(file_dir, clean_url))

            if not os.path.exists(resolved_path):
                # Calculate line number
                line_no = content.count("\n", 0, match.start()) + 1
                self.broken_links.append(
                    {
                        "file": os.path.relpath(file_path, self.root_dir),
                        "line": line_no,
                        "text": link_text,
                        "url": link_url,
                        "resolved": (
                            os.path.relpath(resolved_path, self.root_dir)
                            if resolved_path.startswith(self.root_dir)
                            else resolved_path
                        ),
                    }
                )

    def _is_external(self, url: str) -> bool:
        return url.startswith(("http://", "https://", "mailto:", "tel:"))

    def report(self):
        print(f"\nAudit complete. Scanned {self.total_links_scanned} links.")
        if not self.broken_links:
            print("RESONANCE ACHIEVED: 0 Broken Links Found.")
            return

        print(f"DISSONANCE DETECTED: {len(self.broken_links)} Broken Links Found.\n")

        # Group by file for readability
        by_file = {}
        for bl in self.broken_links:
            by_file.setdefault(bl["file"], []).append(bl)

        for file, links in by_file.items():
            print(f"File: {file}")
            for l in links:
                print(f"  [L{l['line']}] {l['url']} -> (Resolved: {l['resolved']})")


if __name__ == "__main__":
    auditor = LinkAuditor(os.getcwd())
    auditor.scan()
    auditor.report()
