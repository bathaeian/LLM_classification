"""Unit tests for regex intersection."""

import unittest
from regex_intersection import (
    Epsilon,
    Symbol,
    Concat,
    Star,
    Empty,
    intersect_regexes,
    dfa_accepts,
    is_language_empty,
)


class TestIntersection(unittest.TestCase):

    def test_simple_intersection(self):
        r1 = Star(Symbol("a"))
        r2 = Star(Symbol("b"))
        dfa = intersect_regexes(r1, r2)
        self.assertTrue(dfa_accepts(dfa, ""))
        self.assertFalse(dfa_accepts(dfa, "a"))
        self.assertFalse(dfa_accepts(dfa, "b"))
        self.assertFalse(dfa_accepts(dfa, "ab"))
        self.assertFalse(is_language_empty(dfa))

    def test_concatenation_intersection(self):
        r1 = Star(Concat(Symbol("a"), Symbol("b")))
        r2 = Concat(Star(Symbol("a")), Star(Symbol("b")))
        dfa = intersect_regexes(r1, r2)
        self.assertTrue(dfa_accepts(dfa, ""))
        self.assertTrue(dfa_accepts(dfa, "ab"))
        self.assertFalse(dfa_accepts(dfa, "abab"))
        self.assertFalse(dfa_accepts(dfa, "a"))
        self.assertFalse(dfa_accepts(dfa, "b"))
        self.assertFalse(dfa_accepts(dfa, "aabb"))
        self.assertFalse(dfa_accepts(dfa, "aba"))
        self.assertFalse(is_language_empty(dfa))

    def test_empty_language_intersection(self):
        r1 = Star(Symbol("a"))
        r2 = Concat(Symbol("b"), Star(Symbol("b")))
        dfa = intersect_regexes(r1, r2)
        self.assertTrue(is_language_empty(dfa))
        self.assertFalse(dfa_accepts(dfa, ""))

    def test_epsilon_intersection(self):
        r1 = Epsilon()
        r2 = Star(Symbol("a"))
        dfa = intersect_regexes(r1, r2)
        self.assertTrue(dfa_accepts(dfa, ""))
        self.assertFalse(dfa_accepts(dfa, "a"))

    def test_star_of_star(self):
        r1 = Star(Star(Symbol("a")))
        r2 = Star(Symbol("a"))
        dfa = intersect_regexes(r1, r2)
        self.assertTrue(dfa_accepts(dfa, ""))
        self.assertTrue(dfa_accepts(dfa, "a"))
        self.assertTrue(dfa_accepts(dfa, "aaa"))
        self.assertFalse(dfa_accepts(dfa, "b"))

    def test_alphabet_union(self):
        r1 = Star(Concat(Symbol("a"), Symbol("b")))
        r2 = Concat(Star(Symbol("a")), Star(Symbol("b")))
        dfa = intersect_regexes(r1, r2)
        self.assertEqual(dfa.alphabet, {"a", "b"})


if __name__ == "__main__":
    unittest.main()
