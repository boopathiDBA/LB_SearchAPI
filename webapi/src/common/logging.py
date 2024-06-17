import logging
import os

from pythonjsonlogger import jsonlogger


def _get_log_level() -> int:
    """
    Get log level.

    Currently this is derived from environment variable LOG_LEVEL.

    Supported values for LOG_LEVEL environment variable are the following.
    Source: https://docs.python.org/3/library/logging.html#logging-levels
        NOTSET = 0
        DEBUG = 10
        INFO = 20
        WARNING = 30
        ERROR = 40
        CRITICAL = 50

    Additional aliases:
        WARN = WARNING
        FATAL = CRITICAL
    """

    if (log_level := os.getenv("LOG_LEVEL")) is not None:
        return getattr(logging, log_level)

    # Return default level
    return logging.NOTSET


def setup_logging() -> None:
    """Set up logging for application.

    Set up format of logging to be JSON
    """
    logHandler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
        rename_fields={"levelname": "severity", "asctime": "timestamp"},
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    logHandler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(logHandler)

    logger.setLevel(_get_log_level())
