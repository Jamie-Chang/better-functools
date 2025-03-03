"""Override builtin functional helpers with stricter better typed versions."""

from typing import Callable, Iterable, Iterator

__all__ = (
    "filter",
    "map",
    "sum",
    "zip2",
    "zip3",
    "zip4",
    "zip5",
)

orig_filter, orig_sum, orig_map, orig_zip = filter, sum, map, zip


def filter[T](fn: Callable[[T], bool], it: Iterable[T]) -> Iterator[T]:
    return orig_filter(fn, it)


def map[T, R](fn: Callable[[T], R], it: Iterable[T]) -> Iterator[R]:
    return orig_map(fn, it)


def sum(it: Iterable[int]) -> int:
    return orig_sum(it)


def zip[T1, T2](it1: Iterable[T1], it2: Iterable[T2]) -> Iterator[tuple[T1, T2]]:
    return orig_zip(it1, it2)


def zip2[T1, T2](it1: Iterable[T1], it2: Iterable[T2]) -> Iterator[tuple[T1, T2]]:
    return orig_zip(it1, it2)


def zip3[T1, T2, T3](
    it1: Iterable[T1], it2: Iterable[T2], it3: Iterable[T3]
) -> Iterator[tuple[T1, T2, T3]]:
    return orig_zip(it1, it2, it3)


def zip4[T1, T2, T3, T4](
    it1: Iterable[T1], it2: Iterable[T2], it3: Iterable[T3], it4: Iterable[T4]
) -> Iterator[tuple[T1, T2, T3, T4]]:
    return orig_zip(it1, it2, it3, it4)


def zip5[T1, T2, T3, T4, T5](
    it1: Iterable[T1],
    it2: Iterable[T2],
    it3: Iterable[T3],
    it4: Iterable[T4],
    it5: Iterable[T5],
) -> Iterator[tuple[T1, T2, T3, T4, T5]]:
    return orig_zip(it1, it2, it3, it4, it5)
