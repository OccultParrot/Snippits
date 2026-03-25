"""
String utility snippets for common string operations.
"""

import re
import unicodedata
from collections import Counter


def slugify(text: str, separator: str = "-") -> str:
    """Convert a string to a URL-friendly slug.

    Example:
        slugify("Hello World!") -> "hello-world"
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_-]+", separator, text)


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to max_length characters, appending suffix if cut.

    Example:
        truncate("Hello World", 8) -> "Hello..."
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def camel_to_snake(name: str) -> str:
    """Convert a camelCase or PascalCase string to snake_case.

    Example:
        camel_to_snake("MyVariableName") -> "my_variable_name"
    """
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(name: str, pascal: bool = False) -> str:
    """Convert a snake_case string to camelCase or PascalCase.

    Example:
        snake_to_camel("my_variable_name") -> "myVariableName"
        snake_to_camel("my_variable_name", pascal=True) -> "MyVariableName"
    """
    parts = name.split("_")
    if pascal:
        return "".join(word.capitalize() for word in parts)
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def count_words(text: str) -> dict[str, int]:
    """Return a word-frequency dictionary for the given text (case-insensitive).

    Example:
        count_words("the cat sat on the mat") -> {"the": 2, "cat": 1, ...}
    """
    words = re.findall(r"\b\w+\b", text.lower())
    return dict(Counter(words))


def is_palindrome(text: str) -> bool:
    """Return True if text is a palindrome, ignoring case and non-alphanumeric characters.

    Example:
        is_palindrome("A man a plan a canal Panama") -> True
    """
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return cleaned == cleaned[::-1]


def wrap_text(text: str, width: int = 80) -> str:
    """Wrap plain text to a given column width without breaking words.

    Example:
        wrap_text("one two three four five", width=10)
    """
    import textwrap
    return textwrap.fill(text, width=width)


def remove_duplicates_preserve_order(items: list[str]) -> list[str]:
    """Remove duplicate strings while preserving original insertion order.

    Example:
        remove_duplicates_preserve_order(["a", "b", "a", "c"]) -> ["a", "b", "c"]
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def extract_urls(text: str) -> list[str]:
    """Extract all http/https URLs from a string.

    Example:
        extract_urls("Visit https://example.com or http://test.org for info.")
    """
    pattern = r"https?://[^\s\"'<>]+"
    return re.findall(pattern, text)


def multi_replace(text: str, replacements: dict[str, str]) -> str:
    """Replace multiple substrings in a single pass.

    Example:
        multi_replace("foo bar baz", {"foo": "one", "bar": "two"}) -> "one two baz"
    """
    if not replacements:
        return text
    pattern = re.compile("|".join(re.escape(k) for k in replacements))
    return pattern.sub(lambda m: replacements[m.group(0)], text)
