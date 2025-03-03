"""
Stricter copies of builtins and standard library functions.

Typing for some functions in Python are too permissive or overloaded.
Causing problems for the type checker. Here we bundle strict versions
of some of them so that they can be used instead whilst maintaining type safety.
"""

from . import builtins, operator

__all__ = ("builtins", "operator")
