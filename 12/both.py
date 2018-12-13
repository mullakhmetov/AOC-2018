import sys


RULE_LENGTH = 5
PLANT = '#'
EMPTY = '.'
MAX_GEN = int(5e10)


def resize_left_if_needed(state):
    # always keep 5 empty pots on the left side
    first_plant_index = state.index(PLANT)
    diff = RULE_LENGTH - first_plant_index

    if diff > 0:
        state = diff * EMPTY + state

    elif diff < 0:
        state = state[abs(diff):]

    return state, diff


def resize_right_if_needed(state):
    # always keep 5 empty pots on the right side
    last_plant_index = state.rindex(PLANT)
    diff = RULE_LENGTH - (len(state) - last_plant_index - 1)

    if diff > 0:
        state = state + diff * EMPTY

    elif diff < 0:
        state = state[abs(diff):]

    return state


def resize_if_needed(state):
    # should be exactly 5 empty pots on each size
    state, diff = resize_left_if_needed(state)
    state = resize_right_if_needed(state)
    return state, diff


def mutate(pattern, rules):
    return rules.get(pattern, EMPTY)


def pretty_state(state):
    start = state.index(PLANT)
    end = state.rindex(PLANT)
    return state[start:end + 1]


def main():
    with open('initial_state.txt') as s, open('rules.txt') as r:
        rules = dict([l.strip().split(' => ') for l in r.readlines()])
        initial_state = s.readline().strip()

    zero_index = 0
    prev_state = ''
    state = prev_state = initial_state

    for g in range(1, MAX_GEN + 1):
        state, c = resize_if_needed(state)
        zero_index += c

        stack = list(state)

        for i in range(len(stack)):
            left_edge = i - RULE_LENGTH // 2
            right_edge = i + (RULE_LENGTH - RULE_LENGTH // 2)
            pattern = state[left_edge:right_edge]
            s = mutate(pattern, rules)
            stack[i] = s

        state = ''.join(stack)

        if g == 20:
            result_1 = sum([i for i, v in enumerate(state, start=-zero_index) if v == PLANT])
            print(f'part 1: {result_1}')


        if state == prev_state:
            # since then the state will not change, but will "move" right one step per generation
            last_state_indexes = [i for i, v in enumerate(state, start=-zero_index) if v == PLANT]
            break

        prev_state = state

    else:
        # unlucky
        sys.exit()

    result_2 = sum([i + MAX_GEN - g for i in last_state_indexes])
    print(f'part 2: {result_2}')


if __name__ == '__main__':
    main()
