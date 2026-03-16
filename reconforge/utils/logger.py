import logging
import sys

def setup_logger(name="ReconForge"):
    """
    Configure and return a logger for ReconForge.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)

    # Avoid adding multiple handlers if the logger is reused
    if not logger.handlers:
        logger.addHandler(ch)

    return logger
