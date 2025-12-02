import unittest
from unittest.mock import MagicMock, patch

import requests

from nova_forge.association_core import AssociationManager


class TestAssociationManager(unittest.TestCase):
    def setUp(self):
        self.manager = AssociationManager(api_token="fake_token")

    @patch("requests.patch")
    def test_link_entities_success(self, mock_patch):
        # Configure the mock to return a successful response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_patch.return_value = mock_response

        source_id = "page-1"
        target_id = "page-2"

        result = self.manager.link_entities(source_id, target_id)

        self.assertTrue(result)

        # Verify the API call
        expected_url = "https://api.notion.com/v1/pages/page-1"
        expected_payload = {"properties": {"Related": {"relation": [{"id": "page-2"}]}}}

        mock_patch.assert_called_once()
        args, kwargs = mock_patch.call_args
        self.assertEqual(args[0], expected_url)
        self.assertEqual(kwargs["json"], expected_payload)
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer fake_token")

    @patch("requests.patch")
    def test_link_entities_failure(self, mock_patch):
        # Configure the mock to raise an exception
        mock_patch.side_effect = requests.exceptions.RequestException("Network error")

        result = self.manager.link_entities("page-1", "page-2")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
