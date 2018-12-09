from collections import deque


def get_node_sum(numbers):
    child_q, meta_q = numbers.popleft(), numbers.popleft()

    meta_sum = sum([get_node_sum(numbers) for i in range(child_q)])

    meta_sum += sum([numbers.popleft() for i in range(meta_q)])

    return meta_sum


def get_node_value(numbers):
    child_q, meta_q = numbers.popleft(), numbers.popleft()

    values_list = [get_node_value(numbers) for i in range(child_q)]

    meta_list = [numbers.popleft() for i in range(meta_q)]

    if not child_q:
        return sum(meta_list)

    return sum([values_list[meta - 1] if len(values_list) >= meta else 0 for meta in meta_list])


def main():
    with open('input.txt', 'r') as f:
         numbers = [int(l.strip()) for l in f.readline().split(' ')]

    print('part 1: {}'.format(get_node_sum(deque(numbers))))
    print('part 2: {}'.format(get_node_value(deque(numbers))))




if __name__ == '__main__':
    main()
