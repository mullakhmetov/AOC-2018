from collections import deque, defaultdict


PLAYERS = 478
MARBLES = 71240


def play(players, marbles):
    circle = deque([0])
    players_score = defaultdict(int)

    for i, m in enumerate(range(1, marbles + 1), start=1):
        player = i % players

        if not m % 23:
            circle.rotate(7)
            players_score[player] += m + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(m)

    return max(players_score.values())


def main():
    part_1_result = play(PLAYERS, MARBLES)
    print(f'part 1: {part_1_result}')
    part_2_result = play(PLAYERS, MARBLES * 100)
    print(f'part 2: {part_2_result}')


if __name__ == '__main__':
    main()
