# -*- coding: UTF-8 -*-

import math


class LCABuilder(object):
    """
    On this task we should find least common ancestor (lca) of two vertexes. I made this with binary lift method.

    Precalculate for each vertexes their first ancestor, second ancestor, foth and so on. Keep this information
    in 2D array self.parent, so, for example, self.parent[ver][index] means 2^index ancestor of vertex ver
    (ver=0.. n - 1, index = 0, ... log n; ancestor of root is root). Also save time in and time out for each vertex.
    This information calculated with dfs. I do this because it gives me to understand with O(1), if one vertex is
    an ancestor of another (if it's true, time in of ancestor should be earlier and time out later). I implement
    this check in self._check(first_ver, second_ver) method.

    This preprocessing are made in build method with O(n log n), where n is a number of vertexes in a graph.

    Than we get some request to find lca of two vertexes A and B.

    Time complexity:
    * prepocessing: O(n log n)
    * get answer for (A, B) request: O(log n)
    """
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
        """
        Parameters:
        -----------
        ver: int
            current vertex, which is investigate on this iteration
        pnt: int
            previous vertex, from which we can go to current vertex (closest ancestor of current vertex)

        Save time of arrival in vertex. Need for checking if one vertex in an ancestor of another with O(1)
        time complexity (this checking is implementing in _check method). Save closest ancestor of current
        vertex ver.

        We precalculate on previous iterations of dfs answer for all ancestors of current vertex, and now
        get this ancestors and update information in self.parent array for ver. Go to all of descendants of current
        vertex and make the same operations.

        Save leaving time from vertex. Need for checking if one vertex in an ancestor of another with O(1)
        time complexity (this checking is implementing in _check method

        """
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
        """
        Check if one vertex is an ancestor of another with self._check method.

        If this is not true, starting from power log_2(n) (keep this in self.two_pow attribute) try to find
        highest (closest to root) vertex for A, that not the ancestor of B (that vertex C, for which C is
        not the ancestor or B, but self.parent[C][0] - ancestor of B ). We can find this vertex with O(log n)
        time complexity.

        So what we do: start from step = self.two_pow (or step = log_2(n) as we understand above). If
        self.parent[A][step] is not the ancestor of B (all the vertexes on the way of ancestor(A, B) to root
        also get True from self._check method and marked as ancestors, but not least; ancestor of root is root),
        make A = self.parent[A][step] and make step -=1. If self.parent[A][step] is an ancestor, just make
        decrease of step.

        Obviously, when step becomes less than zero, the vertex of A will be the desired vertex (A is not an
        ancestor of B, but self.parent[A][0] is an ancestor of B) and self.parent[A][0]will be the answer.
        """
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

