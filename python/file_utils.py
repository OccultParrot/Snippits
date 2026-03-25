"""
File utility snippets for common file operations.
"""

import os
import json
import csv
import shutil
from pathlib import Path
from typing import Any, Generator


def read_json(filepath: str) -> Any:
    """Read and parse a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath: str, data: Any, indent: int = 2) -> None:
    """Write data to a JSON file with pretty-printing."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def read_csv_as_dicts(filepath: str) -> list[dict]:
    """Read a CSV file and return a list of row dictionaries."""
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_dicts_to_csv(filepath: str, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    """Write a list of dictionaries to a CSV file."""
    if not rows:
        return
    keys = fieldnames or list(rows[0].keys())
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def read_lines(filepath: str) -> list[str]:
    """Read all lines from a text file, stripping trailing newlines."""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def iter_lines(filepath: str) -> Generator[str, None, None]:
    """Lazily iterate over lines of a large text file."""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def ensure_dir(path: str) -> Path:
    """Create a directory (and parents) if it does not exist. Returns a Path object."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_remove(path: str) -> bool:
    """Delete a file or directory tree without raising an error if it doesn't exist."""
    p = Path(path)
    if p.is_dir():
        shutil.rmtree(p)
        return True
    if p.exists():
        p.unlink()
        return True
    return False


def find_files(root: str, pattern: str = "*") -> list[Path]:
    """Recursively find all files matching a glob pattern under root."""
    return list(Path(root).rglob(pattern))


def file_size_mb(filepath: str) -> float:
    """Return the size of a file in megabytes."""
    return os.path.getsize(filepath) / (1024 * 1024)
