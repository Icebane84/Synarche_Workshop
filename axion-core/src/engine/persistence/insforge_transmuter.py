"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-PER-INS-001`             | The Sovereign ID. |
| **Official Name**   | `insforge_transmuter.py`      | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-PER`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Systemic Persistence (Law 19)**
> Implemented from Blueprint `GVRN.REG.InsforgeTransmuter.md`.
> Ethos: Continuity through Cloud Synthesis.
"""

import base64
import logging
import pickle
import uuid
from typing import Any, Dict, List, Optional

import requests


class InsforgeTransmuter:
    """Bridges the Axion Engine state to the Insforge Cloud.
    Handles entity/component upserts and frame snapshotting using REST protocols.

    This class implements the 'Transmutation' protocol, allowing
    local deterministic states to be persisted and restored from the cloud
    for cross-session continuity and multiplayer synchronization.
    """

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initializes the transmuter with cloud credentials.

        Args:
            base_url (str): The endpoint for the Insforge API.
            api_key (str): The authorization token.

        """
        self.base_url: str = base_url.rstrip("/")
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",  # Required for UPSERT behavior
        }
        self.logger: logging.Logger = logging.getLogger("PhoenixLogger")

    def transmute_entities(self, entities: List[uuid.UUID]) -> None:
        """Persists the entity registry to the axion_entities table.

        Args:
            entities (List[uuid.UUID]): The list of entity handles to save.

        """
        if not entities:
            return

        payload = [{"id": str(eid)} for eid in entities]
        url = f"{self.base_url}/api/database/records/axion_entities"

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Transmutation Failure (Entities): {e}")

    def transmute_components(self, component_store: Any) -> None:
        """Persists all components for all entities to the axion_components table.
        Extracts serializable data from component instances.

        Args:
            component_store (Any): The ComponentStore instance containing the data.

        """
        payload = []
        # Access the internal stores of the ComponentStore
        for comp_type, entity_map in component_store.stores.items():
            type_name = comp_type.__name__
            for entity_id, comp_instance in entity_map.items():
                # Extract data: objects use __dict__, primitives are wrapped
                if hasattr(comp_instance, "__dict__"):
                    data = comp_instance.__dict__.copy()
                    # Remove non-serializable transient fields
                    if "_lock" in data:
                        del data["_lock"]
                else:
                    data = {"value": comp_instance}

                payload.append(
                    {"entity_id": str(entity_id), "type": type_name, "data": data}
                )

        if not payload:
            return

        url = f"{self.base_url}/api/database/records/axion_components"
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Transmutation Failure (Components): {e}")

    def save_snapshot(self, frame: int, state: Dict[str, Any]) -> None:
        """Saves a binary save-state to the cloud snapshots table.
        Converts state to base64 encoded pickle data for transport.

        Args:
            frame (int): The current simulation frame index.
            state (Dict[str, Any]): The state dictionary to persist.

        """
        try:
            # Binary pickle -> Base64 for JSON transport
            binary_data = pickle.dumps(state)
            b64_data = base64.b64encode(binary_data).decode("utf-8")

            payload = [{"frame": frame, "state_data": b64_data}]

            url = f"{self.base_url}/api/database/records/axion_snapshots"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Snapshot Failure (Frame {frame}): {e}")

    def load_snapshot(self, frame: int) -> Optional[Dict[str, Any]]:
        """Retrieves and restores a snapshot from the cloud.

        Args:
            frame (int): The target frame index to restore.

        Returns:
            Optional[Dict[str, Any]]: The restored state dict, or None if retrieval fails.

        """
        url = f"{self.base_url}/api/database/records/axion_snapshots?frame=eq.{frame}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                return None

            b64_data = data[0]["state_data"]
            binary_data = base64.b64decode(b64_data)
            return pickle.loads(binary_data)
        except Exception as e:
            self.logger.error(f"Cloud Load Failure (Frame {frame}): {e}")
            return None
