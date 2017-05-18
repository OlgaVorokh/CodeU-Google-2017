# -*- coding: UTF-8 -*-

from collections import defaultdict


def check_words(first_word, second_word):
    if len(first_word) != len(second_word):
        return False

    first_word = first_word.decode('utf-8').lower()
    second_word = second_word.decode('utf-8').lower()

    diff_coutner = defaultdict(int)
    for index in xrange(len(first_word)):
        diff_coutner[first_word[index]] += 1
        diff_coutner[second_word[index]] -= 1

    for key in diff_coutner:
        if diff_coutner[key]:
            return False

    return True


def main():
    assert check_words('Listen', 'Silent')
    assert check_words('Triangle', 'Integral')
    assert not check_words('Apple', 'Pabble')
    assert check_words('Оля', 'Яло')
    assert check_words('кАрОлИнА', 'Анилорак')
    assert check_words('', '')

if __name__ == '__main__':
    main()

