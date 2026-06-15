# _shared/utils.py
# Common helpers: structured logging, timing decorators, and token counting.
import logging
import time
from functools import wraps
from _shared.config import settings


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger configured from settings."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    return logging.getLogger(name)


def timer(func):
    """Decorator: log wall-clock execution time of any function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        logger.debug(f"{func.__name__} completed in {elapsed:.1f}ms")
        return result
    return wrapper


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token (good enough for prompt budgeting)."""
    return len(text) // 4
