"""DFA representation and algorithms: subset construction and product."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, Tuple, Optional, FrozenSet
from collections import deque
from .nfa import NFA


@dataclass
class DFA:
    states: Set[int]
    alphabet: Set[str]
    transitions: Dict[Tuple[int, str], int]
    start: int
    accept: Set[int]

    def __init__(
        self, states=None, alphabet=None, transitions=None, start=None, accept=None
    ):
        self.states = states if states is not None else set()
        self.alphabet = alphabet if alphabet is not None else set()
        self.transitions = transitions if transitions is not None else {}
        self.start = start
        self.accept = accept if accept is not None else set()


def epsilon_closure(nfa: NFA, states: Set[int]) -> Set[int]:
    closure = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for nxt in nfa.transitions.get((s, None), set()):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure


def nfa_to_dfa(nfa: NFA) -> DFA:
    alphabet = nfa.alphabet
    if not alphabet:
        start_closure = epsilon_closure(nfa, {nfa.start})
        states = {0}
        transitions = {}
        accept = {0} if nfa.accept in start_closure else set()
        return DFA(
            states=states,
            alphabet=set(),
            transitions=transitions,
            start=0,
            accept=accept,
        )
    start_set = epsilon_closure(nfa, {nfa.start})
    dfa_states = [start_set]
    dfa_transitions = {}
    dfa_accept = set()
    state_map = {frozenset(start_set): 0}
    queue = deque([0])
    while queue:
        idx = queue.popleft()
        subset = dfa_states[idx]
        if nfa.accept in subset:
            dfa_accept.add(idx)
        for sym in alphabet:
            reach = set()
            for s in subset:
                for nxt in nfa.transitions.get((s, sym), set()):
                    reach.add(nxt)
            closure = epsilon_closure(nfa, reach)
            if not closure:
                continue
            fs = frozenset(closure)
            if fs not in state_map:
                state_map[fs] = len(dfa_states)
                dfa_states.append(closure)
                queue.append(state_map[fs])
            dfa_transitions[(idx, sym)] = state_map[fs]
    return DFA(
        states=set(range(len(dfa_states))),
        alphabet=alphabet,
        transitions=dfa_transitions,
        start=0,
        accept=dfa_accept,
    )


def product_dfa(dfa1: DFA, dfa2: DFA) -> DFA:
    alphabet = dfa1.alphabet | dfa2.alphabet
    start = (dfa1.start, dfa2.start)
    states = [start]
    transitions = {}
    accept = set()
    state_map = {start: 0}
    queue = deque([0])
    while queue:
        idx = queue.popleft()
        q1, q2 = states[idx]
        if q1 in dfa1.accept and q2 in dfa2.accept:
            accept.add(idx)
        for sym in alphabet:
            if (q1, sym) in dfa1.transitions and (q2, sym) in dfa2.transitions:
                nxt1 = dfa1.transitions[(q1, sym)]
                nxt2 = dfa2.transitions[(q2, sym)]
                nxt_state = (nxt1, nxt2)
                if nxt_state not in state_map:
                    state_map[nxt_state] = len(states)
                    states.append(nxt_state)
                    queue.append(state_map[nxt_state])
                transitions[(idx, sym)] = state_map[nxt_state]
    return DFA(
        states=set(range(len(states))),
        alphabet=alphabet,
        transitions=transitions,
        start=0,
        accept=accept,
    )
