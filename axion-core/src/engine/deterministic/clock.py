"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-CLK-001`             | The Sovereign ID. |
| **Official Name**   | `clock.py`                    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[ASTEROID]`                  | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Temporal Precision (Law 09)**
> Implemented from Blueprint `GVRN.REG.DeterministicClock.md`.
> Ethos: Synchronicity through fixed intervals.
"""


class FixedClock:
    """
    Provides a deterministic time reference for the Axion Engine.
    Ensures that delta-time is constant and frame counts are synchronized across all nodes.
    
    This component is critical for maintaining consistency in networked simulations
    and enabling reproducible execution logs.
    """

    def __init__(self, dt: float = 1/60) -> None:
        """
        Initializes the clock with a fixed delta time.
        
        Args:
            dt (float): The constant time step for each frame. Defaults to 1/60.
        """
        self.frame: int = 0
        self.dt: float = dt

    def tick(self) -> int:
        """
        Advances the clock by one frame increment.
        
        Returns:
            int: The new frame ID after incrementing.
        """
        self.frame += 1
        return self.frame

    def reset(self, frame: int = 0) -> None:
        """
        Resets the clock to a specific frame ID. 
        Primarily used during simulation rollback operations.
        
        Args:
            frame (int): The target frame ID to reset to. Defaults to 0.
        """
        self.frame = frame

    def __repr__(self) -> str:
        """Returns a string representation of the clock's current state."""
        return f"<FixedClock frame={self.frame} dt={self.dt:.4f}>"
