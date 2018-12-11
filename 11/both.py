GRID_SERIAL_NUMBER = 7315
GRID_SIZE = 300


def get_cell_power_level(x, y):
    rack_id = x + 10
    return ((((rack_id * y) + GRID_SERIAL_NUMBER) * rack_id) // 100 % 10) - 5


def get_frame_power_level(summed_area_table, x, y, frame_size):
    frame_offset = frame_size - 1

    # x and y now bottom-right frame corner
    x += frame_offset
    y += frame_offset

    return (
        summed_area_table[x, y] -
        summed_area_table.get((x - frame_size, y), 0) -
        summed_area_table.get((x, y - frame_size), 0) +
        summed_area_table.get((x - frame_size, y - frame_size), 0)
    )


def get_summed_area_table(grid_size):
    summed_area_table = {}
    for x in range(grid_size + 1):
        for y in range(grid_size + 1):
            summed_area_table[x, y] = (
                get_cell_power_level(x, y) +
                summed_area_table.get((x - 1, y), 0) +
                summed_area_table.get((x, y - 1), 0) -
                summed_area_table.get((x - 1, y - 1), 0)
            )

    return summed_area_table


def main():
    # https://en.wikipedia.org/wiki/Summed-area_table
    summed_area_table = get_summed_area_table(GRID_SIZE)

    best_x, best_y, best_size = 0, 0, 0
    best_power_level = 0

    for frame_size in range(1, GRID_SIZE + 1):
        for x in range(1, GRID_SIZE + 1 - frame_size):
            for y in range(1, GRID_SIZE + 1 - frame_size):
                power_level = get_frame_power_level(summed_area_table, x, y, frame_size)
                if power_level > best_power_level:
                    best_power_level = power_level
                    best_x, best_y, best_size = x, y, frame_size

        if frame_size == 3:
            print('part 1: {},{}'.format(best_x, best_y))

    print('part 2: {},{},{}'.format(best_x, best_y, best_size))


if __name__ == '__main__':
    main()
