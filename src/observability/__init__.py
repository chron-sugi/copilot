"""Observability helpers (logging, tracing, metrics).

This package provides lightweight, dependency-free helpers suitable for
small projects and tests. Each module contains a minimal implementation
that can be replaced with a real observability library later.
"""

from .logger import configure_logger
from .tracing import trace
from .metrics import MetricsCollector

__all__ = ["configure_logger", "trace", "MetricsCollector"]
