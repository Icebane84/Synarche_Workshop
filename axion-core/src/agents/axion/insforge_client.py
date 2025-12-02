"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-CLIENT-IF-001
Official Name: insforge_client.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Digital Persistence. Event Chronometer."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

import asyncio
import json
import logging
import urllib.request
from typing import Any

# Project Imports
from .config import settings

logger = logging.getLogger("axion.client.insforge")


class InsForgeClient:
    """
    Communicates with the InsForge cloud infrastructure for logging and persistence.
    Operates as the 'Chronicler' for the High Priestess.
    """

    def __init__(self) -> None:
        self.api_key = settings.INSFORGE_API_KEY
        self.base_url = settings.INSFORGE_BASE_URL
        self.active = bool(self.api_key and self.base_url)

    async def log_event(self, type: str, description: str, payload: dict[str, Any] | None = None) -> None:
        """Logs a sovereign event to the InsForge backend via the 'event-chronicler' function."""
        if not self.active:
            # Silent failure or local logging if not configured
            logger.debug(f"   > [LOCAL_LOG] {type}: {description}")
            return

        # Prepare the Chronicler's Payload
        event_data = {
            "type": type,
            "description": description,
            "payload": payload or {},
        }

        # Execute the request in a thread to prevent blocking the async loop
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, self._send_request, event_data)
            logger.info(f"   > [CHRONICLE] Event Logged: {type}")
        except Exception:
            logger.exception(f"   > [DISSONANCE] Chronicler Failure for {type}")

    def _send_request(self, data: dict[str, Any]) -> None:
        """Synchronous helper for urllib.request."""
        url = f"{self.base_url}/functions/v1/event-chronicler"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-Client-Info": "axion-core/v15.0",
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        error_threshold = 400
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status >= error_threshold:
                raise RuntimeError(f"InsForge API Error: {response.status}")


# Singleton instance
insforge = InsForgeClient()
