"""Minimal logging helper.

Provides a small wrapper to configure and return a standard library logger.
This keeps tests deterministic and avoids pulling heavy logging frameworks.
"""
import logging


def configure_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger.

    Args:
        name: logger name
        level: logging level (defaults to logging.INFO)

    Returns:
        A configured ``logging.Logger`` instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
