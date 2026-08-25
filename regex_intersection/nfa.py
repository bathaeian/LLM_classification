"""NFA representation and Thompson construction."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple, Optional
from .regex import Regex, Epsilon, Symbol, Concat, Star, Empty


@dataclass
class NFA:
    states: Set[int]
    alphabet: Set[str]
    transitions: Dict[Tuple[int, Optional[str]], Set[int]]
    start: int
    accept: int

    def __init__(
        self, states=None, alphabet=None, transitions=None, start=None, accept=None
    ):
        self.states = states if states is not None else set()
        self.alphabet = alphabet if alphabet is not None else set()
        self.transitions = transitions if transitions is not None else {}
        self.start = start
        self.accept = accept


# Global counter for fresh state ids
_state_counter = 0


def _fresh_state() -> int:
    global _state_counter
    s = _state_counter
    _state_counter += 1
    return s


def _add_transition(trans: Dict, src: int, sym: Optional[str], dst: int) -> None:
    trans.setdefault((src, sym), set()).add(dst)


def thompson(regex: Regex) -> NFA:
    """Convert a regex to an NFA using Thompson's construction."""
    global _state_counter
    _state_counter = 0
    return _thompson_rec(regex)


def _thompson_rec(regex: Regex) -> NFA:
    if isinstance(regex, Empty):
        s = _fresh_state()
        a = _fresh_state()
        return NFA(states={s, a}, alphabet=set(), transitions={}, start=s, accept=a)
    elif isinstance(regex, Epsilon):
        s = _fresh_state()
        a = _fresh_state()
        trans = {}
        _add_transition(trans, s, None, a)
        return NFA(states={s, a}, alphabet=set(), transitions=trans, start=s, accept=a)
    elif isinstance(regex, Symbol):
        s = _fresh_state()
        a = _fresh_state()
        trans = {}
        _add_transition(trans, s, regex.char, a)
        return NFA(
            states={s, a}, alphabet={regex.char}, transitions=trans, start=s, accept=a
        )
    elif isinstance(regex, Concat):
        nfa1 = _thompson_rec(regex.left)
        nfa2 = _thompson_rec(regex.right)
        states = nfa1.states | nfa2.states
        alphabet = nfa1.alphabet | nfa2.alphabet
        trans = {}
        for (st, sym), dsts in nfa1.transitions.items():
            trans[(st, sym)] = set(dsts)
        for (st, sym), dsts in nfa2.transitions.items():
            if (st, sym) in trans:
                trans[(st, sym)].update(dsts)
            else:
                trans[(st, sym)] = set(dsts)
        _add_transition(trans, nfa1.accept, None, nfa2.start)
        return NFA(
            states=states,
            alphabet=alphabet,
            transitions=trans,
            start=nfa1.start,
            accept=nfa2.accept,
        )
    elif isinstance(regex, Star):
        sub = _thompson_rec(regex.child)
        s = _fresh_state()
        a = _fresh_state()
        states = sub.states | {s, a}
        alphabet = sub.alphabet
        trans = dict(sub.transitions)
        _add_transition(trans, s, None, sub.start)
        _add_transition(trans, sub.accept, None, sub.start)
        _add_transition(trans, sub.accept, None, a)
        _add_transition(trans, s, None, a)
        return NFA(
            states=states, alphabet=alphabet, transitions=trans, start=s, accept=a
        )
    else:
        raise TypeError(f"Unknown regex node: {type(regex)}")
