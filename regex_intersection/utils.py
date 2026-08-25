"""Utility functions for testing and working with DFAs."""

from .dfa import DFA


def dfa_accepts(dfa: DFA, string: str) -> bool:
    state = dfa.start
    for ch in string:
        if (state, ch) not in dfa.transitions:
            return False
        state = dfa.transitions[(state, ch)]
    return state in dfa.accept


def is_language_empty(dfa: DFA) -> bool:
    if dfa.start in dfa.accept:
        return False
    visited = {dfa.start}
    stack = [dfa.start]
    while stack:
        s = stack.pop()
        for sym in dfa.alphabet:
            nxt = dfa.transitions.get((s, sym))
            if nxt is not None and nxt not in visited:
                if nxt in dfa.accept:
                    return False
                visited.add(nxt)
                stack.append(nxt)
    return True
