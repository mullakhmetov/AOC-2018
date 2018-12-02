import sys
from itertools import cycle


def main():
    with open('input.txt', 'r') as f:
        changes = [l.strip() for l in f.readlines() if l.strip()]

    freqs = set([0])
    freq = 0
    for change in cycle(changes):
        freq = eval('{} {}'.format(freq, change))
        if freq in freqs:
            print(freq)
            sys.exit()

        freqs.add(freq)


if __name__ == '__main__':
    main()
