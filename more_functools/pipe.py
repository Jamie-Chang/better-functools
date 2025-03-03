from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterator, TypeVar, overload

__all__ = (
    "Composition",
    "Pipeline",
)

T = TypeVar("T")
R = TypeVar("R")
S = TypeVar("S")


@dataclass
class Pipeline(Generic[T]):
    value: T

    class Unwrap: ...

    unwrap = Unwrap()

    @overload
    def __or__(self, val: Callable[[T], R]) -> Pipeline[R]: ...

    @overload
    def __or__(self, val: Unwrap) -> T: ...

    def __or__(self, val: Callable | Unwrap) -> Pipeline | T:
        match val:
            case Pipeline.Unwrap():
                return self.value
            case _:
                return Pipeline(val(self.value))


@dataclass
class Composition(Generic[T, R]):
    fn: Callable[[T], R]
    prev: Composition | None = None

    def __or__(self, fn: Callable[[R], S]) -> Composition[T, S]:
        def _new_fn(v: T) -> S:
            return fn(self(v))

        return Composition(_new_fn, prev=self)

    def __call__(self, arg: T) -> R:
        return self.fn(arg)

    def __iter__(self) -> Iterator[Callable]:
        if self.prev is not None:
            yield from self.prev

        yield self.fn
