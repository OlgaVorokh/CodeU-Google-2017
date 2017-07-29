import unittest


def solve(input_array, result_array):
    """
    Functions takes as input two array: input and resulting
    Function generates moves to get result_array from input_array,
    returns and print moves.

    We build current_array - copy of input_array and move numbers in it.
    We build reverse_index - array, such that
    if reverse_index[x] = i then current_array[i] == x.
    Using reverse_index we can found any element in array at O(1).

    Than we iterate over current array from the beginning to the end.
    For each iteration if value on current position is equal to the
    item on current position in result_array then we just continue.
    Else if element on current position is not equal to 0, we swap
    item in current position and zero element. After that we have
    zero element in current position and we can just swap element in
    current position and target element for this position.

    Asymptotics of algorithm is O(n) because we make not more than
    2n swaps, each in O(1) time.
    """

    moves = []

    def swap_positions(current_array, reverse_index, ind1, ind2):
        """
        This functions swaps items on positions ind1 and ind2 in O(1).
        Move appends to move list and prints to stdout.
        Function swaps items at positions ind1 and ind2 in current_array
        and reverse_index for items current_array[ind1] and
        current_array[ind2].
        """
        moves.append((ind1, ind2))
        print 'move from {} to {}'.format(ind1, ind2)
        current_array[ind1], current_array[ind2] = current_array[ind2], current_array[ind1]

        reverse_index[current_array[ind1]], reverse_index[current_array[ind2]] = \
            reverse_index[current_array[ind2]], reverse_index[current_array[ind1]]

    current_array = input_array[:]
    input_size = len(input_array)
    reverse_index = [0] * input_size
    for index, element in enumerate(input_array):
        reverse_index[element] = index

    for index in xrange(input_size):
        if current_array[index] == result_array[index]:
            continue
        if current_array[index] != 0:
            swap_positions(current_array, reverse_index,
                           index, reverse_index[0])
        swap_positions(current_array, reverse_index, reverse_index[result_array[index]], index)
    return moves


def data_from_file(filename):
    """
    Get two arrays from .txt file
    First line contains n space separated integers - first array
    Second line contains n space separated integers - second array
    """
    with open(filename, 'r') as f:
        def read_array():
            return [int(item) for item in f.readline().split()]
        input_array = read_array()
        result_array = read_array()
    return input_array, result_array


def make_moves(input_array, moves):
    """
    Function applies moves to input array if possible
    For each move (from, to) in moves list functions tries to swap
    list elements at positions from and to.
    Value of item at positions with index to must be equal to 0.
    Function returns array after applying moves from moves array to it.
    """
    current_array = input_array[:]
    for move in moves:
        assert current_array[move[1]] == 0
        current_array[move[0]], current_array[move[1]] = \
            current_array[move[1]], current_array[move[0]]
    return current_array


class TestSolver(unittest.TestCase):

    def test_sample(self):
        input_array, result_array = data_from_file('inputs/sample_test.txt')
        moves = solve(input_array, result_array)
        out_array = make_moves(input_array, moves)
        self.assertListEqual(result_array, out_array)

    def test_equal(self):
        input_array, result_array = data_from_file('inputs/equal_test.txt')
        moves = solve(input_array, result_array)
        out_array = make_moves(input_array, moves)
        self.assertListEqual(result_array, out_array)

    def test_random(self):
        input_array, result_array = data_from_file('inputs/random_test.txt')
        moves = solve(input_array, result_array)
        out_array = make_moves(input_array, moves)
        self.assertListEqual(result_array, out_array)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
