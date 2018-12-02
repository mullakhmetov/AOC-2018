from collections import Counter


def main():
    two_times = three_times = 0
    with open('input.txt', 'r') as f:
        ids = [l.strip() for l in f.readlines()]

    for id_ in ids:
        appearings = set(Counter(id_).values())
        if 2 in appearings:
            two_times += 1
        if 3 in appearings:
            three_times += 1
    print(two_times * three_times)


if __name__ == '__main__':
    main()
