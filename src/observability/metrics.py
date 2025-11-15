"""Simple in-memory metrics collector for tests.

This collector is intentionally tiny and dependency-free. It stores counters
in a dict and exposes increment/get operations suitable for unit tests.
"""
from typing import Dict


class MetricsCollector:
    """A tiny metrics collector that supports counters.

    Example:
        m = MetricsCollector()
        m.increment("requests")
        assert m.get("requests") == 1
    """

    def __init__(self) -> None:
        self._counters: Dict[str, int] = {}

    def increment(self, name: str, amount: int = 1) -> None:
        """Increment a named counter by amount (default 1)."""
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self._counters[name] = self._counters.get(name, 0) + amount

    def get(self, name: str) -> int:
        """Get the value of a named counter (0 if missing)."""
        return self._counters.get(name, 0)
