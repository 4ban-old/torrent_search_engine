# coding: utf-8
"""
    Unittests for relevance.
    Call relevance.relevance(blocks) where blocks is dictionary
    which consist of key 'name' and value as tuple('words', coefficient, call_position)
    For instance:
        blocks = {'name1': ('word1 word2 word3', 0.4, True),
                'name2': ('word1 word2 word3 word4', 0.3, False)}
"""
import unittest

import relevance


class FlagFalse(unittest.TestCase):
    def test_simple_text_without_coefficient(self):
        blocks = {'keywords': ('a b c a', 0, False),
                'description': ('c a d e', 0, False),
                'text': ('a a a a', 0, False)}
        result = {'a': 0.4375, 'c': 0.21875, 'b': 0.09375, 'e': 0.125, 'd': 0.125}
        self.assertEqual(relevance.relevance(blocks), result)


class FlagTrue(unittest.TestCase):
    def test_simple_text_without_coefficient(self):
        blocks = {'keywords': ('a b c a', 0, True),
                'description': ('a c d e', 0, True),
                'text': ('a a a a', 0, True)}
        result = {'a': 0.5125, 'c': 0.225, 'b': 0.11249999999999999, 'd': 0.1, 'e': 0.05}
        self.assertEqual(relevance.relevance(blocks), result)

    def test_simple_text_with_coefficient(self):
        blocks = {'keywords': ('a b c a', 0.3, True),
                'description': ('a c d e', 0.6, True),
                'text': ('a a a a', 0.1, True)}
        result = {'a': 0.49, 'c': 0.24, 'b': 0.09, 'd': 0.12, 'e': 0.06}
        self.assertEqual(relevance.relevance(blocks), result)
    def test_simple_text_coefficient_not_given(self):
        blocks = {'keywords': ('a b c a', True),
                'description': ('a c d e', True),
                'text': ('a a a a', True)}
        result = {'a': 0.5125, 'c': 0.225, 'b': 0.11249999999999999, 'd': 0.1, 'e': 0.05}
        self.assertEqual(relevance.relevance(blocks), result)

    def test_simple_text_shit(self):
        blocks = {'keywords': ('a', 0.3, True),
                'description': ('e', 0.6, True),
                'text': ('', 0.1, True)}
        result = {'a': 0.3, 'e': 0.6, '': 0.1}
        self.assertEqual(relevance.relevance(blocks), result)

if __name__ == '__main__':
    unittest.main()
