# Phase 8: Reconciliation Engine
# Formats language-specific comment blocks and handles safe, non-destructive file updates

import os
import yaml
import textwrap

class Reconciler:
    @staticmethod
    def wrap_anchor_block(metadata: dict, ext: str) -> str:
        """Formats and encloses metadata in comment delimiters matching the target file type,
        injecting formatter-ignore flags to prevent IDE mangling on save.
        """
        yaml_str = yaml.dump(metadata, sort_keys=False, default_flow_style=False)
        indented_yaml = "artifact_anchor:\n" + textwrap.indent(yaml_str, "  ")

        ext = ext.lower()
        if ext == ".py":
            # Python formatters leave column-0 module-level docstrings alone
            return f'"""\n{indented_yaml}"""'
        elif ext in (".js", ".ts"):
            # Prepend prettier-ignore to prevent JS/TS IDE comment-collapse mangling
            return f'// prettier-ignore\n/*\n{indented_yaml}*/'
        elif ext == ".html":
            # Prepend prettier-ignore to prevent HTML comment reformatting
            return f'<!-- prettier-ignore -->\n<!--\n{indented_yaml}-->'
        elif ext == ".md":
            # Markdown frontmatter is natively recognized and left untouched by standard formatters
            return f'---\n{indented_yaml}---'
        return indented_yaml

    @staticmethod
    def prompt_interactive_reconciliation(file_path: str, diagnostics: list[dict]) -> bool:
        """Interactively requests permission via terminal stdin before applying code edits."""
        filename = os.path.basename(file_path)
        print(f"\n[RECONCILIATION NEEDED] file: {filename}")
        for diag in diagnostics:
            icon = "❌" if diag["severity"] == "ERROR" else ("⚠️" if diag["severity"] == "WARNING" else "ℹ️")
            print(f"  {icon} {diag['severity']}: {diag['msg']}")
        
        try:
            choice = input(f"Apply standardizations to '{filename}'? [y/N]: ").strip().lower()
            return choice == 'y'
        except (KeyboardInterrupt, EOFError):
            print("\nReconciliation prompt bypassed.")
            return False
