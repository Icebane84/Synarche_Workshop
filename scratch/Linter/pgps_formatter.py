#!/usr/bin/env python3
"""
# GVRN.Tool.PgpsFormatter
# ID: GVRN.Tool.PgpsFormatter
# Version: v15.1 [ETERNAL]
# Domain: GVRN
# Status: ACTIVE
# Objective: Programmatically enforce and auto-correct Markdown files to comply with
#            the Phoenix Genesis Presentation Standard (AOP-PGPS-001) using deterministic heuristics.
"""

import argparse
import datetime  # For time formatting
import json
import os
import re  # For regex operations
import uuid  # For UUID validation
from typing import Any, Dict, List, Tuple

try:
    from dateutil.parser import parse as date_parse
except ImportError:
    print("Warning: 'python-dateutil' library not found. Date formatting will be skipped. Please run 'pip install python-dateutil'.")
    date_parse = None
try:
    import pathspec
except ImportError:
    print("Warning: 'pathspec' library not found. .gitignore patterns will not be respected. Please run 'pip install pathspec'.")
    pathspec = None


class PgpsConfigLoader:
    """Utility to load configuration from .pgps-formatter.json."""
    @staticmethod
    def load_config(start_dir: str) -> Dict[str, Any] | None:
        config_name = ".pgps-formatter.json"
        current_dir = start_dir
        # Search up to 3 levels up or until root
        for _ in range(4):
            config_path = os.path.join(current_dir, config_name)
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    return {} # Return default on error
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir: # Reached root
                break
            current_dir = parent_dir
        return None

DEFAULT_FORMATTER_CONFIG = {
  "headings": {
    "style": "atx",
    "number_headings": False,
    "numbering_style": "decimal"
  },
  "inclusive_language": {
    "replacements": [
      {"find": "\\b(whitelist|blacklist)(s?)\\b", "replace": "allowlist/denylist$2"},
      {"find": "\\b(master|slave)(s?)\\b", "replace": "primary/replica$2"},
      {"find": "\\b(man|men)\\b", "replace": "person"},
      {"find": "\\bguys\\b", "replace": "folks"}
    ]
  },
  "list_formatting": {
    "convert_bullets_to_numbered_threshold": 0,
    "ordered_list_style": "decimal"
  },
  "table_formatting": {
    "sort_by_column": -1,
    "sort_order": "asc",
    "add_total_row": False,
    "format_numbers": False
  },
  "toc": {
    "max_depth": 6
  },
  "time_formatting": {
    "timezone_replacements": {
      "PST": "UTC-8",
      "PDT": "UTC-7",
      "EST": "UTC-5",
      "EDT": "UTC-4",
      "CST": "UTC-6",
      "CDT": "UTC-5",
      "MST": "UTC-7",
      "MDT": "UTC-6",
      "GMT": "UTC+0",
      "CET": "UTC+1",
      "CEST": "UTC+2"
    }
  },
  "files_to_process": []
}


