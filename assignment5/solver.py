# -*- coding: UTF-8 -*-
"""
Using the topological sort, build resulting alphabet.
"""


import unittest

from collections import defaultdict


class AlphabetBuilder(object):
    def __init__(self):
        self.graph = None
        self.used = None
        self.alphabet = None

    def get_alphabet(self, words):
        self._build_graph(words)
        self._find_alphabet()
        return self.alphabet

    def _build_graph(self, words):
        """
        This function build oriented graph of letter relations in alphabet.

        Look through two neighboring words in `words` list and find
        two letters A and B, that are not equal and make some relation. Save this
        order (A -> B) in graph and start to check the next one pair of words.
        """
        self.graph = {}
        for word in words:
            for letter in word:
                self.graph[letter] = []

        for i in xrange(len(words) - 1):
            word_first = words[i]
            word_second = words[i + 1]
            min_word_len = min(len(word_first), len(word_second))
            for j in xrange(min_word_len):
                if word_first[j] != word_second[j]:
                    self.graph[word_first[j]].append(word_second[j])
                    break

    def _find_alphabet(self):
        """
        This function build alphabet with using topological sort.
        """
        self.used = defaultdict(bool)
        self.alphabet = []
        for ver in self.graph.keys():
            if not self.used[ver]:
                self._dfs(ver)
        self.alphabet.reverse()

    def _dfs(self, ver):
        """
        Parameters:
        -----------
        ver: str
            Some letter.
        """
        self.used[ver] = True
        for to in self.graph[ver]:
            if not self.used[to]:
                self._dfs(to)
        self.alphabet.append(ver)


def data_from_file(filename):
    """
    Get input words from file.
    Each line in the file contain one word.
    All words are ordered by some alphabet that we should recognize.
    """
    with open(filename, 'r') as f:
        words = [line.decode('UTF-8').strip().lower() for line in f]
    return words


class TestSolver(unittest.TestCase):
    def test_google_test(self):
        words = data_from_file('input/google_test.txt')
        self.assertListEqual(AlphabetBuilder().get_alphabet(words), [u't', u'a', u'r', u'c'])

    def test_no_words(self):
        words = data_from_file('input/no_words.txt')
        self.assertListEqual(AlphabetBuilder().get_alphabet(words), [])

    def test_only_one_letter(self):
        words = data_from_file('input/only_one_letter.txt')
        self.assertListEqual(AlphabetBuilder().get_alphabet(words), [u'a'])

    def test_different_case(self):
        words = data_from_file('input/different_case.txt')
        self.assertListEqual(AlphabetBuilder().get_alphabet(words), [u's', u'l', u'b', u'a', u'c', u't'])

    def test_similar_words(self):
        words = data_from_file('input/similar_words.txt')
        self.assertListEqual(AlphabetBuilder().get_alphabet(words), [u'c', u'a', u's', u'e'])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
