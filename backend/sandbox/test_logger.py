# backend/sandbox/test_logger.py
"""Demo the custom logger — Work #... (Logging #1)"""
import sys
from pathlib import Path

# Add 'backend' (parent of this sandbox/ dir) to the path so 'core' resolves
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.logger import get_logger

log = get_logger(__name__)


def main():
    # The 5 standard levels, from least to most severe
    log.debug("DEBUG level - detailed info for developers")
    log.info("INFO level - normal application event")
    log.warning("WARNING level - unexpected, but still running")
    log.error("ERROR level - an operation failed")
    log.critical("CRITICAL level - severe failure, needs attention")

    # exception() is meant for an except block — it attaches the traceback for you
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("EXCEPTION - error captured with traceback")


if __name__ == "__main__":
    main()
