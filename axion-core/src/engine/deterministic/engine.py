"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-ENG-001`             | The Sovereign ID. |
| **Official Name**   | `engine.py`                  | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `GOVERNED_BY: TOOL-ENUMS-001` | The Network.      |

**The Spirit Bomb Axiom: Deterministic Synthesis (Law 01)**
> Implemented from Blueprint `CORE-ENGINE-DET-001`.
> Ethos: Frame-accurate simulation through structural rigidity.
"""

from typing import Any, Optional, Union

from ..ecs.component import ComponentStore
from ..ecs.manager import EntityManager
from ..ecs.resonance import ResonanceAuditor, ResonanceRegistry
from ..ecs.synergy import SynergyMetrics, SynergySystem
from ..persistence.insforge_transmuter import InsforgeTransmuter
from .clock import FixedClock
from .executor import Executor
from .graph import TaskGraph
from .parallel_scheduler import ParallelScheduler
from .scheduler import DeterministicScheduler
from .state import StateManager


class DeterministicEngine:
    """The High-Level Interface for the Axion Deterministic Engine.
    Encapsulates the graph, scheduler, and executor for easy use.
    Integrated with Insforge Cloud Persistence and ECS Synergy Metrics.

    This engine acts as the primary orchestrator for the simulation substrate,
    ensuring that all tasks are executed in a reproducible, frame-accurate manner.
    """

    def __init__(
        self,
        dt: float = 1 / 60,
        use_parallel: bool = False,
        insforge_key: Optional[str] = None,
    ) -> None:
        """Initializes the deterministic engine with the specified configuration.

        Args:
            dt (float): The fixed delta time for each simulation frame.
            use_parallel (bool): Whether to use the parallel scheduler.
            insforge_key (Optional[str]): API key for cloud state persistence.

        """
        self.graph = TaskGraph()
        self.use_parallel = use_parallel

        # Select scheduler based on requested mode
        if use_parallel:
            self.scheduler: Union[ParallelScheduler, DeterministicScheduler] = (
                ParallelScheduler(self.graph)
            )
        else:
            self.scheduler = DeterministicScheduler(self.graph)

        self.state_manager = StateManager()
        self.clock = FixedClock(dt)
        self.executor = Executor(self.scheduler, self.state_manager, self.clock)

        # Cloud Transmutation
        self.transmuter: Optional[InsforgeTransmuter] = None
        if insforge_key:
            self.transmuter = InsforgeTransmuter(
                "https://x93i6uma.us-east.insforge.app", insforge_key
            )

        # Resonance & Semantic Security
        self.resonance_registry = ResonanceRegistry()
        self.resonance_auditor = ResonanceAuditor(self.resonance_registry)

        # ECS Core Integration
        self.entity_manager = EntityManager()
        self.component_store = ComponentStore(self.resonance_auditor)
        self.synergy_system = SynergySystem(self.component_store)

        # Register ECS structures into the deterministic state map
        self.executor.state["entities"] = self.entity_manager
        self.executor.state["components"] = self.component_store
        self.synergy_metrics: Optional[SynergyMetrics] = None

    def register_task(self, task: Any) -> None:
        """Adds a task to the engine's execution graph.

        Args:
            task: The task object to be integrated into the simulation cycle.

        """
        self.graph.add_task(task)

    def step(self) -> None:
        """Advances the simulation by a single deterministic frame.
        Triggers execution, state updates, and synergy calculations.
        """
        self.executor.step()

        # Calculate Synergy Metrics for the current frame
        self.synergy_metrics = self.synergy_system.calculate_gss()

    def sync_to_cloud(self) -> None:
        """Synchronizes the current engine state to the Insforge cloud layer.
        Performs transmutation of entities, components, and binary snapshots.
        """
        if self.transmuter:
            # Sync Registry
            self.transmuter.transmute_entities(list(self.entity_manager.entities))
            # Sync Data
            self.transmuter.transmute_components(self.component_store)
            # Sync Binary Snapshot
            self.transmuter.save_snapshot(self.clock.frame, self.state)

    def initialize(self) -> None:
        """Validates the task graph and initializes all subsystems before simulation starts.
        Ensures the structural integrity of the dependency graph.
        """
        self.graph.validate()

    def run(self, frames: int = 1) -> None:
        """Executes the specified number of simulation frames sequentially.

        Args:
            frames (int): Number of frames to advance. Defaults to 1.

        """
        for _ in range(frames):
            self.step()

    def rollback(self, steps: int = 1) -> None:
        """Rolls back the simulation by a specified number of frames.
        Re-synchronizes high-level entity and component managers with the restored state.

        Args:
            steps (int): Number of frames to go back in time.

        """
        target_frame = max(0, self.clock.frame - steps)
        self.executor.rollback(target_frame)

        # Re-synchronize high-level pointers to the restored objects
        if "entities" in self.executor.state:
            self.entity_manager = self.executor.state["entities"]
        if "components" in self.executor.state:
            self.component_store = self.executor.state["components"]

    @property
    def state(self) -> Any:
        """Retrieves the current simulation state from the executor."""
        return self.executor.state

    @state.setter
    def state(self, value: Any) -> None:
        """Updates the engine's current state with the provided value."""
        self.executor.state = value

    def __repr__(self) -> str:
        """Returns a string representation showing the current frame of simulation."""
        return f"<DeterministicEngine frame={self.clock.frame}>"
