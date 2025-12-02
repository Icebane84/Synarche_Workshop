"""
Artifact ID: CODE-REF-001
Module: Association Manager
Context: Nova Forge > Backend > Data Layer
Description: Manages the extraction and linkage of entities within the Notion Database.
"""

from typing import Any, Dict

import requests

from .config import settings

# Reference: DOC-STD-001 (Coding Standards)


class AssociationManager:
    """
    Central controller for handling database relationships.
    Adheres to OGLN extraction protocols.
    """

    def __init__(self):
        self.api_token = settings.NOTION_API_TOKEN
        self.base_url = settings.NOTION_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def fetch_database_meta(self, database_id: str) -> Dict[str, Any]:
        """
        Retrieves metadata for a specific target database.

        Args:
            database_id (str): The UUID of the Notion database.

        Returns:
            Dict[str, Any]: Raw JSON response from the API.

        Raises:
            ConnectionError: If the API returns a non-200 status.
        """
        endpoint = f"{self.base_url}/databases/{database_id}"

        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()  # Why: Immediate failure on bad auth/ID
            return response.json()
        except requests.exceptions.RequestException as e:
            # Why: We catch specific network errors to log them before crashing
            print(f"[ERROR] Failed to fetch metadata: {e}")
            raise

    def link_entities(
        self, source_id: str, target_id: str, relation_property: str = "Related"
    ) -> bool:
        """
        Creates a bi-directional link between two pages by updating a Relation property.

        Args:
            source_id (str): The UUID of the source page.
            target_id (str): The UUID of the target page to link to.
            relation_property (str): The name of the Relation property in Notion. Defaults to "Related".

        Returns:
            bool: True if the link was successfully created, False otherwise.
        """
        endpoint = f"{self.base_url}/pages/{source_id}"

        payload = {"properties": {relation_property: {"relation": [{"id": target_id}]}}}

        try:
            response = requests.patch(
                endpoint, headers=self.headers, json=payload, timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to link entities: {e}")
            return False
