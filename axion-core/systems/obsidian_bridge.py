"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-OBSID-001`              | The Sovereign ID. |
| **Official Name** | `obsidian_bridge.py`           | The Filename.     |
| **Version**       | **v14.0**                      | The Standard.     |
| **Domain**        | `COG`                          | The Subject.      |
| **Evolution**     | **Knowledge Resonance**        | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |.

## Sovereign Ethos
A Cognitive Bridge connecting Axion to the Obsidian Local REST API.
This tool transfigures flat local notes into a synergistic graph of wisdom.

The bridge is the nexus where memory meets logic.
"""

import logging
import os
import sys
from typing import Any

import requests

# Try to import shared exceptions, fallback to local if not found
try:
    from axion_core.tools.exceptions import IntegrityError, ObsidianConnectionError
except ImportError:
    # Local fallback for development/standalone use
    class ObsidianConnectionError(Exception):
        pass

    class IntegrityError(Exception):
        pass


# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class ObsidianBridge:
    """The Obsidian Knowledge Bridge (v14.0).
    Connects Axion to the Obsidian Local REST API for hybrid graph interaction.
    """

    def __init__(
        self,
        api_key: str,
        host: str = "127.0.0.1",
        port: int = 27124,
        cert_path: str | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.api_key = api_key
        self.base_url = f"https://{host}:{port}"
        self.cert_path = cert_path

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Handles HTTP requests to the Obsidian Local REST API."""
        url = f"{self.base_url}{endpoint}"
        try:
            # We use the provided certificate for verification if available
            verify = (
                self.cert_path
                if self.cert_path and os.path.exists(self.cert_path)
                else False
            )

            # Disable verify warning if not verifying
            if not verify:
                requests.packages.urllib3.disable_warnings()

            response = requests.request(
                method=method, url=url, headers=self.headers, verify=verify, **kwargs
            )

            if response.status_code == 401:
                raise ObsidianConnectionError("Authentication failed: Invalid API Key.")

            response.raise_for_status()
            return response

        except requests.exceptions.ConnectionError:
            raise ObsidianConnectionError(
                f"Connection failed: Is the Obsidian Local REST API running on {url}?"
            )
        except requests.exceptions.HTTPError as e:
            raise ObsidianConnectionError(f"API Error: {e}")

    def check_connection(self) -> bool:
        """Verifies that the API is active and reachable."""
        try:
            self._request("GET", "/")
            logger.info("✅ Obsidian Knowledge Bridge: [ACTIVE]")
            return True
        except Exception as e:
            logger.error(f"❌ Obsidian Knowledge Bridge: [OFFLINE] - {e}")
            return False

    def list_notes(self) -> list[str]:
        """Lists all markdown notes in the vault."""
        response = self._request("GET", "/vault/")
        # The /vault/ endpoint returns { "files": ["path1.md", "path2.md", ...] }
        data = response.json()
        files = data.get("files", [])
        return [f for f in files if isinstance(f, str) and f.endswith(".md")]

    def get_note(self, path: str) -> str:
        """Retrieves the full content of a note."""
        response = self._request("GET", f"/vault/{path}")
        return response.text

    def get_note_metadata(self, path: str) -> dict[str, Any]:
        """Retrieves JSON metadata for a note (frontmatter, tags, links)."""
        response = self._request(
            "GET",
            f"/vault/{path}",
            headers={**self.headers, "Accept": "application/vnd.olra.v1.non-raw+json"},
        )
        return response.json()

    def search(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        """Executes a search query (Dataview or JSON-based).
        Example query: {"query": "path:notes", "contextLength": 100}.
        """
        response = self._request("POST", "/search/", json=query)
        return response.json()

    def update_note(self, path: str, content: str, mode: str = "replace") -> None:
        """Updates a note. Mode can be 'append', 'prepend', or 'replace'."""
        headers = {**self.headers, "Heading-Boundary": "bottom"}
        if mode == "append":
            self._request("POST", f"/vault/{path}", data=content, headers=headers)
        elif mode == "prepend":
            headers["Heading-Boundary"] = "top"
            self._request("POST", f"/vault/{path}", data=content, headers=headers)
        else:
            self._request("PUT", f"/vault/{path}", data=content)


if __name__ == "__main__":
    # Example usage / Heartbeat check
    # These would normally be loaded from environment variables
    API_KEY = "75d743e71b4e0ec1b4e04aeabea1a2695b5cff03a899020de6519248e3c26db2"
    CERT = "c:/Users/Chris/Synarche_Workspace/obsidian-local-rest-api.crt"

    print("Initiating Heartbeat Check on port 27124...", flush=True)
    bridge = ObsidianBridge(api_key=API_KEY, cert_path=CERT)
    if bridge.check_connection():
        notes = bridge.list_notes()
        print(f"✅ SUCCESS: Connected to vault with {len(notes)} notes.", flush=True)
        if notes:
            print(f"Sample Note: {notes[0]}", flush=True)
    else:
        print("❌ FAILURE: Could not connect to Obsidian.", flush=True)
        sys.exit(1)
