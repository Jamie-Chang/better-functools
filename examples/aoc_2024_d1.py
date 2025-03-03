import itertools
from math import prod
from typing import Iterable

from more_functools.apply import bind, compose, func
from more_functools.pipe import Pipeline
from more_functools.strict.builtins import filter, map, sum
from more_functools.strict.operator import eq


def part1(inputs: Iterable[int]) -> int:
    return (
        Pipeline(inputs)
        | func(itertools.combinations @ func.arg(Iterable[int]) @ bind(2))
        | filter @ bind(sum @ compose(eq @ bind(2020)))
        | map @ bind(prod)
        | sum
        | Pipeline.unwrap
    )


def part2(inputs: Iterable[int]) -> int:
    return (
        Pipeline(inputs)
        | func(itertools.combinations @ func.arg(Iterable[int]) @ bind(3))
        | filter @ bind(sum @ compose(eq @ bind(2020)))
        | map @ bind(prod)
        | sum
        | Pipeline.unwrap
    )
