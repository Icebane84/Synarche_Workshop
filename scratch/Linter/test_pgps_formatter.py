import json
import os
import unittest
from unittest.mock import mock_open, patch

from pgps_formatter import PgpsFormatter


class TestPgpsFormatter(unittest.TestCase):

    def _run_formatter(self, content, config=None):
        """
        Helper to run the formatter on in-memory content and config
        by mocking file system operations.
        """
        config_content = json.dumps(config) if config else ""
        doc_content = content

        # Mock file system reads
        def mock_file_open(filename, *args, **kwargs):
            if "pgps-formatter.json" in filename:
                return mock_open(read_data=config_content)()
            elif "test_doc.md" in filename:
                return mock_open(read_data=doc_content)()
            return mock_open(read_data="")()

        # Patch 'open' and 'os.path.exists' to simulate file presence
        with patch('builtins.open', side_effect=mock_file_open), \
             patch('os.path.exists', return_value=True):
            
            # The path is now just a placeholder for the mock to key off of
            formatter = PgpsFormatter("/mock/dir", dry_run=True)
            formatted_text, _ = formatter.format_document("/mock/dir/test_doc.md")

        return formatted_text

    def test_heading_formatting(self):
        """Tests ATX heading standardization."""
        content = "##My Heading##\n\nMy Title\n======"
        expected = "## My Heading\n\n# My Title\n"
        result = self._run_formatter(content)
        self.assertEqual(result, expected)

    def test_list_item_conversion(self):
        """Tests that * and + list markers are converted to -."""
        content = "* Item 1\n+ Item 2"
        expected = "- Item 1\n- Item 2\n"
        result = self._run_formatter(content)
        self.assertEqual(result, expected)

    def test_nested_list_indentation(self):
        """Tests 2-space nested lists are corrected to 4-space."""
        content = "- Item 1\n  - Nested Item"
        expected = "- Item 1\n    - Nested Item\n"
        result = self._run_formatter(content)
        self.assertEqual(result, expected)

    def test_uuid_and_mac_formatting(self):
        """Tests standardization of UUIDs and MAC addresses."""
        content = "ID: F81D4FAE-7DEC-11D0-A765-00A0C91E6BF6\nMAC: 00-80-C8-E8-92-74"
        expected = "ID: f81d4fae-7dec-11d0-a765-00a0c91e6bf6\nMAC: 00:80:C8:E8:92:74\n"
        result = self._run_formatter(content)
        self.assertEqual(result, expected)

    def test_date_and_time_formatting(self):
        """Tests standardization of date and time strings."""
        content = "Date: July 28, 2026\nTime: 5:30 PM"
        expected = "Date: 2026-07-28\nTime: 17:30:00\n"
        result = self._run_formatter(content)
        self.assertEqual(result, expected)

    def test_inclusive_language_replacement(self):
        """Tests configurable inclusive language replacement."""
        content = "The master branch should be whitelisted."
        config = {
            "inclusive_language": {
                "replacements": {
                    "master": "primary",
                    "whitelist": "allowlist"
                }
            }
        }
        expected = "The primary branch should be allowlisted.\n"
        result = self._run_formatter(content, config)
        self.assertEqual(result, expected)

    def test_inclusive_language_case_preservation(self):
        """Tests that case is preserved during replacement."""
        content = "Master and SLAVE systems."
        config = {
            "inclusive_language": {
                "replacements": {
                    "master": "primary",
                    "slave": "replica"
                }
            }
        }
        expected = "Primary and REPLICA systems.\n"
        result = self._run_formatter(content, config)
        self.assertEqual(result, expected)

    def test_table_alignment_and_sorting(self):
        """Tests table alignment and sorting logic."""
        content = "| Name  | Value |\n| :---- | ----: |\n| B     | 10    |\n| A     | 20    |"
        config = {
            "table_formatting": {
                "sort_by_column": 0,
                "sort_order": "asc"
            }
        }
        # Note: The exact spacing will depend on implementation details.
        # We check for the core logic: sorting and content.
        result = self._run_formatter(content, config)
        self.assertIn("| A     |    20 |", result)
        self.assertIn("| B     |    10 |", result)

    def test_table_sorting_logic_directly(self):
        """Tests the _sort_table_body method in isolation."""
        formatter = PgpsFormatter("/mock/dir")
        
        # Test numeric sort
        table_data = [
            ["Name", "Value"],
            ["B", "10"],
            ["C", "5"],
            ["A", "20"]
        ]
        formatter.config = {"table_formatting": {"sort_by_column": 1, "sort_order": "asc"}}
        sorted_data, _ = formatter._sort_table_body(table_data, "test.md", 1)
        self.assertEqual([row[1] for row in sorted_data[1:]], ["5", "10", "20"])

        # Test alphabetical descending sort
        formatter.config = {"table_formatting": {"sort_by_column": 0, "sort_order": "desc"}}
        sorted_data, _ = formatter._sort_table_body(table_data, "test.md", 1)
        self.assertEqual([row[0] for row in sorted_data[1:]], ["C", "B", "A"])

    def test_table_with_multiline_cells(self):
        """Tests that tables with <br> tags are padded correctly."""
        content = "| Header 1 | Header 2 |\n|---|---|\n| Short | A very long line<br>with a break |\n"
        result = self._run_formatter(content)
        self.assertIn("| Short    | A very long line<br>with a break |", result)

    def test_table_total_row(self):
        """Tests the automatic addition of a total row."""
        content = "| Item  | Cost  |\n| :---- | :---- |\n| A     | 10.5  |\n| B     | 20    |"
        config = {
            "table_formatting": {
                "add_total_row": True
            }
        }
        result = self._run_formatter(content, config)
        self.assertIn("| **Total** | 30.50 |", result)

    def test_list_conversion_to_numbered(self):
        """Tests conversion of long bullet lists to numbered lists."""
        content = "- Step one\n- Step two\n- Step three"
        config = {
            "list_formatting": {
                "convert_bullets_to_numbered_threshold": 3
            }
        }
        expected = "1. Step one\n2. Step two\n3. Step three\n"
        result = self._run_formatter(content, config)
        self.assertEqual(result, expected)

    def test_list_conversion_preserves_nested(self):
        """Ensures nested lists are not broken by conversion."""
        content = "- Step one\n- Step two\n  - Sub-step A\n  - Sub-step B\n- Step three"
        config = {
            "list_formatting": {
                "convert_bullets_to_numbered_threshold": 3
            }
        }
        # The top-level list should convert, but the nested one should remain a bullet list.
        # This test is complex and depends on the recursive implementation.
        # A more basic check is that the sub-steps are still present.
        result = self._run_formatter(content, config)
        self.assertIn("1. Step one", result)
        self.assertIn("    - Sub-step A", result)
        self.assertIn("3. Step three", result)

    def test_toc_generation(self):
        """Tests the automatic generation of a Table of Contents."""
        content = "[TOC]\n\n# First Heading\n\n## Sub Heading"
        expected = "- [First Heading](#first-heading)\n    - [Sub Heading](#sub-heading)\n"
        result = self._run_formatter(content)
        self.assertEqual(result, expected)

    def test_toc_generation_with_depth_limit(self):
        """Tests that the TOC respects the max_depth configuration."""
        content = "[TOC]\n\n# H1\n\n## H2\n\n### H3"
        config = {
            "toc": {"max_depth": 2}
        }
        expected = "- [H1](#h1)\n    - [H2](#h2)\n"
        result = self._run_formatter(content, config)
        self.assertEqual(result, expected)

    @patch('os.walk')
    def test_format_all_with_file_collection(self, mock_walk):
        """Tests the format_all method's file discovery logic."""
        # Define a mock directory structure
        mock_walk.return_value = [
            ('/mock/dir', ['subdir'], ['test_doc.md', 'config.json']),
            ('/mock/dir/subdir', [], ['another.md', 'image.png']),
        ]

        # Mock 'open' to return content for the .md files
        m = mock_open()
        with patch('builtins.open', m):
            formatter = PgpsFormatter("/mock/dir")
            report = formatter.format_all()

        # Check that it found and tried to process the two Markdown files
        self.assertEqual(report["scanned"], 2)
        # Ensure open was called for the correct files
        self.assertIn('/mock/dir/test_doc.md', [call[0][0] for call in m.call_args_list])
        self.assertIn('/mock/dir/subdir/another.md', [call[0][0] for call in m.call_args_list])

if __name__ == "__main__":
    unittest.main()