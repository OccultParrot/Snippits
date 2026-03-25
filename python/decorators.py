"""
Decorator snippets for common use-cases.
"""

import time
import functools
import logging
from typing import Callable, Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def timer(func: F) -> F:
    """Log the execution time of a function.

    Usage:
        @timer
        def slow_function():
            time.sleep(1)
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug("%s took %.4f seconds", func.__name__, elapsed)
        return result
    return wrapper  # type: ignore[return-value]


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple[type[Exception], ...] = (Exception,)) -> Callable[[F], F]:
    """Retry a function up to max_attempts times on specified exceptions.

    Usage:
        @retry(max_attempts=5, delay=2.0, exceptions=(IOError,))
        def flaky_request():
            ...
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    logger.warning(
                        "%s failed (attempt %d/%d): %s",
                        func.__name__, attempt, max_attempts, exc,
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise RuntimeError(f"{func.__name__} failed after {max_attempts} attempts") from last_exc
        return wrapper  # type: ignore[return-value]
    return decorator


def singleton(cls: type) -> type:
    """Ensure only one instance of a class is created.

    Usage:
        @singleton
        class Config:
            pass
    """
    instances: dict[type, Any] = {}

    @functools.wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance  # type: ignore[return-value]


def memoize(func: F) -> F:
    """Cache the return value of a function based on its arguments.

    Usage:
        @memoize
        def fib(n):
            return n if n < 2 else fib(n - 1) + fib(n - 2)
    """
    cache: dict[Any, Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper  # type: ignore[return-value]


def deprecated(message: str = "") -> Callable[[F], F]:
    """Mark a function as deprecated; emits a warning when it is called.

    Usage:
        @deprecated("Use new_function() instead.")
        def old_function():
            pass
    """
    import warnings

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warn_msg = f"{func.__name__} is deprecated."
            if message:
                warn_msg += f" {message}"
            warnings.warn(warn_msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper  # type: ignore[return-value]
    return decorator
