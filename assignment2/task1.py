# -*- coding: UTF-8 -*-


class AncestorsFinder(object):
    def __init__(self, graph):
        self.graph = graph
        self.root = 0
        self.ancestors = None

    def find(self, value):
        self.ancestors = []
        self._dfs(self.root, -1, value)
        return self.ancestors

    def _dfs(self, ver, prev, value):
        if self.graph[ver]['value'] == value:
            return True
        for to in self.graph[ver]['edges']:
            if to == prev or not self._dfs(to, ver, value):
                continue
            self.ancestors.append(self.graph[ver]['value'])
            return True
        return False


def get_graph(filename):
    """
    Build graph from input_task1.txt

    First line contain number N of vertex.
    Next N lines (indexing starting from 0) have same format:
    First element is value in vertex with number index
    Other elements in line is number of vertexes that are connected with current vertex
    """
    g = {}
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        for index in xrange(n):
            line_values = map(int, f.readline().strip().split())
            g[index] = {
                'value': line_values[0],
                'edges': line_values[1:],
            }
    return g


def main():
    graph = get_graph('input_task1.txt')

    ancestors_finder = AncestorsFinder(graph=graph)

    assert ancestors_finder.find(5) == [3, 9, 16]
    assert ancestors_finder.find(11) == []
    assert ancestors_finder.find(16) == []
    assert ancestors_finder.find(9) == [16]
    assert ancestors_finder.find(19) == [18, 16]


if __name__ == '__main__':
    main()
