import sys
from collections import Counter


def get_diff_len(a, b):
    return len([True for (a_letter, b_letter) in zip(a, b) if a_letter != b_letter])

def get_common_letters(a, b):
    return ''.join([a_letter for a_letter, b_letter in zip(a, b) if a_letter == b_letter])


def get_common_letters_if_satisfy(a, b):
    diff_len = get_diff_len(a, b)
    if diff_len == 1:
        return get_common_letters(a, b)

def main():
    two_times = three_times = 0
    with open('input.txt', 'r') as f:
        ids = [l.strip() for l in f.readlines()]

    for id_ in ids:
        for id_2 in ids:
            common = get_common_letters_if_satisfy(id_, id_2)
            if not common:
                continue
            print(common)
            sys.exit()


if __name__ == '__main__':
    main()
