from typing import Callable, TypeVar

T = TypeVar("T")


def singleton(cls: Callable[[], T]) -> T:
    """Decorator to create a single instance of a class without constructor args.

    The resulting object is not strictly speaking a singleton, but
    the class itself is now obscured.

    >>> @singleton
    ... class single:
    ...     def zero(self) -> int:
    ...         return 0
    >>> single.zero()
    0
    """
    return cls()
