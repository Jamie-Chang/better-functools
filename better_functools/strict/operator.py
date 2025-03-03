from typing import Any


def eq[T](a: T, b: T, /) -> bool:
    return a == b


def ne[T](a: T, b: T, /) -> bool:
    return a != b


def not_(v: Any, /) -> bool:
    return not v


def gt[T](a: T, b: T, /) -> bool:
    return a > b


def ge[T](a: T, b: T, /) -> bool:
    return a >= b


def lt[T](a: T, b: T, /) -> bool:
    return a < b


def le[T](a: T, b: T, /) -> bool:
    return a <= b
