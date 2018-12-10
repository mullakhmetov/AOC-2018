import re
from dataclasses import dataclass


POINT_RE = re.compile(r'\-?\d+')


@dataclass
class Point:
    x: int
    y: int
    x_velocity: int
    y_velocity: int

    @classmethod
    def parse_point(cls, string):
        return cls(*[int(i) for i in POINT_RE.findall(string)])

    def shift(self, x_offset, y_offset):
        self.x -= x_offset
        self.y -= y_offset

    def next_position(self):
        self.x += self.x_velocity
        self.y += self.y_velocity


@dataclass
class Screen:
    points: list
    steps_q: int = 0

    def _get_min_coordinates(self):
        min_x = min(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        return min_x, min_y

    def _get_max_coordinates(self):
        max_x = max(p.x for p in self.points)
        max_y = max(p.y for p in self.points)
        return max_x, max_y

    def _shift_points_to_edge(self):
        min_x, min_y = self._get_min_coordinates()

        for point in self.points:
            point.shift(min_x, min_y)

    def _get_size(self):
        min_x, min_y = self._get_min_coordinates()
        max_x, max_y = self._get_max_coordinates()

        return max_x - min_x, max_y - min_y

    def _step(self):
        self.steps_q += 1
        for point in self.points:
            point.next_position()

    @staticmethod
    def _is_acceptable(size):
        # punch card legacy right?
        return sum(size) < 80

    def _get_state(self):
        self._shift_points_to_edge()

        max_x, max_y = self._get_max_coordinates()
        f = [['.' for x in range(max_x + 1)] for y in range(max_y + 1)]
        for point in self.points:
            f[point.y][point.x] = '#'

        return f

    def get_acceptable_state(self):
        while not self._is_acceptable(self._get_size()):
            self._step()

        return self._get_state()


def main():
    with open('input.txt', 'r') as f:
        points = [Point.parse_point(l.strip()) for l in f.readlines()]

    screen = Screen(points)

    print(f'part 1:')
    [print(''.join(l)) for l in screen.get_acceptable_state()]

    print(f'part 2: {screen.steps_q}')


if __name__ == '__main__':
    main()
