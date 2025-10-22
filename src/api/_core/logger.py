from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

load_dotenv()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)

TRACE = 1
logging.addLevelName(TRACE, "TRACE")


class Log(logging.Logger):
    def __init__(self, name, level=LOGGING_LEVEL):
        super().__init__(name, level)

    def trace(self, message, *args, **kws):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, message, args, **kws)


logging.setLoggerClass(Log)


logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s::%(name)s::%(levelname)s::%(message)s",
    encoding="utf-8",
    force=True,
)
logger = logging.getLogger("pyctrld")
