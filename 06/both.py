from collections import defaultdict


def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def shift_points_to_edge(points):
    min_x = min(c[0] for c in points)
    min_y = min(c[1] for c in points)
    return [(x - min_x, y - min_y) for (x, y) in points]


def main():
    with open('input.txt', 'r') as f:
        raw_coordinates = [l.strip() for l in f.readlines()]

    points = [tuple(map(int, crs.split(', '))) for crs in raw_coordinates]
    # optimize
    points = shift_points_to_edge(points)

    last_x = max(c[0] for c in points)
    last_y = max(c[1] for c in points)

    def is_infinite(x, y):
        return x < 0 or y < 1 or x > last_x  or y > last_y

    infinite_points = set()
    points_to_coordinates = defaultdict(list)
    coordinates_to_distances = defaultdict(int)

    for x in range(-1, last_x + 2):  # cross the edge to detect infinite
        for y in range(-1, last_y + 2):
            distances_list = []
            distances_set = set()
            for p_x, p_y in points:
                distance = get_distance(x, y, p_x, p_y)
                coordinates_to_distances[x, y] += distance
                if distance not in distances_set:
                    distances_set.add(distance)
                    distances_list.append((distance, p_x, p_y))
                else:
                    # equally far from two or more points
                    continue

            p_x, p_y = min(distances_list, key=lambda x: x[0])[1:]
            if is_infinite(x, y):
                infinite_points.add((p_x, p_y))
                continue
            else:
                points_to_coordinates[p_x, p_y].append((x, y))

    for i in infinite_points:
        points_to_coordinates.pop(i, None)

    part_1_result = max(len(v) for v in points_to_coordinates.values())
    print(f'part 1: {part_1_result}')

    part_2_result = (len([(x, y) for (x, y), d in coordinates_to_distances.items() if d < 10000]))
    print(f'part 2: {part_2_result}')


if __name__ == '__main__':
    main()
