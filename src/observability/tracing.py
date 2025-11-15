"""Tiny tracing helper for tests.

This file provides a simple context manager that records when a traced block
starts and ends. It is not a real tracer but is useful for tests and demos.
"""
from __future__ import annotations
from contextlib import ContextDecorator
import time
from typing import Optional, Callable, Any


class trace(ContextDecorator):
    """Context manager used as a lightweight tracer.

    Usage:
        with trace("operation"):
            ...
    """

    def __init__(self, name: str, recorder: Optional[Callable[[str], Any]] = None):
        self.name = name
        self.recorder = recorder
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        if self.recorder:
            self.recorder(f"start:{self.name}")
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        duration = time.time() - (self.start_time or time.time())
        if self.recorder:
            self.recorder(f"end:{self.name}:{duration:.6f}")
        return False
