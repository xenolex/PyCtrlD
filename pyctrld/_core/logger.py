"""Custom logging configuration for the PyCtrlD library.

This module provides a custom logger with an additional TRACE level for detailed debugging.
The logging level can be configured via the LOGGING_LEVEL environment variable.
"""

from __future__ import annotations

import logging
import os
from typing import Any

LOGGING_LEVEL: int | str = os.getenv("LOGGING_LEVEL", logging.INFO)

TRACE: int = 1
logging.addLevelName(TRACE, "TRACE")


class Log(logging.Logger):
    """Custom logger class with TRACE level support.

    This logger extends the standard logging.Logger to provide an additional
    TRACE level (level 1) for very detailed debugging output.

    Args:
        name: The name of the logger.
        level: The logging level threshold. Defaults to LOGGING_LEVEL from environment.
    """

    def __init__(self, name: str, level: int | str = LOGGING_LEVEL) -> None:
        """Initialize the custom logger.

        Args:
            name: The name of the logger instance.
            level: The minimum logging level. Can be an int or string like 'DEBUG'.
        """
        super().__init__(name, level)

    def trace(self, message: str, *args: Any, **kws: Any) -> None:
        """Log a message with TRACE level.

        TRACE is a level below DEBUG for extremely detailed diagnostic information.

        Args:
            message: The log message format string.
            *args: Variable arguments for message formatting.
            **kws: Keyword arguments passed to the logging system.
        """
        if self.isEnabledFor(TRACE):
            self._log(TRACE, message, args, **kws)


logging.setLoggerClass(Log)


logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s::%(name)s::%(levelname)s::%(message)s",
    encoding="utf-8",
    force=True,
)

# Main logger instance for the pyctrld library
logger: Log = logging.getLogger("pyctrld")  # type: ignore[assignment]
