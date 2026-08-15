# Architectural Operations Playbook: Developer Environment Setup

**Playbook_ID:** `AOP-ENV-001`

**Version:** `1.0`

**Status:** `CANONICAL`

---

## Objective

---

To establish a standardized, repeatable procedure for configuring a new developer's local environment, ensuring all Synarche-specific dependencies and pathing are correctly initialized for seamless development and execution.

---

## Phase 1: Setup & Context

---

### Prerequisites

---

1. **Git:** A functional Git installation is required to clone the repository.
2. **Python:** A supported version of Python (e.g., 3.9+) must be installed and accessible from the command line.
3. **Repository Access:** The developer must have read access to the `Synarche_Workspace` repository.

### Architectural Rationale

---

The Synarche ecosystem is built upon a modular, package-based architecture. CORE utilities, such as the `synarche_logger`, reside in the `/packages` directory. For these packages to be universally importable by any script within the workspace, the Python interpreter must be explicitly told to include the workspace root in its search path. This playbook ensures this critical configuration is applied consistently.

---

## Phase 2: Execution Steps

---

1. **Clone the Repository:**
    Open a terminal or command prompt and clone the Synarche Workspace to your local machine.

    ```bash
    git clone <repository_url> c:\Users\Chris\Synarche_Workspace
    ```

2. **Configure PYTHONPATH:**
    This is the most critical step. You must set the `PYTHONPATH` environment variable to point to the **root** of the `Synarche_Workspace` directory. This allows Python to discover the shared packages.

    * **For Windows (Command Prompt):**

        ```bash
        set PYTHONPATH=C:\Users\Chris\Synarche_Workspace
        ```

        *(Note: To make this permanent, search for "Edit the system environment variables" in the Start Menu and add it to your User or System variables.)*

    * **For macOS / Linux (bash/zsh):**

        ```bash
        export PYTHONPATH=/c/Users/Chris/Synarche_Workspace
        ```

        *(Note: To make this permanent, add this line to your `~/.bashrc`, `~/.zshrc`, or `~/.profile` file.)*

---

## Phase 3: Validation & Verification

---

1. Create a temporary Python script named `validate_setup.py` in any directory **outside** of `c:\Users\Chris\Synarche_Workspace\packages`.
2. Add the following CODE to the script:

    ```python
    from synarche_logger import get_logger

    try:
        logger = get_logger("validation_script")
        logger.info("PYTHONPATH configuration is correct. The Synarche logger was successfully imported.")
        print("Validation successful!")
    except ImportError as e:
        print(f"Validation FAILED. Could not import from a shared package. Error: {e}")
    ```

3. Run the script from your terminal: `python validate_setup.py`.
4. **Success Condition:** The script executes without an `ImportError` and prints the "Validation successful!" message.
5. **Failure Condition:** The script raises an `ImportError`, indicating that `PYTHONPATH` is not set correctly.

---

## Rollback_Plan

---

If validation fails, the rollback procedure is straightforward:

1. **Unset the Variable:** Close the terminal session to clear the temporary variable. If set permanently, remove the `PYTHONPATH` entry from your system's environment variables.
2. **Verify Path:** Double-check that the path `C:\Users\Chris\Synarche_Workspace` is the correct, absolute path to the root of the cloned repository.
3. **Re-execute Phase 2:** Carefully repeat the steps to set the environment variable.
