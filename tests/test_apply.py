import subprocess
from typing import Any, Callable, assert_type

import pytest

from better_functools.apply import apply, bind, compose, func, invoke, nvl, star_args, static


def mul(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a + b


def mod(a: int, b: int, /) -> int:
    return a % b


def fetch(v: int, return_none: bool) -> int | None:
    if return_none:
        return None
    return v


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        (lambda: assert_type(nvl(fetch(1, True) @ nvl @ apply(add @ bind(1))), int | None), None),
        (lambda: assert_type(nvl(fetch(1, False) @ nvl @ apply(add @ bind(1))), int | None), 2),
        (lambda: assert_type(func(mod @ func.arg(int) @ bind(2)) @ invoke(3), int), 1),
        (lambda: assert_type(mod @ star_args @ invoke((3, 2)), int), 1),
        (lambda: assert_type(add @ compose(mul @ bind(2)) @ invoke(1, 2), int), 6),
        (lambda: assert_type({"id": 1234} @ static(dict[str, int].get)("id"), int | None), 1234),
    ],
)
def test_expressions(expression: Callable[[], Any], expected: Any) -> None:
    assert expression() == expected


def test_type_check() -> None:
    result = subprocess.run(
        ["pyright", __file__],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
