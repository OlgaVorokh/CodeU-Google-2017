# -*- coding: UTF-8 -*-

class ListNode(object):
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node


class LinkedList(object):
    def __init__(self):
        self.root = None

    def build_from_lst(self, lst):
        for index in xrange(len(lst) - 1, -1, -1):
            self.add_on_top(lst[index])

    def add_on_top(self, value):
        new_root = ListNode(value, self.root)
        self.root = new_root

    def __len__(self):
        start = self.root
        length = 0
        while start:
            length += 1
            start = start.next_node
        return length

    def get_kth_from_end(self, k):
        lst_len = len(self)
        result_index = lst_len - k - 1
        if not (0 <= result_index < lst_len):
            return None

        index = 0
        start = self.root
        while start:
            if index == result_index:
                break
            index += 1
            start = start.next_node
        return start.value


def main():
    linked_lst = LinkedList()
    array = [0, 1, 2, 11, 123]
    linked_lst.build_from_lst(array)

    assert linked_lst.get_kth_from_end(0) == array[-1]
    assert linked_lst.get_kth_from_end(1) == array[-2]
    assert linked_lst.get_kth_from_end(2) == array[-3]
    assert linked_lst.get_kth_from_end(3) == array[-4]
    assert linked_lst.get_kth_from_end(len(array) - 1) == array[0]
    assert linked_lst.get_kth_from_end(55) is None
    assert linked_lst.get_kth_from_end(-123) is None


if __name__ == '__main__':
    main()

