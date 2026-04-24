"""
---
# Block A: Universal Identification & Provenance (UIP-V15)
artifact_anchor:
  id: "TOOL.GUCA.Command"
  version: "v1.1.0"
  provenance: "2026-04-23"
  domain: "TOOL"
  celestial_class: "PLANET"
  tier: "SOVEREIGN"
  state: "CANONIZED"
  ethos: "ZERO-ENTROPY"
  layer: "@system/"
  relations:
    - type: "SYNERGIZES_WITH"
      node: "TOOL.Forge.SourceMap"
    - type: "SYNERGIZES_WITH"
      node: "TOOL.Forge.Daemon"
    - type: "INTEGRATES_WITH"
      node: "TOOL.StructureEnforcer"
    - type: "GOVERNED_BY"
      node: "CODEX-LAW-01"
---

TOOL.GUCA.Command — The Sovereign Command Pipeline
===================================================
Canonical path: @system/guca_command
Physical path:  axion-core/src/cse/guca_command.py

Full GUCACommand ABC + GUCAExecutor polymorphic pipeline.
Implements the four OOP pillars as sovereign architectural axioms:
  1. Abstraction  → GUCACommand (Abstract Base Class)
  2. Polymorphism → GUCAExecutor.execute_commands()
  3. Inheritance  → DataProcessingCommand hierarchy
  4. Encapsulation → DataStore (private __data)

Relations:
  SYNERGIZES_WITH: TOOL.Forge.SourceMap
  SYNERGIZES_WITH: TOOL.Forge.Daemon
  INTEGRATES_WITH: TOOL.StructureEnforcer
  GOVERNED_BY: CODEX-LAW-01 (Code-Law: Abstraction Sovereignty)

[OMNI-ARTIFACT-ANCHOR] ID: TOOL.GUCA.Command VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-23
"""

import abc
import json  # FIX: moved from __main__ to module level (CODEX-LAW-03 compliance)
from collections.abc import Sequence
from typing import Any

# --- Core GUCA Framework ---


class GUCACommand(abc.ABC):
    """Abstract Base Class for all GUCA Commands (Abstraction)."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abc.abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Executes the command with the given context."""
        pass

    def __str__(self) -> str:
        return f"[Command: {self.name}] {self.description}"


class GUCAExecutor:
    """
    Executes GUCA Commands polymorphically.

    Synergy Note: Can wrap calls to structure_enforcer.py as GUCACommand
    subclasses to integrate automated enforcement into any pipeline.
    """

    def execute_commands(self, commands: Sequence[GUCACommand], initial_context: dict[str, Any]) -> dict[str, Any]:
        current_context = initial_context.copy()
        for command in commands:
            current_context = command.execute(current_context)
        return current_context


# --- Command Implementations ---


class DataProcessingCommand(GUCACommand):
    """Base command for data processing operations (Inheritance)."""

    def __init__(self, name: str, description: str, data_key: str) -> None:
        super().__init__(name, description)
        self.data_key = data_key

    def _get_data(self, context: dict[str, Any]) -> Any:
        data = context.get(self.data_key)
        if data is None:
            raise ValueError(f"Context missing required data_key: {self.data_key}")
        return data

    def _set_data(self, context: dict[str, Any], new_data: Any) -> None:
        context[self.data_key] = new_data


class FlattenJsonCommand(DataProcessingCommand):
    """Flattens a nested JSON object into a flat key-value dict."""

    def __init__(self, input_key: str = "raw_json_data", output_key: str = "flattened_json_data"):
        super().__init__(
            name="Flatten JSON",
            description=f"Flattens JSON data from '{input_key}' to '{output_key}'.",
            data_key=input_key,
        )
        self.output_key = output_key

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        raw_json = self._get_data(context)
        try:
            obj = json.loads(raw_json)
            flattened = {
                f"{k}.{inner_k}": inner_v
                for k, v in obj.items()
                if isinstance(v, dict)
                for inner_k, inner_v in v.items()
            }
            for k, v in obj.items():
                if not isinstance(v, dict):
                    flattened[k] = v
            self._set_data(context, flattened)
            context[self.output_key] = flattened
        except json.JSONDecodeError as e:
            context["error"] = f"JSON Decode Error: {e}"
        return context


class DataStore:
    """Encapsulates data storage operations (Encapsulation — The Boundary Principle)."""

    def __init__(self) -> None:
        self.__data: dict[str, Any] = {}

    def save(self, key: str, value: Any) -> None:
        self.__data[key] = value
        print(f"  - DataStore: Saved '{key}'")

    def load(self, key: str) -> Any:
        return self.__data.get(key)


class SaveToDataStoreCommand(GUCACommand):
    """Saves a context value to the encapsulated DataStore."""

    def __init__(
        self,
        data_store: DataStore,
        input_key: str = "data_to_save",
        store_key: str = "processed_data",
    ) -> None:
        super().__init__(
            name="Save to DataStore",
            description=f"Saves data from '{input_key}' to encapsulated DataStore as '{store_key}'.",
        )
        self.__data_store = data_store
        self.input_key = input_key
        self.store_key = store_key

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        data = context.get(self.input_key)
        if data is None:
            print(f"  - No data found in context for key: {self.input_key}")
            return context
        self.__data_store.save(self.store_key, data)
        context["data_store_status"] = f"Saved {self.store_key}"
        return context


if __name__ == "__main__":
    executor = GUCAExecutor()
    data_store = DataStore()

    initial_context = {"raw_json_data": '{"user": {"id": 101, "name": "Charlie"}, "preferences": {"theme": "dark"}}'}

    commands_to_run = [
        FlattenJsonCommand(),
        SaveToDataStoreCommand(data_store, input_key="flattened_json_data", store_key="user_config"),
    ]

    final_context = executor.execute_commands(commands_to_run, initial_context)
    print("\nFinal Context:", final_context)
    print("DataStore:", data_store.load("user_config"))
