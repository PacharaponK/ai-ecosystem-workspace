# backend/core/logger.py
"""
Design:
  1. levels     — DEBUG / INFO / WARNING / ERROR / CRITICAL, the logging module standard
  2. formatter  — timestamp + level + module + message
  3. handlers   — RotatingFileHandler (writes to logs/app.log, rotates when full)
                  + StreamHandler (prints to the console at the same time)
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import settings

# Anchor paths to backend/ (parent of core/) so logs always land in the same
# place no matter which directory the script is run from
BACKEND_DIR = Path(__file__).resolve().parent.parent

# timestamp + level + module + message
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "app") -> logging.Logger:
    """Build (or reuse) a logger wired to a console + rotating file handler.

    Usage:
        from core.logger import get_logger
        log = get_logger(__name__)
        log.info("message")
    """
    logger = logging.getLogger(name)

    # logging.getLogger(name) returns the same object for the same name. Without
    # this guard, calling get_logger() again would stack another set of handlers
    # and every message would be printed multiple times.
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # 1) console handler — immediate feedback while running a script
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2) rotating file handler — persists to disk; once a file hits max_bytes it
    #    starts a new one, keeping backup_count older files (app.log.1, app.log.2, ...)
    log_path = BACKEND_DIR / settings.log_file
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Don't bubble up to the root logger, otherwise records get emitted twice
    logger.propagate = False

    return logger
