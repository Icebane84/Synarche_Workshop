# AOP-PHX-LOG-001: The Phoenix Logging Protocol Setup
# This playbook defines the executable workflow for configuring the dual-stream logger
# and the `synarche_audit` decorator as per UMB-PHX-LOG-001.

import asyncio
import functools
import logging
import time
import traceback
from enum import Enum, auto
from typing import Callable, Any

# --- DEPENDENCIES ---
# @system/logging (Kernel) - Core logger initialization
# @nexus/decorators (Synapse) - For the `synarche_audit` decorator
# GVRN-STD-ENUM-001 - Mandates Enum for logging levels
# UMB-PHX-LOG-001 - The overarching logging protocol


# Define ProcessStatus Enum as per GVRN-STD-ENUM-001
class ProcessStatus(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    DEBUG = auto()  # Added for decorator's debug entry log

# --- I. Standard Initialization (from GUCA: Core Implementation Standard) ---
# This function would reside in @system/logging/phoenix_logger.py
def setup_synarche_logging() -> logging.Logger:
    """Initializes the PhoenixLogger with dual-stream handlers:
    Console (INFO+) for Transparency, File (ERROR+) for Accountability.
    """
    logger = logging.getLogger("PhoenixLogger")
    logger.setLevel(logging.DEBUG)  # Root logger captures all, handlers filter

    # ISO-8601 Format for V-Control (Timestamping)
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler (INFO and above) - The Pulse
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(log_format)

    # File Handler (ERROR and above) - The Memory
    f_handler = logging.FileHandler("error_audit.log")
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(log_format)

    # Prevent duplicate handlers on re-run (important for system entry points)
    if not logger.handlers:
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    logger.info(
        "PhoenixLogger initialized: Dual-stream logging active (Console INFO+, File ERROR+)."
    )
    return logger


# --- II. The `synarche_audit` Decorator (from GUCA: Core Implementation Standard) ---
# This decorator would reside in @nexus/decorators/synarche_audit.py
def synarche_audit(func: Callable[..., Any]) -> Callable[..., Any]:
    """Architectural wrapper for standardized logging compliance.
    Automates function entry/exit/error logging with full stack traces.
    Enforces T201 by routing all diagnostic output through PhoenixLogger.
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Ensure logger is fetched, assuming it's been set up
        logger = logging.getLogger("PhoenixLogger")
        start_time = time.perf_counter()

        # Phase: Start (Level: DEBUG) - Captures arguments for context
        logger.debug(f"Executing {func.__name__} | Args: {args} | Kwargs: {kwargs}")

        try:
            # Execute original function (handles both sync and async)
            result = (
                await func(*args, **kwargs)
                if asyncio.iscoroutinefunction(func)
                else func(*args, **kwargs)
            )

            end_time = time.perf_counter()
            duration = end_time - start_time
            # Phase: Success (Level: INFO) - Logs execution time
            logger.info(f"Finished {func.__name__} in {duration:.4f}s")
            return result
        except Exception as e:
            # Phase: Failure (Level: ERROR) - Captures full trace for FileHandler audit (UMB-PHX-LOG-001, T202)
            error_message = f"CRITICAL FAILURE in {func.__name__}: {type(e).__name__}: {e!s}\n{traceback.format_exc()}"
            logger.error(error_message)
            raise  # Re-raise to ensure system-level awareness (Integrity pillar, T203)

    return wrapper


# --- EXECUTION BLOCKS (Illustrative usage, simulating directives from SELT-PHX-LOG-DEPLOY-001) ---

# Global logger setup (simulates application entry point)
phoenix_logger = setup_synarche_logging()


# Example function demonstrating Directive Alpha: `synarche_audit` deployment
@synarche_audit
async def process_core_axiom(axiom_id: str, payload: dict):
    """Simulates a core processing function within the AISTF engine."""
    phoenix_logger.info(
        f"Processing axiom {axiom_id} with payload {payload.get('type')}."
    )
    if "error" in payload.get("type", "").lower():
        raise ValueError(f"Simulated error for axiom {axiom_id}")
    await asyncio.sleep(0.1)  # Simulate work
    return {"status": "processed", "axiom_id": axiom_id}


# Example of how Directive Beta's updated Sentinel would interact (conceptual)
def simulate_sentinel_audit(code_snippet: str) -> bool:
    """Conceptual function for Sentinel's updated audit process."""
    if "print(" in code_snippet or "console.log(" in code_snippet:
        phoenix_logger.error(
            f"AUDIT VIOLATION: T201 found in code snippet. {code_snippet[:50]}..."
        )
        return False
    if "@synarche_audit" not in code_snippet:
        phoenix_logger.warning(
            f"AUDIT WARNING: `synarche_audit` missing from critical function: {code_snippet[:50]}..."
        )
        return True  # It's a warning, not a hard fail for this simulation
    phoenix_logger.info(f"AUDIT PASSED: Code snippet compliant. {code_snippet[:50]}...")
    return True


# Example of how Directive Gamma's OGLN would use the log file (conceptual, relies on actual `error_audit.log` content)
async def ogln_ingest_error_logs(log_file_path: str) -> list[dict[str, Any]]:
    """Simulates OGLN reading and processing the error_audit.log."""
    phoenix_logger.info(f"OGLN @mem-proc initiating ingestion of {log_file_path}.")
    processed_errors = []
    try:
        with open(log_file_path) as f:
            for line in f:
                if "CRITICAL FAILURE" in line:
                    phoenix_logger.debug(
                        f"OGLN identified critical error: {line.strip()[:100]}"
                    )
                    # This would call a more sophisticated parsing function (like parse_error_log_entry from previous turns)
                    processed_errors.append(
                        {"raw_log": line.strip(), "parsed_status": "ready_for_analysis"}
                    )
                    await asyncio.sleep(0.01)  # Simulate async processing
        phoenix_logger.info(
            f"OGLN completed ingestion. {len(processed_errors)} critical errors identified."
        )
        return processed_errors
    except FileNotFoundError:
        phoenix_logger.warning(
            f"OGLN: Log file '{log_file_path}' not found, no errors to ingest."
        )
        return []


if __name__ == "__main__":

    async def run_all_demos() -> None:
        # Demo Directive Alpha: Deploy synarche_audit
        try:
            await process_core_axiom("AX-42", {"type": "data_stream"})
            await process_core_axiom("AX-FAIL-01", {"type": "error_injection"})
        except ValueError:
            pass  # Expected for the error injection

        # Demo Directive Beta: Update Sentinel-PRS-Check
        print("\n--- Sentinel Audit Simulation ---")
        simulate_sentinel_audit("def my_func(): print('hello')")
        simulate_sentinel_audit("def another_func(): console.log('hello')") # Test for console.log
        simulate_sentinel_audit("@synarche_audit\nasync def compliant_func(): pass")
        simulate_sentinel_audit("def compliant_func_sync(): pass") # Test for missing decorator on sync func
        simulate_sentinel_audit("def compliant_func_sync_with_print(): print('hello')") # Test for missing decorator on sync func with print
        simulate_sentinel_audit("@synarche_audit\nasync def compliant_async_func_with_print(): print('hello')") # Test for compliant async func with print
        simulate_sentinel_audit("@synarche_audit\nasync def compliant_async_func(): pass") # Test for compliant async func
        simulate_sentinel_audit("@synarche_audit\nclass MyClass:\n    def my_method(self): pass") # Test for decorator on a method
        simulate_sentinel_audit("class MyClass:\n    @synarche_audit\n    def my_method(self): pass") # Test for decorator on a method, different syntax
        simulate_sentinel_audit("class MyClass:\n    def my_method(self): print('hello')") # Test for missing decorator on a method with print
        simulate_sentinel_audit("class MyClass:\n    def my_method(self): console.log('hello')") # Test for missing decorator on a method with console.log
        simulate_sentinel_audit("class MyClass:\n    @synarche_audit\n    async def my_async_method(self): pass") # Test for decorator on an async method
        simulate_sentinel_audit("class MyClass:\n    async def my_async_method(self): pass") # Test for missing decorator on an async method
        simulate_sentinel_audit("class MyClass:\n    async def my_async_method_with_print(self): print('hello')") # Test for missing decorator on an async method with print
        simulate_sentinel_audit("class MyClass:\n    async def my_async_method_with_console_log(self): console.log('hello')") # Test for missing decorator on an async method with console.log
        simulate_sentinel_audit("class MyClass:\n    @synarche_audit\n    async def compliant_async_method_with_print(self): print('hello')") # Test for compliant async method with print
        simulate_sentinel_audit("class MyClass:\n    @synarche_audit\n    async def compliant_async_method_with_console_log(self): console.log('hello')") # Test for compliant async method with console.log
        simulate_sentinel_audit("class MyClass:\n    @synarche_audit\n    def compliant_method_with_print(self): print('hello')") # Test for compliant method with print
        simulate_sentinel_audit("class MyClass:\n    @synarche_audit\n    def compliant_method_with_console_log(self): console.log('hello')") # Test for compliant method with console.log
        simulate_sentinel_audit("@synarche_audit\ndef compliant_sync_func(): pass") # Test for compliant sync func
        simulate_sentinel_audit("def non_compliant_func() -> None: pass") # Test for missing decorator
        # Demo Directive Gamma: Integrate error_audit.log with OGLN
        print("\n--- OGLN Error Ingestion Simulation ---")
        await ogln_ingest_error_logs("error_audit.log")

    print("\n--- Running all demos ---")
    asyncio.run(run_all_demos())
    print("--- Demos finished ---")
