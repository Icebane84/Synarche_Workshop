"""
# UMB-TASKCONTEXT-001: The Task Context Manager (Hephaestus)

# I. Universal Identification & Provenance (The Vector Signature)
| Field | Value |
| :--- | :--- |
| **1. Artifact ID** | `UMB-TASKCONTEXT-001` |
| **2. Official Name** | `task_context.py` |
| **3. Version** | **v15.0 [OMEGA]** |
| **4. Provenance** | **Reforged: 2026-04-28** |
| **5. Domain** | `GVRN` |
| **6. Evolution** | **Purposeful Drive** |
| **7. Celestial Class** | `[PLANET]` |
| **8. Tier** | **Operational** |
| **9. Status (State)** | `[ACTIVE]` |
| **10. Ethos** | **Zero Entropy** |
| **11. Integrity Hash** | `[UIP-V15-LOCK]` |

---

### **I.B. Axiom Reference**
> "The Context is the Law that governs the parameters of the Task."

"""

from typing import Any, Dict, List, Optional


class TaskContext:
    """
    The Nexus Context Repository.
    Stores the immutable parameters of the current work session.
    """

    # --- Core Identity ---
    task_id: str
    task_name: str
    task_type: str  # Development, Audit, Refactor, Documentation

    # --- State ---
    status: str  # PENDING, IN_PROGRESS, COMPLETE
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    progress_pct: float = 0.0

    # --- Creative State ---
    max_depth: int = 3  # Limit for recursion
    is_recursive: bool = False  # Trigger for recursive operations
    resonance_bias: float = 0.5  # Influences AI generation (0.0 to 1.0)

    # --- Procedural Configuration ---
    allow_unsafe: bool = False  # Flag to bypass safety checks (ADMIN ONLY)
    max_operations: int = 100  # Hard limit to prevent infinite loops
    output_format: str = "TEXT"  # Options: TEXT, JSON, MARKDOWN, TUPLE

    # --- Connection ---
    supabase_client: Any | None = None  # Database connection

    def __init__(self, task_id: str = "001-TASK-ID"):
        self.task_id = task_id
        self.status = "PENDING"
        self.is_recursive = False
        self.task_name = "NEXUS DIRECTIVE"
        self.task_type = "DEVELOPMENT"
        self.priority = "CRITICAL"
        self.progress_pct = 0.0
        self.max_depth = 3
        self.resonance_bias = 0.5
        self.allow_unsafe = False
        self.max_operations = 100
        self.output_format = "TEXT"

    def update_progress(self, value: float) -> None:
        """Updates the completion percentage."""
        self.progress_pct = max(0.0, min(100.0, value))
        if self.progress_pct == 100.0:
            self.status = "COMPLETE"

    def set_recursive(self, value: bool, depth: int = 3) -> None:
        """Enables/Disables recursion and sets depth."""
        self.is_recursive = value
        self.max_depth = depth

    def validate_operation(self, operation_cost: int = 1) -> bool:
        """
        Checks if an operation is permitted under current constraints.
        """
        if self.status == "COMPLETE":
            raise PermissionError(f"Task {self.task_id} is already COMPLETE.")

        if not self.allow_unsafe:
            # Check if operation is too deep
            current_depth = self._calculate_current_depth()
            if current_depth >= self.max_depth:
                raise RecursionError(f"Operation exceeds max depth of {self.max_depth}.")

        # Check if we've hit the operation limit
        self.max_operations -= operation_cost
        if self.max_operations < 0:
            raise RuntimeError(f"Operation limit reached for task {self.task_id}.")

        return True

    def _calculate_current_depth(self) -> int:
        """Calculates the current recursion depth based on logs (simple simulation)."""
        # In a real scenario, this would check the call stack or logs
        # For now, we assume a simple linear progression if active
        if self.is_recursive:
            return int(self.progress_pct / 20)  # Rough estimate based on completion
        return 0
