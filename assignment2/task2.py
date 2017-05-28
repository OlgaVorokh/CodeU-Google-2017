# -*- coding: UTF-8 -*-

import math


class LCABuilder(object):
    def __init__(self, graph):
        self.graph = graph
        self.root = 0
        self.two_pow = int(math.ceil(math.log(len(graph), 2)))

        self.time_in = [0] * len(graph)
        self.time_out = [0] * len(graph)
        self.parent = [[0] * (self.two_pow + 1) for _ in xrange(len(graph))]
        self.timer = 1

    def build(self):
        self._dfs(self.root)

    def _dfs(self, ver, pnt=0):
        self.time_in[ver] = self.timer
        self.timer += 1

        self.parent[ver][0] = pnt
        for index in xrange(1, self.two_pow + 1):
            prev = self.parent[ver][index - 1]
            self.parent[ver][index] = self.parent[prev][index - 1]
        for index in xrange(len(self.graph[ver])):
            to = self.graph[ver][index]
            if to == pnt:
                continue
            self._dfs(to, ver)

        self.time_out[ver] = self.timer
        self.timer += 1

    def find(self, first_ver, second_ver):
        if self._check(first_ver, second_ver):
            return first_ver
        if self._check(second_ver, first_ver):
            return second_ver
        for step in xrange(self.two_pow, -1, -1):
            if not self._check(self.parent[first_ver][step], second_ver):
                first_ver = self.parent[first_ver][step]
        return self.parent[first_ver][0]

    def _check(self, first_ver, second_ver):
        return (
            self.time_in[first_ver] <= self.time_in[second_ver] and
            self.time_out[first_ver] >= self.time_out[second_ver]
        )


def get_graph(filename):
    """
    Build graph from input_task2.txt

    First line contain number N of vertex.
    Next N lines (indexing starting from 0) have same format:
    Each line contain number of vertexes that are connected with current vertex
    """
    g = {}
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        for index in xrange(n):
            g[index] = map(int, f.readline().strip().split())
    return g


def main():
    g = get_graph('input_task2.txt')

    lca_builder = LCABuilder(g)
    lca_builder.build()

    assert lca_builder.find(4, 7) == 1
    assert lca_builder.find(6, 7) == 3
    assert lca_builder.find(6, 5) == 0
    assert lca_builder.find(4, 2) == 0 and lca_builder.find(2, 4) == 0
    assert lca_builder.find(3, 7) == 3 and lca_builder.find(7, 3) == 3


if __name__ == '__main__':
    main()
