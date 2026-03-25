"""
Data structure utility snippets.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Chunking / batching
# ---------------------------------------------------------------------------

def chunks(lst: list[T], size: int) -> list[list[T]]:
    """Split a list into consecutive chunks of a given size.

    Example:
        chunks([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
    """
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def flatten(nested: list[Any]) -> list[Any]:
    """Recursively flatten a nested list of arbitrary depth.

    Example:
        flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]
    """
    result: list[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# Dictionary helpers
# ---------------------------------------------------------------------------

def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge *override* into *base*, returning a new dictionary.

    Override values win for scalar conflicts; nested dicts are merged recursively.

    Example:
        deep_merge({"a": 1, "b": {"x": 1}}, {"b": {"y": 2}, "c": 3})
        -> {"a": 1, "b": {"x": 1, "y": 2}, "c": 3}
    """
    merged = base.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def invert_dict(d: dict[Any, Any]) -> dict[Any, list[Any]]:
    """Invert a dictionary, mapping each value to a list of keys that held it.

    Example:
        invert_dict({"a": 1, "b": 2, "c": 1}) -> {1: ["a", "c"], 2: ["b"]}
    """
    result: dict[Any, list[Any]] = defaultdict(list)
    for k, v in d.items():
        result[v].append(k)
    return dict(result)


def pick(d: dict[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    """Return a new dict containing only the specified keys.

    Example:
        pick({"a": 1, "b": 2, "c": 3}, ["a", "c"]) -> {"a": 1, "c": 3}
    """
    return {k: d[k] for k in keys if k in d}


def omit(d: dict[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    """Return a new dict with the specified keys removed.

    Example:
        omit({"a": 1, "b": 2, "c": 3}, ["b"]) -> {"a": 1, "c": 3}
    """
    exclude = set(keys)
    return {k: v for k, v in d.items() if k not in exclude}


# ---------------------------------------------------------------------------
# Set helpers
# ---------------------------------------------------------------------------

def group_by(items: Iterable[T], key_fn: Any) -> dict[Any, list[T]]:
    """Group items by a key function, similar to SQL GROUP BY.

    Example:
        group_by(["ant", "bee", "cat", "dog"], key_fn=lambda s: s[0])
        -> {"a": ["ant"], "b": ["bee"], "c": ["cat"], "d": ["dog"]}
    """
    groups: dict[Any, list[T]] = defaultdict(list)
    for item in items:
        groups[key_fn(item)].append(item)
    return dict(groups)


# ---------------------------------------------------------------------------
# Stack / Queue implemented as a class
# ---------------------------------------------------------------------------

class Stack(list[T]):
    """A simple LIFO stack built on top of Python's list."""

    def push(self, item: T) -> None:
        self.append(item)

    def peek(self) -> T:
        if not self:
            raise IndexError("peek from empty stack")
        return self[-1]


class Queue(list[T]):
    """A simple FIFO queue built on top of Python's list."""

    def enqueue(self, item: T) -> None:
        self.append(item)

    def dequeue(self) -> T:
        if not self:
            raise IndexError("dequeue from empty queue")
        return self.pop(0)
