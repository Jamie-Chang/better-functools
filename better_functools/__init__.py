"""Better functools improves functional programming ergonomics in Python

## Installation
```
$ pip install better-functools
```

## Background

The library introduces 2 different operators for use with functions:
- `|` which we'll call "pipe"
- `@` which we'll call "apply"


The following is an example:
```python
Pipeline(inputs)
| func(itertools.combinations @ func.arg(Iterable[int]) @ bind(2))
| filter @ bind(sum @ compose(eq @ bind(2020)))
| map @ bind(prod)
| sum
| Pipeline.unwrap
```

This may look strange but we can break this down.

### `pipe`
`Pipeline` wraps inputs and enables unix like pipes.
So `Pipeline(v) | fn` is equal to `Pipeline(fn(v))`.

`| Pipeline.unwrap` is finally used to unwrap the `Pipeline` and extract the value.


### `apply`
`better_functools.apply` includes a number of functions that implements `@`.

For example, `map @ bind(prod)` means bind `prod` to the first arg of `map`.
More apply functions can be called directly too, the above expression is equivalent to
`bind(prod)(map)`.

The usual pattern is: `some_value @ some_operator(args)`

The `@` operator takes some getting used to, but the main benefit is how chainable operators are.

```python
add @ bind(1) @ bind(2)
```
reads left to right fairly well, but if we were to call directly:

```python
bind(2)(bind(1)(add))
```
It's just a lot harder to read and we need more brackets.


### Putting `@` and `|` together
You can see that `@` and `|` both facilitate some sort of "function chaining". So why add 2
different operators?

`@` is higher precedence than `|` so it can be used in each stage of a `pipe` without brackets.
Generally the idea is to use `@` operators to build the function for each stage of a `|`.

Without `@` functions are a lot harder to build inline and often must be defined explicitly
elsewhere.

## General Tips

### Type Checking
- The typing here is built for Pyright.
- Mypy compatibility is okay, specific issues with mypy are highlighted in function docs.
- Other type checkers simply lack the popularity for me to support actively.

### `functools.partial`
Feel free to use `functools.partial` to create partial functions in place of `bind` and `func`.
Both MyPy and Pyright has a custom type checking handler for `partial`. This is the best way to 
bind keyword arguments right now.

```python
partial(itertools.combinations, r=2)
```
"""
