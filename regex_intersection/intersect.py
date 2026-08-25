"""High-level functions for regex intersection."""

from .regex import Regex, Epsilon, Symbol, Concat, Star, Empty
from .nfa import NFA, thompson
from .dfa import DFA, nfa_to_dfa, product_dfa


def regex_to_dfa(regex: Regex) -> DFA:
    nfa = thompson(regex)
    return nfa_to_dfa(nfa)


def intersect_regexes(regex1: Regex, regex2: Regex) -> DFA:
    dfa1 = regex_to_dfa(regex1)
    dfa2 = regex_to_dfa(regex2)
    return product_dfa(dfa1, dfa2)
