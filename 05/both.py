from string import ascii_lowercase


def are_react(a, b):
    return a != b and a.lower() == b.lower()


def react(polymer):
    result_polymer_list = [polymer[0]]
    for unit in polymer[1:]:
        if result_polymer_list:
            prev_unit = result_polymer_list[-1]
            if are_react(prev_unit, unit):
                result_polymer_list.pop()
                continue

        result_polymer_list.append(unit)

    return result_polymer_list


def main():
    with open('input.txt', 'r') as f:
        polymer = f.readline().strip()

    part_1_result_polymer_list = react(polymer)
    part_1_result = len(part_1_result_polymer_list)
    print(f'part 1: {part_1_result}')

    part_2_result = min([len(react(polymer.replace(char, '').replace(char.upper(), ''))) for char in ascii_lowercase])
    print(f'part 2: {part_2_result}')

if __name__ == '__main__':
    main()
