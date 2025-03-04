from __future__ import annotations

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Concatenate,
    Generic,
    ParamSpec,
    TypeVar,
    cast,
    overload,
)

from typing_extensions import Self, TypeVarTuple, Unpack

from .helpers import singleton

__all__ = (
    "apply",
    "bind",
    "compose",
    "star_args",
    "invoke",
    "func",
    "nvl",
    "static",
)


T_APPLY = TypeVar("T_APPLY", bound=Callable[[Any], Any])
T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")
Ts = TypeVarTuple("Ts")


class apply(Generic[T_APPLY]):
    """Make a function callable by using `@` operator.

    This is the `@` version of `... | fn` in `better_functools.pipe.Composition`.

    >>> "1234" @ apply(int)
    1234
    """

    def __init__(self, fn: T_APPLY) -> None:
        self.fn = fn

    if TYPE_CHECKING:
        __call__: T_APPLY
        __rmatmul__: T_APPLY
    else:

        def __call__(self, *args, **kwargs):
            return self.fn(*args, **kwargs)

        __rmatmul__ = __call__


@dataclass
class bind(Generic[T]):
    """Bind the first argument to the function.

    >>> def add(x: int, y: int) -> int:
    ...     return x + y
    >>> (add @ bind(2))(5)
    7
    """

    val: T

    def __call__(self, fn: Callable[Concatenate[T, P], R]) -> Callable[P, R]:
        def _new_fn(*args: P.args, **kwargs: P.kwargs) -> R:
            return fn(self.val, *args, **kwargs)

        return _new_fn

    def __rmatmul__(self, fn: Callable[Concatenate[T, P], R]) -> Callable[P, R]:
        return self(fn)


@dataclass
class compose(Generic[T, R]):
    """Compose functions.

    This is similar to `better_functools.pipe.Composition`,
    but allows it to be done with `@`.

    >>> def add(x: int, y: int) -> int:
    ...     return x + y
    >>> add_plus_one = add @ compose(add @ bind(1))
    >>> add_plus_one(2, 3)
    6
    """

    fn: Callable[[T], R]

    def __call__(self, other: Callable[P, T]) -> Callable[P, R]:
        def _call(*args: P.args, **kwargs: P.kwargs) -> R:
            return self.fn(other(*args, **kwargs))

        return _call

    __rmatmul__ = __call__


@singleton
class _star_args:
    def __call__(self, fn: Callable[[Unpack[Ts]], R]) -> Callable[[tuple[Unpack[Ts]]], R]:
        def _fn(args: tuple[Unpack[Ts]]) -> R:
            return fn(*args)

        return _fn

    __rmatmul__ = __call__


star_args = _star_args
"""Convert a function with positional args to one that takes a single tuple.

This is useful when used with `better_functools.pipe.Pipeline`.

>>> def add(x: int, y: int) -> int:
...     return x + y
>>> (add @ star_args)((1, 2))
"""


class invoke(Generic[Unpack[Ts]]):
    """Invoke a function with the given positional args.

    This is useful when dealing with a `@` chain.

    >>> def add(x: int, y: int, z: int) -> int:
    ...     return x + y + z
    >>> (add @ bind(1) @ bind(2))(3)  # hard to read
    6
    >>> add @ bind(1) @ bind(2) @ invoke(3)
    6
    """

    def __init__(self, *args: Unpack[Ts]) -> None:
        self.args = args

    def __call__(self, fn: Callable[[Unpack[Ts]], R]) -> R:
        return fn(*self.args)

    __rmatmul__ = __call__


class _func:
    @dataclass
    class arg(Generic[T]):
        type_: type[T]

        def __call__(self, fn: Callable[Concatenate[T, P], R]) -> Callable[P, Callable[[T], R]]:
            def _inner(*args: P.args, **kwargs: P.kwargs) -> Callable[[T], R]:
                def _fn(first: T) -> R:
                    return fn(first, *args, **kwargs)

                return _fn

            return _inner

        __rmatmul__ = __call__

    def __call__(self, fn: Callable[[], Callable[[T], R]]) -> Callable[[T], R]:
        return fn()


func = _func()
"""Useful for creating a partial function of an argument
which is not the last and not named.

Suppose we have a `fn: (a, b, c) -> d`
arg(fn): (b, c) -> ((a) -> d)

>>> def mod(a: int, b: int, /) -> int:
...     return a % b
>>> is_odd = func(mod @ func.arg(int) @ bind(2)) @ compose(bool)
>>> is_odd @ invoke(5)
True
>>> is_odd(4)
False
"""


class _nvl:
    def __call__(self, v: Self | T) -> T | None:
        if isinstance(v, type(self)):
            return None

        return cast("T", v)

    def __matmul__(self, _: Any) -> Self:
        return self

    @overload
    def __rmatmul__(self, left: None) -> Self: ...

    @overload
    def __rmatmul__(self, left: T) -> T: ...

    def __rmatmul__(self, left: T | None) -> T | Self:
        if left is None:
            return self

        return left


nvl = _nvl()
"""None-Coalescing function.

`nvl` is used in 2 ways.

When used with `@` it checks the result of the left-hand side expression
and ignores further `@` operations if `None`.

When called it cleans up the result of an `@ nvl` chain.

The operation should be used as

nvl(expr1 @ nvl @ expr2 @ nvl @ ...)

>>> def squared(n: int) -> int:
...     return n * n
>>> def squared_or_none(v: int | None):
...     return nvl(v @ nvl @ squared)
>>> squared_or_none(5)
25
>>> squared_or_none(None)
None
"""


def static(fn: Callable[Concatenate[T, P], R]) -> Callable[P, apply[Callable[[T], R]]]:
    """*Experimental*: Make a bound method static.

    This makes it easier to chain the method.

    suppose you have a bound method on an object of type `MyType`
    ```
    obj.method: (*args, **kwargs) -> ReturnType
    ```
    Applying static:
    ```
    static(MyType.method): (*args, **kwargs) -> ((MyType) -> ReturnType)
    ```

    Example:
    >>> get_id = static(dict[str, int].__getitem__)("id")
    >>> get_id({"id": 1234})
    1234

    Limitations:
    - Generics on the parent class maybe lost explicitly specify the generic type in such cases.
    - Does not work well with MyPy.
    """

    def _outer(*args: P.args, **kwargs: P.kwargs) -> apply[Callable[[T], R]]:
        @apply
        def _inner(first: T) -> R:
            return fn(first, *args, **kwargs)

        return _inner

    return _outer