class PgpsFormatter:
    """
    Automates the formatting of PGPS-001 standards using deterministic heuristics
    to eliminate 'Scribal Errors' and ensure structural and layout clarity.
    """

    def __init__(self, target_path: str, dry_run: bool = False):
        self.target_path = os.path.abspath(target_path)
        self.dry_run = dry_run
        self.logs: List[str] = []
        config_data = PgpsConfigLoader.load_config(self.target_path)
        if config_data is None:
            self.logs.append("[CONFIG-WARN] No .pgps-formatter.json found. Running with default settings.")
            self.config = {}
        else:
            self.config = config_data
        self.file_anchor_cache: Dict[str, List[str]] = {} # Cache for link validation
        self.corrections_count = 0

    def log_correction(self, rule_id: str, desc: str, file_name: str, line_no: int = -1):
        self.corrections_count += 1
        line_str = f"Line {line_no}: " if line_no != -1 else ""
        self.logs.append(f"[{rule_id}] {file_name} -> {line_str}{desc}")

    def format_document(self, file_path: str) -> Tuple[str, bool]:
        """
        Parses and auto-corrects a single Markdown document against core PGPS-001 mandates.
        Returns the formatted string and a boolean indicating if mutations occurred.
        """
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        except IOError as e:
            self.logs.append(f"[IO-ERROR] Failed to read {file_name}: {e}")
            return "", False
 
        mutated = False
        formatted_lines: List[str] = []
        in_code_block = False
        
        heading_style = self.config.get("headings", {}).get("style", "atx")

        i = 0
        while i < len(lines):
            new_line = lines[i]
            line_mutated = False
 
            block_processed = False
            processed_block_lines: List[str] = []
            consumed_lines = 1 # Default to consuming 1 line if no block handler

            # Try block-level processors first
            if new_line.strip().startswith("```"):
                processed_block_lines, consumed_lines, block_mutated = self._process_code_block(lines, i, file_name, in_code_block)
                in_code_block = not in_code_block # Toggle code block state
                block_processed = True
            elif in_code_block: # If inside a code block, just append and continue
                formatted_lines.append(new_line)
                i += 1
                continue
            elif i + 1 < len(lines) and self._is_table_separator(lines[i+1]):
                processed_block_lines, consumed_lines, block_mutated = self._format_table(lines[i:], file_name, i + 1)
                block_processed = True
            elif i + 1 < len(lines): # Setext heading needs to look ahead
                processed_block_lines, consumed_lines, block_mutated = self._process_setext_heading(lines, i, file_name, heading_style)
                if consumed_lines > 0: # Only if it was actually a Setext heading
                    block_processed = True

            if block_processed:
                formatted_lines.extend(processed_block_lines)
                i += consumed_lines
                if block_mutated:
                    mutated = True
            else:
                # If no block processor handled it, run line-by-line formatters
                new_line, line_was_mutated = self._run_line_formatters(new_line, file_name, i + 1)
                if line_was_mutated:
                    line_mutated = True
 
                if line_mutated:
                    mutated = True
                formatted_lines.append(new_line)
                i += 1 # Consume 1 line for line-by-line processing

        # Post-processing stages (already somewhat declarative)
        processed_lines_after_blocks, block_mutated = self._apply_list_block_formatting(formatted_lines, file_name)
        if block_mutated:
            mutated = True
        final_lines, spacing_mutated = self._clean_spacing(processed_lines_after_blocks, file_name)
        if spacing_mutated:
            mutated = True

        # Apply heading numbering
        final_lines, numbering_mutated = self._apply_heading_numbering(final_lines, file_name)
        if numbering_mutated:
            mutated = True

        # Final pass for document-wide transformations like TOC
        final_lines, toc_mutated = self._generate_table_of_contents(final_lines, file_name)
        if toc_mutated:
            mutated = True
        return "\n".join(final_lines) + "\n", mutated
 
    def _process_code_block(self, lines: List[str], start_index: int, file_name: str, in_code_block_state: bool) -> Tuple[List[str], int, bool]:
        """Processes a fenced code block, ensuring language is declared."""
        mutated = False
        block_lines: List[str] = []
        
        # Start of code block
        current_line = lines[start_index]
        block_lines.append(current_line)
        
        # Rule: Code blocks must declare language if it's the opening fence
        if not in_code_block_state and len(current_line.strip()) == 3: # Only ```, no language specified
            new_line = "```text"
            self.log_correction("INDENT-CODE-FENCED-001", "Declared default 'text' language for code block", file_name, start_index + 1)
            block_lines[0] = new_line
            mutated = True
        
        consumed_lines = 1
        i = start_index + 1

        # Content of code block
        while i < len(lines):
            current_line = lines[i]
            block_lines.append(current_line)
            consumed_lines += 1
            if current_line.strip().startswith("```"):
                break # End of code block
            i += 1
        
        return block_lines, consumed_lines, mutated

    def _process_setext_heading(self, lines: List[str], start_index: int, file_name: str, heading_style: str) -> Tuple[List[str], int, bool]:
        """Converts Setext headings to ATX style if configured."""
        mutated = False
        
        if heading_style == "atx" and start_index + 1 < len(lines):
            current_line = lines[start_index]
            next_line = lines[start_index+1].strip()
            
            if next_line and all(c == '=' for c in next_line):
                new_heading = f"# {current_line.strip()}"
                self.log_correction("INDENT-H-002", "Converted Setext H1 to ATX heading", file_name, start_index + 1)
                return [new_heading], 2, True # Consume current line and underline
            elif next_line and all(c == '-' for c in next_line):
                new_heading = f"## {current_line.strip()}"
                self.log_correction("INDENT-H-002", "Converted Setext H2 to ATX heading", file_name, start_index + 1)
                return [new_heading], 2, True # Consume current line and underline
        
        return [], 0, False # Not a Setext heading or not converting

    def _run_line_formatters(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Runs a pipeline of formatting functions on a single line."""
        mutated = False
        formatters = [
            self._format_heading,
            self._format_list_item,
            self._format_nested_list,
            self._format_inclusive_language,
            self._format_date_strings,
            self._format_time_strings,
            self._format_timezone_strings,
            self._format_uuids,
            self._format_mac_addresses,
            self._check_broken_links,
        ]
        
        # Special case for horizontal rule as it doesn't need file_name/line_no
        line, hr_mutated = self._format_horizontal_rule(line)
        if hr_mutated:
                mutated = True
        for formatter in formatters:
            line, was_mutated = formatter(line, file_name, line_no)
            if was_mutated:
                mutated = True
        return line, mutated

    def _format_heading(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Standardizes ATX heading format."""
        if not line.lstrip().startswith("#"):
            return line, False
        
        match = re.match(r"^(#{1,6})\s*(.*?)\s*#*$", line)
        if not match:
            return line, False

        hashes, title_text = match.groups()
        reconstructed = f"{hashes} {title_text.strip()}"
        if line != reconstructed:
            self.log_correction("INDENT-H-001", f"Standardized heading to '{reconstructed}'", file_name, line_no)
            return reconstructed, True
        return line, False
 
    def _format_list_item(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Converts '*' and '+' list markers to '-' and ensures proper spacing."""
        match = re.match(r"^(\s*)([*+])(\s+.*)$", line)
        if match:
            indent, char, item_text = match.groups()
            reconstructed = f"{indent}- {item_text}"
            self.log_correction("INDENT-LIST-001", f"Converted list marker from '{char}' to '-'", file_name, line_no)
            return reconstructed, True
        return line, False
 
    def _format_nested_list(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Corrects indentation for nested list items to multiples of 4 spaces."""
        match = re.match(r"^(\s+)-\s+(.*)$", line)
        if match:
            spaces_str, item_text = match.groups()
            spaces = len(spaces_str)
            if spaces % 4 != 0:
                target_spaces = round(spaces / 4.0) * 4
                if target_spaces == 0: # Ensure at least 4 spaces for a nested item
                    target_spaces = 4 
                reconstructed = f"{' ' * target_spaces}- {item_text}"
                self.log_correction("INDENT-NEST-LIST-001", f"Aligned nested list indentation from {spaces} to {target_spaces} spaces", file_name, line_no)
                return reconstructed, True
        return line, False
 
    def _format_horizontal_rule(self, line: str) -> Tuple[str, bool]:
        """Standardizes horizontal rules to '---'."""
        trimmed = line.strip()
        # Match any combination of 3 or more *, -, or _ characters, optionally separated by spaces
        if re.fullmatch(r"(\* *){3,}|(- *){3,}|(_ *){3,}", trimmed) and trimmed != "---": # type: ignore
            return "---", True
        return line, False

    def _format_inclusive_language(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        def _preserve_case_replacement(original_word: str, replacement: str) -> str:
            if not original_word:
                return replacement
            if original_word.isupper(): # All caps
                return replacement.upper()
            if original_word.isupper(): # Title case
                return replacement.capitalize()
            return replacement

        """Finds and replaces non-inclusive terms based on the configuration."""
        inclusive_config = self.config.get("inclusive_language", {})
        replacement_rules: List[Dict[str, str]] = inclusive_config.get("replacements", [])
        if not replacement_rules:
            return line, False

        mutated = False
        current_line = line
        for rule in replacement_rules:
            find_pattern = rule.get("find")
            replace_string = rule.get("replace")
            
            if not find_pattern or not replace_string:
                continue # Skip malformed rules

            pattern = re.compile(find_pattern, re.IGNORECASE)

            new_line_after_rule, num_replacements = pattern.subn(
                lambda m: _preserve_case_replacement(m.group(0), replace_string), current_line
            )
            
            if num_replacements > 0:
                if not mutated: # Log only the first time a replacement occurs on this line
                    self.log_correction("STYLE-INCLUSIVE-001", "Applied inclusive language replacement", file_name, line_no)
                current_line = new_line_after_rule
                mutated = True
        return current_line, mutated
 
    def _format_date_strings(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Finds and reformats common date strings to ISO 8601 format (YYYY-MM-DD)."""
        if not date_parse:
            return line, False

        # Regex to find various common date formats.
        # This is not exhaustive but covers many cases.
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # 07-28-2026, 28/07/26
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b' # July 28, 2026
        ]
        
        mutated = False
        for pattern in date_patterns:
            for match in re.finditer(pattern, line):
                date_str = match.group(0)
                try:
                    iso_date: str = date_parse(date_str).strftime('%Y-%m-%d')
                    line = line.replace(date_str, iso_date)
                    self.log_correction("STYLE-DATE-001", f"Reformatted date '{date_str}' to ISO 8601", file_name, line_no)
                    mutated = True
                except (ValueError, TypeError):
                    continue # Ignore strings that look like dates but can't be parsed
        return line, mutated

    def _format_time_strings(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Finds and reformats common time strings to ISO 8601 format (HH:MM:SS)."""
        if not date_parse:
            return line, False

        # Regex to find common time formats
        time_pattern = r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?\b'
        
        mutated = False
        for match in re.finditer(time_pattern, line):
            time_str = match.group(0)
            try:
                # Use a default date to allow the parser to focus on the time
                parsed_time: datetime.datetime = date_parse(time_str, default=datetime.datetime(2000, 1, 1))
                iso_time = parsed_time.strftime('%H:%M:%S')
                line = line.replace(time_str, iso_time)
                self.log_correction("STYLE-TIME-001", f"Reformatted time '{time_str}' to 24-hour format", file_name, line_no)
                mutated = True
            except (ValueError, TypeError):
                continue # Ignore strings that look like times but can't be parsed
        return line, mutated

    def _format_timezone_strings(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Replaces common timezone abbreviations with their UTC offset."""
        tz_config = self.config.get("time_formatting", {})
        tz_replacements = tz_config.get("timezone_replacements", {})
        if not tz_replacements:
            return line, False

        mutated = False
        for abbr, offset in tz_replacements.items():
            # Use a regex to match the abbreviation as a whole word
            pattern = re.compile(r'\b' + re.escape(abbr) + r'\b', re.IGNORECASE)
            if pattern.search(line):
                line = pattern.sub(offset, line)
                self.log_correction("STYLE-TIME-002", f"Replaced timezone '{abbr}' with '{offset}'", file_name, line_no)
                mutated = True
        
        return line, mutated

    def _format_mac_addresses(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Finds and reformats MAC addresses to a consistent AA:BB:CC:DD:EE:FF format."""
        # Regex to find common MAC address patterns (with colons, hyphens, or dots, and mixed case)
        mac_pattern = re.compile(r'\b(?:[0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}\b|\b(?:[0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}\b')
        
        mutated = False
        
        def to_standard_mac(match: re.Match) -> str:
            nonlocal mutated
            original_mac = match.group(0)
            # Remove all non-alphanumeric characters and convert to uppercase
            cleaned_mac = re.sub(r'[^0-9a-fA-F]', '', original_mac).upper()
            # Reformat to AA:BB:CC:DD:EE:FF
            standard_mac = ':'.join(cleaned_mac[i:i+2] for i in range(0, 12, 2))
            
            if original_mac != standard_mac:
                mutated = True
            return standard_mac

        new_line = re.sub(mac_pattern, to_standard_mac, line)

        if mutated:
            self.log_correction("STYLE-MAC-001", "Standardized MAC address format", file_name, line_no)

        return new_line, mutated

    def _format_uuids(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Finds, validates, and reformats all UUIDs to a consistent lowercase format."""
        uuid_pattern = re.compile(r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b')

        mutated = False
        
        def to_lower(match: re.Match) -> str:
            nonlocal mutated
            uuid_str = match.group(0)
            try:
                # Validate UUID and get its version/variant
                parsed_uuid: uuid.UUID = uuid.UUID(uuid_str)
                if uuid_str != str(parsed_uuid).lower(): # Check if formatting is needed
                    mutated = True
                    self.log_correction("STYLE-UUID-001", f"Standardized UUID to lowercase (Version: {parsed_uuid.version}, Variant: {parsed_uuid.variant.name})", file_name, line_no)
                return str(parsed_uuid).lower() # Always return lowercase canonical form
            except ValueError:
                # If it matches the pattern but isn't a valid UUID, don't modify and log
                self.log_correction("STYLE-UUID-001", f"Found string matching UUID pattern but is invalid: '{uuid_str}'", file_name, line_no)
                return uuid_str # Return original if invalid

        return re.sub(uuid_pattern, to_lower, line), mutated

    def _is_table_separator(self, line: str) -> bool:
        """Checks if a line is a valid markdown table separator."""
        return "|" in line and "-" in line and re.search(r"^\s*\|?[-:|\s]+\|?\s*$", line) is not None

    def _format_table(self, table_lines: List[str], file_name: str, start_line_no: int) -> Tuple[List[str], int, bool]: # type: ignore
        """Parses and reformats a markdown table for visual alignment."""
        header_line: str = table_lines[0]
        separator_line = table_lines[1]

        # 1. Parse table content
        table_data = []
        header_cells = [cell.strip() for cell in header_line.strip().strip("|").split("|")]
        num_cols = len(header_cells)
        table_data.append(header_cells)
        
        alignments = []
        separator_cells = [cell.strip() for cell in separator_line.strip().strip("|").split("|")]
        # Normalize separator cells to handle cases where they don't match header column count
        while len(separator_cells) < num_cols:
            separator_cells.append("---")
        separator_cells = separator_cells[:num_cols]

        body_lines = []
        for cell_content in separator_cells:
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')

        lines_consumed = 2
        for line in table_lines[2:]:
            if not line.strip().startswith("|"):
                break
            body_lines.append(line)
            lines_consumed += 1
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            while len(cells) < num_cols: # type: ignore
                cells.append("")
            table_data.append(cells[:num_cols])

        # 2. Calculate max width for each column
        col_widths: List[int] = [0] * num_cols
        for row in table_data:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))
        
        # --- New Sorting Logic ---
        table_config = self.config.get("table_formatting", {})
        sort_col_idx = table_config.get("sort_by_column", -1)
        sort_order = table_config.get("sort_order", "asc")

        if 0 <= sort_col_idx < num_cols:
            body_rows: List[List[str]] = table_data[1:]
            
            # Attempt to sort numerically if possible, otherwise alphabetically
            try:
                # Try converting the sort column to float for all rows
                for row in body_rows:
                    float(row[sort_col_idx])
                # If successful, sort numerically
                body_rows.sort(key=lambda row: float(row[sort_col_idx]), reverse=(sort_order == 'desc'))
                self.log_correction("STYLE-TABLE-002", f"Sorted table by column {sort_col_idx} (numeric)", file_name, start_line_no)
            except (ValueError, IndexError):
                # Fallback to case-insensitive string sort
                body_rows.sort(key=lambda row: row[sort_col_idx].lower() if sort_col_idx < len(row) else "", reverse=(sort_order == 'desc'))
                self.log_correction("STYLE-TABLE-002", f"Sorted table by column {sort_col_idx} (alphabetic)", file_name, start_line_no)
            
            # Re-assemble table_data with sorted body
            table_data = [table_data[0]] + body_rows
            mutated = True # Sorting is a mutation
        # --- End Sorting Logic ---

        # --- New Number Formatting Logic ---
        format_numbers = table_config.get("format_numbers", False)
        if format_numbers:
            # Iterate over body rows only
            for r_idx in range(1, len(table_data)):
                for c_idx in range(len(table_data[r_idx])):
                    cell_value: str = table_data[r_idx][c_idx].strip()
                    try:
                        # Check if it's a number, but not if it's already formatted
                        if ',' not in cell_value:
                            number = float(cell_value)
                            if number.is_integer():
                                table_data[r_idx][c_idx] = f"{int(number):,}"
                            else:
                                table_data[r_idx][c_idx] = f"{number:,.2f}"
                    except (ValueError, IndexError):
                        continue # Not a number, do nothing

        # --- New Total Row Logic ---
        add_total_row = table_config.get("add_total_row", False)
        if add_total_row and len(table_data) > 1:
            total_row = [''] * num_cols
            has_numeric_cols: bool = False
            for c_idx in range(num_cols):
                try:
                    # Attempt to sum the column, skipping the header
                    column_values = [float(row[c_idx].replace(',', '')) for row in table_data[1:] if row[c_idx].strip()]
                    if column_values:
                        total = sum(column_values)
                        # Simple formatting for the total
                        if all(val.is_integer() for val in column_values):
                            total_row[c_idx] = str(int(total))
                        else:
                            total_row[c_idx] = f"{total:.2f}"
                        has_numeric_cols = True
                except (ValueError, IndexError):
                    # This column is not purely numeric, leave it blank
                    total_row[j] = ''
            
            if has_numeric_cols:
                # Set the first cell to "Total"
                total_row[0] = '**Total**'
                # Add a separator line before the total row for clarity
                separator_line = ['---' * len(cell) for cell in header_cells] # Visual separator
                table_data.append(separator_line)
                table_data.append(total_row)
                self.log_correction("STYLE-TABLE-003", "Added calculated 'Total' row to table", file_name, start_line_no)
                mutated = True
        # --- End Total Row Logic ---

        # Separator line also contributes to width (min 3 chars, e.g., ':-:')
        for i in range(num_cols):
            col_widths[i] = max(col_widths[i], 3)

        # 3. Reconstruct the table
        new_table_lines = []
        # Header
        header_parts: List[str] = []
        for i, cell in enumerate(header_cells): # type: ignore
            align_method = getattr(str, alignments[i].ljust(7, ' ').rstrip()) # type: ignore # ljust, center, rjust
            header_parts.append(align_method(cell, col_widths[i]))
        header_row_str = "| " + " | ".join(header_parts) + " |"
        new_table_lines.append(header_row_str)

        # Separator
        sep_row_str = "| " + " | ".join((":" if c.startswith(":") else "") + "-" * (col_widths[i] - (1 if c.startswith(":") else 0) - (1 if c.endswith(":") else 0)) + (":" if c.endswith(":") else "") for i, c in enumerate(separator_cells)) + " |" # type: ignore
        new_table_lines.append(sep_row_str)

        # Body
        for row in table_data[1:]:
            body_parts: List[str] = []
            for i, cell in enumerate(row): # type: ignore
                align_method = getattr(str, alignments[i].ljust(7, ' ').rstrip()) # type: ignore
                body_parts.append(align_method(cell, col_widths[i]))
            body_row_str = "| " + " | ".join(body_parts) + " |"
            new_table_lines.append(body_row_str)

        original_block = [header_line, separator_line] + body_lines
        mutated = original_block != new_table_lines
        return new_table_lines, lines_consumed, mutated

    def _apply_list_block_formatting(self, lines: List[str], file_name: str) -> Tuple[List[str], bool]:
        """
        Processes blocks of list items, e.g., converting bulleted lists to numbered lists
        if they meet a certain threshold.
        """
        mutated = False
        list_config = self.config.get("list_formatting", {})
        convert_threshold: int = list_config.get("convert_bullets_to_numbered_threshold", 0)

        processed_lines: List[str] = []
        line_idx = 0
        while line_idx < len(lines):
            line = lines[line_idx]
            match = re.match(r"^(\s*)-\s", line)
            ordered_match = re.match(r"^(\s*)\d+\.\s", line)

            if match and convert_threshold > 0:
                indent_level = len(match.group(1))
                block, consumed = self._process_list_level(lines, line_idx, indent_level, convert_threshold, file_name)
                processed_lines.extend(block)
                line_idx += consumed
                if consumed > 0: # If we processed a block, there might have been a mutation
                    mutated = True # Assume mutation for simplicity, could be refined
            elif ordered_match:
                # Re-format existing ordered lists
                indent_level = len(ordered_match.group(1))
                block, consumed = self._reformat_ordered_list(lines, line_idx, indent_level, list_config, file_name)
                processed_lines.extend(block)
                line_idx += consumed
                if consumed > 0:
                    mutated = True
            else:
                processed_lines.append(line)
                line_idx += 1
        
        # A simple check to see if mutation actually occurred
        final_mutated = "".join(lines) != "".join(processed_lines)
        return processed_lines, final_mutated

    def _process_list_level(self, lines: List[str], start_index: int, indent_level: int, threshold: int, file_name: str) -> Tuple[List[str], int]:
        """Processes a single level of a list, converting to numbered if threshold met."""
        list_items: List[str] = []
        consumed_count = 0
        
        # Collect all items at the current indentation level
        for i in range(start_index, len(lines)):
            line: str = lines[i]
            match = re.match(r"^(\s*)-\s+(.*)", line)
            if match and len(match.group(1)) == indent_level:
                list_items.append(match.group(2))
                consumed_count += 1
            else:
                break # End of this list level

        if len(list_items) >= threshold:
            indent_str = " " * indent_level
            return [f"{indent_str}{i+1}. {item}" for i, item in enumerate(list_items)], consumed_count
        else:
            # Return original lines if not converting
            return lines[start_index : start_index + consumed_count], consumed_count

    def _reformat_ordered_list(self, lines: List[str], start_index: int, indent_level: int, config: Dict[str, Any], file_name: str) -> Tuple[List[str], int]:
        """Reformats an existing ordered list to a configured style."""
        style: str = config.get("ordered_list_style", "decimal")
        if style == "decimal":
            return lines[start_index:], 0 # No change needed if default

        items: List[str] = []
        consumed_count: int = 0
        for i in range(start_index, len(lines)):
            line = lines[i]
            match = re.match(r"^(\s*)\d+\.\s+(.*)", line)
            if match and len(match.group(1)) == indent_level:
                items.append(match.group(2))
                consumed_count += 1
            else:
                break
        
        self.log_correction("STYLE-LIST-003", f"Reformatted ordered list to '{style}' style", file_name, start_index + 1)
        indent_str = " " * indent_level
        style_map: Dict[str, Any] = {"roman": self._to_roman, "alpha": self._to_alpha}
        formatter = style_map.get(style, str)
        return [f"{indent_str}{formatter(i+1)}. {item}" for i, item in enumerate(items)], consumed_count

    def _clean_spacing(self, lines: List[str], file_name: str) -> Tuple[List[str], bool]:
        mutated = False
        final_lines: List[str] = []
        if not lines:
            return [], False
 
        # Ensure there's a blank line after a heading if it's not the last line
        for i in range(len(lines) - 1):
            line = lines[i]
            final_lines.append(line)
            if line.strip().startswith("#") and lines[i+1].strip() != "":
                final_lines.append("")
                self.log_correction("INDENT-PARA-001", "Inserted missing blank line after heading", file_name, i + 2)
                mutated = True
        final_lines.append(lines[-1])
 
        # Remove consecutive blank lines
        deduped_lines: List[str] = []
        last_was_blank = False
        for i, line in enumerate(final_lines):
            is_blank = line.strip() == ""
            if is_blank and last_was_blank:
                self.log_correction("INDENT-PARA-001", "Suppressed consecutive blank line", file_name, i + 1)
                mutated = True
                continue
            deduped_lines.append(line)
            last_was_blank = is_blank
 
        return deduped_lines, mutated
 
    def _to_roman(self, n: int) -> str:
        """Converts an integer to a Roman numeral."""
        if not 0 < n < 4000:
            return str(n) # Fallback for out-of-range numbers
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman_num = ''
        i = 0
        while n > 0:
            for _ in range(n // val[i]):
                roman_num += syb[i]
                n -= val[i]
            i += 1
        return roman_num

    def _to_alpha(self, n: int) -> str:
        """Converts an integer to a lowercase letter (a, b, c...)."""
        if n <= 0 or n > 26:
            return str(n) # Fallback
        return chr(ord('a') + n - 1)

    def _apply_heading_numbering(self, lines: List[str], file_name: str) -> Tuple[List[str], bool]:
        """
        Applies hierarchical numbering to ATX headings based on configuration.
        """
        heading_config: Dict[str, Any] = self.config.get("headings", {})
        number_headings = heading_config.get("number_headings", False)
        if not number_headings: # type: ignore
            return lines, False

        mutated = False
        new_lines = []
        heading_numbers = [0, 0, 0, 0, 0, 0] # Max 6 levels

        for i, line in enumerate(lines):
            # Match headings that may or may not already be numbered
            match = re.match(r"^(#{1,6})\s+(?:\d+(?:\.\d+)*\.\s+)?(.*)", line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()

                # Increment current level, reset lower levels
                heading_numbers[level - 1] += 1
                for j in range(level, 6):
                    heading_numbers[j] = 0
                
                # Construct the number string
                numbering_style: str = heading_config.get("numbering_style", "decimal") # type: ignore
                if numbering_style == "roman":
                    number_prefix = self._to_roman(heading_numbers[level - 1]) + "."
                elif numbering_style == "alpha":
                    number_prefix = self._to_alpha(heading_numbers[level - 1]) + "."
                else: # decimal
                    current_number_parts = [str(num) for num in heading_numbers[:level] if num > 0]
                    number_prefix = ".".join(current_number_parts) + "." if current_number_parts else ""

                # Prepend number to heading
                new_heading = f"{match.group(1)} {number_prefix} {title}"
                if new_heading != line:
                    new_lines.append(new_heading)
                    self.log_correction("STRUCT-HNUM-001", f"Numbered heading: '{new_heading}'", file_name, i + 1)
                    mutated = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        return new_lines, mutated

    def _generate_table_of_contents(self, lines: List[str], file_name: str) -> Tuple[List[str], bool]:
        """Finds a [TOC] placeholder and replaces it with a generated table of contents."""
        toc_placeholder = "[TOC]"
        toc_start_marker = "<!-- TOC START -->"
        toc_end_marker = "<!-- TOC END -->"
        
        toc_placeholder_index = -1
        toc_start_index = -1
        toc_end_index = -1

        for i, line in enumerate(lines):
            if toc_placeholder in line:
                toc_placeholder_index = i
            elif toc_start_marker in line:
                toc_start_index = i
            elif toc_end_marker in line:
                toc_end_index = i

        if toc_placeholder_index == -1 and (toc_start_index == -1 or toc_end_index == -1):
            return lines, False

        toc_config = self.config.get("toc", {})
        max_depth: int = toc_config.get("max_depth", 6) # type: ignore

        headings = []
        for line in lines:
            match = re.match(r"^(#{1,6})\s+(.*)", line)
            if match:
                # Exclude the TOC heading itself if it exists
                # Extract title, removing any numbering that might have been added
                title = re.sub(r"^\d+(\.\d+)*\.\s+", "", match.group(2).strip())
                if "table of contents" not in title.lower():
                    level = len(match.group(1))
                    if level <= max_depth:
                        headings.append((level, title))

        toc_lines = []
        for level, title in headings:
            # Create GitHub-style anchor links
            anchor = re.sub(r'[^\w\s-]', '', title.lower())
            anchor = re.sub(r'[\s-]+', '-', anchor).strip('-')
            indent = "    " * (level - 1)
            toc_lines.append(f"{indent}- [{title}](#{anchor})")

        # If we found a placeholder, replace it with the managed TOC block
        if toc_placeholder_index != -1:
            final_toc_block = [toc_start_marker] + toc_lines + [toc_end_marker]
            lines[toc_placeholder_index:toc_placeholder_index+1] = final_toc_block
            self.log_correction("STRUCT-TOC-001", "Generated Table of Contents", file_name, toc_placeholder_index + 1)
            return lines, True
        # If we found an existing TOC block, replace its contents
        elif toc_start_index != -1 and toc_end_index != -1:
            # Check if the content is already correct to avoid unnecessary mutation
            existing_toc_content = lines[toc_start_index+1:toc_end_index]
            if existing_toc_content == toc_lines:
                return lines, False # No change needed
            
            lines[toc_start_index+1:toc_end_index] = toc_lines
            self.log_correction("STRUCT-TOC-001", "Updated existing Table of Contents", file_name, toc_start_index + 1)
            return lines, True

        return lines, False

    def _collect_files(self) -> List[str]:
        """Collects all markdown files from the target path."""
        targets: List[str] = []
        if os.path.isdir(self.target_path):
            for root, _, files in os.walk(self.target_path):
                for filename in files:
                    if filename.endswith(".md"):
                        targets.append(os.path.join(root, filename))

            # Add files specified in config
            explicit_files: List[str] = self.config.get("files_to_process", []) # type: ignore
            for f_path in explicit_files:
                abs_path = os.path.abspath(os.path.join(self.target_path, f_path))
                if abs_path.endswith(".md") and os.path.exists(abs_path):
                    targets.append(abs_path)

            if pathspec:
                if os.path.exists(os.path.join(self.target_path, ".gitignore")):
                    with open(os.path.join(self.target_path, ".gitignore"), "r", encoding="utf-8") as f: # type: ignore
                        spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
                    
                    # Filter out ignored files
                    filtered_targets = []
                    for file_path in targets:
                        relative_path = os.path.relpath(file_path, self.target_path).replace('\\', '/')
                        if not spec.match_file(relative_path):
                            filtered_targets.append(file_path)
                    targets = filtered_targets

            # Remove duplicates and return
            return sorted(list(set(targets)))
            
        elif self.target_path.endswith(".md"):
            targets.append(self.target_path)
        return targets
 
    def _check_broken_links(self, line: str, file_name: str, line_no: int) -> Tuple[str, bool]:
        """Finds and verifies internal Markdown links, including anchors."""
        link_pattern: re.Pattern[str] = re.compile(r'(?:!\[.*?\]|\[[^\]]*?\])\((.*?)\)')
        base_dir = os.path.dirname(os.path.abspath(file_name))
        
        for match in link_pattern.finditer(line):
            link_target = match.group(1)
            
            # Ignore external links, mailto links, and pure anchors
            if link_target.startswith(('http://', 'https://', 'mailto:', '#')) or not link_target:
                continue

            link_parts = link_target.split('#', 1)
            link_path: str = link_parts
            anchor = link_parts[1] if len(link_parts) > 1 else None

            abs_link_path = os.path.abspath(os.path.join(base_dir, link_path))

            if not os.path.exists(abs_link_path):
                self.log_correction("LINT-LINK-001", f"Broken internal link found: '{link_target}'", file_name, line_no)
            elif anchor:
                # File exists, now check the anchor
                if abs_link_path not in self.file_anchor_cache:
                    # Parse the file and cache its anchors
                    try:
                        with open(abs_link_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        headings: List[str] = re.findall(r"^(?:#{1,6})\s+(.*)", content, re.MULTILINE)
                        self.file_anchor_cache[abs_link_path] = {re.sub(r'[^\w\s-]', '', h.lower()).replace(' ', '-') for h in headings} # type: ignore
                    except Exception:
                        self.file_anchor_cache[abs_link_path] = set() # Cache failure
                
                if anchor not in self.file_anchor_cache.get(abs_link_path, set()):
                    self.log_correction("LINT-LINK-002", f"Broken link anchor: '#{anchor}' not found in '{link_path}'", file_name, line_no)

        return line, False # This is a linting check, it does not mutate the line

    def format_all(self) -> Dict[str, Any]:
        targets = self._collect_files()
        modified_files: List[str] = []
 
        for file_path in targets:
            formatted_text, is_mutated = self.format_document(file_path)
            if is_mutated:
                modified_files.append(file_path)
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(formatted_text)
 
        evidence_confidence = 100 if len(targets) > 0 else 0
        comp_status = "PASS" if self.corrections_count == 0 else "CORRECTED"
 
        return {
            "target": self.target_path,
            "status": comp_status,
            "scanned": len(targets),
            "mutated": len(modified_files),
            "total_corrections": self.corrections_count,
            "evidence_confidence": evidence_confidence,
            "logs": self.logs
        }
 
def main():
    parser = argparse.ArgumentParser(description="Deterministic PGPS-001 Linter and Auto-Formatter")
    parser.add_argument("target", help="Markdown file or directory to format")
    parser.add_argument("--dry-run", action="store_true", help="Report violations without writing changes")
    parser.add_argument("--init-config", action="store_true", help="Generate a default .pgps-formatter.json file in the current directory.")
    args = parser.parse_args()

    if args.init_config:
        config_path = os.path.join(os.getcwd(), ".pgps-formatter.json")
        if os.path.exists(config_path):
            print(f"Error: .pgps-formatter.json already exists at {config_path}. Aborting.")
            sys.exit(1)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_FORMATTER_CONFIG, f, indent=2)
        print(f"Default .pgps-formatter.json generated at {config_path}")
        sys.exit(0)
 
    formatter = PgpsFormatter(args.target, dry_run=args.dry_run)
    report = formatter.format_all()
 
    print("\n=======================================================")
    print("  PGPS-001 AUTO-FORMATTER LOG -- COGNITIVE ENGINE v15.1")
    print("=======================================================")
    print(f"Target Processed:     {report['target']}")
    print(f"Scanned Files:        {report['scanned']}")
    print(f"Mutated Files:        {report['mutated']} (Dry-Run: {args.dry_run})")
    print(f"Total Corrections:    {report['total_corrections']}")
    print(f"Evidence Confidence:  {report['evidence_confidence']}%")
    print(f"Sovereignty Status:   {report['status']}")
    print("=======================================================")
 
    if report["logs"]:
        print("\n--- Traceable Corrections Log ---")
        for log in report["logs"]:
            print(f"  ✔ {log}")
    else:
        print("\n  ✔ Zero structural deviations identified. Absolute alignment achieved.")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
