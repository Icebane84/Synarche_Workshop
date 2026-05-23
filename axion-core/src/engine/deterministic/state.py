"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-STA-001`             | The Sovereign ID. |
| **Official Name**   | `state.py`                    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: State Persistence (Law 03)**
> Implemented from Blueprint `GVRN.REG.StateManager.md`.
> Ethos: Immortality through serialization.
"""

import hashlib
import pickle
from typing import Any, Dict, List, Optional


class StateSnapshot:
    """Captures a serialized, hashable snapshot of the engine state at a specific frame.
    Uses binary serialization to ensure all object properties are preserved.
    """

    def __init__(self, data: Dict[str, Any], frame_id: int) -> None:
        """Initializes a state snapshot.

        Args:
            data (Dict[str, Any]): The state dictionary to capture.
            frame_id (int): The current simulation frame ID.

        """
        self.frame_id: int = frame_id
        self.data: Dict[str, Any] = data
        # Use pickle for robust serialization of arbitrary objects in the state map.
        self.blob: bytes = pickle.dumps(data)
        self.hash: str = hashlib.sha256(self.blob).hexdigest()

    def __repr__(self) -> str:
        """Returns a string representation of the snapshot identification."""
        return f"<StateSnapshot frame={self.frame_id} hash={self.hash[:8]}>"


class StateManager:
    """Handles a history of state snapshots to enable deterministic rollback and replay.
    Manages the temporal storage of simulation states.
    """

    def __init__(self) -> None:
        """Initializes the state manager with an empty history."""
        self.history: Dict[int, StateSnapshot] = {}

    def save_state(self, frame_id: int, data: Dict[str, Any]) -> StateSnapshot:
        """Creates and stores a snapshot of the provided state data.

        Args:
            frame_id (int): The frame ID associated with the state.
            data (Dict[str, Any]): The state data to save.

        Returns:
            StateSnapshot: The generated snapshot object.

        """
        snapshot = StateSnapshot(data, frame_id)
        self.history[frame_id] = snapshot
        return snapshot

    def load_state(self, frame_id: int) -> Optional[Dict[str, Any]]:
        """Restores a state dictionary from a saved snapshot.

        Args:
            frame_id (int): The frame ID to load.

        Returns:
            Optional[Dict[str, Any]]: The deserialized state dictionary, or None if not found.

        """
        snapshot = self.history.get(frame_id)
        return pickle.loads(snapshot.blob) if snapshot else None

    def purge_after(self, frame_id: int) -> None:
        """Removes all snapshots occurring after the specified frame ID.
        This is typically called during a rollback to prevent history drift.

        Args:
            frame_id (int): The cutoff frame ID.

        """
        keys_to_remove: List[int] = [k for k in self.history.keys() if k > frame_id]
        for k in keys_to_remove:
            del self.history[k]
