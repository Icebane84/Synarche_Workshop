"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `TOOL-GUCA-COM-001`           | The Sovereign ID. |
| **Official Name**   | `guca_command.py`             | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `TOOL-GUCA`                   | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `SYNERGIZES: SourceMap`       | The Sovereign.    |

**The Spirit Bomb Axiom: Command Sovereignty (Law 01)**
> Implemented from Blueprint `GVRN.REG.GucaCommand.md`.
> Ethos: Action through Abstraction.
"""

import abc
import json  # FIX: moved from __main__ to module level (CODEX-LAW-03 compliance)
from collections.abc import Sequence
from typing import Any

# --- Core GUCA Framework ---


class GUCACommand(abc.ABC):
    """
    Abstract Base Class for all GUCA Commands (Abstraction).
    Defines the standard interface for executable operations within the pipeline.
    """

    def __init__(self, name: str, description: str) -> None:
        """
        Initializes the command with a name and description.
        
        Args:
            name (str): The display name of the command.
            description (str): A brief description of the command's purpose.
        """
        self.name = name
        self.description = description

    @abc.abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Executes the command with the given context.
        
        Args:
            context (dict[str, Any]): The operational context to modify.
            
        Returns:
            dict[str, Any]: The updated operational context.
        """
        pass

    def __str__(self) -> str:
        """Returns the string representation of the command."""
        return f"[Command: {self.name}] {self.description}"


class GUCAExecutor:
    """
    Executes GUCA Commands polymorphically.
    Manages the sequential execution of command pipelines and context propagation.
    
    Synergy Note: Can wrap calls to structure_enforcer.py as GUCACommand
    subclasses to integrate automated enforcement into any pipeline.
    """

    def execute_commands(self, commands: Sequence[GUCACommand], initial_context: dict[str, Any]) -> dict[str, Any]:
        """
        Executes a sequence of commands starting with an initial context.
        
        Args:
            commands (Sequence[GUCACommand]): The list of commands to execute.
            initial_context (dict[str, Any]): The starting context.
            
        Returns:
            dict[str, Any]: The final context after all commands have executed.
        """
        current_context = initial_context.copy()
        for command in commands:
            current_context = command.execute(current_context)
        return current_context


# --- Command Implementations ---


class DataProcessingCommand(GUCACommand):
    """
    Base command for data processing operations (Inheritance).
    Provides utility methods for getting and setting data within the context.
    """

    def __init__(self, name: str, description: str, data_key: str) -> None:
        """
        Initializes the data processing command.
        
        Args:
            name (str): Command name.
            description (str): Command description.
            data_key (str): The key in the context to operate on.
        """
        super().__init__(name, description)
        self.data_key = data_key

    def _get_data(self, context: dict[str, Any]) -> Any:
        """
        Retrieves data from the context using the data_key.
        
        Args:
            context (dict[str, Any]): The current context.
            
        Returns:
            Any: The retrieved data.
            
        Raises:
            ValueError: If the data_key is missing from the context.
        """
        data = context.get(self.data_key)
        if data is None:
            raise ValueError(f"Context missing required data_key: {self.data_key}")
        return data

    def _set_data(self, context: dict[str, Any], new_data: Any) -> None:
        """
        Sets data in the context using the data_key.
        
        Args:
            context (dict[str, Any]): The current context.
            new_data (Any): The data to set.
        """
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
    """
    Encapsulates data storage operations (Encapsulation — The Boundary Principle).
    Provides a private storage mechanism for processed artifacts.
    """

    def __init__(self) -> None:
        """Initializes an empty private data dictionary."""
        self.__data: dict[str, Any] = {}

    def save(self, key: str, value: Any) -> None:
        """
        Saves a value to the private store.
        
        Args:
            key (str): The storage key.
            value (Any): The value to persist.
        """
        self.__data[key] = value
        print(f"  - DataStore: Saved '{key}'")

    def load(self, key: str) -> Any:
        """
        Loads a value from the private store.
        
        Args:
            key (str): The storage key.
            
        Returns:
            Any: The retrieved value, or None if not found.
        """
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
