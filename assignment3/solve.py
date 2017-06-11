# -*- coding: UTF-8 -*-

import unittest


class BorNode(object):
    def __init__(self):
        self.edges = {}
        self.word_end = False


class Bor(object):
    """
    For solving this problem I used Bor data structure.

    Bor data structure means a tree, every edge of this tree
    is named by some letter, all the edges from one vertex have
    different names.

    The more detail description of building Bor you can find in
    class methods below.

    Time complexity:
    * building: O(n * max_len_word), where
        - n is the number of words in dictionary
        - max_len_word is the maximal length of word in the dictionary
    * check ifPrefix(string): O(len_string), len_string = len(string)
    * check ifWord(string): O(len_word), len_word = len(word)
    """
    def __init__(self):
        self.root = BorNode()

    def build(self, words_list):
        for word in words_list:
            self.add_word(word)

    def add_word(self, word):
        """
        Add word to Bor data structure.

        Starting from root, checking if we can go from current node
        to new one by some letter from word.
        If we can do that, just go to new one and start checking next
        letter from word.
        If not, create new Bor Node and add new edge to the current node.
        Than make the same step as described above.

        When we checked last letter from word, set attribute word_end in
        last checked Node on True.
        """
        node = self.root
        for letter in word:
            if letter not in node.edges:
                node.edges[letter] = BorNode()
            node = node.edges[letter]
        node.word_end = True

    def _get_node(self, word):
        """
        Checked if word in Bor data structure.

        Return last node in Bor, if word found in structure,
        else return None.

        Starting from root, go over the every letter in word and
        try to go over Bor structure. If we can go over all letters
        in word, return Bor Node, else return None.
        """
        node = self.root
        for letter in word:
            if letter not in node.edges:
                return None
            node = node.edges[letter]
        return node

    def is_prefix(self, string):
        """Checked if we can go over all the words letters in Bor"""
        return self._get_node(string) is not None

    def is_word(self, string):
        """
        The same as is_prefix plus checked if some word from dictionary
        ends in last node, that returns from self._get_node method.
        """
        node = self._get_node(string)
        return node is not None and node.word_end


class GridWordsFinder(object):
    def __init__(self, grid):
        self.grid = grid
        self.used = None
        self.bor = None
        self.grid_words = set()

    def find(self, bor):
        """
        Go over every cell in grid, set current cell as start point for
        finding words in dictionary and run finding with method self._find_words
        (described below).

        Return sorted list of dictionary words that can be founded in input grid.
        """
        if not len(self.grid):
            return []

        self.bor = bor
        n, m = len(self.grid), len(self.grid[0])
        for i in xrange(len(self.grid)):
            for j in xrange(len(self.grid[0])):
                self.used = [[False] * m for _ in xrange(n)]
                self._find_words(i, j, '')
        return sorted(list(self.grid_words))

    def _find_words(self, i, j, string):
        """
        Method get current position (i, j) in grid and string that is built by
        going over the grid in previous iterations of this method.

        First check,if string can be a word from dictionary with help of Bor
        structure (described above). If it's true, add this string to result
        self.grid_words set (set, because we don't want to save duplicates).

        Than try to go to the adjacent cells and check, if string + letter from
        adjacent cell can be a prefix of some word from dictionary. If it's true,
        go to that cell and continue previous step from it.

        For avoiding go twice in one cell, mark in self.used 2D array (have the
        same shape as input grid) value for this (x, y) cell as True, if we be
        in it in previous steps. When stop checking current cell, marked this value
        in False.
        """
        self.used[i][j] = True
        if self.bor.is_word(string):
            self.grid_words.add(string)

        for dx in xrange(-1, 2):
            for dy in xrange(-1, 2):
                if not (
                    0 <= i + dx < len(self.used) and
                    0 <= j + dy < len(self.used[0])
                ):
                    continue
                if self.used[i + dx][j + dy]:
                    continue
                if not self.bor.is_prefix(string):
                    continue
                self._find_words(i + dx, j + dy, string + self.grid[i + dx][j + dy])
        self.used[i][j] = False


def data_from_file(filename):
    """
    Get words list and grid from .txt file.

    First line contain number N of words in dictionary.
    Next N lines contains dictionary words.

    Then next N and M means size of grid.
    Next N lines represent grid row and contain M letters (M columns in the grid).
    """
    with open(filename, 'r') as f:
        words_list = []
        word_count = int(f.readline().decode('utf-8').strip())
        for _ in xrange(word_count):
            words_list.append(f.readline().decode('utf-8').strip())
        n, m = map(int, f.readline().decode('utf-8').strip().split())
        grid = []
        for i in xrange(n):
            grid.append(f.readline().decode('utf-8').strip().split())
    return words_list, grid


class TestSolver(unittest.TestCase):
    def test_bad_grid(self):
        grid = []
        solver = GridWordsFinder(grid)
        self.assertListEqual(solver.find(None), [])

    def test_bad_words_list(self):
        words_list, grid = [], [[u'A'], [u'B']]
        bor = Bor()
        bor.build(words_list=words_list)
        solver = GridWordsFinder(grid=grid)
        self.assertListEqual(solver.find(bor=bor), [])

    def test_task_example(self):
        words_list, grid = data_from_file('input_task_example.txt')
        bor = Bor()
        bor.build(words_list=words_list)
        solver = GridWordsFinder(grid=grid)
        self.assertListEqual(solver.find(bor=bor), [u'CAR', u'CARD', u'CAT'])

    def test_another_language(self):
        words_list, grid = data_from_file('input_another_language.txt')
        bor = Bor()
        bor.build(words_list=words_list)
        solver = GridWordsFinder(grid=grid)
        self.assertListEqual(solver.find(bor=bor), [u'МАМА', u'ОЛЯ', u'ПЕТЯ', u'ЮЛА'])

    def test_different_languages(self):
        words_list, grid = data_from_file('input_different_languages.txt')
        bor = Bor()
        bor.build(words_list=words_list)
        solver = GridWordsFinder(grid=grid)
        self.assertListEqual(solver.find(bor=bor), [u'DADDY', u'ЮЛА'])


def main():
    unittest.main()


if __name__ == '__main__':
    main()

