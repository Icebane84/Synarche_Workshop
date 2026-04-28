"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `NEX-DEC-AUD-001`             | The Sovereign ID. |
| **Official Name**   | `synarche_audit.py`           | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `NEX-DEC`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Telemetry Transparency (Law 22)**
> Implemented from Blueprint `GVRN.REG.SynarcheAudit.md`.
> Ethos: Accountability through automated logging.
"""

import asyncio
import functools
import logging
import time
import traceback
from typing import Any, Callable


def synarche_audit(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    The @synarche_audit architectural wrapper.
    Automates function entry/exit/error logging with full stack traces.
    Enforces Rule T201 by routing all diagnostic output through PhoenixLogger.
    
    Args:
        func (Callable): The function to be audited.
        
    Returns:
        Callable: The audited wrapper function (sync or async).
    """

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Asynchronous execution auditor.
        Captures start time, logs context, executes, and captures completion/failure.
        """
        logger = logging.getLogger("PhoenixLogger")
        start_time = time.perf_counter()

        logger.debug(f"EXEC_START: {func.__name__} | Context: {args}, {kwargs}")

        try:
            result = await func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            logger.info(f"EXEC_SUCCESS: {func.__name__} | Duration: {duration:.4f}s")
            return result
        except Exception as e:
            logger.error(
                f"EXEC_FAILURE: {func.__name__} | {type(e).__name__}: {str(e)}\n"
                f"STACK_TRACE:\n{traceback.format_exc()}"
            )
            raise

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Synchronous execution auditor.
        Captures start time, logs context, executes, and captures completion/failure.
        """
        logger = logging.getLogger("PhoenixLogger")
        start_time = time.perf_counter()

        logger.debug(f"EXEC_START: {func.__name__} | Context: {args}, {kwargs}")

        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            logger.info(f"EXEC_SUCCESS: {func.__name__} | Duration: {duration:.4f}s")
            return result
        except Exception as e:
            logger.error(
                f"EXEC_FAILURE: {func.__name__} | {type(e).__name__}: {str(e)}\n"
                f"STACK_TRACE:\n{traceback.format_exc()}"
            )
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
