# -*- coding: UTF-8 -*-

import unittest
import Queue


def bfs(greed, start_x, start_y, used):
    """
    Parameters:
    -----------
    greed: 2D int array
        illustrate input map, contain only {0, 1} as values
    start_x: int 
        number of row from starting for checking coordinates
    start_y: int
        number of column from starting for checking coordinates
    used: 2D bool array
        array used for marking if we were in some cell in previous iterations

    Starting from (start_x, start_y) coordinates try to go to horizontally and vertically
    cells. If new cell is water or cell is land and we checked and marked it in previous iterations, don't 
    check this cells. Otherwise marked land-cell, that we be in it, and do the same for it as I write above.
    """
    n_rows = len(greed)
    n_columns = len(greed[0])

    queue = Queue.Queue()
    queue.put((start_x, start_y))
    while not queue.empty():
        x, y = queue.get()
        used[x][y] = True
        for dx, dy in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
            if not (
                    0 <= x + dx < n_rows and
                    0 <= y + dy < n_columns
                ):
                continue
            if not greed[x + dx][y + dy]:
                continue
            if used[x + dx][y + dy]:
                continue
            queue.put((x + dx, y + dy))  


def find_islands(n_rows, n_columns, greed):
    """
    Find all islands.

    Go through all cells, if cell is water or cell is land, but 
    we checked land-cell on previous iterations of bfs function, don't start
    to check this cell. Otherwise we find some island and want to get 
    all land-cells, that are connected with this land-cell. Function
    bfs can make this.
    """
    islands_counter = 0
    used = [[False] * n_columns for _ in xrange(n_rows)]
    for i in xrange(n_rows):
        for j in xrange(n_columns):
            if used[i][j]:
                continue
            if not greed[i][j]:
                continue 
            islands_counter += 1 
            bfs(greed, i, j, used)
    return islands_counter


def data_from_file(filename):
    """
    Get input greed from file.

    First line contains two integers: 
    -- number of rows N
    -- number of columns M

    Next N lines contain M values from set {0, 1}.
    Value 0 means there is water in the cell.
    Value 1 means there is land in the cell.
    """
    greed = []
    with open(filename, 'r') as f:
        n_rows, n_columns = map(int, f.readline().decode('UTF-8').strip().split())
        for _ in xrange(n_rows):
            values = map(int, f.readline().decode('UTF-8').strip().split())
            assert len(values) == n_columns
            greed.append(values)
    return n_rows, n_columns, greed


class TestSolver(unittest.TestCase):
    def test_no_greed(self):
        n_rows, n_columns, greed = data_from_file('inputs/input_no_greed.txt')
        self.assertEqual(find_islands(n_rows, n_columns, greed), 0)

    def test_no_islands(self):
        n_rows, n_columns, greed = data_from_file('inputs/input_no_islands.txt')
        self.assertEqual(find_islands(n_rows, n_columns, greed), 0)

    def test_islands_near_fringe(self):
        n_rows, n_columns, greed = data_from_file('inputs/input_islands_near_fringe.txt')
        self.assertEqual(find_islands(n_rows, n_columns, greed), 3)

    def test_many_islands(self):
        n_rows, n_columns, greed = data_from_file('inputs/input_many_islands.txt')
        self.assertEqual(find_islands(n_rows, n_columns, greed), 4)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
