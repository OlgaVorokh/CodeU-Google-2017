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
        """
        Parameters:
        -----------
        ver: int
            current vertex, that we want to check; if it contain value that we try to find,
            stop investigating with dfs graph and build the answer; otherwise make new dfs iteration
        prev: int
            previous vertex, from which we can go to current vertex; need for not checking twice one vertex
        value: int
            value, that we want to find in a graph (as I understand from task, all the values in a graph
            should be unique)

        What this function do:
        * check current vertex: if it contain value, go out from recursion and save all previous vertexes
          in self.ancestors attribute during the exit. Previous vertexes - vertexes, from which we can go
          to current. List self.ancestors will be the answer.
        * Otherwise look through all the vertexes, that we can go from current vertex, and named this vertexes to.
          If some edge go to previous vertex (from which we go to current), we skip this vertex (don't need to check
          one vertex twice). Otherwise for all to vertexes start new iteration of dfs method with parameters
          self._dfs(to, ver, value). If descendants of to vertex do not contain value, go to next to and check
          it in the same way
        * If we find vertex with value, we should save all the ancestors of it. So if some descendant of current
          vertex contain value, we should save it to the result

        Time complexity: O(n + m), where n - number of vertexes, m - number of edges in a graph
        """
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

