"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `TOOL-KCAP-LITE-001`          | The Sovereign ID. |
| **Official Name** | `kcap_prototype_lite.py`      | The Filename.     |
| **Version** | **v1.0 [PROTOTYPE]** | The Standard.     |
| **Domain** | `TOOL-KCAP`                   | The Subject.      |
| **Celestial Class** | `[ASTEROID]`                  | The Weight.       |
| **Evolution** | `Core Stability`              | The Maturity.     |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations** | `IDENTITY: AxionRuntime`      | The Sovereign.    |

**The Spirit Bomb Axiom: Unambiguous Execution (Law 35)**
> Ethos: Clarity through DAMP (Descriptive and Meaningful Phrases).

WHAT: A lightweight, encapsulated capability for safely extracting string data from a specific file path.
HOW: Validates the target file path and returns the explicit UTF-8 encoded text using strictly DAMP-compliant variable names.
WHY: To serve as the structural, zero-entropy baseline for all future Kinetic Capabilities deployed within the Synarche.
"""

import os
from typing import Optional


class LiteNodeExtractor:
    """Encapsulated class to handle safe, deterministic file reading operations.
    Built to adhere to DAMP principles.
    """

    def __init__(self, repository_root_directory: str) -> None:
        """Initializes the extractor with a defined boundary.

        Args:
            repository_root_directory (str): The absolute path to the permitted root directory.

        """
        self.repository_root_directory = repository_root_directory

    def _validate_target_path(self, target_file_path: str) -> bool:
        """Private boundary method. Validates that the file exists and is safely
        within the repository bounds before attempting extraction.

        Args:
            target_file_path (str): The absolute path to the file.

        Returns:
            bool: True if the file exists and is accessible, False otherwise.

        """
        is_path_valid = os.path.exists(target_file_path)
        is_file = os.path.isfile(target_file_path)
        return is_path_valid and is_file

    def extract_text_from_node(self, target_file_path: str) -> Optional[str]:
        """The primary kinetic action. Extracts the exact string content from the validated path.

        Args:
            target_file_path (str): The file to read.

        Returns:
            Optional[str]: The extracted text if successful, or None if validation fails.

        """
        if not self._validate_target_path(target_file_path):
            print(
                f"[REJECTED] The target path is invalid or unreadable: {target_file_path}"
            )
            return None

        try:
            with open(target_file_path, mode="r", encoding="utf-8") as target_file:
                extracted_text = target_file.read()
                return extracted_text
        except IOError as input_output_error:
            print(
                f"[ERROR] A deterministic extraction failure occurred: {input_output_error!s}"
            )
            return None
