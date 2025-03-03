from __future__ import annotations

from dataclasses import dataclass

from better_functools.pipe import Composition, Pipeline


@dataclass
class User:
    name: str
    age: int


def multiply_by_two(x: int) -> int:
    return x * 2


def add_three(x: int) -> int:
    return x + 3


def uppercase_string(s: str) -> str:
    return s.upper()


def append_world(s: str) -> str:
    return s + " WORLD"


def int_to_string(x: int) -> str:
    return str(x)


def append_is_a_number(s: str) -> str:
    return s + " is a number"


def add_one(x: int) -> int:
    return x + 1


def double(x: int) -> int:
    return x * 2


def add_two(x: int) -> int:
    return x + 2


def five_times(x: int) -> int:
    return x * 5


def subtract_five(x: int) -> int:
    return x - 5


def subtract_three(x: int) -> int:
    return x - 3


def get_user_age(user: User) -> int:
    return user.age


def add_five_to_age(age: int) -> int:
    return age + 5


def test_pipeline_basic():
    result = Pipeline(5) | multiply_by_two | add_three | Pipeline.unwrap
    assert result == 13


def test_pipeline_with_strings():
    result = Pipeline("hello") | uppercase_string | append_world | Pipeline.unwrap
    assert result == "HELLO WORLD"


def test_pipeline_with_different_types():
    result = Pipeline(5) | int_to_string | append_is_a_number | Pipeline.unwrap
    assert result == "5 is a number"


def test_pipeline_dataclass():
    result = Pipeline(User("Alice", 30)) | get_user_age | add_five_to_age | Pipeline.unwrap
    assert result == 35


def test_composition_basic():
    fn = Composition(multiply_by_two) | add_three
    assert fn(5) == 13


def test_composition_call_directly():
    fn = Composition(multiply_by_two)
    assert fn(5) == 10

    fn2 = fn | add_three
    assert fn2(5) == 13


def test_composition_with_strings():
    fn = Composition(uppercase_string) | append_world
    assert fn("hello") == "HELLO WORLD"


def test_composition_with_different_types():
    fn = Composition(int_to_string) | append_is_a_number
    assert fn(5) == "5 is a number"


def test_composition_dataclass():
    fn = Composition(get_user_age) | add_five_to_age
    assert fn(User("Alice", 30)) == 35


def test_composition_and_pipeline_together():
    fn = Composition(get_user_age) | add_one
    result = Pipeline(User(name="Test", age=29)) | fn | Pipeline.unwrap
    assert result == 30


def test_composition_and_pipeline_together2():
    result2 = Pipeline(User("Bob", 25)) | get_user_age | double | Pipeline.unwrap
    assert result2 == 50


def test_composition_full_flow():
    fn2 = Composition(add_two) | five_times
    pipeline_result = Pipeline(10) | fn2 | subtract_five | Pipeline.unwrap
    assert pipeline_result == 55


def test_composition_and_pipeline_combined():
    fn = Composition(get_user_age) | add_one
    fn2 = Composition(add_two) | five_times

    full_pipe = Pipeline(User("Charlie", 33)) | fn | fn2 | subtract_three | Pipeline.unwrap
    assert full_pipe == 177
