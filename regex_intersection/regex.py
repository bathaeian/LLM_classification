"""Regular expression AST nodes for languages without union."""

from __future__ import annotations
from dataclasses import dataclass


class Regex:
    """Base class for all regex nodes."""

    pass


@dataclass(frozen=True)
class Epsilon(Regex):
    """Matches the empty string ε."""

    def __str__(self) -> str:
        return "ε"


@dataclass(frozen=True)
class Symbol(Regex):
    """Matches a single character."""

    char: str

    def __str__(self) -> str:
        return self.char


@dataclass(frozen=True)
class Concat(Regex):
    """Concatenation of two regexes."""

    left: Regex
    right: Regex

    def __str__(self) -> str:
        return f"({self.left}{self.right})"


@dataclass(frozen=True)
class Star(Regex):
    """Kleene star of a regex."""

    child: Regex

    def __str__(self) -> str:
        return f"({self.child})*"


@dataclass(frozen=True)
class Empty(Regex):
    """Matches no strings (empty language)."""

    def __str__(self) -> str:
        return "∅"
