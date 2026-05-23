"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-EXE-001`             | The Sovereign ID. |
| **Official Name**   | `executor.py`                 | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Execution Control (Law 12)**
> Implemented from Blueprint `GVRN.REG.DeterministicExecutor.md`.
> Ethos: Orchestration through precise synchronization.
"""

from typing import Any, Dict, Union

from .clock import FixedClock
from .parallel_scheduler import ParallelScheduler
from .scheduler import DeterministicScheduler
from .state import StateManager


class Executor:
    """Coordinates the execution of a frame by linking the scheduler, state, and clock.
    The Executor is responsible for the discrete simulation step logic, managing
    state snapshots, and handling temporal shifts (rollback).
    """

    def __init__(
        self,
        scheduler: Union[DeterministicScheduler, ParallelScheduler],
        state_manager: StateManager,
        clock: FixedClock,
    ) -> None:
        """Initializes the executor with required simulation components.

        Args:
            scheduler (Union[DeterministicScheduler, ParallelScheduler]): The task scheduler.
            state_manager (StateManager): The system for capturing/restoring state snapshots.
            clock (FixedClock): The deterministic time reference.

        """
        self.scheduler = scheduler
        self.state_manager = state_manager
        self.clock = clock
        # Global application state container
        self.state: Dict[str, Any] = {}

    def step(self) -> None:
        """Advances the simulation by one discrete frame.
        Captures a state snapshot, executes the task graph, and increments the clock.
        """
        # 1. Capture state snapshot BEFORE execution
        # Rollback reverts to the state AT the start of a frame.
        self.state_manager.save_state(self.clock.frame, self.state)

        # 2. Build execution context
        context: Dict[str, Any] = {
            "state": self.state,
            "dt": self.clock.dt,
            "frame": self.clock.frame,
        }

        # 3. Reset and execute the task graph
        self.scheduler.graph.reset()
        self.scheduler.execute(context)

        # 4. Advance the clock
        self.clock.tick()

    def rollback(self, target_frame: int) -> None:
        """Reverts the executor state and clock to a specific previous frame.

        Args:
            target_frame (int): The destination frame ID for the rollback operation.

        """
        if target_frame >= self.clock.frame:
            return

        restored_state = self.state_manager.load_state(target_frame)
        if restored_state is not None:
            self.state = restored_state
            self.clock.reset(target_frame)
            self.state_manager.purge_after(target_frame)
