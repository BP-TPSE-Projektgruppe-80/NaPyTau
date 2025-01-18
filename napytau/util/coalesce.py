from __future__ import annotations

from typing import Optional


def coalesce[T](*args: Optional[T]) -> T:
    for arg in args:
        if arg is not None:
            return arg
    raise ValueError("All arguments are None")
